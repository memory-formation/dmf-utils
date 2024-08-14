Welcome to DMF Utils's documentation!
=====================================

.. image:: https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue.svg
   :alt: Python Versions

.. image:: https://readthedocs.org/projects/dmf-utils/badge/?version=latest
    :target: https://dmf-utils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/memory-formation/dmf-utils/blob/main/LICENSE
   :alt: License

----------------

DMF Utils is a Python package that provides a collection of utility functionalities to 
simplify common tasks in experiment and data analysis workflows. 
The package contains modules used by our group to facilitate tasks in neuroscience and artificial intelligence research.

.. toctree::
   :maxdepth: 2
   :caption: Content

   installation
   modules/index

Quick Start
-----------
.. _quick-start:

DMF Utils is designed in a modular way, allowing you to install only the components needed for a specific project. 
This modularity also ensures compatibility with a wide range of Python versions.

To install all modules:

.. code-block:: bash

    pip install dmf-utils[all]

See the :doc:`installation` section for more details.

You can use DMF Utils to send alerts and manage experiments efficiently. For example, here is how you can use the Alerts module:

.. code-block:: python

    from dmf.alerts import alert

    @alert
    def my_function(name):
        sleep(5)
        return f"Hello, {name}!"

    my_function("World")

Or from the command line:

.. code-block:: bash

    ./my_function > output.txt
    dmf-alert "Execution finished" -a output.txt

For more information on setting up the messaging service and using other functionalities, see the :doc:`modules/index` section.

Contributing
------------

DMF Utils is maintained by the DMF Group at the University of Barcelona. We welcome contributions from the community. If you would like to contribute, open an issue or submit a pull request on our `GitHub repository <https://github.com/memory-formation/dmf-utils>`

License
-------

DMF Utils is licensed under the MIT License. See the license file for more details.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`