import setuptools
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kplot",
    version="0.0.12",
    author="Keyan Gootkin",
    author_email="KeyanGootkin@gmail.com",
    description="A small package for making matplotlib plots pretty <3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    data_files=[('styles', glob('*.mplstyle'))],
    url="https://github.com/KeyanGootkin/kplot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)