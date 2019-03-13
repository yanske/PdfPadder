import re
from setuptools import setup
 
"""Setup script to distribute PDF Padder.

Creates an executable callable by `padder`
Run script by `python3 setup.py install`
"""

setup(
  name = "pdf-padder",
  packages = ["padder"],
  entry_points = {
    "console_scripts": ['padder = padder.padder:main']
  },
  version = 1.1,
  description = "Add whitespace to PDF files.",
  author = "Yan Ke",
)
