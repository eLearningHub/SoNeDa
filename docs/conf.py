"""Sphinx configuration."""
project = "Social networks cli"
author = "Behzad Samadi"
copyright = "2022, Behzad Samadi"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
