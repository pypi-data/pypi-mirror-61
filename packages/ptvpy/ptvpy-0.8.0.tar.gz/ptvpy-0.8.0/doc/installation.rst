.. highlight:: none

.. _installation:

===============
Installation
===============


With pip
========

PtvPy is available_ on the Python Package Index.
To install, simply open a command line prompt where pip_ is available and type::

    pip install ptvpy


.. _available: https://pypi.org/project/ptvpy/
.. _pip: https://pip.pypa.io/en/stable/


..  With Anaconda
    =============

    .. warning:: This doesn't work yet!

    If you haven't yet installed the `Anaconda distribution`_ please do so before
    continuing. [#]_
    Once this is done open the `Anaconda Command Prompt`_ and type ::

        conda --version

    to verify that you have access to the package manager.
    PtvPy and some of its dependencies are not available in Anaconda's official
    repositories.
    Therefore we need to append the community managed repository `conda forge`_ to its
    search path [#]_ with the command::

        conda config --append channels conda-forge

    Then you can simply install PtvPy with::

        conda install ptvpy

    .. [#] If you don't want to install the full distribution and are experienced with the
       command line you can use miniconda_.
       This lightweight installer only contains Python and the package manager ``conda``.
    .. [#] When installing or updating packages, conda will still search the official
       repositories first.
       Only if the desired package is not found will it look to conda-forge.

    .. _Anaconda distribution: https://www.anaconda.com/download/
    .. _Anaconda Command Prompt: https://docs.anaconda.com/anaconda/user-guide/getting-started/#open-anaconda-prompt
    .. _conda forge: https://conda-forge.org/
    .. _miniconda: https://docs.conda.io/en/latest/miniconda.html


From source
===========

If you want to install PtvPy from source you can download the project files manually or
with git and then install from source with pip_::

    git clone https://gitlab.com/tud-mst/ptvpy.git
    pip install ptvpy/
