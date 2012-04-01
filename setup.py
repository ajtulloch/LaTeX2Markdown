from distutils.core import setup
import os


def get_rst():
    os.system("pandoc -f markdown -t rst README.md > README.rst")
    with open("README.rst", "r") as f:
        long_description = f.read()
    os.system("rm README.rst")
    return long_description

setup(name='latex2markdown',
      author="Andrew Tulloch",
      author_email="andrew@tullo.ch",
      version='1.0',
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
       long_description=long_description)
