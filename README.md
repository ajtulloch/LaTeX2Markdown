# LaTeX2Markdown

An AMSTeX compatible converter from (a subset of) LaTeX to MathJaX compatible Markdown.

## Who should use this?

Anyone who writes LaTeX documents using the AMSTeX packages (`amsmath`, `amsthm`, `amssymb`) and wants to convert these documents to Markdown format to use with MathJaX.  The outputted Markdown files can then be easily added to any web platform - Jekyll blogs, Wordpress, basic HTML sites, etc. 

In short, if you seek to use MathJaX to view your LaTeX documents online, then you might be interested in this.

## Why not use Pandoc?

Pandoc is an excellent document converter for less complex LaTeX documents.  Unfortunately, it is not designed to deal with documents that use the AMSTeX extensions - which include the theorem, lemma, proof, and exercise environments that are heavily used for typesetting papers, lecture notes, and other documents.

As neither Pandoc nor MathJax can deal with these documents, I hacked together a set of regular expressions that can convert a subset of LaTeX to Markdown, and used a few more to convert this Markdown to MathJaX-convertible Markdown.

## What's an example?

Go to [tullo.ch/LaTeX2Markdown](http://tullo.ch/LaTeX2Markdown) for a live demonstration of the converter.

As an example, the following LaTeX code:

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

is converted into the following Markdown markup:
    
    ###  Example Section
    #### Theorem 1 (Euclid)

    > There are infinitely many primes.

    #### Proof

    Suppose that $p_1 < p_2 < \dots < p_n$ are all of the primes. 
    Let $P = 1 + \prod_{i=1}^n p_i$ and let $p$ be a prime dividing $P$.

    Then $p$ can not be any of $p_i$, for otherwise $p$ would divide the difference 
    $P - \left(\prod_{i=1}^n p_i \right) - 1$, which is impossible. So this prime 
    $p$ is still another prime, and $p_1, p_2, \dots p_n$ cannot be all of the primes.

## Usage

Once the repository has been cloned, converting your LaTeX files is as simple as calling:

    python latex2markdown.py path/to/latex/file path/to/output/file

## Supported LaTeX/AMSTeX Environments

* `emph`, `textbf`, `texttt`
* `thm`
* `prop`
* `lem`
* `exer  `
* `proof`
* `chapter`
* `section`
* `subsection`
* `itemize`
* `enumerate`