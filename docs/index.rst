Welcome to DMF Utils's documentation!
=====================================

.. image:: https://badge.fury.io/py/dmf-utils.svg
   :target: https://pypi.org/project/dmf-utils/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/dmf-utils
   :alt: PyPI - Python Version

.. image:: https://readthedocs.org/projects/dmf-utils/badge/?version=latest
   :target: https://dmf-utils.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/memory-formation/dmf-utils/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/memory-formation/dmf-utils/actions/workflows/tests.yml
   :alt: Tests

.. image:: https://www.repostatus.org/badges/latest/wip.svg
   :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
   :target: https://www.repostatus.org/#wip

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/memory-formation/dmf-utils/blob/main/LICENSE
   :alt: License

----------------

DMF Utils is a Python package that provides a collection of utility functionalities to simplify 
common tasks in experiment and data analysis workflows. 
The package contains reusable modules to facilitate tasks in neuroscience research.

.. toctree::
   :maxdepth: 2
   :caption: Content

   installation
   modules/index

Installation
------------

DMF Utils can be installed directly from PyPI. To install all available modules, use the following command:

.. code-block:: bash

    pip install dmf-utils[all]

For more detailed installation instructions and options, please refer to the :doc:`installation` page.

Modules
-------

DMF Utils is designed in a modular way, allowing you to install only the components needed for your specific project. The available modules include:

- :doc:`modules/alerts`: Tools for sending notifications and alerts via Slack and Telegram.
- :doc:`modules/io`: Input/output utilities for file handling and data management.


For more detailed information about each module, see the :doc:`modules/index` section.

Contributing
------------

DMF Utils is maintained by the Dynamics of Memory Formation (DMF) Group at the University of Barcelona. 
We welcome contributions from the community. 
If you would like to contribute, please open an issue or submit a pull request on our `GitHub repository <https://github.com/memory-formation/dmf-utils>`_.

License
-------

DMF Utils is licensed under the MIT License. 
For more details, see the full license text in the `license <https://raw.githubusercontent.com/memory-formation/dmf-utils/main/LICENSE>`_ file.

Indices and tables
------------------

* :ref:`search`
* :ref:`genindex`
