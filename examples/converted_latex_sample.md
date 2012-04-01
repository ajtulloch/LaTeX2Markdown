###  Simple Examples


This section introduces the usage of the LaTeX2Markdown tool, showing an example of the various environments available.  

#### Theorem 1 (Euclid, 300 BC)

> There are infinitely many primes.


#### Proof

Suppose that $p_1 < p_2 < \dots < p_n$ are all of the primes. Let $P = 1 + \prod_{i=1}^n p_i$ and let $p$ be a prime dividing $P$.

Then $p$ can not be any of $p_i$, for otherwise $p$ would divide the difference $P - \left(\prod_{i=1}^n p_i \right) - 1$, which is impossible. So this prime $p$ is still another prime, and $p_1, p_2, \dots p_n$ cannot be all of the primes.


#### Exercise 1

> Give an alternative proof that there are an infinite number of prime numbers.


To solve this exercise, we first introduce the following lemma.
#### Lemma 1

> The Fermat numbers $F_n = 2^{2^{n}} + 1$ are pairwise relatively prime.


#### Proof

It is easy to show by induction that
\[ F_m - 2 = F_0 F_1 \dots F_{m-1}. \]
This means that if $d$ divides both $F_n$ and $F_m$ (with $n < m$), then $d$ also divides $F_m - 2$.  Hence, $d$ divides 2.  But every Fermat number is odd, so $d$ is necessarily one.  This proves the lemma.


We can now provide a solution to the exercise.

#### Theorem 2 (Goldbach, 1750)

> There are infinitely many prime numbers.


#### Proof

Choose a prime divisor $p_n$ of each Fermat number $F_n$.  By the lemma we know these primes are all distinct, showing there are infinitely many primes.


###  Demonstration of the environments


We can format *italic text*, **bold text**, and `code` blocks.



1.  A numbered list item
1.  Another numbered list item




*  A bulleted list item
*  Another bulleted list item


#### Theorem 3

> This is a theorem.  It contains an `align` block.
> 
> All math environments supported by MathJaX should work with LaTeX - a full list is available on the MathJaX homepage.
> 
> Maxwell's equations, differential form.
> \begin{align}
> \nabla \cdot \mathbf{E} &= \frac {\rho} {\varepsilon_0} \\\\
> \nabla \cdot \mathbf{B} &= 0 \\\\
> \nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}} {\partial t} \\\\
> \nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}} {\partial t} \\\\
> \end{align}


#### Theorem 4 (Theorem name)

> This is a named theorem.


#### Lemma 2

> This is a lemma.


#### Proposition 1

> This is a proposition


#### Proof

This is a proof.




    This is a code listing.
    One line of code
    Another line of code