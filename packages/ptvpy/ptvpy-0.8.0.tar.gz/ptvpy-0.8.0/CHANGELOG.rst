.. _Changelog:

=========
Changelog
=========

.. Once 1.0.0 is reached, use https://semver.org/spec/v2.0.0.html


Version 0.8.0 (latest)
==============================

Released on 2020-02-07. This release introduces new behavior, deprecations and patches
the test suite and project configuration in anticipation of the package release on
conda-forge.

.. rubric:: Highlights

- PtvPy now considers the third dimension when linking and calculating velocities.
- The coordinate and velocity columns for the third dimension are now named ``z``
  (previously ``angle``) and ``dz`` respectively.
- Deprecates the functions ``xy_velocity`` and ``absolute_velocity`` in favor of the new
  function :func:`~.particle_velocity`.

.. rubric:: Other

- The continous integration now covers Python 3.8 and tests the package on Windows as
  well.
- The test suite no longer catches exceptions when testing commands. This makes
  inspecting failed tests easier.
- PtvPy is now `featured and analysed`_ on LGTM.com, a static code analysis tool.

.. _featured and analysed: https://lgtm.com/projects/gl/tud-mst/ptvpy/


Version 0.7.0
=============

Released on 2019-10-28. This is a large release new features and many improvements.
The list below isn't complete but highlights the most important changes.

.. rubric:: Highlights

- Subcommands of :click-cmd:`ptvpy generate` can now generate double images of particles
  which are seen as if evaluated with a double-helix point spread.
  Use the ``--helix`` option to encode the position of particles in the 3rd dimension
  as an angle between the double image of a particle.
- PtvPy tries to be more informative about errors and shows hints for known cases. The
  ``--debug`` option now works for all exceptions.
- Added the new command :click-cmd:`ptvpy profile diff` that gives an quick overview
  about which profile values were changed.
- A new plot type was added with :click-cmd:`ptvpy view violin`.

.. rubric:: Command line

- :click-cmd:`ptvpy process` will try to give a better summary after processing data.
  The report may even include warnings if frames without any detected particles were
  encountered.
  The report can be shown at any time with :click-cmd:`ptvpy view summary`.
- :click-cmd:`ptvpy view`'s subcommands are named more consistently and generate
  cleaner plots.
- The :click-cmd:`ptvpy profile create` command does not require the user to input a
  pattern matching the data files any more and uses the default value ``*.tif*`` unless
  a different pattern is passed with the option ``--data-files TEXT``.
- Commands that try to automatically detect a profile in the local folder now use the
  more liberal pattern ``*ptvpy*.toml`` (was ``*.ptvpy.toml``).
  The new option ``--no-validation`` was added to these commands as well and explicitly
  toggles whether an invalid profile will be used.
- The ``--profile`` option in :click-cmd:`ptvpy view` was moved to its subcommands.
- :click-cmd:`ptvpy process`'s ``--step`` option can now be given multiple times.
- Added examples to many commands to demonstrate their usage.

.. rubric:: Other

- Many changes to the Python API to facilitate the changes above.
- Improved the :ref:`Installation`, :ref:`Introduction` and :ref:`Contributing` guides.
- This documentation now uses a new directives to automatically document PtvPy's command
  line interface and profile options.
- Provide project links in the sidebar of this documentation.


Version 0.6.1
=============

Released on 2019-05-25. This is mainly a small bug fix release concerning the package
documentation and information on PyPI.

.. rubric:: Changed

- Improve the :ref:`Releasing a new version` guide and ensure that it is up to date.

.. rubric:: Fixed

- Make sure that package classifiers are correctly displayed on PyPI
  (`#11 <https://gitlab.com/tud-mst/ptvpy/issues/11>`_).
- Ensure README links are still valid on PyPI
  (`#12 <https://gitlab.com/tud-mst/ptvpy/issues/12>`_).
- Pin build dependencies for the HTML documentation
  (`#14 <https://gitlab.com/tud-mst/ptvpy/issues/14>`_).
- Make sure that the logo font is rendered the same regardless of installed fonts.


Version 0.6.0
=============

Released on 2019-05-17. This release marks the transition to an open-source project.
While there are new features the focus was on improving the infrastructure of the
project itself and preparing the releases on PyPI and conda-forge.

The highlights of this release are included below.

.. rubric:: New

- The new option ``--pattern`` was added to the :click-cmd:`ptvpy profile create`
  command. This option allows to use the command even if no input prompt is desired,
  e.g. when PtvPy is used programmatically.
- Added the new option ``--documentation`` to the root command :click-cmd:`ptvpy` which
  will open the online documentation inside the default browser.
- Released PtvPy under the BSD 3-Clause License as free and open-source software.
- New functions in :mod:`~.generate` module providing a more powerful API for
  frame generation. Generation of particles moving in a whirlpool was added as
  a new scenario, the optional addition of white noise to the background
  of frames and helper functions to render a frames with helix pairs.
- New wrapper class :class:`HdfFile <ptvpy.io.Storage>` that allows round-tripping
  pandas's DataFrames while exposing the more powerful API of h5py_. This makes
  the removing the dependency pytables_ possible.
- After processing the used profile is stored as a string alongside the results
  making them reproducible using only the storage file alone.
- Created a new logo to make the project more recognizable.

.. rubric:: Changed

- New commands :click-cmd:`ptvpy generate whirlpool` and
  :click-cmd:`ptvpy generate lines` replaced the old ``generate`` command.
- Renamed ``calculate_background`` to :func:`~.mean_frame`.
- Renamed ``process_helix_frame`` to :func:`~.find_helix_particles`.

.. rubric:: Removed

- Private parts of the Python API are no longer included by default in the HTML
  documentation.
- Removed the dependency on pytables_.

.. rubric:: Fixed

- Highlighting particles using the :click-cmd:`slideshow <ptvpy view slideshow>` will no
  longer fail if the linking step hasn't been performed and particle IDs are not
  available yet.
- In certain situations a particle would be assigned to more than one helix pair despite
  :profile-option:`helix.unique` being ``true``. As part of the fix the implementation of
  the responsible function was rewritten and is now covered by tests.

.. _pytables: http://www.pytables.org/


Version 0.5.0
=============

Released on 2019-02-11.

.. rubric:: New

- All possible configuration options are now listed inside a profile file (see
  :ref:`Profile configuration`) and completely covered by an extended validation
  schema (see :mod:`~._schema`).
- Add command :click-cmd:`ptvpy view background` to make inspection of
  this intermediate result possible.
- Add option ``--force-profile`` to the commands :click-cmd:`ptvpy view`,
  :click-cmd:`ptvpy process` and :click-cmd:`ptvpy export`.
- Added runtime dependencies h5py_ and `toml (Python package)`_ and updated
  existing dependencies.
- Extended the coverage of the test suite (now at 78%).

.. rubric:: Changed

- Profile files now use the `TOML language`_ and a new template.
- Replaced ``load_frames`` with :class:`~.FrameLoader` to allow finer control
  without wasting CPU-time or memory. This new class allows to cache and reuse
  the background between consecutive runs with the same input data (frames).
  On the first run the computed background is stored in the ``storage_file`` with
  a hash of the used data. The cached result is then reused the next time if the
  hash and thus the data stayed the same. Otherwise the background is computed
  again.
- Changed command line options of the :click-cmd:`ptvpy process` command.
- The :click-cmd:`ptvpy process` command no longer loads all frames into
  memory at once but sequentially when required. Thus the input data is no longer
  required to fit into memory all at once. In this regard the new function
  ``calculate_background`` was added. It calculates the average of frames
  sequentially without loading all frames into memory at once.
- Added functions :func:`~.hash_files` and :func:`~.hash_arrays`. These are
  useful when summarizing data on disk or in memory.
- The profile documentation is no longer included as a raw template but is
  automatically generated as a RestructuredText document (see
  :ref:`Profile configuration`).
- Renamed ``LazyLoadingSequence`` to :class:`~.LazyMapSequence`.
- Moved modules inside the subpackage ``_app`` to the top level and removed
  the subpackage.

.. rubric:: Removed

- Removed supported for multiple iterations of the location step. This might get
  readded in the future when detection of duplicates is implemented.
- Remove ``ptvpy.process.locate``, ``ptvpy.process.link`` and
  ``ptvpy.process.locate_helix_pairs``. The former two where wrappers around
  trackpy_ functions which are now directly used in :mod:`~._cli_process`.

.. rubric:: Fixed

- Removed unjustified scaling of frames with the factor 1/255 when removing
  the background (average per pixel of all used frames). This means that ``minmass``
  values derived from old profiles must be increased by the factor 255 to yield
  the same results (see :profile-option:`trackpy_locate.minmass`).

.. _h5py: http://docs.h5py.org/en/stable/index.html
.. _toml (Python package): https://github.com/uiri/toml
.. _TOML language: https://github.com/toml-lang/toml


Version 0.4.0
=============

Released on 2018-12-12.

.. rubric:: New

- Add basic test coverage for the commands :click-cmd:`ptvpy profile`,
  :click-cmd:`ptvpy view` and :click-cmd:`ptvpy export`.
- Add `pytest fixtures`_ which create dummy projects during testing.

.. rubric:: Changed

- Change backend of command :click-cmd:`ptvpy view slideshow` and introduce
  several improvements. The slide show is now animated (pause-able) and shows tracked
  particles. Upon clicking on a tracked particle it will display its properties
  and trajectory.
- Rename subcommand ``ptvpy view subpixel-bias`` to
  :click-cmd:`ptvpy view subpixel`.
- Switch to `Python 3.7`_ and update dependencies.

.. rubric:: Fixed

- Exports to MAT files will no longer contain the column names "angle" and "size"
  which clash with MATLAB's builtin symbols. Instead an "_" will be appended to
  those names (see :click-cmd:`ptvpy export`).
- The subcommand :click-cmd:`ptvpy profile check` can deal with more error
  cases now and its output should be more useful even for unexpected errors.

.. rubric:: Removed

- Remove ``ptvpy view annotated-frame`` command which is obsolete now.

.. _Python 3.7: https://docs.python.org/3.7/whatsnew/3.7.html
.. _pytest fixtures: https://docs.pytest.org/en/latest/fixture.html


Version 0.3.0
=============

Released on 2018-10-02.

.. rubric:: New

- New CLI command :click-cmd:`ptvpy generate` that can generate synthetic
  images for particle tracking velocimetry.
- Add new functions :func:`~.overlay_gaussian_blob` and
  ``constant_velocity_generator`` and remove old functions in :mod:`~.generate`.
- New tests that cover the basic workflow a user might have when using the CLI:
  image generation, profile creation, processing, viewing and exporting.
- Extend the developer guide with a description of
  how to setup the environment, run the test suite, make a release and build the
  documentation.
- Add a tutorial documenting the basic workflow <section-first-steps
  when using the CLI.
- New build script that nearly fully automates the documentation of the CLI and
  API.

.. rubric:: Changed

- Steps in the command :click-cmd:`ptvpy process` are now supplied as arguments.
- Rename subpackages with conciser names which are more inline with other scientific
  libraries and make the subpackage containing the CLI application private.
- Use a new HTML theme from `Read the docs`_ with several CSS tweaks.
- Use the :file:`setup.py` as the single truth for the current version and generate
  a :file:`src/ptvpy/version.py` (including the git-commit hash of HEAD) during
  installation.
- Use the `src/package layout`_ (`see also`_).

.. rubric:: Fixed

- Patched several bugs in Sphinx when documenting functions that were jitted with
  numba_ or whose docstrings contain special characters used by click_.

.. _src/package layout: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
.. _see also: https://hynek.me/articles/testing-packaging/
.. _Read the docs: https://sphinx-rtd-theme.readthedocs.io/en/latest/
.. _numba: http://numba.pydata.org/


Version 0.2.1
=============

Released on 2018-09-18.

- Redesign configuration file to profile file
- Definition of a schema for the profile file using Cerberus_
- Validate profiles files with schema
- Multiple iteration steps for particle location
- Redesign command line interface (CLI) with click_
- Full integration of new profile module into the workflow of the CLI
- Use explicit lazy imports for heavy libraries for the CLI
- Setup pytest and integrate into conda-build process
- Automatic generation of reference documentation

.. _Cerberus: https://github.com/pyeve/cerberus
.. _click: http://click.pocoo.org/5/


Version 0.1.1
=============

- Basic command line interface with ``argparse``
- Configuration of processing steps with YAML document
- Particle tracking in 2 dimensions with trackpy_
- Particle tracking in 3 dimensions with double helix
- Distributable as conda_ package
- Basic HTML documentation
- Export functionality to common formats: CSV, MAT, XLSX, SQLITE

.. _trackpy: https://github.com/soft-matter/trackpy
.. _conda: https://conda.io/
