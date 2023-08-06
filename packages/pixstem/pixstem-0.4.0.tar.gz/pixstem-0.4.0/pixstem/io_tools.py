import h5py
import logging
import numpy as np
import dask.array as da
from hyperspy.io_plugins import emd
from hyperspy.io import load_with_reader
from hyperspy.io import load
from pixstem.pixelated_stem_class import (
        PixelatedSTEM, DPCBaseSignal, DPCSignal1D, DPCSignal2D,
        LazyPixelatedSTEM)


def _get_dtype_from_header_string(header_string):
    header_split_list = header_string.split(",")
    dtype_string = header_split_list[6]
    if dtype_string == 'U08':
        dtype = ">u1"
    elif dtype_string == 'U16':
        dtype = ">u2"
    elif dtype_string == 'U32':
        dtype = ">u4"
    else:
        print("dtype {0} not recognized, trying unsigned 16 bit".format(
            dtype_string))
        dtype = ">u2"
    return dtype


def _get_detector_pixel_size(header_string):
    header_split_list = header_string.split(",")
    det_x_string = header_split_list[4]
    det_y_string = header_split_list[5]
    try:
        det_x = int(det_x_string)
        det_y = int(det_y_string)
    except NameError:
        print(
                "detector size strings {0} and {1} not recognized, "
                "trying 256 x 256".format(det_x_string, det_y_string))
        det_x, det_y = 256, 256
    if det_x == 256:
        det_x_value = det_x
    elif det_x == 512:
        det_x_value = det_x
    else:
        print("detector x size {0} not recognized, trying 256".format(det_x))
        det_x_value = 256
    if det_y == 256:
        det_y_value = det_y
    elif det_y == 512:
        det_y_value = det_y
    else:
        print("detector y size {0} not recognized, trying 256".format(det_y))
        det_y_value = 256
    return(det_x_value, det_y_value)


def load_binary_merlin_signal(
        filename, probe_x=None, probe_y=None, chunks=(32, 32, 32, 32),
        flyback_pixels=1, datatype=None, lazy_result=True):
    """Temporary function for loading Merlin binary data.

    Parameters
    ----------
    filename : string
    probe_x, probe_y : int
    chunks : tuple
        Default (32, 32, 32, 32)
    flyback_pixels : int
    datatype : string
         6 bit: ">u1". 12 bit: ">u2". 24 bit: ">u4".
    lazy_result : bool

    This function will be replaced at some point, so do not rely on it for
    other functions!

    """
    if (probe_x is None) and (probe_y is None):
        flyback_pixels = 0
        lazy_result = False
    if probe_x is None:
        probe_x = 1
    if probe_y is None:
        probe_y = 1

    f = open(filename, 'rb')
    header_string = f.read(50).decode()
    f.close()

    if datatype is None:
        datatype = _get_dtype_from_header_string(header_string)
    det_x, det_y = _get_detector_pixel_size(header_string)

    value_between_frames = 192

    frametype = np.dtype(
            [
                ('head', np.uint8, value_between_frames*2),
                ('data', datatype, (det_x, det_y))])

    data_with_HF = np.memmap(
            filename, frametype, mode='r',
            shape=(probe_y, probe_x + flyback_pixels))
    if flyback_pixels != 0:
        data_with_HF = data_with_HF[:, 0:-flyback_pixels]

    data_array = data_with_HF['data']

    dask_array = da.from_array(data_array, chunks=chunks)
    dask_array = dask_array.squeeze()
    if lazy_result:
        s = LazyPixelatedSTEM(dask_array)
    else:
        s = PixelatedSTEM(dask_array.compute())
    return s


def _fpd_checker(filename, attr_substring='fpd_version'):
    if h5py.is_hdf5(filename):
        hdf5_file = h5py.File(filename, mode='r')
        for attr in hdf5_file.attrs:
            if attr_substring in attr:
                return(True)
    return(False)


def _hspy_checker(filename, attr_substring='fpd_version'):
    if h5py.is_hdf5(filename):
        hdf5_file = h5py.File(filename, mode='r')
        for attr in hdf5_file.attrs:
            if 'file_format' in attr:
                if hdf5_file.attrs['file_format'] == 'HyperSpy':
                    return(True)
    return(False)


def _load_fpd_sum_im(filename):
    s = load_with_reader(
            filename, reader=emd, dataset_name="/fpd_expt/fpd_sum_im")
    if len(s.axes_manager.shape) == 3:
        s = s.isig[0, :, :]
    return s


def _load_fpd_sum_dif(filename):
    s = load_with_reader(
            filename, reader=emd, dataset_name="/fpd_expt/fpd_sum_dif")
    if len(s.axes_manager.shape) == 3:
        s = s.isig[:, :, 0]
    return s


def _load_fpd_emd_file(filename, lazy=False):
    s = load_with_reader(
            filename, reader=emd, lazy=lazy, dataset_name="/fpd_expt/fpd_data")
    if len(s.axes_manager.shape) == 5:
        s = s.isig[:, :, 0, :, :]
    s = s.transpose(signal_axes=(0, 1))
    s._lazy = lazy
    s_new = signal_to_pixelated_stem(s)
    return(s_new)


def _load_other_file(filename, lazy=False):
    s = load(filename, lazy=lazy)
    s_new = signal_to_pixelated_stem(s)
    return s_new


def _copy_axes_ps_to_dpc(s_ps, s_dpc):
    if s_ps.axes_manager.navigation_dimension > 2:
        raise ValueError(
                "s_ps can not have more than 2 navigation dimensions, "
                "not {0}".format(s_ps.axes_manager.navigation_dimension))
    if s_ps.axes_manager.navigation_shape != s_dpc.axes_manager.signal_shape:
        raise ValueError(
                "s_ps navigation shape {0}, must be the same "
                "as s_dpc signal shape {1}".format(
                    s_ps.axes_manager.navigation_shape,
                    s_dpc.axes_manager.signal_shape))
    ps_a_list = s_ps.axes_manager.navigation_axes
    dp_a_list = s_dpc.axes_manager.signal_axes
    for ps_a, dp_a in zip(ps_a_list, dp_a_list):
        dp_a.offset = ps_a.offset
        dp_a.scale = ps_a.scale
        dp_a.units = ps_a.units
        dp_a.name = ps_a.name


def signal_to_pixelated_stem(s):
    """Make a PixelatedSTEM object from a HyperSpy signal.

    This will retain both the axes information and the metadata.
    If the signal is lazy, the function will return LazyPixelatedSTEM.

    Parameters
    ----------
    s : HyperSpy signal
        Should work for any HyperSpy signal.

    Returns
    -------
    pixelated_stem_signal : PixelatedSTEM or LazyPixelatedSTEM object

    Examples
    --------
    >>> import numpy as np
    >>> import hyperspy.api as hs
    >>> s = hs.signals.Signal2D(np.random.random((8, 11, 21, 13)))
    >>> s.metadata.General.title = "test dataset"
    >>> s
    <Signal2D, title: test dataset, dimensions: (11, 8|13, 21)>
    >>> from pixstem.io_tools import signal_to_pixelated_stem
    >>> s_new = signal_to_pixelated_stem(s)
    >>> s_new
    <PixelatedSTEM, title: test dataset, dimensions: (11, 8|13, 21)>

    """
    # Sorting axes as a function of its index
    axes_list = [x for _, x in sorted(s.axes_manager.as_dictionary().items())]
    metadata = s.metadata.as_dictionary()
    if s._lazy:
        s_new = LazyPixelatedSTEM(s.data, axes=axes_list, metadata=metadata)
    else:
        s_new = PixelatedSTEM(s.data, axes=axes_list, metadata=metadata)
    return s_new


def load_ps_signal(
        filename, lazy=False, chunk_size=None,
        navigation_signal=None):
    """
    Parameters
    ----------
    filename : string
    lazy : bool, default False
    chunk_size : tuple, optional
        Used if Lazy is True. Sets the chunk size of the signal.
        If it is not specified, the file chunking will be used.
        Higher number will potentially make the calculations be faster,
        but use more memory.
    navigation_signal : Signal2D

    """
    if _fpd_checker(filename, attr_substring='fpd_version'):
        s = _load_fpd_emd_file(filename, lazy=lazy)
    elif _hspy_checker(filename, attr_substring='HyperSpy'):
        s = _load_other_file(filename, lazy=lazy)
    else:
        # Attempt to load non-fpd and non-HyperSpy signal
        s = _load_other_file(filename, lazy=lazy)
    if navigation_signal is None:
        try:
            s_nav = _load_fpd_sum_im(filename)
            s.navigation_signal = s_nav
        except IOError:
            logging.debug("Nav signal not found in {0}".format(filename))
            s.navigation_signal = None
        except ValueError:
            logging.debug("Nav signal in {0}: wrong shape".format(filename))
            s.navigation_signal = None
    else:
        nav_im_shape = navigation_signal.axes_manager.signal_shape
        nav_ax_shape = s.axes_manager.navigation_shape
        if nav_im_shape == nav_ax_shape:
            s.navigation_signal = navigation_signal
        else:
            raise ValueError(
                    "navigation_signal does not have the same shape ({0}) as "
                    "the signal's navigation shape ({1})".format(
                        nav_im_shape, nav_ax_shape))
    if lazy:
        if chunk_size is not None:
            s.data = s.data.rechunk(chunks=chunk_size)
    return s


def load_dpc_signal(filename):
    """Load a differential phase contrast style signal.

    This function can both files saved directly using HyperSpy,
    and saved using this library. The only requirement is that
    the signal has one navigation dimension, with this one dimension
    having a size of two. The first navigation index is the x-shift,
    while the second is the y-shift.
    The signal dimension contains the spatial dimension(s), i.e. the
    probe positions.

    The return signal depends on the dimensions of the input file:
    - If two signal dimensions: DPCSignal2D
    - If one signal dimension: DPCSignal1D
    - If zero signal dimension: DPCBaseSignal

    Parameters
    ----------
    filename : string

    Returns
    -------
    dpc_signal : DPCBaseSignal, DPCSignal1D, DPCSignal2D
        The type of return signal depends on the signal dimensions of the
        input file.

    Examples
    --------
    >>> import numpy as np
    >>> s = ps.DPCSignal2D(np.random.random((2, 90, 50)))
    >>> s.save("test_dpc_signal2d.hspy", overwrite=True)
    >>> s_dpc = ps.load_dpc_signal("test_dpc_signal2d.hspy")
    >>> s_dpc
    <DPCSignal2D, title: , dimensions: (2|50, 90)>
    >>> s_dpc.plot()

    Saving a HyperSpy signal

    >>> import hyperspy.api as hs
    >>> s = hs.signals.Signal1D(np.random.random((2, 10)))
    >>> s.save("test_dpc_signal1d.hspy", overwrite=True)
    >>> s_dpc_1d = ps.load_dpc_signal("test_dpc_signal1d.hspy")
    >>> s_dpc_1d
    <DPCSignal1D, title: , dimensions: (2|10)>

    """
    s = load(filename)
    if s.axes_manager.navigation_shape != (2,):
        raise Exception(
                "DPC signal needs to have 1 navigation "
                "dimension with a size of 2.")
    if s.axes_manager.signal_dimension == 0:
        s_out = DPCBaseSignal(s).T
    elif s.axes_manager.signal_dimension == 1:
        s_out = DPCSignal1D(s)
    elif s.axes_manager.signal_dimension == 2:
        s_out = DPCSignal2D(s)
    else:
        raise NotImplementedError(
                "DPC signals only support 0, 1 and 2 signal dimensions")
    s_out.metadata = s.metadata.deepcopy()
    s_out.axes_manager = s.axes_manager.deepcopy()
    return s_out
