import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from scipy.ndimage import rotate, gaussian_filter
from skimage import morphology
import dask.array as da
from dask.diagnostics import ProgressBar
import hyperspy.api as hs
from hyperspy.signals import BaseSignal, Signal1D, Signal2D
from hyperspy._signals.lazy import LazySignal
from hyperspy._signals.signal2d import LazySignal2D
from hyperspy.misc.utils import isiterable
import pixstem.pixelated_stem_tools as pst
import pixstem.fem_tools as femt
import pixstem.dask_tools as dt
import pixstem.marker_tools as mt
import pixstem.ransac_ellipse_tools as ret
from tqdm import tqdm


class PixelatedSTEM(Signal2D):

    def plot(self, *args, **kwargs):
        if 'navigator' in kwargs:
            super().plot(*args, **kwargs)
        elif hasattr(self, *args, 'navigation_signal'):
            if self.navigation_signal is not None:
                nav_sig_shape = self.navigation_signal.axes_manager.shape
                self_nav_shape = self.axes_manager.navigation_shape
                if nav_sig_shape == self_nav_shape:
                    kwargs['navigator'] = self.navigation_signal
                    super().plot(*args, **kwargs)
                else:
                    raise ValueError(
                            "navigation_signal does not have the same shape "
                            "({0}) as the signal's navigation shape "
                            "({1})".format(nav_sig_shape, self_nav_shape))
            else:
                super().plot(*args, **kwargs)
        else:
            super().plot(*args, **kwargs)

    def as_lazy(self, *args, **kwargs):
        res = super().as_lazy(*args, **kwargs)
        res.__class__ = LazyPixelatedSTEM
        res.__init__(**res._to_dictionary())
        return res

    def shift_diffraction(
            self, shift_x, shift_y, interpolation_order=1, parallel=True,
            inplace=False, show_progressbar=True):
        """Shift the diffraction patterns in a pixelated STEM signal.

        The points outside the boundaries are set to zero.

        Parameters
        ----------
        shift_x, shift_y : int or NumPy array
            If given as int, all the diffraction patterns will have the same
            shifts. Each diffraction pattern can also have different shifts,
            by passing a NumPy array with the same dimensions as the navigation
            axes.
        interpolation_order : int
            When shifting, a spline interpolation is used. This parameter
            sets the order of this spline. Must be between 0 and 5.
            Note that in some low-signal and high noise datasets, using a
            non-zero order might lead to artifacts. See the docstring in
            scipy.ndimage.shift for more information. Default 1.
        parallel : bool
            If True, run the processing on several cores.
            In most cases this should be True, but for debugging False can be
            useful. Default True
        inplace : bool
            If True (default), the data is replaced by the result. Useful when
            working with very large datasets, as this avoids doubling the
            amount of memory needed. If False, a new signal with the results
            is returned.
        show_progressbar : bool
            Default True.

        Returns
        -------
        shifted_signal : PixelatedSTEM signal

        Examples
        --------
        >>> s = ps.dummy_data.get_disk_shift_simple_test_signal()
        >>> s_c = s.center_of_mass(threshold=3., show_progressbar=False)
        >>> s_c -= 25 # To shift the center disk to the middle (25, 25)
        >>> s_shift = s.shift_diffraction(
        ...     s_c.inav[0].data, s_c.inav[1].data,
        ...     show_progressbar=False)
        >>> s_shift.plot()

        Using a different interpolation order

        >>> s_shift = s.shift_diffraction(
        ...     s_c.inav[0].data, s_c.inav[1].data, interpolation_order=3,
        ...     show_progressbar=False)

        """

        if (not isiterable(shift_x)) or (not isiterable(shift_y)):
            shift_x, shift_y = pst._make_centre_array_from_signal(
                    self, x=shift_x, y=shift_y)
        shift_x = shift_x.flatten()
        shift_y = shift_y.flatten()
        iterating_kwargs = [('shift_x', shift_x), ('shift_y', shift_y)]

        s_shift = self._map_iterate(
                pst._shift_single_frame, iterating_kwargs=iterating_kwargs,
                inplace=inplace, ragged=False, parallel=parallel,
                show_progressbar=show_progressbar,
                interpolation_order=interpolation_order)
        if not inplace:
            return s_shift

    def threshold_and_mask(
            self, threshold=None, mask=None, show_progressbar=True):
        """Get a thresholded and masked of the signal.

        Useful for figuring out optimal settings for the center_of_mass
        method.

        Parameters
        ----------
        threshold : number, optional
            The thresholding will be done at mean times
            this threshold value.
        mask : tuple (x, y, r)
            Round mask centered on x and y, with radius r.
        show_progressbar : bool
            Default True

        Returns
        -------
        s_out : PixelatedSTEM signal

        Examples
        --------
        >>> import pixstem.dummy_data as dd
        >>> s = dd.get_disk_shift_simple_test_signal()
        >>> mask = (25, 25, 10)
        >>> s_out = s.threshold_and_mask(
        ...     mask=mask, threshold=2, show_progressbar=False)
        >>> s_out.plot()

        """
        if self._lazy:
            raise NotImplementedError(
                    "threshold_and_mask is currently not implemented for "
                    "lazy signals. Use compute() first to turn signal into "
                    "a non-lazy signal. Note that this will load the full "
                    "dataset into memory, which might crash your computer.")
        if mask is not None:
            x, y, r = mask
            im_x, im_y = self.axes_manager.signal_shape
            mask = pst._make_circular_mask(x, y, im_x, im_y, r)
        s_out = self.map(
                function=pst._threshold_and_mask_single_frame,
                ragged=False, inplace=False, parallel=True,
                show_progressbar=show_progressbar,
                threshold=threshold, mask=mask)
        return s_out

    def rotate_diffraction(self, angle, parallel=True, show_progressbar=True):
        """
        Rotate the diffraction dimensions.

        Parameters
        ----------
        angle : scalar
            Clockwise rotation in degrees.
        parallel : bool
            Default True
        show_progressbar : bool
            Default True

        Returns
        -------
        rotated_signal : PixelatedSTEM class

        Examples
        --------
        >>> s = ps.dummy_data.get_holz_simple_test_signal()
        >>> s_rot = s.rotate_diffraction(30, show_progressbar=False)

        """
        s_rotated = self.map(
                rotate, ragged=False, angle=-angle, reshape=False,
                parallel=parallel, inplace=False,
                show_progressbar=show_progressbar)
        if self._lazy:
            s_rotated.compute(progressbar=show_progressbar)
        return s_rotated

    def flip_diffraction_x(self):
        """Flip the dataset along the diffraction x-axis.

        The function returns a new signal, but the data itself
        is a view of the original signal. So changing the returned signal
        will also change the original signal (and visa versa). To avoid
        changing the original signal, use the deepcopy method afterwards,
        but note that this requires double the amount of memory.
        See below for an example of this.

        Returns
        -------
        flipped_signal : PixelatedSTEM signal

        Example
        -------
        >>> s = ps.dummy_data.get_holz_simple_test_signal()
        >>> s_flip = s.flip_diffraction_x()

        To avoid changing the original object afterwards

        >>> s_flip = s.flip_diffraction_x().deepcopy()

        """
        s_out = self.copy()
        s_out.axes_manager = self.axes_manager.deepcopy()
        s_out.metadata = self.metadata.deepcopy()
        s_out.data = np.flip(self.data, axis=-1)
        return s_out

    def flip_diffraction_y(self):
        """Flip the dataset along the diffraction y-axis.

        The function returns a new signal, but the data itself
        is a view of the original signal. So changing the returned signal
        will also change the original signal (and visa versa). To avoid
        changing the original signal, use the deepcopy method afterwards,
        but note that this requires double the amount of memory.
        See below for an example of this.


        Returns
        -------
        flipped_signal : PixelatedSTEM signal

        Example
        -------
        >>> s = ps.dummy_data.get_holz_simple_test_signal()
        >>> s_flip = s.flip_diffraction_y()

        To avoid changing the original object afterwards

        >>> s_flip = s.flip_diffraction_y().deepcopy()

        """
        s_out = self.copy()
        s_out.axes_manager = self.axes_manager.deepcopy()
        s_out.metadata = self.metadata.deepcopy()
        s_out.data = np.flip(self.data, axis=-2)
        return s_out

    def center_of_mass(
            self, threshold=None, mask=None, lazy_result=False,
            show_progressbar=True, chunk_calculations=None):
        """Get the centre of the STEM diffraction pattern using
        center of mass. Threshold can be set to only use the most
        intense parts of the pattern. A mask can be used to exclude
        parts of the diffraction pattern.

        Parameters
        ----------
        threshold : number, optional
            The thresholding will be done at mean times
            this threshold value.
        mask : tuple (x, y, r), optional
            Round mask centered on x and y, with radius r.
        lazy_result : bool, optional
            If True, will not compute the data directly, but
            return a lazy signal. Default False
        show_progressbar : bool, optional
            Default True
        chunk_calculations : tuple, optional
            Chunking values when running the calculations.

        Returns
        -------
        s_com : DPCSignal
            DPCSignal with beam shifts along the navigation dimension
            and spatial dimensions as the signal dimension(s).

        Examples
        --------
        With mask centered at x=105, y=120 and 30 pixel radius

        >>> import pixstem.dummy_data as dd
        >>> s = dd.get_disk_shift_simple_test_signal()
        >>> mask = (25, 25, 10)
        >>> s_com = s.center_of_mass(mask=mask, show_progressbar=False)
        >>> s_color = s_com.get_color_signal()

        Also threshold

        >>> s_com = s.center_of_mass(threshold=1.5, show_progressbar=False)

        Get a lazy signal, then calculate afterwards

        >>> s_com = s.center_of_mass(lazy_result=True, show_progressbar=False)
        >>> s_com.compute(progressbar=False)

        """
        det_shape = self.axes_manager.signal_shape
        nav_dim = self.axes_manager.navigation_dimension
        if chunk_calculations is None:
            chunk_calculations = [16] * nav_dim + list(det_shape)
        if mask is not None:
            x, y, r = mask
            mask_array = pst._make_circular_mask(
                    x, y, det_shape[0], det_shape[1], r)
            mask_array = np.invert(mask_array)
        else:
            mask_array = None
        if self._lazy:
            dask_array = self.data.rechunk(chunk_calculations)
        else:
            dask_array = da.from_array(self.data, chunks=chunk_calculations)
        data = dt._center_of_mass_array(
                dask_array, threshold_value=threshold, mask_array=mask_array)
        if lazy_result:
            if nav_dim == 2:
                s_com = LazyDPCSignal2D(data)
            elif nav_dim == 1:
                s_com = LazyDPCSignal1D(data)
            elif nav_dim == 0:
                s_com = LazyDPCBaseSignal(data).T
        else:
            if show_progressbar:
                pbar = ProgressBar()
                pbar.register()
            data = data.compute()
            if show_progressbar:
                pbar.unregister()
            if nav_dim == 2:
                s_com = DPCSignal2D(data)
            elif nav_dim == 1:
                s_com = DPCSignal1D(data)
            elif nav_dim == 0:
                s_com = DPCBaseSignal(data).T
        s_com.axes_manager.navigation_axes[0].name = "Beam position"
        for nav_axes, sig_axes in zip(
                self.axes_manager.navigation_axes,
                s_com.axes_manager.signal_axes):
            pst._copy_axes_object_metadata(nav_axes, sig_axes)
        return s_com

    def add_peak_array_as_markers(
            self, peak_array, color='red', size=20, bool_array=None,
            bool_invert=False):
        """Add a peak array to the signal as HyperSpy markers.

        Parameters
        ----------
        peak_array : NumPy 4D array
        color : string, optional
            Default 'red'
        size : scalar, optional
            Default 20
        bool_array : NumPy array
            Must be the same size as peak_array
        bool_invert : bool

        Examples
        --------
        >>> s, parray = ps.dummy_data.get_simple_ellipse_signal_peak_array()
        >>> s.add_peak_array_as_markers(parray)
        >>> s.plot()

        """
        mt.add_peak_array_to_signal_as_markers(
                self, peak_array, color=color, size=size,
                bool_array=bool_array, bool_invert=bool_invert)

    def add_ellipse_array_as_markers(
            self, ellipse_array, inlier_array=None, peak_array=None,
            nr=20, color_ellipse='blue', linewidth=1, linestyle='solid',
            color_inlier='blue', color_outlier='red', point_size=20):
        """Add a ellipse parameters array to a signal as HyperSpy markers.

        Useful to visualize the ellipse results.

        Parameters
        ----------
        ellipse_array : NumPy array
        inlier_array : NumPy array, optional
        peak_array : NumPy array, optional
        nr : scalar, optional
            Default 20
        color_ellipse : string, optional
            Default 'blue'
        linewidth : scalar, optional
            Default 1
        linestyle : string, optional
            Default 'solid'
        color_inlier : string, optional
            Default 'blue'
        color_outlier : string, optional
            Default 'red'
        point_size : scalar, optional

        Examples
        --------
        >>> s, parray = ps.dummy_data.get_simple_ellipse_signal_peak_array()
        >>> import pixstem.ransac_ellipse_tools as ret
        >>> ellipse_array, inlier_array = ret.get_ellipse_model_ransac(
        ...     parray, xf=95, yf=95, rf_lim=20, semi_len_min=40,
        ...     semi_len_max=100, semi_len_ratio_lim=5, max_trails=50)
        >>> s.add_ellipse_array_as_markers(
        ...     ellipse_array, inlier_array=inlier_array, peak_array=parray)
        >>> s.plot()

        """
        if len(self.data.shape) != 4:
            raise ValueError("Signal must be 4 dims to use this function")
        marker_list = ret._get_ellipse_markers(
                ellipse_array, inlier_array, peak_array, nr=20,
                color_ellipse='blue', linewidth=1, linestyle='solid',
                color_inlier='blue', color_outlier='red', point_size=20,
                signal_axes=self.axes_manager.signal_axes)

        mt._add_permanent_markers_to_signal(self, marker_list)

    def virtual_bright_field(
            self, cx=None, cy=None, r=None,
            lazy_result=False, show_progressbar=True):
        """Get a virtual bright field signal.

        Can be sum the whole diffraction plane, or a circle subset.
        If any of the parameters are None, it will sum the whole diffraction
        plane.

        Parameters
        ----------
        cx, cy : floats, optional
            x- and y-centre positions.
        r : float, optional
            Outer radius.
        lazy_result : bool, optional
            If True, will not compute the data directly, but
            return a lazy signal. Default False
        show_progressbar : bool, optional
            Default True.

        Returns
        -------
        virtual_bf_signal : HyperSpy 2D signal

        Examples
        --------
        >>> s = ps.dummy_data.get_holz_heterostructure_test_signal()
        >>> s_bf = s.virtual_bright_field(show_progressbar=False)
        >>> s_bf.plot()

        Sum a subset of the diffraction pattern

        >>> s_bf = s.virtual_bright_field(40, 40, 10, show_progressbar=False)
        >>> s_bf.plot()

        Get a lazy signal, then compute

        >>> s_bf = s.virtual_bright_field(
        ...     lazy_result=True, show_progressbar=False)
        >>> s_bf.compute(progressbar=False)

        """
        det_shape = self.axes_manager.signal_shape
        if (cx is None) or (cy is None) or (r is None):
            mask_array = np.zeros(det_shape[::-1], dtype=np.bool)
        else:
            mask_array = pst._make_circular_mask(
                    cx, cy, det_shape[0], det_shape[1], r)
            mask_array = np.invert(mask_array)
        data = dt._mask_array(
                self.data, mask_array=mask_array).sum(axis=(-2, -1))
        s_bf = LazySignal2D(data)
        if not lazy_result:
            s_bf.compute(progressbar=show_progressbar)
        for nav_axes, sig_axes in zip(
                self.axes_manager.navigation_axes,
                s_bf.axes_manager.signal_axes):
            pst._copy_axes_object_metadata(nav_axes, sig_axes)

        return s_bf

    def virtual_annular_dark_field(
            self, cx, cy, r_inner, r, lazy_result=False,
            show_progressbar=True):
        """Get a virtual annular dark field signal.

        Parameters
        ----------
        cx, cy : floats
            x- and y-centre positions.
        r_inner : float
            Inner radius.
        r : float
            Outer radius.
        lazy_result : bool, optional
            If True, will not compute the data directly, but
            return a lazy signal. Default False
        show_progressbar : bool, default True

        Returns
        -------
        virtual_adf_signal : HyperSpy 2D signal

        Examples
        --------
        >>> s = ps.dummy_data.get_holz_heterostructure_test_signal()
        >>> s_adf = s.virtual_annular_dark_field(
        ...     40, 40, 20, 40, show_progressbar=False)
        >>> s_adf.plot()

        Get a lazy signal, then compute

        >>> s_adf = s.virtual_annular_dark_field(
        ...     40, 40, 20, 40, lazy_result=True, show_progressbar=False)
        >>> s_adf.compute(progressbar=False)
        >>> s_adf.plot()

        """
        if r_inner > r:
            raise ValueError(
                    "r_inner must be higher than r. The argument order is " +
                    "(cx, cy, r_inner, r)")
        det_shape = self.axes_manager.signal_shape

        mask_array0 = pst._make_circular_mask(
                cx, cy, det_shape[0], det_shape[1], r)
        mask_array1 = pst._make_circular_mask(
                cx, cy, det_shape[0], det_shape[1], r_inner)
        mask_array = mask_array0 == mask_array1

        data = dt._mask_array(
                self.data, mask_array=mask_array).sum(axis=(-2, -1))
        s_adf = LazySignal2D(data)
        if not lazy_result:
            s_adf.compute(progressbar=show_progressbar)
        for nav_axes, sig_axes in zip(
                self.axes_manager.navigation_axes,
                s_adf.axes_manager.signal_axes):
            pst._copy_axes_object_metadata(nav_axes, sig_axes)
        return s_adf

    def radial_integration(self):
        raise Exception(
                "radial_integration has been renamed radial_average")

    def radial_average(
            self, centre_x=None, centre_y=None, mask_array=None,
            normalize=True, parallel=True, show_progressbar=True):
        """Radially average a pixelated STEM diffraction signal.

        Done by integrating over the azimuthal dimension, giving a
        profile of intensity as a function of scattering angle.

        Parameters
        ----------
        centre_x, centre_y : int or NumPy array, optional
            If given as int, all the diffraction patterns will have the same
            centre position. Each diffraction pattern can also have different
            centre position, by passing a NumPy array with the same dimensions
            as the navigation axes.
            Note: in either case both x and y values must be given. If one is
            missing, both will be set from the signal (0., 0.) positions.
            If no values are given, the (0., 0.) positions in the signal will
            be used.
        mask_array : Boolean NumPy array, optional
            Mask with the same shape as the signal.
        normalize : bool, default True
            If true, the returned radial profile will be normalized by the
            number of bins used for each average.
        parallel : bool, default True
            If True, run the processing on several cores.
            In most cases this should be True, but for debugging False can be
            useful.
        show_progressbar : bool
            Default True

        Returns
        -------
        HyperSpy signal, one less signal dimension than the input signal.

        Examples
        --------
        >>> import pixstem.dummy_data as dd
        >>> s = dd.get_holz_simple_test_signal()
        >>> s_r = s.radial_average(centre_x=25, centre_y=25,
        ...     show_progressbar=False)
        >>> s_r.plot()

        Using center_of_mass to find bright field disk position

        >>> s = dd.get_disk_shift_simple_test_signal()
        >>> s_com = s.center_of_mass(threshold=2, show_progressbar=False)
        >>> s_r = s.radial_average(
        ...     centre_x=s_com.inav[0].data, centre_y=s_com.inav[1].data,
        ...     show_progressbar=False)
        >>> s_r.plot()

        """
        if (centre_x is None) or (centre_y is None):
            centre_x, centre_y = pst._make_centre_array_from_signal(self)
        elif (not isiterable(centre_x)) or (not isiterable(centre_y)):
            centre_x, centre_y = pst._make_centre_array_from_signal(
                self, x=centre_x, y=centre_y)
        radial_array_size = pst._find_longest_distance(
                self.axes_manager.signal_axes[0].size,
                self.axes_manager.signal_axes[1].size,
                centre_x.min(), centre_y.min(),
                centre_x.max(), centre_y.max()) + 1
        centre_x = centre_x.flatten()
        centre_y = centre_y.flatten()
        iterating_kwargs = [('centre_x', centre_x), ('centre_y', centre_y)]
        if mask_array is not None:
            #  This line flattens the mask array, except for the two
            #  last dimensions. This to make the mask array work for the
            #  _map_iterate function.
            mask_flat = mask_array.reshape(-1, *mask_array.shape[-2:])
            iterating_kwargs.append(('mask', mask_flat))

        if self._lazy:
            data = pst._radial_average_dask_array(
                self.data, return_sig_size=radial_array_size,
                centre_x=centre_x, centre_y=centre_y,
                mask_array=mask_array, normalize=normalize,
                show_progressbar=show_progressbar)
            s_radial = hs.signals.Signal1D(data)
        else:
            s_radial = self._map_iterate(
                    pst._get_radial_profile_of_diff_image,
                    normalize=normalize,
                    iterating_kwargs=iterating_kwargs,
                    inplace=False, ragged=False,
                    parallel=parallel,
                    radial_array_size=radial_array_size,
                    show_progressbar=show_progressbar)
            data = s_radial.data
        s_radial = hs.signals.Signal1D(data)
        return (s_radial)

    def template_match_disk(
            self, disk_r=4, lazy_result=True, show_progressbar=True):
        """Template match the signal dimensions with a disk.

        Used to find diffraction disks in convergent beam electron
        diffraction data.

        Parameters
        ----------
        disk_r : scalar, optional
            Radius of the disk. Default 4.
        lazy_result : bool, default True
            If True, will return a LazyPixelatedSTEM object. If False,
            will compute the result and return a PixelatedSTEM object.
        show_progressbar : bool, default True

        Returns
        -------
        template_match : PixelatedSTEM object

        Examples
        --------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> s_template = s.template_match_disk(
        ...     disk_r=5, show_progressbar=False)
        >>> s.plot()

        See also
        --------
        template_match_ring
        template_match_with_binary_image

        """
        disk = morphology.disk(disk_r, self.data.dtype)
        s = self.template_match_with_binary_image(
                disk,
                lazy_result=lazy_result,
                show_progressbar=show_progressbar)
        return s

    def template_match_ring(
            self, r_inner=5, r_outer=7, lazy_result=True,
            show_progressbar=True):
        """Template match the signal dimensions with a ring.

        Used to find diffraction rings in convergent beam electron
        diffraction data.

        Parameters
        ----------
        r_inner, r_outer : scalar, optional
            Inner and outer radius of the rings.
        lazy_result : bool, default True
            If True, will return a LazyPixelatedSTEM object. If False,
            will compute the result and return a PixelatedSTEM object.
        show_progressbar : bool, default True

        Returns
        -------
        template_match : PixelatedSTEM object

        Examples
        --------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> s_template = s.template_match_ring(show_progressbar=False)
        >>> s.plot()

        See also
        --------
        template_match_disk
        template_match_with_binary_image

        """
        if r_outer <= r_inner:
            raise ValueError(
                    "r_outer ({0}) must be larger than r_inner ({1})".format(
                        r_outer, r_inner))
        edge = r_outer - r_inner
        edge_slice = np.s_[edge:-edge, edge:-edge]

        ring_inner = morphology.disk(r_inner, dtype=np.bool)
        ring = morphology.disk(r_outer, dtype=np.bool)
        ring[edge_slice] = ring[edge_slice] ^ ring_inner
        s = self.template_match_with_binary_image(
                ring,
                lazy_result=lazy_result,
                show_progressbar=show_progressbar)
        return s

    def template_match_with_binary_image(
            self, binary_image, lazy_result=True, show_progressbar=True):
        """Template match the signal dimensions with a binary image.

        Used to find diffraction disks in convergent beam electron
        diffraction data.

        Might also work with non-binary images, but this haven't been
        extensively tested.

        Parameters
        ----------
        binary_image : 2-D NumPy array
        lazy_result : bool, default True
            If True, will return a LazyPixelatedSTEM object. If False,
            will compute the result and return a PixelatedSTEM object.
        show_progressbar : bool, default True

        Returns
        -------
        template_match : PixelatedSTEM object

        Examples
        --------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> binary_image = np.random.randint(0, 2, (6, 6))
        >>> s_template = s.template_match_with_binary_image(
        ...     binary_image, show_progressbar=False)
        >>> s.plot()

        See also
        --------
        template_match_disk
        template_match_ring

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)
        output_array = dt._template_match_with_binary_image(
                dask_array, binary_image)
        if not lazy_result:
            if show_progressbar:
                pbar = ProgressBar()
                pbar.register()
            output_array = output_array.compute()
            if show_progressbar:
                pbar.unregister()
            s = PixelatedSTEM(output_array)
        else:
            s = LazyPixelatedSTEM(output_array)
        pst._copy_signal_all_axes_metadata(self, s)
        return s

    def find_peaks(self, method='dog', lazy_result=True,
                   show_progressbar=True, **kwargs):
        """Find peaks in the signal dimensions.

        Can use either skimage's blob_dog or blob_log.

        Parameters
        ----------
        method: string, optional
            'dog': difference of Gaussians. 'log': Laplacian of Gaussian.
            Default 'dog'.
        min_sigma : float, optional
            Default 0.98.
        max_sigma : float, optional
            Default 55.
        sigma_ratio : float, optional
            For method 'dog'. Default 1.76.
        num_sigma: float, optional
            For method 'log'. Default 10.
        threshold : float, optional
            Default 0.36.
        overlap : float, optional
            Default 0.81.
        normalize_value : float, optional
            All the values in the signal will be divided by this value.
            If no value is specified, the max value in each individual image
            will be used.
        max_r : float
            Maximum radius compared from the center of the diffraction pattern
        lazy_result : bool, optional
            Default True
        show_progressbar : bool, optional
            Default True

        Returns
        -------
        peak_array : dask 2D object array
            Same size as the two last dimensions in data, in the form
            [[y0, x0], [y1, x1], ...].
            The peak positions themselves are stored in 2D NumPy arrays
            inside each position in peak_array. This is done instead of
            making a 4D NumPy array, since the number of found peaks can
            vary in each position.

        Example
        -------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> peak_array = s.find_peaks()
        >>> peak_array_computed = peak_array.compute(show_progressbar=False)
        >>> peak02 = peak_array_computed[0, 2]
        >>> s.add_peak_array_as_markers(peak_array_computed)
        >>> s.plot()

        Change parameters

        >>> peak_array = s.find_peaks(
        ...     method='dog', min_sigma=1.2, max_sigma=27, sigma_ratio=2.2,
        ...     threshold=0.6, overlap=0.6, lazy_result=False,
        ...     show_progressbar=False)

        Using Laplacian of Gaussian

        >>> s = ps.dummy_data.get_cbed_signal()
        >>> peak_array = s.find_peaks(
        ...     method='log', min_sigma=5, max_sigma=55, num_sigma=10,
        ...     threshold=0.2, overlap=0.86, lazy_result=False,
        ...     show_progressbar=False)
        >>> s.add_peak_array_as_markers(peak_array)
        >>> s.plot()

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)

        if (method == 'dog'):
            output_array = dt._peak_find_dog(dask_array, **kwargs)
        elif (method == 'log'):
            output_array = dt._peak_find_log(dask_array, **kwargs)
        else:
            raise ValueError(
                "Method is not a valid name, should be dog or log")

        if not lazy_result:
            if show_progressbar:
                pbar = ProgressBar()
                pbar.register()
            output_array = output_array.compute()
            if show_progressbar:
                pbar.unregister()
        return output_array

    def peak_position_refinement_com(self, peak_array, square_size=10,
                                     lazy_result=True, show_progressbar=True):
        """Refines the peak position using the center of mass.

        Parameters
        ----------
        peak_array : Numpy or Dask array
            Object with x and y coordinates of the peak positions.
            Must have the same dimensions as this signal's navigation
            dimensions.
        square_size : int
            Even integer, sub image from which the center of mass is
            calculated. Default 5.
        lazy_result : bool, default True
            If True, will return a LazyPixelatedSTEM object. If False,
            will compute the result and return a PixelatedSTEM object.
        show_progressbar : bool, default True

        Returns
        -------
        output_array : dask 2D object array
            Same size as the two last dimensions in data, in the form
            [[y0, x0], [y1, x1], ...].
            The peak positions themselves are stored in 2D NumPy arrays
            inside each position in peak_array. This is done instead of
            making a 4D NumPy array, since the number of found peaks can
            vary in each position.

        Examples
        --------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> peak_array = s.find_peaks()
        >>> refined_peak_array = s.peak_position_refinement_com(peak_array, 20)
        >>> refined_peak_array_com = refined_peak_array.compute(
        ...     show_progressbar=False)
        >>> s.add_peak_array_as_markers(refined_peak_array_com)
        >>> s.plot()

        """
        if square_size % 2 != 0:  # If odd number, raise error
            raise ValueError(
                    "square_size must be even number, not {0}".format(
                        square_size))
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)

        chunks_peak = dask_array.chunksize[:-2]
        if hasattr(peak_array, 'chunks'):
            peak_array_dask = da.rechunk(peak_array, chunks=chunks_peak)
        else:
            peak_array_dask = da.from_array(peak_array, chunks=chunks_peak)

        output_array = dt._peak_refinement_centre_of_mass(
                dask_array, peak_array_dask, square_size)

        if not lazy_result:
            if show_progressbar:
                pbar = ProgressBar()
                pbar.register()
            output_array = output_array.compute()
            if show_progressbar:
                pbar.unregister()
        return output_array

    def intensity_peaks(self, peak_array, disk_r=4,
                        lazy_result=True, show_progressbar=True):
        """Get intensity of a peak in the diffraction data.

        The intensity is calculated by taking the mean of the
        pixel values inside radius disk_r from the peak
        position.

        Parameters
        ----------
        peak_array : Numpy or Dask array
            Must have the same navigation shape as this signal.
        disk_r : int
            Radius of the disc chosen to take the mean value of
        lazy_result : bool, default True
            If True, will return a LazyPixelatedSTEM object. If False,
            will compute the result and return a PixelatedSTEM object.
        show_progressbar : bool, default True

        Returns
        -------
        intensity_array: Numpy or Dask array
            Same navigation shape as this signal, with peak position in
            x and y coordinates and the mean intensity.

        Examples
        --------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> peak_array = s.find_peaks()
        >>> intensity_array = s.intensity_peaks(peak_array, disk_r=6)
        >>> intensity_array_computed = intensity_array.compute()

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)

        chunks_peak = dask_array.chunksize[:-2]
        if hasattr(peak_array, 'chunks'):
            peak_array_dask = da.rechunk(peak_array, chunks=chunks_peak)
        else:
            peak_array_dask = da.from_array(peak_array, chunks=chunks_peak)

        output_array = dt._intensity_peaks_image(
            dask_array, peak_array_dask, disk_r)

        if not lazy_result:
            if show_progressbar:
                pbar = ProgressBar()
                pbar.register()
            output_array = output_array.compute()
            if show_progressbar:
                pbar.unregister()
        return output_array

    def subtract_diffraction_background(
            self, method='median kernel',
            lazy_result=True, show_progressbar=True, **kwargs):
        """Background subtraction of the diffraction data.

        There are three different methods for doing this:
        - Difference of Gaussians
        - Median kernel
        - Radial median

        Parameters
        ----------
        method : string
            'difference of gaussians', 'median kernel' and 'radial median'.
            Default 'median kernel'.
        lazy_result : bool, default True
            If True, will return a LazyPixelatedSTEM object. If False,
            will compute the result and return a PixelatedSTEM object.
        show_progressbar : bool, default True
        sigma_min : float, optional
            Standard deviation for the minimum Gaussian convolution
            (difference of Gaussians only)
        sigma_max : float, optional
            Standard deviation for the maximum Gaussian convolution
            (difference of Gaussians only)
        footprint : int, optional
            Size of the window that is convoluted with the
            array to determine the median. Should be large enough
            that it is about 3x as big as the size of the
            peaks (median kernel only).
        centre_x : int, optional
            Centre x position of the coordinate system on which to map
            to radial coordinates (radial median only).
        centre_y : int, optional
            Centre y position of the coordinate system on which to map
            to radial coordinates (radial median only).

        Returns
        -------
        s : PixelatedSTEM or LazyPixelatedSTEM signal

        Examples
        --------
        >>> s = ps.dummy_data.get_cbed_signal()
        >>> s_r = s.subtract_diffraction_background(method='median kernel',
        ...     footprint=20, lazy_result=False, show_progressbar=False)
        >>> s_r.plot()

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)

        if (method == 'difference of gaussians'):
            output_array = dt._background_removal_dog(dask_array, **kwargs)
        elif (method == 'median kernel'):
            output_array = dt._background_removal_median(
                dask_array, **kwargs)
        elif (method == 'radial median'):
            output_array = dt._background_removal_radial_median(
                dask_array, **kwargs)
        else:
            raise NotImplementedError(
                "The method specified, '{}', is not implemented. "
                "The different methods are: 'difference of gaussians',"
                " 'median kernel' or 'radial median'.".format(
                    method))

        if not lazy_result:
            if show_progressbar:
                pbar = ProgressBar()
                pbar.register()
            output_array = output_array.compute()
            if show_progressbar:
                pbar.unregister()
            s = PixelatedSTEM(output_array)
        else:
            s = LazyPixelatedSTEM(output_array)
        pst._copy_signal_all_axes_metadata(self, s)
        return s

    def angular_mask(
            self, angle0, angle1,
            centre_x_array=None, centre_y_array=None):
        """Get a bool array with True values between angle0 and angle1.
        Will use the (0, 0) point as given by the signal as the centre,
        giving an "angular" slice. Useful for analysing anisotropy in
        diffraction patterns.

        Parameters
        ----------
        angle0, angle1 : numbers
        centre_x_array, centre_y_array : NumPy 2D array, optional
            Has to have the same shape as the navigation axis of
            the signal.

        Returns
        -------
        mask_array : NumPy array
            The True values will be the region between angle0 and angle1.
            The array will have the same dimensions as the signal.

        Examples
        --------
        >>> import pixstem.dummy_data as dd
        >>> s = dd.get_holz_simple_test_signal()
        >>> s.axes_manager.signal_axes[0].offset = -25
        >>> s.axes_manager.signal_axes[1].offset = -25
        >>> mask_array = s.angular_mask(0.5*np.pi, np.pi)

        """

        bool_array = pst._get_angle_sector_mask(
                self, angle0, angle1,
                centre_x_array=centre_x_array,
                centre_y_array=centre_y_array)
        return bool_array

    def angular_slice_radial_integration(self):
        raise Exception(
                "angular_slice_radial_integration has been renamed "
                "angular_slice_radial_average")

    def angular_slice_radial_average(
            self, angleN=20, centre_x=None, centre_y=None,
            slice_overlap=None, show_progressbar=True):
        """Do radial average of different angular slices.
        Useful for analysing anisotropy in round diffraction features,
        such as diffraction rings from polycrystalline materials or
        higher order Laue zone rings.

        Parameters
        ----------
        angleN : int, default 20
            Number of angular slices. If angleN=4, each slice
            will be 90 degrees. The average will start in the top left
            corner (0, 0) when plotting using s.plot(), and go clockwise.
        centre_x, centre_y : int or NumPy array, optional
            If given as int, all the diffraction patterns will have the same
            centre position. Each diffraction pattern can also have different
            centre position, by passing a NumPy array with the same dimensions
            as the navigation axes.
            Note: in either case both x and y values must be given. If one is
            missing, both will be set from the signal (0., 0.) positions.
            If no values are given, the (0., 0.) positions in the signal will
            be used.
        slice_overlap : float, optional
            Amount of overlap between the slices, given in fractions of
            angle slice (0 to 1). For angleN=4, each slice will be 90
            degrees. If slice_overlap=0.5, each slice will overlap by 45
            degrees on each side. The range of the slices will then be:
            (-45, 135), (45, 225), (135, 315) and (225, 45).
            Default off: meaning there is no overlap between the slices.
        show_progressbar : bool
            Default True

        Returns
        -------
        signal : HyperSpy 1D signal
            With one more navigation dimensions (the angular slices) compared
            to the input signal.

        Examples
        --------
        >>> import pixstem.dummy_data as dd
        >>> s = dd.get_holz_simple_test_signal()
        >>> s_com = s.center_of_mass(show_progressbar=False)
        >>> s_ar = s.angular_slice_radial_average(
        ...     angleN=10, centre_x=s_com.inav[0].data,
        ...     centre_y=s_com.inav[1].data, slice_overlap=0.2,
        ...     show_progressbar=False)
        >>> s_ar.plot() # doctest: +SKIP

        """
        signal_list = []
        angle_list = []
        if slice_overlap is None:
            slice_overlap = 0
        else:
            if (slice_overlap < 0) or (slice_overlap > 1):
                raise ValueError(
                        "slice_overlap is {0}. But must be between "
                        "0 and 1".format(slice_overlap))
        angle_step = 2 * np.pi / angleN
        for i in range(angleN):
            angle0 = (angle_step * i) - (angle_step * slice_overlap)
            angle1 = (angle_step * (i + 1)) + (angle_step * slice_overlap)
            angle_list.append((angle0, angle1))
        if (centre_x is None) or (centre_y is None):
            centre_x, centre_y = pst._make_centre_array_from_signal(self)
        elif (not isiterable(centre_x)) or (not isiterable(centre_y)):
            centre_x, centre_y = pst._make_centre_array_from_signal(
                    self, x=centre_x, y=centre_y)

        for angle in tqdm(angle_list, disable=(not show_progressbar)):
            mask_array = self.angular_mask(
                    angle[0], angle[1],
                    centre_x_array=centre_x,
                    centre_y_array=centre_y)
            s_r = self.radial_average(
                    centre_x=centre_x,
                    centre_y=centre_y,
                    mask_array=mask_array,
                    show_progressbar=show_progressbar)
            signal_list.append(s_r)
        angle_scale = angle_list[1][1] - angle_list[0][1]
        signal = hs.stack(signal_list, new_axis_name='Angle slice')
        signal.axes_manager['Angle slice'].offset = angle_scale / 2
        signal.axes_manager['Angle slice'].scale = angle_scale
        signal.axes_manager['Angle slice'].units = 'Radians'
        signal.axes_manager[-1].name = 'Scattering angle'
        return (signal)

    def fem_analysis(self, centre_x=None, centre_y=None,
                     show_progressbar=True):
        """Perform analysis of fluctuation electron microscopy (FEM) data.

        This is outlined in:
        T. L. Daulton, et al., Ultramicroscopy 110 (2010) 1279-1289.
        doi:10.1016/j.ultramic.2010.05.010

        Parameters
        ----------
        centre_x, centre_y : int, optional
            All the diffraction patterns assumed to have the same
            centre position.
        show_progressbar : bool, optional
            Default True

        Returns
        -------
        results : Python dictionary
            Results of FEM data analysis, including the normalized variance
            of the annular mean (V-Omegak), mean of normalized variances of
            rings (V-rk), normalized variance of ring ensemble (Vrek),
            the normalized variance image (Omega-Vi), and annular mean of
            the variance image (Omega-Vk).

        Examples
        --------
        >>> s = ps.dummy_data.get_fem_signal()
        >>> fem_results = s.fem_analysis(
        ...     centre_x=50, centre_y=50,
        ...     show_progressbar=False)
        >>> fem_results['V-Omegak'].plot()

        """
        results = femt.fem_calc(self, centre_x=centre_x, centre_y=centre_y,
                                show_progressbar=show_progressbar)
        return results

    def find_dead_pixels(
            self, dead_pixel_value=0, mask_array=None, lazy_result=False,
            show_progressbar=True):
        """Find dead pixels in the diffraction images.

        Parameters
        ----------
        dead_pixel_value : scalar
            Default 0
        mask_array : Boolean Numpy array
        lazy_result : bool
            If True, return a lazy signal. If False, compute
            the result and return a non-lazy signal. Default False.
        show_progressbar : bool

        Returns
        -------
        s_dead_pixels : HyperSpy 2D signal
            With dead pixels as True, rest as False.

        Examples
        --------
        >>> s = ps.dummy_data.get_dead_pixel_signal()
        >>> s_dead_pixels = s.find_dead_pixels(show_progressbar=False)

        Using a mask array

        >>> import numpy as np
        >>> mask_array = np.zeros((128, 128), dtype=np.bool)
        >>> mask_array[:, 100:] = True
        >>> s = ps.dummy_data.get_dead_pixel_signal()
        >>> s_dead_pixels = s.find_dead_pixels(
        ...     mask_array=mask_array, show_progressbar=False)

        Getting a lazy signal as output

        >>> s_dead_pixels = s.find_dead_pixels(
        ...     lazy_result=True, show_progressbar=False)

        See also
        --------
        find_hot_pixels
        correct_bad_pixels

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)
        dead_pixels = dt._find_dead_pixels(
                dask_array, dead_pixel_value=dead_pixel_value,
                mask_array=mask_array)
        s_dead_pixels = LazySignal2D(dead_pixels)
        if not lazy_result:
            s_dead_pixels.compute(progressbar=show_progressbar)
        return s_dead_pixels

    def find_hot_pixels(
            self, threshold_multiplier=500, mask_array=None, lazy_result=True,
            show_progressbar=True):
        """Find hot pixels in the diffraction images.

        Note: this method will be default return a lazy signal, since the
        size of the returned signal is the same shape as the original
        signal. So for large datasets actually calculating computing
        the results can use a lot of memory.

        In addition, this signal is currently not very optimized with
        regards to memory use, so be careful when using this method
        for large datasets.

        Parameters
        ----------
        threshold_multiplier : scalar
            Default 500
        mask_array : Boolean NumPy array
        lazy_result : bool
            If True, return a lazy signal. If False, compute
            the result and return a non-lazy signal. Default True.
        show_progressbar : bool

        Examples
        --------
        >>> s = ps.dummy_data.get_hot_pixel_signal()
        >>> s_hot_pixels = s.find_hot_pixels(show_progressbar=False)

        Using a mask array

        >>> import numpy as np
        >>> mask_array = np.zeros((128, 128), dtype=np.bool)
        >>> mask_array[:, 100:] = True
        >>> s = ps.dummy_data.get_hot_pixel_signal()
        >>> s_hot_pixels = s.find_hot_pixels(
        ...     mask_array=mask_array, show_progressbar=False)

        Getting a non-lazy signal as output

        >>> s_hot_pixels = s.find_hot_pixels(
        ...     lazy_result=False, show_progressbar=False)

        See also
        --------
        find_dead_pixels
        correct_bad_pixels

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)
        hot_pixels = dt._find_hot_pixels(
                dask_array, threshold_multiplier=threshold_multiplier,
                mask_array=mask_array)

        s_hot_pixels = LazySignal2D(hot_pixels)
        if not lazy_result:
            s_hot_pixels.compute(progressbar=show_progressbar)
        return s_hot_pixels

    def correct_bad_pixels(
            self, bad_pixel_array, lazy_result=True, show_progressbar=True):
        """Correct bad pixels by getting mean value of neighbors.

        Note: this method is currently not very optimized with regards
        to memory use, so currently be careful when using it on
        large datasets.

        Parameters
        ----------
        bad_pixel_array : array-like
        lazy_result : bool
            Default True.
        show_progressbar : bool
            Default True

        Returns
        -------
        signal_corrected : PixelatedSTEM or LazyPixelatedSTEM

        Examples
        --------
        >>> s = ps.dummy_data.get_hot_pixel_signal()
        >>> s_hot_pixels = s.find_hot_pixels(
        ...     show_progressbar=False, lazy_result=True)
        >>> s_corr = s.correct_bad_pixels(s_hot_pixels)

        Dead pixels

        >>> s = ps.dummy_data.get_dead_pixel_signal()
        >>> s_dead_pixels = s.find_dead_pixels(
        ...     show_progressbar=False, lazy_result=True)
        >>> s_corr = s.correct_bad_pixels(s_dead_pixels)

        Combine both dead pixels and hot pixels

        >>> s_bad_pixels = s_hot_pixels + s_dead_pixels
        >>> s_corr = s.correct_bad_pixels(s_bad_pixels)

        See also
        --------
        find_dead_pixels
        find_hot_pixels

        """
        if self._lazy:
            dask_array = self.data
        else:
            sig_chunks = list(self.axes_manager.signal_shape)[::-1]
            chunks = [8] * len(self.axes_manager.navigation_shape)
            chunks.extend(sig_chunks)
            dask_array = da.from_array(self.data, chunks=chunks)
        bad_pixel_removed = dt._remove_bad_pixels(
                dask_array, bad_pixel_array.data)
        s_bad_pixel_removed = LazyPixelatedSTEM(bad_pixel_removed)
        pst._copy_signal2d_axes_manager_metadata(self, s_bad_pixel_removed)
        if not lazy_result:
            s_bad_pixel_removed.compute(progressbar=show_progressbar)
        return s_bad_pixel_removed


class DPCBaseSignal(BaseSignal):
    """
    Signal for processing differential phase contrast (DPC) acquired using
    scanning transmission electron microscopy (STEM).

    The signal assumes the data is 3 dimensions, where the two
    signal dimensions are the probe positions, and the navigation
    dimension is the x and y disk shifts.

    The first navigation index (s.inav[0]) is assumed to the be x-shift
    and the second navigation is the y-shift (s.inav[1]).

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DPCSignal1D(Signal1D):
    """
    Signal for processing differential phase contrast (DPC) acquired using
    scanning transmission electron microscopy (STEM).

    The signal assumes the data is 2 dimensions, where the
    signal dimension is the probe position, and the navigation
    dimension is the x and y disk shifts.

    The first navigation index (s.inav[0]) is assumed to the be x-shift
    and the second navigation is the y-shift (s.inav[1]).

    """

    def get_bivariate_histogram(
            self,
            histogram_range=None,
            masked=None,
            bins=200,
            spatial_std=3):
        """
        Useful for finding the distribution of magnetic vectors(?).

        Parameters
        ----------
        histogram_range : tuple, optional
            Set the minimum and maximum of the histogram range.
            Default is setting it automatically.
        masked : 1-D NumPy bool array, optional
            Mask parts of the data. The array must be the same
            size as the signal. The True values are masked.
            Default is not masking anything.
        bins : integer, default 200
            Number of bins in the histogram
        spatial_std : number, optional
            If histogram_range is not given, this value will be
            used to set the automatic histogram range.
            Default value is 3.

        Returns
        -------
        s_hist : Signal2D

        """
        x_position = self.inav[0].data
        y_position = self.inav[1].data
        s_hist = pst._make_bivariate_histogram(
                x_position, y_position,
                histogram_range=histogram_range,
                masked=masked,
                bins=bins,
                spatial_std=spatial_std)
        return s_hist


class DPCSignal2D(Signal2D):
    """
    Signal for processing differential phase contrast (DPC) acquired using
    scanning transmission electron microscopy (STEM).

    The signal assumes the data is 3 dimensions, where the two
    signal dimensions are the probe positions, and the navigation
    dimension is the x and y disk shifts.

    The first navigation index (s.inav[0]) is assumed to the be x-shift
    and the second navigation is the y-shift (s.inav[1]).

    """

    def correct_ramp(self, corner_size=0.05, only_offset=False, out=None):
        """
        Subtracts a plane from the signal, useful for removing
        the effects of d-scan in a STEM beam shift dataset.

        The plane is calculated by fitting a plane to the corner values
        of the signal. This will only work well when the property one
        wants to measure is zero in these corners.

        Parameters
        ----------
        corner_size : number, optional
            The size of the corners, as a percentage of the image's axis.
            If corner_size is 0.05 (5%), and the image is 500 x 1000,
            the size of the corners will be (500*0.05) x (1000*0.05) = 25 x 50.
            Default 0.05
        only_offset : bool, optional
            If True, will subtract a "flat" plane, i.e. it will subtract the
            mean value of the corners. Default False
        out : optional, DPCSignal2D signal

        Returns
        -------
        corrected_signal : Signal2D

        Examples
        --------
        >>> s = ps.dummy_data.get_square_dpc_signal(add_ramp=True)
        >>> s_corr = s.correct_ramp()
        >>> s_corr.plot()

        Only correct offset

        >>> s_corr = s.correct_ramp(only_offset=True)
        >>> s_corr.plot()

        """
        if out is None:
            output = self.deepcopy()
        else:
            output = out

        for i, s in enumerate(self):
            if only_offset:
                corners = pst._get_corner_values(s, corner_size=corner_size)[2]
                ramp = corners.mean()
            else:
                ramp = pst._fit_ramp_to_image(s, corner_size=0.05)
            output.data[i, :, :] -= ramp
        if out is None:
            return output

    def get_magnitude_signal(self, autolim=True, autolim_sigma=4):
        """Get DPC magnitude image visualized as greyscale.

        Converts the x and y beam shifts into a magnitude map, showing the
        magnitude of the beam shifts.

        Useful for visualizing magnetic domain structures.

        Parameters
        ----------
        autolim : bool, default True
        autolim_sigma : float, default 4

        Returns
        -------
        magnitude_signal : HyperSpy 2D signal

        Examples
        --------
        >>> s = ps.dummy_data.get_simple_dpc_signal()
        >>> s_magnitude = s.get_magnitude_signal()
        >>> s_magnitude.plot()

        See also
        --------
        get_color_signal : Signal showing both phase and magnitude
        get_phase_signal : Signal showing the phase

        """
        inav02 = np.abs(self.inav[0].data) ** 2
        inav12 = np.abs(self.inav[1].data) ** 2
        magnitude = np.sqrt(inav02 + inav12)
        magnitude_limits = None
        if autolim:
            magnitude_limits = pst._get_limits_from_array(
                    magnitude, sigma=autolim_sigma)
            np.clip(
                    magnitude, magnitude_limits[0],
                    magnitude_limits[1], out=magnitude)

        signal = Signal2D(magnitude)
        pst._copy_signal2d_axes_manager_metadata(self, signal)
        return signal

    def get_phase_signal(self, rotation=None):
        """Get DPC phase image visualized using continuous color scale.

        Converts the x and y beam shifts into an RGB array, showing the
        direction of the beam shifts.

        Useful for visualizing magnetic domain structures.

        Parameters
        ----------
        rotation : float, optional
            In degrees. Useful for correcting the mismatch between
            scan direction and diffraction pattern rotation.
        autolim : bool, default True
        autolim_sigma : float, default 4

        Returns
        -------
        phase_signal : HyperSpy 2D RGB signal

        Examples
        --------
        >>> s = ps.dummy_data.get_simple_dpc_signal()
        >>> s_color = s.get_phase_signal(rotation=20)
        >>> s_color.plot()

        See also
        --------
        get_color_signal : Signal showing both phase and magnitude
        get_magnitude_signal : Signal showing the magnitude

        """
        # Rotate the phase by -30 degrees in the color "wheel", to get better
        # visualization in the vertical and horizontal direction.
        if rotation is None:
            rotation = -30
        else:
            rotation = rotation - 30
        phase = np.arctan2(self.inav[0].data, self.inav[1].data) % (2 * np.pi)
        rgb_array = pst._get_rgb_phase_array(phase=phase, rotation=rotation)
        signal_rgb = Signal1D(rgb_array * (2 ** 16 - 1))
        signal_rgb.change_dtype("uint16")
        signal_rgb.change_dtype("rgb16")
        pst._copy_signal2d_axes_manager_metadata(self, signal_rgb)
        return signal_rgb

    def get_color_signal(
            self, rotation=None, autolim=True, autolim_sigma=4):
        """Get DPC image visualized using continuous color scale.

        Converts the x and y beam shifts into an RGB array, showing the
        magnitude and direction of the beam shifts.

        Useful for visualizing magnetic domain structures.

        Parameters
        ----------
        rotation : float, optional
            In degrees. Useful for correcting the mismatch between
            scan direction and diffraction pattern rotation.
        autolim : bool, default True
        autolim_sigma : float, default 4

        Returns
        -------
        color_signal : HyperSpy 2D RGB signal

        Examples
        --------
        >>> s = ps.dummy_data.get_simple_dpc_signal()
        >>> s_color = s.get_color_signal()
        >>> s_color.plot()

        Rotate the beam shift by 30 degrees

        >>> s_color = s.get_color_signal(rotation=30)

        See also
        --------
        get_color_signal : Signal showing both phase and magnitude
        get_phase_signal : Signal showing the phase

        """
        # Rotate the phase by -30 degrees in the color "wheel", to get better
        # visualization in the vertical and horizontal direction.
        if rotation is None:
            rotation = -30
        else:
            rotation = rotation - 30
        inav0 = self.inav[0].data
        inav1 = self.inav[1].data
        phase = np.arctan2(inav0, inav1) % (2 * np.pi)
        magnitude = np.sqrt(np.abs(inav0) ** 2 + np.abs(inav1) ** 2)

        magnitude_limits = None
        if autolim:
            magnitude_limits = pst._get_limits_from_array(
                    magnitude, sigma=autolim_sigma)
        rgb_array = pst._get_rgb_phase_magnitude_array(
                phase=phase, magnitude=magnitude, rotation=rotation,
                magnitude_limits=magnitude_limits)
        signal_rgb = Signal1D(rgb_array * (2 ** 16 - 1))
        signal_rgb.change_dtype("uint16")
        signal_rgb.change_dtype("rgb16")
        pst._copy_signal2d_axes_manager_metadata(self, signal_rgb)
        return signal_rgb

    def get_color_image_with_indicator(
            self, phase_rotation=0, indicator_rotation=0, only_phase=False,
            autolim=True, autolim_sigma=4, scalebar_size=None, ax=None,
            ax_indicator=None):
        """Make a matplotlib figure showing DPC contrast.

        Parameters
        ----------
        phase_rotation : float, default 0
            Changes the phase of the plotted data.
            Useful for correcting scan rotation.
        indicator_rotation : float, default 0
            Changes the color wheel rotation.
        only_phase : bool, default False
            If False, will plot both the magnitude and phase.
            If True, will only plot the phase.
        autolim : bool, default True
        autolim_sigma : float, default 4
        scalebar_size : int, optional
        ax : Matplotlib subplot, optional
        ax_indicator : Matplotlib subplot, optional
            If None, generate a new subplot for the indicator.
            If False, do not include an indicator

        Examples
        --------
        >>> s = ps.dummy_data.get_simple_dpc_signal()
        >>> fig = s.get_color_image_with_indicator()
        >>> fig.savefig("simple_dpc_test_signal.png")

        Only plotting the phase

        >>> fig = s.get_color_image_with_indicator(only_phase=True)
        >>> fig.savefig("simple_dpc_test_signal.png")

        Matplotlib subplot as input

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> ax_indicator = fig.add_subplot(331)
        >>> fig_return = s.get_color_image_with_indicator(
        ...     scalebar_size=10, ax=ax, ax_indicator=ax_indicator)

        """
        indicator_rotation = indicator_rotation + 60
        if ax is None:
            set_fig = True
            fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        else:
            fig = ax.figure
            set_fig = False
        if only_phase:
            s = self.get_phase_signal(rotation=phase_rotation)
        else:
            s = self.get_color_signal(
                    rotation=phase_rotation, autolim=autolim,
                    autolim_sigma=autolim_sigma)
        s.change_dtype('uint16')
        s.change_dtype('float64')
        extent = self.axes_manager.signal_extent
        extent = [extent[0], extent[1], extent[3], extent[2]]
        ax.imshow(s.data / 65536., extent=extent)
        if ax_indicator is not False:
            if ax_indicator is None:
                ax_indicator = fig.add_subplot(331)
            pst._make_color_wheel(
                    ax_indicator,
                    rotation=indicator_rotation + phase_rotation)
        ax.set_axis_off()
        if scalebar_size is not None:
            scalebar_label = '{0} {1}'.format(
                    scalebar_size, s.axes_manager[0].units)
            sb = AnchoredSizeBar(
                    ax.transData, scalebar_size, scalebar_label, loc=4)
            ax.add_artist(sb)
        if set_fig:
            fig.subplots_adjust(0, 0, 1, 1)
        return fig

    def get_bivariate_histogram(
            self,
            histogram_range=None,
            masked=None,
            bins=200,
            spatial_std=3):
        """
        Useful for finding the distribution of magnetic vectors(?).

        Parameters
        ----------
        histogram_range : tuple, optional
            Set the minimum and maximum of the histogram range.
            Default is setting it automatically.
        masked : 2-D NumPy bool array, optional
            Mask parts of the data. The array must be the same
            size as the signal. The True values are masked.
            Default is not masking anything.
        bins : integer, default 200
            Number of bins in the histogram
        spatial_std : number, optional
            If histogram_range is not given, this value will be
            used to set the automatic histogram range.
            Default value is 3.

        Returns
        -------
        s_hist : HyperSpy Signal2D

        Examples
        --------
        >>> s = ps.dummy_data.get_stripe_pattern_dpc_signal()
        >>> s_hist = s.get_bivariate_histogram()
        >>> s_hist.plot()

        """
        x_position = self.inav[0].data
        y_position = self.inav[1].data
        s_hist = pst._make_bivariate_histogram(
                x_position, y_position,
                histogram_range=histogram_range,
                masked=masked,
                bins=bins,
                spatial_std=spatial_std)
        s_hist.metadata.General.title = "Bivariate histogram of {0}".format(
                self.metadata.General.title)
        return s_hist

    def flip_axis_90_degrees(self, flips=1):
        """Flip both the spatial and beam deflection axis

        Will rotate both the image and the beam deflections
        by 90 degrees.

        Parameters
        ----------
        flips : int, default 1
            Number of flips. The default (1) gives 90 degrees rotation.
            2 gives 180, 3 gives 270, ...

        Examples
        --------
        >>> s = ps.dummy_data.get_stripe_pattern_dpc_signal()
        >>> s
        <DPCSignal2D, title: , dimensions: (2|50, 100)>
        >>> s_rot = s.flip_axis_90_degrees()
        >>> s_rot
        <DPCSignal2D, title: , dimensions: (2|100, 50)>

        Do several flips

        >>> s_rot = s.flip_axis_90_degrees(2)
        >>> s_rot
        <DPCSignal2D, title: , dimensions: (2|50, 100)>
        >>> s_rot = s.flip_axis_90_degrees(3)
        >>> s_rot
        <DPCSignal2D, title: , dimensions: (2|100, 50)>

        """
        s_out = self.deepcopy()
        for i in range(flips):
            data0 = copy.deepcopy(s_out.data[0])
            data1 = copy.deepcopy(s_out.data[1])
            s_out = s_out.swap_axes(1, 2)
            s_out.data[0] = np.rot90(data0, -1)
            s_out.data[1] = np.rot90(data1, -1)
            s_out = s_out.rotate_beam_shifts(90)
        return s_out

    def rotate_data(self, angle, reshape=False):
        """Rotate the scan dimensions by angle.

        Parameters
        ----------
        angle : float
            Clockwise rotation in degrees

        Returns
        -------
        rotated_signal : DPCSignal2D

        Example
        -------

        Rotate data by 10 degrees clockwise

        >>> s = ps.dummy_data.get_simple_dpc_signal()
        >>> s_rot = s.rotate_data(10)
        >>> s_rot.plot()

        """
        s_new = self.map(
                rotate, show_progressbar=False,
                inplace=False, reshape=reshape,
                angle=-angle)
        return s_new

    def rotate_beam_shifts(self, angle):
        """Rotate the beam shift vector.

        Parameters
        ----------
        angle : float
            Clockwise rotation in degrees

        Returns
        -------
        shift_rotated_signal : DPCSignal2D

        Example
        -------

        Rotate beam shifts by 10 degrees clockwise

        >>> s = ps.dummy_data.get_simple_dpc_signal()
        >>> s_new = s.rotate_beam_shifts(10)
        >>> s_new.plot()

        """
        s_new = self.deepcopy()
        angle_rad = np.deg2rad(angle)
        x, y = self.inav[0].data, self.inav[1].data
        s_new.data[0] = x * np.cos(angle_rad) - y * np.sin(angle_rad)
        s_new.data[1] = x * np.sin(angle_rad) + y * np.cos(angle_rad)
        return s_new

    def gaussian_blur(self, sigma=2, output=None):
        """Blur the x- and y-beam shifts.

        Useful for reducing the effects of structural diffraction effects.

        Parameters
        ----------
        sigma : scalar, default 2
        output : HyperSpy signal

        Returns
        -------
        blurred_signal : HyperSpy 2D Signal

        Examples
        --------
        >>> s = ps.dummy_data.get_square_dpc_signal(add_ramp=False)
        >>> s_blur = s.gaussian_blur()

        Different sigma

        >>> s_blur = s.gaussian_blur(sigma=1.2)

        Using the signal itself as output

        >>> s.gaussian_blur(output=s)
        >>> s.plot()

        """
        if output is None:
            s_out = self.deepcopy()
        else:
            s_out = output
        gaussian_filter(self.data[0], sigma=sigma, output=s_out.data[0])
        gaussian_filter(self.data[1], sigma=sigma, output=s_out.data[1])
        if output is None:
            return s_out


class LazyDPCBaseSignal(LazySignal, DPCBaseSignal):
    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LazyDPCSignal1D(LazySignal, DPCSignal1D):
    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LazyDPCSignal2D(LazySignal, DPCSignal2D):
    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LazyPixelatedSTEM(LazySignal, PixelatedSTEM):
    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute(self, *args, **kwargs):
        super().compute(*args, **kwargs)
        self.__class__ = PixelatedSTEM
        self.__init__(**self._to_dictionary())
