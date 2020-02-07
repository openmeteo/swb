#!/usr/bin/env python

import os
import re


def get_version():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    init_py_path = os.path.join(scriptdir, "..", "swb", "__init__.py")
    with open(init_py_path) as f:
        return re.search(r'^__version__ = "(.*?)"$', f.read(), re.MULTILINE).group(1)


extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "swb"
copyright = "2018, Antonis Christofides"
author = "Antonis Christofides"
version = get_version()
release = version
language = None
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False
html_theme = "alabaster"
html_static_path = ["_static"]
htmlhelp_basename = "swbdoc"
latex_elements = {}
latex_documents = [
    (master_doc, "swb.tex", "swb Documentation", "Antonis Christofides", "manual")
]
man_pages = [(master_doc, "swb", "swb Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        "swb",
        "swb Documentation",
        author,
        "swb",
        "One line description of project.",
        "Miscellaneous",
    )
]
