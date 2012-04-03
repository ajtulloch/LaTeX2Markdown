from distutils.core import setup

setup(
        name='latex2markdown',
        author="Andrew Tulloch",
        author_email="andrew@tullo.ch",
        version='0.2.1',
        py_modules=['latex2markdown'],
        scripts=['bin/converted_latex_sample.md','bin/latex_sample.tex'],
        url="https://github.com/ajtulloch/LaTeX2Markdown",
        description="An AMS-LaTeX compatible converter that maps a subset of LaTeX to Markdown/MathJaX.",
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
        long_description=open("README.txt").read()
        )
