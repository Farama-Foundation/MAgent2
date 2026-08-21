import os
import platform
import shutil
import subprocess
from subprocess import check_output

import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext


###
# Build process:
# cmake .
# make -j threads
# move libmagent -> build/
###


def get_version():
    """Gets the magent2 version."""
    path = "magent2/__init__.py"
    with open(path) as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("__version__"):
            return line.strip().split()[-1].strip().strip('"')
    raise RuntimeError("bad version data in __init__.py")


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir, config=[]):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        self.config = config


class CMakeBuild(build_ext):
    def build_extensions(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the extensions: %s"
                % ", ".join(ext.name for ext in self.extensions)
            )
        cfg = "Debug" if self.debug else "Release"
        for ext in self.extensions:
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

            cmake_config_args = [
                f"-DCMAKE_BUILD_TYPE={cfg}",
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                f"-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                "-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}".format(
                    cfg.upper(), self.build_temp
                ),
            ]

            make_location = os.path.abspath(self.build_temp)

            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_config_args, cwd=make_location
            )
            print(ext.name)
            if platform.system() == "Windows":
                str(subprocess.check_output(["cd"], shell=True).decode()).strip()
                # subprocess.check_call(["dir"], shell=True)
            else:
                subprocess.check_call(["pwd"])
                print(extdir)
                subprocess.check_call(["ls"])

            if platform.system() == "Darwin":
                lib_name, lib_ext = "libmagent", ".dylib"
                thread_num = check_output(["sysctl", "-n", "hw.ncpu"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()],
                    cwd=extdir,
                )
            elif platform.system() == "Linux":
                lib_name, lib_ext = "libmagent", ".so"
                thread_num = check_output(["nproc"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()],
                    cwd=extdir,
                )
            elif platform.system() == "Windows":
                lib_name, lib_ext = "magent", ".dll"
                # cmake --build . --target ALL_BUILD --config Release
                subprocess.check_call(
                    ["cmake", "--build", ".", "--target", "ALL_BUILD", "--config", cfg],
                    cwd=make_location,
                    shell=True,
                )
            else:
                raise RuntimeError("unsupported system: " + platform.system())

            # CMake emits a generically-named shared library (e.g.
            # libmagent.dylib / libmagent.so / magent.dll). setuptools, however,
            # expects the extension at the interpreter-specific path returned by
            # get_ext_fullpath (e.g. magent2/libmagent.cpython-312-darwin.so).
            # Copy the built library there so both wheel builds and editable
            # (`pip install -e .`) installs can locate it. See c_lib.py, which
            # loads the library from this same EXT_SUFFIX-based name.
            built_lib = self._find_built_lib(extdir, lib_name, lib_ext, cfg)
            ext_fullpath = self.get_ext_fullpath(ext.name)
            os.makedirs(os.path.dirname(ext_fullpath), exist_ok=True)
            shutil.copyfile(built_lib, ext_fullpath)

    @staticmethod
    def _find_built_lib(extdir, lib_name, lib_ext, cfg):
        """Locate the shared library produced by the CMake/make build."""
        candidates = [
            os.path.join(extdir, lib_name + lib_ext),
            # Multi-config generators (e.g. MSVC) nest the output in a
            # per-config subdirectory.
            os.path.join(extdir, cfg, lib_name + lib_ext),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError(
            "Could not find the built magent library. Looked in: "
            + ", ".join(candidates)
        )


setuptools.setup(
    name="magent2",
    version=get_version(),
    packages=setuptools.find_packages(),
    ext_modules=[CMakeExtension("magent2.libmagent", ".", [])],
    cmdclass={"build_ext": CMakeBuild},
    package_data={"magent2": ["environments/*", "config/*", "scenarios/*"]},
    include_package_data=True,
)
