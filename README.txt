LaTeX2Markdown
==============

An `AMS-LaTeX <http://en.wikipedia.org/wiki/AMS-LaTeX>`_ compatible
converter from (a subset of) `LaTeX <http://www.latex-project.org/>`_ to
`MathJaX <http://www.mathjax.org/>`_ compatible
`Markdown <http://daringfireball.net/projects/markdown/>`_.

Anyone who writes LaTeX documents using the AMS-LaTeX packages
(``amsmath``, ``amsthm``, ``amssymb``) and wants to convert these
documents to Markdown format to use with MathJaX. These Markdown files
can then be easily added to any web platform - Jekyll blogs, Wordpress,
basic HTML sites, etc.

In short, if you seek to use MathJaX to view your LaTeX documents
online, then you might be interested in this.

Demonstration
-------------

Check out
`tullo.ch/projects/LaTeX2Markdown <http://tullo.ch/projects/LaTeX2Markdown>`_
for a live demonstration of the converter.

Getting Started
---------------

Installation
~~~~~~~~~~~~

The project is available on PyPI, so getting it is as simple as using

::

    pip install latex2markdown

or

::

    easy_install latex2markdown

Usage
~~~~~

The utility can be called from the command line, or from within a Python
script.

For the command line, the syntax to convert a LaTeX file to a Markdown
file is as follows:

::

    python -m latex2markdown path/to/latex/file path/to/output/markdown/file

For example, to compile a LaTeX file ``sample.tex`` into a Markdown file
``sample.md``, call

::

    python -m latex2markdown sample.tex sample.md

To use it within a Python script (to extend it, modify output, etc.),
you can use it as follows:

::

    import latex2markdown
    with open("latex_file.tex", "r") as f:
        latex_string = f.read()

    l2m = latex2markdown.LaTeX2Markdown(latex_string)

    markdown_string = l2m.to_markdown()

    with open("markdown_file.md", "w") as f:
        f.write(markdown_string)

Finally, add the following snippet to your HTML when loading this
document.

::

    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            extensions: ["tex2jax.js", "AMSmath.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\[","\]"] ],
                processEscapes: true
            },
        });
    </script>
    <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>

For a working example, have a look at the source of the
`tullo.ch <http://tullo.ch>`_ homepage
`here <https://github.com/ajtulloch/ajtulloch.github.com>`_.

Why not use Pandoc?
-------------------

`Pandoc <http://johnmacfarlane.net/pandoc/%20##%20Who%20should%20use%20this?>`_
is an excellent document converter for less complex LaTeX documents.
Indeed, I've used it to convert this README document to a reST version
for use on PyPI.

Unfortunately, it is not designed to deal with documents that use the
AMSTeX extensions - which include the theorem, lemma, proof, and
exercise environments that are heavily used for typesetting papers,
lecture notes, and other documents.

As neither Pandoc nor MathJaX can deal with these documents, I hacked
together a set of regular expressions that can convert a subset of LaTeX
to Markdown, and used a few more to convert the sMarkdown to
MathJaX-convertible Markdown.

Example
-------

As an example, the following LaTeX code:

::

    \section{Example Section}
    \begin{thm}[Euclid]
        There are infinitely many primes.
    \end{thm}

    \begin{proof}
        Suppose that $p_1 < p_2 < \dots < p_n$ are all of the primes. 
        Let $P = 1 + \prod_{i=1}^n p_i$ and let $p$ be a prime dividing $P$.

        Then $p$ can not be any of $p_i$, for otherwise $p$ would divide the 
        difference $P - \left(\prod_{i=1}^n p_i \right) - 1$, which is impossible. 
        So this prime $p$ is still another prime, and $p_1, p_2, \dots p_n$ 
        cannot be all of the primes.
    \end{proof}

is converted into the following Markdown:

::

    ###  Example Section
    #### Theorem 1 (Euclid)

    > There are infinitely many primes.

    #### Proof

    Suppose that $p_1 < p_2 < \dots < p_n$ are all of the primes. 
    Let $P = 1 + \prod_{i=1}^n p_i$ and let $p$ be a prime dividing $P$.

    Then $p$ can not be any of $p_i$, for otherwise $p$ would divide the difference 
    $P - \left(\prod_{i=1}^n p_i \right) - 1$, which is impossible. So this prime 
    $p$ is still another prime, and $p_1, p_2, \dots p_n$ cannot be all of the primes.

Supported LaTeX/AMSTeX Environments
-----------------------------------

-  ``emph``, ``textbf``, ``texttt``
-  ``thm``
-  ``prop``
-  ``lem``
-  ``exer``
-  ``proof``
-  ``chapter``
-  ``section``
-  ``subsection``
-  ``itemize``
-  ``enumerate``

along with everything supported by MathJax - list available
`online <http://www.mathjax.org/docs/2.0/tex.html#supported-latex-commands>`_.
