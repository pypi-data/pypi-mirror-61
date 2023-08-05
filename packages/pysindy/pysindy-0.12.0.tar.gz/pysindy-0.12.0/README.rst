PySINDy
=========

|BuildCI| |RTD| |PyPI| |Codecov|

**PySINDy** is a sparse regression package with several implementations for the Sparse Identification of Nonlinear Dynamical systems (SINDy) method.

Installation
------------

Installing with pip
^^^^^^^^^^^^^^^^^^^

If you are using Linux or macOS you can install PySINDy with pip:

``pip install pysindy``

Installing from source
^^^^^^^^^^^^^^^^^^^^^^
First clone this repository:

``git clone https://github.com/dynamicslab/pysindy``

Then, to install the package, run

``pip install .``

If you do not have pip you can instead use

``python setup.py install``

If you do not have root access, you should add the ``--user`` option to the above lines.

Documentation
-------------
The documentation for PySINDy can be found `here <https://pysindy.readthedocs.io/en/latest/>`_.

Community guidelines
--------------------

Contributing code
^^^^^^^^^^^^^^^^^
We welcome contributions to PySINDy. To contribute a new feature please submit a pull request. To be accepted your code should conform to PEP8 (you may choose to use flake8 to test this before submitting your pull request). Your contributed code should pass all unit tests. Upon submission of a pull request, your code will be linted and tested automatically, but you may also choose to lint it yourself invoking

``pre-commit -a -v``

as well as test it yourself by running

``pytest``

Reporting issues or bugs
^^^^^^^^^^^^^^^^^^^^^^^^
If you find a bug in the code or want to request a new feature, please open an issue.

Getting help
^^^^^^^^^^^^
For help using PySINDy please consult the `documentation <https://pysindy.readthedocs.io/en/latest/>`_ and/or our `examples <https://github.com/dynamicslab/pysindy/tree/master/example>`_, or create an issue.

References
----------------------

-  Brunton, Steven L., Joshua L. Proctor, and J. Nathan Kutz.
   *Discovering governing equations from data by sparse identification
   of nonlinear dynamical systems.* Proceedings of the National
   Academy of Sciences 113.15 (2016): 3932-3937.
   `[DOI] <http://dx.doi.org/10.1073/pnas.1517384113>`__

-  Champion, Kathleen, Peng Zheng, Aleksandr Y. Aravkin, Steven L.
   Brunton, and J. Nathan Kutz. *A unified sparse optimization
   framework to learn parsimonious physics-informed models from
   data.* arXiv preprint arXiv:1906.10612 (2019).
   `[arXiv] <https://arxiv.org/abs/1906.10612>`__


.. |BuildCI| image:: https://github.com/dynamicslab/pysindy/workflows/Build%20CI/badge.svg
    :target: https://github.com/dynamicslab/pysindy/actions?query=workflow%3A%22Build+CI%22

.. |RTD| image:: https://readthedocs.org/projects/pysindy/badge/?version=latest
     :target: https://pysindy.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

.. |PyPI| image:: https://badge.fury.io/py/pysindy.svg
    :target: https://badge.fury.io/py/pysindy

.. |Codecov| image:: https://codecov.io/gh/dynamicslab/pysindy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/dynamicslab/pysindy
