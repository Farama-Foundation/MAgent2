""" some utility for call C++ code"""


import ctypes
import multiprocessing
import os
import platform


def _load_lib():
    """Load the native magent shared library."""
    cur_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))

    if platform.system() == "Darwin":
        lib_names = ["libmagent.dylib"]
    elif platform.system() == "Linux":
        lib_names = ["libmagent.so"]
    elif platform.system() == "Windows":
        lib_names = ["magent.dll"]
    else:
        raise OSError("unsupported system: " + platform.system())

    # Also search for .pyd files (setuptools editable installs on Windows)
    import glob

    pyd_files = glob.glob(os.path.join(cur_path, "libmagent*.pyd"))
    lib_names.extend(os.path.basename(f) for f in pyd_files)

    search_paths = []
    for lib_name in lib_names:
        search_paths.append(os.path.join(cur_path, lib_name))
        search_paths.append(os.path.join(cur_path, "build", lib_name))

    for path in search_paths:
        if os.path.exists(path):
            return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)

    raise FileNotFoundError(
        f"Could not find native magent library. Searched:\n"
        + "\n".join(f"  - {p}" for p in search_paths)
    )


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
