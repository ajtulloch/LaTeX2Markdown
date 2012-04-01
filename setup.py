import os
import sys

from setuptools import setup


def publish():
	"""Publish to PyPi"""
	os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
	publish()
	sys.exit()


setup(
        name='latex2markdown',
        author="Andrew Tulloch",
        author_email="andrew@tullo.ch",
        version='0.1.2',
        py_modules=['latex2markdown'],
        url="https://github.com/ajtulloch/LaTeX2Markdown",
        description="An AMSTeX compatible converter that maps a subset of AMSTeX and LaTeX to Markdown/MathJaX.",      
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Mathematics",
            "Topic :: Software Development :: Documentation",
            "Topic :: Text Processing :: Markup",
            "Topic :: Text Processing :: Markup :: LaTeX",
            "Topic :: Text Processing :: Markup :: HTML"
            ],
        long_description=open("README.rst").read()
        )
