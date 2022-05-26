import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from subprocess import check_call, check_output, Popen, PIPE
import os
import platform
import pathlib
import subprocess

###
# Build process:
# cmake .
# make -j threads
# move libmagent -> build/
###

with open("README.md", "r") as fh:
    long_description = fh.read()

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
                "-DCMAKE_BUILD_TYPE={}".format(cfg),
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir),
                "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir),
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
              cdir = str(subprocess.check_output(["cd"], shell=True).decode()).strip()
              #subprocess.check_call(["dir"], shell=True)
            else:
              subprocess.check_call(["pwd"])
              print(extdir)
              subprocess.check_call(["ls"])

            lib_ext = ""
            lib_name = ""

            if platform.system() == "Darwin":
                lib_ext = ".dylib"
                lib_name = "libmagent"
                thread_num = check_output(["sysctl", "-n", "hw.ncpu"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()], cwd=extdir
                )
            elif platform.system() == "Linux":
                lib_ext = ".so"
                lib_name = "libmagent"
                thread_num = check_output(["nproc"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()], cwd=extdir
                )
            elif platform.system() == "Windows":
                lib_ext = ".dll"
                lib_name = "magent"
                thread_num = 1
                # cmake --build . --target ALL_BUILD --config Release
                subprocess.check_call(
                    ["cmake",
                    "--build",".","--target","ALL_BUILD","--config",cfg], cwd=make_location
                , shell=True)
            # build_res_dir = extdir + "/magent/build/"
            # if not os.path.exists(build_res_dir):
            #     os.makedirs(build_res_dir)
            # lib_name = extdir + "/libmagent" + lib_ext
            # subprocess.check_call(
            #     ["mv", lib_name, build_res_dir]
            # )


setuptools.setup(
    name="magent",
    version="0.2.3",
    author="Farama Foundation",
    author_email="jkterry@farama.org",
    description="Multi-Agent Reinforcement Learning environments with very large numbers of agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Farama-Foundation/MAgent",
    keywords=["Reinforcement Learning", "game", "RL", "AI"],
    packages=setuptools.find_packages(),
    ext_modules=[
        CMakeExtension("magent.libmagent", ".", [])
    ],
    install_requires=[
        'numpy>=1.18.0',
        'pygame==2.1.0'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    cmdclass = {
        "build_ext": CMakeBuild
    },
)
