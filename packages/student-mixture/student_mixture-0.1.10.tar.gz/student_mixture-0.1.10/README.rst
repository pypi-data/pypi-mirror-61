Student's t-Mixture Model
=========================

A Python implementation of "Robust mixture modelling using the t
distribution" (Peel & McLachlan, 2000) and extensions.

Features
========

-  Class StudentMixture: module for fitting a mixture of multivariate
   Student's t-distributions.
-  Class MultivariateT: module for using a multivariate Student's
   t-random variable
-  Class MultivaraiteTFit: module for fitting a multivariate Student's
   t-distribution.

Installation
============

With pip:

::

    pip install student-mixture

From github:

::

    git clone https://github.com/omritomer/student_mixture.git
    cd student_mixture
    python setup.py build
    python setup.py install

Requirements
============

-  numpy==1.17.3
-  scipy==1.3.1
-  scikit-learn==0.21.3

References
==========

1. Peel, D., & McLachlan, G. J. (2000). Robust mixture modelling using
   the t distribution. *Statistics and computing*, *10*\ (4), 339-348.
2. McLachlan, G. J., & Peel, D. (2004). *Finite mixture models*. John
   Wiley & Sons.
3. McLachlan, G. J., & Krishnan, T. (2007). *The EM algorithm and
   extensions* (Vol. 382). John Wiley & Sons.
4. Genz, A., & Bretz, F. (2009). *Computation of multivariate normal and
   t probabilities* (Vol. 195). Springer Science & Business Media.
5. Genz, A. (2004). Numerical computation of rectangular bivariate and
   trivariate normal and t probabilities. *Statistics and Computing*,
   *14*\ (3), 251-260.
6. Genz, A., & Bretz, F. (1999). Numerical computation of multivariate
   t-probabilities with application to power calculation of multiple
   contrasts. *Journal of Statistical Computation and Simulation*,
   *63*\ (4), 103-117.
7. Genz, A., & Bretz, F. (2002). Comparison of methods for the
   computation of multivariate t probabilities. *Journal of
   Computational and Graphical Statistics*, *11*\ (4), 950-971.
8. Kotz, S., & Nadarajah, S. (2004). *Multivariate t-distributions and
   their applications*. Cambridge University Press.

Citation
========

If you used this package to estimate a mixture of Student's
t-distributions, please cite references 1 and 2, which this package is
an implementation of.

If you used this package to estimate a Student's t-distribution, please
cite reference 3.

<<<<<<< HEAD The implementations mentioned above are structurally based
on scikit-learn's mixture module, so please also cite scikit-learn
according to their suggested format, which can be found
`here <[https://scikit-learn.org/stable/about.html#citing-scikit-learn](https://scikit-learn.org/stable/about.html#citing-scikit-learn)>`__.
======= The implementations above are structurally based on
scikit-learn's mixture module, so please also cite scikit-learn
according to their suggested format, which can be found
`here <[https://scikit-learn.org/stable/about.html#citing-scikit-learn](https://scikit-learn.org/stable/about.html#citing-scikit-learn)>`__.
>>>>>>> 194301d0b20537ef19b8eeffa24feb0bcce1a646

If you used the multivariate Student's t-distribution module, please
cite reference 8. As this module is structurally based on scipy's
stats.multivariate module, please also cite scipy according to their
suggested format, which can be found
`here <[https://www.scipy.org/citing.html](https://www.scipy.org/citing.html)>`__.

If you used the cumulative distribution function (CDF) for either a
multivariate t-distribution or a Student's t-mixture model, please cite
reference 4. In addition, for the following cases:

-  If your data has two or three dimensions, please cite reference 5.

-  If your data has four or more dimensions, please cite references 6
   and 7.

Documentation
=============

`Student's t-Mixture
Model <[https://student-mixture.readthedocs.io/](https://student-mixture.readthedocs.io/)>`__

Authors
=======

Omri Tomer (omritomer1@mail.tau.ac.il)

License
=======

<<<<<<< HEAD This package is distributed under the BSD 3-Clause License.
See the LICENSE file for information. ======= This package is
distributed under the BSD 3-Clause License. See the LICENSE file for
information. >>>>>>> 194301d0b20537ef19b8eeffa24feb0bcce1a646
