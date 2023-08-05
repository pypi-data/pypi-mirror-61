# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 19:56:10 2020

@author: HP
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="outliers-ashikothari10", # Replace with your own username
    version="0.0.1",
    author=" Author: Ashi Kothari",
    author_email="ashikothari10@gmail.com",
    description="An outlier removal method (By removing rows)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)