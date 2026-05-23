import os
import platform
import shutil
import subprocess

import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext


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
    def __init__(self, name, sourcedir, config=None):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        self.config = config or []


class CMakeBuild(build_ext):
    def build_extensions(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the extensions: %s"
                % ", ".join(ext.name for ext in self.extensions)
            )
        cfg = "Release"
        for ext in self.extensions:
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

            cmake_config_args = [
                f"-DCMAKE_BUILD_TYPE={cfg}",
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                f"-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                f"-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{cfg.upper()}={self.build_temp}",
            ]

            make_location = os.path.abspath(self.build_temp)

            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_config_args, cwd=make_location
            )

            subprocess.check_call(
                ["cmake", "--build", ".", "--config", cfg],
                cwd=make_location,
            )

            # CMake produces magent.dll / libmagent.so / libmagent.dylib,
            # but setuptools expects a .pyd file on Windows. Copy the built
            # shared library to the path setuptools expects.
            ext_fullpath = self.get_ext_fullpath(ext.name)
            ext_fulldir = os.path.dirname(ext_fullpath)
            if platform.system() == "Windows":
                built_lib = os.path.join(extdir, "magent.dll")
            elif platform.system() == "Darwin":
                built_lib = os.path.join(extdir, "libmagent.dylib")
            else:
                built_lib = os.path.join(extdir, "libmagent.so")

            if os.path.exists(built_lib):
                os.makedirs(ext_fulldir, exist_ok=True)
                shutil.copy2(built_lib, ext_fullpath)


setuptools.setup(
    name="magent2",
    version=get_version(),
    packages=setuptools.find_packages(),
    ext_modules=[CMakeExtension("magent2.libmagent", ".", [])],
    cmdclass={"build_ext": CMakeBuild},
    package_data={"magent2": ["environments/*", "config/*", "scenarios/*"]},
    include_package_data=True,
)
