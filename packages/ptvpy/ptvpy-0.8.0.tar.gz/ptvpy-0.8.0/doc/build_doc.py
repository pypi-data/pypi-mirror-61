#!/usr/bin/env python

"""Helper & command line script to to build the documentation.

Use this script to generate PtvPy's documentation.
This script creates stub pages for the reference section of the documentation.
These stub pages contain directives that allow sphinx to automatically create
documentation for PtvPy's profile file and Python API based on the source code.
The stub pages are created inside the subdirectory "_generated".
See the command line help of this script for usage information.
"""


import os
import re
import shutil
import types
import zipfile
import hashlib
import traceback
from importlib import import_module
from pathlib import Path
from urllib.request import urlopen

import click
import sphinx.cmd.build

import ptvpy
from ptvpy._profile import template_path


here = Path(__file__).parent

#: The images linked to in the documentation are not stored inside the VCS to
#: save space. As a workaround the images are stored online and downloaded when
#: building the documentation.
IMAGES_URL = (
    "https://gitlab.com/tud-mst/ptvpy/uploads/"
    "e304816ac55efcebde892fd0e13e853a/doc_images_v0.6.1+.zip"
)

#: A hash used to validate the file downloaded from `IMAGES_URL`
IMAGES_HASH = "93714a3cfe2d42541118f2d4df968bff0307fde0f5b4d650b1e05849b9464a6d"


#: Document only these modules (order matters).
API_MODULES = [
    "ptvpy",
    "ptvpy.generate",
    "ptvpy.io",
    "ptvpy.plot",
    "ptvpy.process",
    "ptvpy.utils",
    "ptvpy._cli_export",
    "ptvpy._cli_generate",
    "ptvpy._cli_process",
    "ptvpy._cli_profile",
    "ptvpy._cli_root",
    "ptvpy._cli_utils",
    "ptvpy._cli_view",
    "ptvpy._profile",
    "ptvpy._schema",
]


API_DOCUMENT_HEADER = """.. Autogenerated with build_doc.py

:gitlab_url: https://gitlab.com/tud-mst/ptvpy/blob/master/doc/build_doc.py

.. _Python API:

==========
Python API
==========

This page documents PtvPy’s Python API. For more details and examples, refer to the
relevant guides.

.. warning::

   The API is still in development and may change significantly in the future.
   This applies especially to private modules and objects which are prefixed
   with "_".

.. contents:: Content
   :local:

----

"""


API_SECTION_TEMPLATE = """{module_name}
{underline}

.. automodule:: {module_name}

.. currentmodule::  {module_name}

.. autosummary::
   :nosignatures:
   :toctree:
   :template: object.rst

   {members}


"""


PROFILE_DOCUMENT_HEADER = """.. Autogenerated with build_doc.py

:gitlab_url: https://gitlab.com/tud-mst/ptvpy/blob/master/doc/build_doc.py

.. _Profile configuration:

=====================
Profile configuration
=====================

This page lists the configuration options available for PtvPy's profiles. To start with
a fresh profile you can use the command :click-cmd:`ptvpy profile create` or manually
create one using this :download:`template <../../src/ptvpy/profile_template.toml>`.
The file itself uses the TOML_ language.

.. _TOML: https://github.com/toml-lang/toml/blob/master/versions/en/toml-v0.5.0.md

"""


PROFILE_SECTION_TEMPLATE = """.. _{title}:

{title}
{underline}

"""


PROFILE_OPTION_TEMPLATE = """.. profile-option:: {name}

{content}

"""


# Requires http[s]-protocol-string! Source http://urlregex.com/
URL_REGEX = (
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


#: If true, python objects prefix with "_" will be included. Overwritten by
#: command line option "--show-private".
_SHOW_PRIVATE_API = False


def clear_directory(path):
    """Clear directory at `path`."""
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def _in_api(obj_name, obj_value, module_name):
    """Check whether a module level object is part of the API.

    Parameters
    ----------
    obj_name : str
        Name of the object inside the current module.
    obj_value : any
        The object itself.
    module_name : str
        Name of the module the key-value pair was found in.

    Returns
    -------
    in_api : bool
        Whether the object is part of the API that should be documented.
    """
    if obj_name.startswith("__" if _SHOW_PRIVATE_API else "_"):
        return False

    if isinstance(obj_value, click.BaseCommand):
        # Replace object with original wrapped Python function so that the
        # true module origin is tested later
        obj_value = obj_value.callback

    if hasattr(obj_value, "__module__"):
        # Test if function or class was defined in current module
        if obj_value.__module__ == module_name:
            return True

    # Omit imported modules such as `os` which have no attribute "__module__
    elif not isinstance(obj_value, types.ModuleType):
        return True

    return False


def generate_api_doc(path: Path):
    """Create a file documenting the Python API at `path`.

    The function :func:`_in_api` decides which functions are part of the API.
    """
    # Modules that are part of the API
    document = API_DOCUMENT_HEADER

    for module_name in API_MODULES:
        if not _SHOW_PRIVATE_API and (
            module_name.startswith("_") or "._" in module_name
        ):
            # Skip unless _SHOW_PRIVATE_API is True
            continue

        # Get members
        module = import_module(module_name)
        members = sorted(
            obj_name
            for obj_name, obj_value in module.__dict__.items()
            if _in_api(obj_name, obj_value, module_name)
        )
        assert len(members) > 0

        if _SHOW_PRIVATE_API and members:
            # Make sure private members are sorted last
            public = [m for m in members if not m.startswith("_")]
            private = [m for m in members if m.startswith("_")]
            members = public + private

        document += API_SECTION_TEMPLATE.format(
            module_name=module_name,
            underline=("=" * len(module_name)),
            members="\n   ".join(members),
        )

    with open(path, "w") as stream:
        stream.write(document)


def generate_profile_doc(path: Path):
    """Create a file documenting the profile configuration `path`.

    This function parses the raw profile template in a very straight-forward
    (and naive) way and may be prone do breakage. URLs are converted to
    footnotes [#1]_.

    References
    ----------
    .. [1] http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#footnotes
    """  # noqa: E501
    with open(template_path(), "r") as stream:
        profile = stream.read()

    blocks = [s.strip() for s in profile.split("\n\n")]
    blocks = blocks[1:]  # Skip header
    document = []
    for block in blocks:

        if block.startswith("["):
            # Parse section
            title = block.split("\n")[0]
            document.append(
                PROFILE_SECTION_TEMPLATE.format(title=title, underline=len(title) * "=")
            )

        elif block.startswith("# "):
            # Parse option
            lines = block.split("\n")
            name = [l for l in lines if not l.startswith("# ") and "=" in l]
            name = ", ".join(l.split("=")[0].strip() for l in name)
            name = name.replace("#", "")
            comment = [l for l in lines if l.startswith("# ")]
            comment = " ".join(comment)
            comment = comment.replace("# ", "   ")
            document.append(PROFILE_OPTION_TEMPLATE.format(name=name, content=comment))

    document = "\n".join(document)

    # Replace URLs with footnotes and append to the end of the document
    urls = re.findall(URL_REGEX, document)
    urls = list(dict.fromkeys(urls))  # Use unique URLs preserving order
    footnotes = []
    for i, url in enumerate(urls):
        document = document.replace(url, f"[#f{i}]_")
        footnotes.append(f".. [#f{i}] {url}")
    document += "-----\n\n" + "\n".join(footnotes)

    with open(path, "w") as stream:
        stream.write(PROFILE_DOCUMENT_HEADER)
        stream.write(document)


def download_file(url, download_path, **kwargs):
    """Create a file from the given URL.

    Parameters
    ----------
    url : str
        URL where to the file is stored.
    download_path : str or Path
        Path to where the file is downloaded.
    """
    with urlopen(url, **kwargs) as response, open(download_path, "wb") as file:
        shutil.copyfileobj(response, file)


def download_images(url, download_path, *, checksum=None):
    """Download and extract files inside a ZIP file.

    Parameters
    ----------
    url : str
        URL to where the ZIP file with images is stored.
    download_path : str or Path
        Path to where the ZIP file is downloaded. Its contents are extracted
        into the same directory.
    checksum : str
        A checksum to validate the downloaded file with.
    """
    try:
        download_file(url, download_path)
    except Exception:
        tb = traceback.format_exc()
        click.secho(f"Exception while downloading file: {tb}", err=True, fg="red")
        return

    if checksum:
        # Hash the file
        algorithm = hashlib.sha256()
        with open(download_path, "rb") as stream:
            while True:
                buffer = stream.read(2 ** 20)
                if not buffer:
                    break
                algorithm.update(buffer)

        digest = algorithm.hexdigest()
        if digest != checksum:
            os.remove(download_path)
            raise ValueError(f"hash of resource file is unexpected: {digest!r}")

    # Unpack zipfile
    with zipfile.ZipFile(download_path, "r") as zip_file:
        zip_file.extractall(download_path.parent)


@click.command()
@click.argument("build_dir", type=click.Path(file_okay=False))
@click.option(
    "--clear",
    is_flag=True,
    help="Explicitly clear 'doc/_generated' and 'build/html-doc' folders.",
)
@click.option(
    "--sphinx",
    help="Pass extra flags / options to sphinx-build. Be careful not to clash with "
    "options provided by this script.",
    type=click.STRING,
)
@click.option(
    "--show-private",
    is_flag=True,
    help="Include private classes and functions in API documentation.",
)
@click.option("--doctest", is_flag=True, help="Test code snippets in docstrings.")
@click.help_option("-h", "--help")
@click.pass_context
def main(ctx, **kwargs):
    """Build documentation but do some pre-processing first.

    The RST-files documenting PtvPy's CLI and API must be auto-generated before
    invoking sphinx-build. It will generate the files `profile.rst`, `cli.rst`,
    and `api.rst` inside the "doc/_generated" directory before invoking
    sphinx-build which creates the full HTML documentation inside BUILD_DIR.
    """
    click.echo(f"Using PtvPy at '{Path(ptvpy.__file__).parent}'")
    global _SHOW_PRIVATE_API
    _SHOW_PRIVATE_API = kwargs["show_private"]

    # Ensure images are present
    download_path = here / "_images/download.zip"
    download_path.parent.mkdir(parents=True, exist_ok=True)
    if not download_path.is_file():
        click.echo(f"downloading '{IMAGES_URL}' to '{download_path}'...")
        download_images(IMAGES_URL, download_path, checksum=IMAGES_HASH)

    generated_dir = here / "_generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    build_dir = Path(kwargs["build_dir"])
    build_dir.mkdir(parents=True, exist_ok=True)

    if kwargs["clear"]:
        # Optionally clear dynamic directories
        click.echo(f"clearing '{generated_dir}' folder...")
        clear_directory(generated_dir)
        click.echo(f"clearing '{build_dir}' folder...")
        clear_directory(build_dir)

    path = generated_dir / "api.rst"
    click.echo(f"generating '{path}'...")
    generate_api_doc(path)

    path = generated_dir / "profile.rst"
    click.echo(f"generating '{path}'...")
    generate_profile_doc(path)

    builder = "doctest" if kwargs["doctest"] else "html"
    argv = ["-b", builder, str(here), kwargs["build_dir"]]
    if kwargs["sphinx"]:
        argv = kwargs["sphinx"].split(" ") + argv

    click.echo(f"invoking 'sphinx-build {' '.join(argv)}':")
    return_code = sphinx.cmd.build.main(argv)
    ctx.exit(return_code)


if __name__ == "__main__":
    main()
