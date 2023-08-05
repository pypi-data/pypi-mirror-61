from setuptools import setup, find_packages
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kplot",
    version="0.0.13",
    author="Keyan Gootkin",
    author_email="KeyanGootkin@gmail.com",
    description="A small package for making matplotlib plots pretty <3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=find_packages("kplot"), 
    package_dir={"": "kplot"},  

    package_data={"": ["*.mplstyle"]},  
  
    url="https://github.com/KeyanGootkin/kplot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)