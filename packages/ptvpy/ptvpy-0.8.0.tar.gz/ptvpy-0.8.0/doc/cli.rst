.. _Command line interface:

======================
Command line interface
======================

Reference for the command line interface of PtvPy.
For more details and examples, refer to the relevant guides.

.. contents:: Content
   :local:

----


ptvpy
=====

.. click-cmd:: ptvpy._cli_root:root_group
   :name: ptvpy
   :linkcode:
   :subcommands:
   :maxdepth: 0


ptvpy export
============

.. click-cmd:: ptvpy._cli_root:export_command
   :prefix: ptvpy
   :subcommands:
   :linkcode:


ptvpy generate
==============

.. click-cmd:: ptvpy._cli_generate:generate_group
   :prefix: ptvpy
   :subcommands:
   :linkcode:


ptvpy process
=============

.. click-cmd:: ptvpy._cli_process:process_command
   :prefix: ptvpy
   :subcommands:
   :linkcode:


ptvpy profile
=============

.. click-cmd:: ptvpy._cli_profile:profile_group
   :prefix: ptvpy
   :subcommands:
   :linkcode:


ptvpy view
==========

.. click-cmd:: ptvpy._cli_view:view_group
   :prefix: ptvpy
   :subcommands:
   :linkcode:
