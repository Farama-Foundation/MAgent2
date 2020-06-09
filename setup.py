import setuptools
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.install_lib import install_lib
from setuptools.command.build_ext import build_ext as build_ext_orig
from subprocess import check_call
from distutils.sysconfig import get_python_lib
import os
import platform
import pathlib
import atexit
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    version="0.1.6",
    author="PettingZoo Team",
    author_email="justinkterry@gmail.com",
    description="Multi-Agent Reinforcement Learning environments with very large numbers of agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PettingZoo-Team/MAgent",
    keywords=["Reinforcement Learning", "game", "RL", "AI"],
    packages=setuptools.find_packages(),
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
        'install_lib': PostInstallCommand,
    },
)



