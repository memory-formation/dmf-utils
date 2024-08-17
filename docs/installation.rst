Installation
============

DMF Utils can be installed via `pip`, the Python package manager. 
Depending on your needs, you can install the entire package or specific modules.

Installing the Full Package
---------------------------

To install core package in DMF Utils, use the following command:

.. code-block:: bash

    pip install dmf-utils


Installing Modules
------------------

If you only need specific functionality, you can install individual modules.
For example, to install only the Alerts module:

.. code-block:: bash

    pip install dmf-utils[alerts]

This will install the core package along with the dependencies required for the Alerts module.


Check the :doc:`modules/index` page for a list of available modules and their functionalities.


Additional Options
------------------

Installing all packages
~~~~~~~~~~~~~~~~~~~~~~~

To install all modules and external dependencias use

.. code-block:: bash

    pip install 'dmf-utils[all, extra]'


.. note::

    **Disclaimer**: This can be a large installation due to the number of dependencies required for all modules.



Installing Without Internet Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


If you need to install DMF Utils on a machine without internet access, you can download the package and its dependencies as wheel files and install them manually.

1. Download the package and dependencies from PyPI using the following command on a machine with internet access:

   .. code-block:: bash

       pip download dmf-utils[all] --dest /path/to/download

2. Transfer the downloaded files to the target machine.

3. Install the package and dependencies using the following command:

   .. code-block:: bash

       pip install /path/to/download/*.whl

.. note::

    Make sure to download the wheel files on a machine with a similar configuration (e.g., Python version, OS) to the target machine to ensure compatibility.


Installing the Development Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer to install DMF Utils directly from the source code, you can clone the repository and install it manually:

.. code-block:: bash

    git clone https://github.com/memory-formation/dmf-utils.git
    cd dmf-utils
    pip install ".[all]" -e

This will install the package along with all its dependencies and allow you to make changes to the source code that are immediately reflected in your installation.

Verifying Your Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To verify that DMF Utils has been installed correctly, you can check the installed package version:

.. code-block:: python

    import dmf

    print(dmf.__version__)
