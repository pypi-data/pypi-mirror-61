.. _faq:

==========================
Frequently asked questions
==========================

.. contents:: Content
   :local:

----


Why is my profile not detected?
===============================

When you don't specify an explicit file to use with the ``--profile`` option PtvPy tries
to automatically detect a profile inside the current director.
This detection is only successful if

- the directory contains exactly one file matching ``*ptvpy*.toml`` (where ``*`` is a
  placeholder any number of characters)
- and that file contains a valid profile.

PtvPy refrains from guessing which file to load if there are more than one candidate.
You can check the current directory at any time for valid profiles with the command
:click-cmd:`ptvpy profile check` which will attempt to display detailed information about
all candidates and their validity.


How do I report a bug?
======================

If you think that you encountered a bug we are happy to look into it.
We recommend that you get in contact with the developers by
`creating a new issue here`_.

.. _creating a new issue here: https://gitlab.com/tud-mst/ptvpy/issues/new?issue


Where and how are results stored?
=================================

PtvPy stores all results inside the file configured in the profile field
:profile-option:`storage_file`.
Unless changed this will point to the file :file:`ptvpy.h5` inside the
same directory as the profile file.

Independent of the name and location the data will always be stored using the
`HDF5 format`_ which is a scientific hierarchical data format supported by a wide
range of applications and software.
PtvPy itself relies on the excellent implementation provided by h5py_ to work
with the HDF5 format.

This file may contain the following objects:

- The root group has an attribute "created_with" which contains the version of PtvPy
  that created the file.
- A dataset "ptvpy.toml" which directly stores the content of the profile file
  as bytes.
- A group "particles" with several datasets that make up the actual processing results.

If you installed PtvPy through conda you may have access to several
`command line tools`_ which can be used to inspect the storage file, e.g.::

    h5ls -rv ptvpy.h5

.. tip::

    If you want to access the data using another format have a look at the
    :click-cmd:`ptvpy export` command.

.. _HDF5 format: https://support.hdfgroup.org/HDF5/
.. _pandas.HDFStore: https://pandas.pydata.org/pandas-docs/stable/io.html#io-hdf5
.. _PyTables: http://www.pytables.org/index.html
.. _h5py: http://docs.h5py.org/en/stable/
.. _command line tools: https://support.hdfgroup.org/HDF5/doc/RM/Tools.html


Does PtvPy support autocompletion?
==================================

Yes, autocompletion is supported for `Bash and ZSH`_. If you use Bash add the line ::

    eval "$(_PTVPY_COMPLETE=source ptvpy)"

to your ``.bashrc``. For ZSH add ::

    eval "$(_PTVPY_COMPLETE=source_zsh ptvpy)"

to your ``.zshrc`` file instead.

.. _Bash and ZSH: https://click.palletsprojects.com/en/7.x/bashcomplete/
