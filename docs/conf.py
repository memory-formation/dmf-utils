# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import pkg_resources

sys.path.append(os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

try:
    release = pkg_resources.get_distribution("dmf-utils").version
except pkg_resources.DistributionNotFound:
    print(
        "To build the documentation, the distribution information of "
        "dmf-utils has to be available. Either install the package "
        'into your development environment or run "setup.py develop" '
        "to setup the metadata. A virtualenv is recommended. "
    )
    sys.exit(1)

project = "dmf-utils"
copyright = "2024, Dynamics of Memory Formation Group, UB"
author = "Dynamics of Memory Formation Group (DMF)"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]


exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Add mappings
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'pillow': ('https://pillow.readthedocs.io/en/stable/', None),
    'torch': ('https://pytorch.org/docs/stable/', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
    'h5py': ('http://docs.h5py.org/en/stable/', None),
    'joblib': ('https://joblib.readthedocs.io/en/latest/', None),
}
autodoc_default_options = {"members": True, "inherited-members": True, "show-inheritance": True}

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_favicon = "https://brainvitge.org/website/wp-content/themes/brainvitge/favicon.png"
html_logo = "https://raw.githubusercontent.com/memory-formation/.github/main/logos/brainvitge.png"
html_theme_options = {
    "github_url": "https://github.com/memory-formation/dmf-utils",
    # "navbar_start": ["navbar-logo"],
    "logo": {
        "text": "dmf-utils",
    },
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/dmf-utils",
            "icon": "fab fa-python",
        },
         {
            "name": "DMF",
            "url": "https://brainvitge.org/groups/memory_formation/",
            "icon": "https://brainvitge.org/website/wp-content/themes/brainvitge/library/images/brainvitge-logo-45x40.png",
            "type": "url",
        },
    ],
}
html_context = {
    "github_user": "memory-formation",
    "github_repo": "dmf-utils",
    "github_version": "main",
    "doc_path": "docs",
}

