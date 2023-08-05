.. highlight:: none

.. _Contributing:

============
Contributing
============

We would be excited to have you as a contributor to the project!
This guide aims to make the process of contributing as easy as possible for you.
However basic knowledge concerning the command line and tools such as Python, git and
conda will be helpful to understand this guide.
If you encounter any hiccups or get stuck, feel free to `ask on GitLab`_.

.. _ask on GitLab: https://gitlab.com/tud-mst/ptvpy/issues/new?issue

.. contents:: Content
   :local:

----


Setup
=====

.. _Cloning the repository:

Cloning the repository
----------------------

> Requires git_

Fork the repository_ (referred to as `upstream`) on GitLab.com by clicking the
appropriate button and clone your fork into a local directory with (replace
``USERNAME`` with your actual username)::

    git clone https://gitlab.com/USERNAME/ptvpy.git ptvpy
    cd ptvpy
    git remote add upstream https://gitlab.com/tud-mst/ptvpy.git

The local repository is now linked to two remote repositories:

- `origin` - referring to your personal copy (fork) of the source code
- `upstream` - referring to the original repository.

Changes to the upstream repository are not automatically pushed to origin and your
local copy.
However you can update those with::

    git checkout master
    git pull upstream master
    git push origin master

.. _git: https://git-scm.com/doc
.. _repository: https://gitlab.com/tud-mst/ptvpy


The development environment
---------------------------

> Requires Python >= 3.6

It is recommended to develop PtvPy in its own virtual environment that is separate
from the OS.

.. tip::

   Checkout this `guide on PyPA`_ if you are not familiar with creating and managing
   virtual environments in Python.

Once you have activated your new environment install PtvPy in development mode
together with its development dependencies::

    pip install --editable .[dev]

This command must be executed in the directory containing the ``setup.py`` file.
If the installation was successful the command ::

    ptvpy --version

should output a version number suffixed with the revision number of the current
checkout (compare with output of ``git describe --tags --dirty --always``).

.. _guide on PyPA: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/


.. _Testing:

Testing
=======

If all steps in the previous section were followed correctly the tests can be
run with pytest_ by executing ::

    pytest --doctest-modules

The ``--doctest-modules`` flag will ensure that examples in docstrings are tested
as well.

Adding the flag ``--cov`` will record the test coverage as well and display a basic
summary.
To measure the coverage for `just-in-time compiled`_ code you need to set the
environment variable `NUMBA_DISABLE_JIT`_ ::

    NUMBA_DISABLE_JIT=1 pytest --cov

Finally to generate a detailed HTML report use ::

    coverage html -d build/coverage

and open the file ``build/coverage/index.html`` with a browser. The implicit
configuration of how pytest and the coverage analysis runs are configured inside
:file:`setup.cfg`.

Some tests don't pass in environments without a window manager.
The test suite can adapt to this (skipping some tests) by setting the environment
variable ``CI`` for the command in question::

    CI=1 pytest

.. _pytest: https://docs.pytest.org
.. _just-in-time compiled:
   http://numba.pydata.org/numba-doc/latest/reference/jit-compilation.html
.. _NUMBA_DISABLE_JIT:
   http://numba.pydata.org/numba-doc/latest/reference/envvars.html#envvar-NUMBA_DISABLE_JIT


Building the documentation
==========================

PtvPy's online documentation is build with the static site generator Sphinx_ and the
`Read The Docs Sphinx Theme`_. Its configuration can be found inside the file
:file:`doc/conf.py`.

The reference part of the documentation is directly generated from PtvPy's APIs.
In case of the Python API this is accomplished via Sphinx's autodoc extension.
However the source files for the the command line interface and profile file are
generated with the script :file:`build_doc.py` before invoking Sphinx.
This script manages both steps directly and may be called like this::

   python doc/build_doc.py build/html-doc

To include private parts of the Python API as well, add the flag ``--show-private``
behind ``build_doc.py``.
Supply the ``--help`` option to display a full list of its options.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
.. _Read The Docs Sphinx Theme: https://sphinx-rtd-theme.readthedocs.io/en/stable/


Creating a merge request
========================

Merge requests (GitHub calls these pull requests) are a way to contribute changes
even without commit rights to PtvPy's repository.
Start by creating a new branch for the feature or change you want to contribute::

    git checkout master
    git pull upstream master
    git checkout -b FEATURE-BRANCH

Then you can commit local changes to this branch using the ``git add`` and
``git commit`` commands. You can find a good introduction on recording changes
here_. You then need to push these changes to your fork with ::

    git push -u origin FEATURE-BRANCH

You only need to add the ``-u`` flag the first time you do this. If that was successful
git will display a link inside the console to create a new merge request. Otherwise
just head to your fork on GitLab.com and click on `Merge Requests > New merge request`.

Before suggesting any changes in a new merge request make sure that you have read the
:ref:`guidelines` in the next section. It is recommended to run the test suite and
black_ locally beforehand as well.

.. _here: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository


.. _Guidelines:

Guidelines
==========

- Use the code formatter black_ to style your code. E.g. ``black src/ptvpy/process.py``.
  Sometimes big, deeply nested structures may be significantly more readable if
  formatted manually. To preserve the format for these exceptions you can wrap the code
  block into `# fmt: off ... # fmt: on` statements.
- Every module, class or function should include documentation in the form of
  docstrings. Their format should follow the `NumPy style`_.
- New functionality or changes especially to the public API should be covered by tests.
- Make sure that your contributions are compatible with this project's license_
  (see also :ref:`Using Stack Overflow`).
- Try to write concise and useful commit messages. To see why and how have a look at
  this `Chris Beams guide`_.

In general you should follow good practices already established in the scientific Python
community.
It's often useful to look at content already present and try to follow its style.
If in doubt feel free to ask.

.. _black: https://black.readthedocs.io/en/stable/
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _license: https://gitlab.com/tud-mst/ptvpy/blob/master/LICENSE.txt
.. _Chris Beams guide: https://chris.beams.io/posts/git-commit/

.. _Using Stack Overflow:

Using Stack Overflow
--------------------

.. important::

   Please avoid copying non-trivial code directly from Stack Overflow unless the
   author has explicitly placed the content under a compatible license!

By default `content on Stack Overflow`_ is licensed under the `CC BY-SA 3.0`_ which
demands derivative work to be licensed under a compatible license.
As of now only CC-licenses are `listed as compatible`_ which excludes most common
open source licenses.
Using Stack Overflow as a knowledge base and point of reference should be okay
though. [#f]_
In this case please include a hyperlink to the appropriate comment or answer.

Further reading:

- `Proposal to use the MIT License`_ for code on Stack Overflow and the follow-up_
- Blogpost `Stack Overflow Code Snippets`_ by Sebastian Baltes.

.. [#f] This is not legal advice. So if in doubt please consult an attorney or
        avoid the issue altogether.

.. _content on Stack Overflow: https://stackoverflow.com/legal/terms-of-service
.. _CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/
.. _listed as compatible: https://creativecommons.org/share-your-work/licensing-considerations/compatible-licenses
.. _Proposal to use the MIT License: https://meta.stackexchange.com/q/271080
.. _follow-up: https://meta.stackexchange.com/q/272956
.. _Stack Overflow Code Snippets: https://empirical-software.engineering/blog/so-snippets-in-gh-projects


Useful Links
============

* `trackpy <http://soft-matter.github.io/trackpy>`_
* `conda-build <https://docs.conda.io/projects/conda-build>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_
