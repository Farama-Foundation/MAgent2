""" some utility for call C++ code"""


import ctypes
import multiprocessing
import os
import platform
import sysconfig


def _load_lib():
    """Load library in local."""
    lib_path = os.path.dirname(os.path.abspath(__file__))
    if platform.system() not in ("Darwin", "Linux", "Windows"):
        raise BaseException("unsupported system: " + platform.system())

    # setup.py copies the built library to the interpreter-specific extension
    # path (magent2/libmagent<EXT_SUFFIX>, e.g. libmagent.cpython-312-darwin.so
    # or libmagent.cp312-win_amd64.pyd), so load it from that same name.
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
    path_to_so_file = os.path.join(lib_path, "libmagent" + ext_suffix)

    if not os.path.exists(path_to_so_file):
        raise FileNotFoundError(f"Could not find the DLL file at: {path_to_so_file}")

    lib = ctypes.CDLL(path_to_so_file, ctypes.RTLD_GLOBAL)
    return lib


def as_float_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_float))


def as_int32_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))


def as_bool_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_bool))


if "OMP_NUM_THREADS" not in os.environ:
    os.environ["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count() // 2)
_LIB = _load_lib()
