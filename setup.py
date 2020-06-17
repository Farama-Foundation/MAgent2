import setuptools
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.install_lib import install_lib
from setuptools.command.build_ext import build_ext
from subprocess import check_call
from distutils.sysconfig import get_python_lib
import os
import platform
import pathlib
import atexit
import shutil
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

            cmake_config_args = [
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), self.build_temp),
                "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), self.build_temp),
                "-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}".format(
                    cfg.upper(), self.build_temp
                ),
            ]

            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_config_args, cwd=self.build_temp
            )

            subprocess.check_call(["pwd"])
            print(self.build_temp)
            subprocess.check_call(["ls"])
            lib_ext = ""

            if platform.system() == "Darwin":
                lib_ext = ".dylib"
                subprocess.check_call(
                    ["make", "-C", ext.sourcedir], cwd=self.build_temp
                )
            elif platform.system() == "Linux":
                lib_ext = ".so"
                subprocess.check_call(
                    ["make", "-C", ext.sourcedir, "-j", "`nproc`"], cwd=self.build_temp, shell=True
                )

            build_res_dir = ext.sourcedir + "/magent/build/"
            if not os.path.exists(build_res_dir):
                os.makedirs(build_res_dir)
            lib_name = ext.sourcedir + "/libmagent" + lib_ext
            subprocess.check_call(
                ["mv", lib_name, build_res_dir]
            )

class PostInstallCommand(install_lib):
    def run(self):
        build_dir = self.build_dir
        post_install_script(build_dir)
        install_lib.run(self)
        
def post_install_script(s):
    current_dir = os.getcwd()
    site_p = pathlib.Path(s).parent
    print("b dir", site_p)
    raw_build_dir = site_p / "lib" / "magent"
    raw_build_dir = str(raw_build_dir.absolute())
    print("r dir ", raw_build_dir)
    if raw_build_dir != "":
        os.chdir(str(raw_build_dir))
        check_call("bash build.sh".split())
        magent_site = get_python_lib() + "/magent/build"
        built_path = raw_build_dir + "/build"
        print("b path ", built_path)
        print("m site ", magent_site)
        if platform.system() == "Darwin":
            shutil.move(built_path, magent_site)
        os.chdir(str(current_dir))
    else:
        print("pre-built src not available, cannot build.")


setuptools.setup(
    name="magent",
    version="0.1.8",
    author="PettingZoo Team",
    author_email="justinkterry@gmail.com",
    description="Multi-Agent Reinforcement Learning environments with very large numbers of agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PettingZoo-Team/MAgent",
    keywords=["Reinforcement Learning", "game", "RL", "AI"],
    packages=setuptools.find_packages(),
    ext_modules=[
        CMakeExtension("libmagent", ".", [])
    ],
    install_requires=[
        'numpy>=1.18.0',
        'pygame>=2.0.0.dev10'
    ],
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    cmdclass = {
        "build_ext": CMakeBuild
    },
)



