import os
import platform
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

            # lib_ext = ""
            # lib_name = ""

            if platform.system() == "Darwin":
                # lib_ext = ".dylib"
                # lib_name = "libmagent"
                thread_num = check_output(["sysctl", "-n", "hw.ncpu"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()],
                    cwd=extdir,
                )
            elif platform.system() == "Linux":
                # lib_ext = ".so"
                # lib_name = "libmagent"
                thread_num = check_output(["nproc"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()],
                    cwd=extdir,
                )
            elif platform.system() == "Windows":
                # lib_ext = ".dll"
                # lib_name = "magent"
                thread_num = 1
                # cmake --build . --target ALL_BUILD --config Release
                subprocess.check_call(
                    ["cmake", "--build", ".", "--target", "ALL_BUILD", "--config", cfg],
                    cwd=make_location,
                    shell=True,
                )
            # build_res_dir = extdir + "/magent/build/"
            # if not os.path.exists(build_res_dir):
            #     os.makedirs(build_res_dir)
            # lib_name = extdir + "/libmagent" + lib_ext
            # subprocess.check_call(
            #     ["mv", lib_name, build_res_dir]
            # )


setuptools.setup(
    name="magent2",
    version=get_version(),
    ext_modules=[CMakeExtension("magent2.libmagent", ".", [])],
    cmdclass={"build_ext": CMakeBuild},
)
