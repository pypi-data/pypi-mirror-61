.. highlight:: none

.. _tutorial:

============
Introduction
============

This document aims to give a brief tour and overview of PtvPy's functionality.
The different sections build on one another and demonstrate a possible workflow
when using the tool.

.. contents:: Content
   :local:

----


Overview
========

PtvPy is controlled through its :ref:`Command line interface` consisting of the
following subcommands:

- :click-cmd:`ptvpy process` detects particles inside a given dataset.
  The way the data is processed and analyzed is mainly controlled by and configured
  through :ref:`profile files <Profile configuration>`.
- :click-cmd:`ptvpy view` can be used to inspect and visualize the dataset and
  processing results.
- :click-cmd:`ptvpy profile` assists the user in managing profile files. It can create,
  validate, edit and show profiles.
- :click-cmd:`ptvpy export` is used to make processing results available in commonly
  supported file formats.


.. _intro-generating:

Generate an artificial dataset
==============================

PtvPy provides the means to :click-cmd:`generate <ptvpy generate>` artificial
data for different scenarios.
This is not only useful when testing the application but also to demonstrate its
capabilities.
Starting our work inside an empty directory, we will create a dataset of 200 images
(or frames) inside the subdirectory ``data/`` with the following command::

    ptvpy generate whirlpool --seed 42 --white-noise 40 10 -- data/ 200

As you may have guessed this dataset simulates particles floating inside a whirlpool.
The option ``--white-noise 40 10`` will add white noise (mean: 40, variance: 10)
to the background and ``--seed 42`` will ensure that PtvPy will generate the
same data as used by this tutorial.
For non-specified options, PtvPy will use default values, e.g. 20 particles (compare
:click-cmd:`ptvpy generate whirlpool`).
At this point you can already inspect the images with a conventional image viewer.


Create a new profile
====================

To do anything meaningful with a dataset PtvPy requires a profile file that
informs it how to find the input data and how to process it.
You can create a new profile file using the command ::

    ptvpy profile create --data-files "data/*tiff"

In this case we inform PtvPy with the pattern_ ``data/*.tiff`` were the data files are
located.
PtvPy will check that the new profile is valid and then create the file
``ptvpy.toml`` inside the current directory.

.. _pattern: https://docs.python.org/3/library/glob.html


Track particles & fine-tune the profile
=======================================

Now we are ready to start processing. For now we only want to track the particles
without linking them by calling::

    ptvpy process --step locate

PtvPy will start by averaging each pixel across all frames (calculating the background).
This background will be subtracted from each frame before searching for particles
which will suppress background noise and isolate the dynamic parts: moving particles.
PtvPy will try to inform you about the progress which can take some time for large
datasets.
Once it's done it will show you a summary of the results which should look like
this::

    Using profile: 'ptvpy.toml'
    Calculating background: 0.20 s | done
    Locating particles: 200/200 (100.0%), 1.9 s (+ 0 s) | done

    Summary:

    19229 particles in 200 frames (96.14 particles/frame)

          median   mean     std    min    max
    mass   67.55  114.2   123.7  18.06  626.6
    size   2.592  2.529  0.4748  1.393  3.863
    x      99.22  99.45   55.81  3.449  195.6
    y      99.35  99.41    55.8    3.3  195.5


At this point we have tried to find particles using the default values given in
a new profile.
However these are rarely optimal as can be easily seen when looking at the summary or
when plotting the results with :click-cmd:`ptvpy view slideshow`::

    ptvpy view slideshow

.. image:: _images/slideshow-0.svg
   :align: center
   :width: 75%

Due to the background noise PtvPy detected fake particles that we don't want in
the final results.
To resolve this we have to find a property that effectively differentiates fake
particles from true ones.
When looking back at the summary we can see that the statistics for the particles's
`mass` indicate a large variability.
This assumption holds when looking at the
:click-cmd:`relationship <ptvpy view scatter2d>` between the particle's `mass` and
`size`::

    ptvpy view scatter2d mass size

.. _image-scatter2d:

.. image:: _images/scatter2d.png
   :align: center
   :width: 75%

At this stage both parameters are often useful to effectively group detected particles
into fake (group to the left with a small `mass` and larger variance in `size`) and true
particles (group to the right).

.. tip::

    Use :click-cmd:`ptvpy profile edit` to quickly edit the current profile and print
    an overview of your changes with :click-cmd:`ptvpy profile diff`.

After setting the profile field :profile-option:`trackpy_locate.minmass` to
150 we process the dataset a second time, this time including all processing steps::

    $ ptvpy process
    Using profile: 'ptvpy.toml'
    Calculating background: 0.01 s | done (used cache)
    Locating particles: 200/200 (100.0%), 1.8 s (+ 0 s) | done
    Linking particles: 0.19 s | done
    Calculating velocities: 0.02 s | done

    Summary:

    2968 particles in 200 frames (14.84 particles/frame)
    33 unique trajectories spanning on average 89.94 frames

          median       mean     std     min    max
    mass     362      383.8   108.1   151.9  626.6
    size   1.752      1.766  0.1451   1.463  3.186
    x      104.7      105.4   50.09   4.444  194.4
    y      95.06      94.84   50.51   4.875  194.6
    dx    0.3026    0.07922   3.518  -7.565  7.556
    dy    0.3136  0.0007102   3.478  -7.572  8.662
    v      4.533      4.292    2.46  0.4896   9.86

We can see that the number of detected particles per frame is already much closer to the
20 synthetic particles that were simulated :ref:`earlier <intro-generating>`.
And the slideshow confirms this::

    ptvpy view slideshow

.. _image-slideshow-1:

.. image:: _images/slideshow-1.svg
   :align: center
   :width: 75%

While the results are still not perfect were are detecting only valid particles now.
We could improve upon this by tweaking other parameters inside the profile.
Parameters that often prove useful are:

- :profile-option:`trackpy_locate.minmass` - Particles can often be differentiated based on
  their `mass`. As such this parameter is useful to suppress small particles or "fake"
  ones detected due to background noise.
- :profile-option:`trackpy_locate.diameter` - The expected diameter of of particles.
  If in doubt choose a larger value (must always be odd).
- :profile-option:`trackpy_locate.separation` - If not given this one defaults to
  "`diameter` + 1" which might not be optimal when the particle density is high.
- :profile-option:`trackpy_link.search_range` - This parameter should match the maximal
  expected particle velocity.
- :profile-option:`trackpy_link.memory` - Increasing this parameter helps tracking
  particles over multiple frames when they weren't detected in all consecutive frames.


Visualizing results
===================

PtvPy supports a wide range of plot types that allow you to choose how and which
variables you want to visualize.
The help option returns an overview about all available subcommands for
:click-cmd:`ptvpy view` while :click-cmd:`ptvpy view summary` with the ``--all``
option which prints an overview about all variables available as input for the different
plot types. ::

    $ ptvpy view summary --all
    Using profile: 'ptvpy.toml'

    Summary:

    2968 particles in 200 frames (14.84 particles/frame)
    33 unique trajectories spanning on average 89.94 frames

               median       mean      std       min     max
    dx         0.3026    0.07922    3.518    -7.565   7.556
    dy         0.3136  0.0007102    3.478    -7.572   8.662
    ecc       0.09867     0.1054  0.05766  0.009122  0.7049
    ep         0.1435     0.5118    15.08    -82.39   534.9
    frame        99.5      100.3    56.68         0     199
    mass          362      383.8    108.1     151.9   626.6
    particle       11      14.34    11.51         0      42
    raw_mass    892.7      915.1    205.8     393.4    1493
    signal      30.78      31.43    6.467     16.37   45.56
    size        1.752      1.766   0.1451     1.463   3.186
    v           4.533      4.292     2.46    0.4896    9.86
    x           104.7      105.4    50.09     4.444   194.4
    y           95.06      94.84    50.51     4.875   194.6


Often particle tracking velocimetry is performed to measure the local velocity of a
fluid in which the tracked particles are suspended.
Now with our analysis done we can interpolate those local velocities with
:click-cmd:`ptvpy view vector`::

    ptvpy view vector --heatmap x y dx dy

.. _image-vector:

.. image:: _images/vector.svg
  :align: center
  :width: 75%

Or, in case we are actually interested in the speed of individual particles, we can
use :click-cmd:`ptvpy view scatter3d` for visualization.
E.g. displaying the displacement of particles at their respective coordinates yields
interesting results for the current data::

    ptvpy view scatter3d --color dx x y dx

.. _image-scatter3d:

.. image:: _images/scatter3d.svg
  :alt: Scatter plot in 3 dimension visualizing the measured absolute velocity of
        particles.
  :align: center
  :width: 75%

There are many more plot types and combinations available so start exploring your data!


.. Todo Exporting results
