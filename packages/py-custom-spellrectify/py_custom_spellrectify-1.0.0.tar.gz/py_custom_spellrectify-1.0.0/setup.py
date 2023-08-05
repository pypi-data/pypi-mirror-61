import os.path

from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="py_custom_spellrectify",
    version="1.0.0",
    author="Vimal Dharmalingam",
    author_email="vimald8959@gmail.com",
    description="Python Custom Spell Rectifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vimal-dharmalingam/py_custom_spellrectify",
    packages=find_packages(),
    install_requires=['requests>=1.16.4'],
    classifiers=[

        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
