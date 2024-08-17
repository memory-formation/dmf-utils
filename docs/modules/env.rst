Env
===

The `env` module in DMF Utils provides utilities to manage environment variables.
It wraps python-dotenv to load automatically environment variables from `.env` files in different scopes.

This module is included in the base package:

.. code-block:: bash

    pip install dmf-utils

Overview
--------

Sometimes, you need to manage environment variables in your projects to configure settings, secrets, and other sensitive information.
However, in some cases, it can be challenging to keep track of all the environment variables you need to set, for example, when using several 
projects at the same time or when working with multiple environments (e.g., development, testing, production), or when you need to install
an experiment in different machines with different configurations.

This `env` module allows you to:

- Load environment variables from user-level and project-level `.env` files.
- Set, get, and unset environment variables at different levels, ensuring your environment is configured correctly for your needs.
- Work with environment variables in a flexible manner, using either a global instance or custom `EnvManager` instances.
- Filter and retrieve all environment variables based on a specific scope or pattern.

By default, it reads env variables from the user config file ``~/.env.dmf`` and the project config file ``.env``, if 
they exist. Joining with the existing environment variables.

Environment Management Functions
--------------------------------

Functions included in this module:

.. autosummary::
   :toctree: autosummary

   dmf.env.setup
   dmf.env.getenv
   dmf.env.setenv
   dmf.env.unsetenv
   dmf.env.EnvManager

Examples
--------

**Basic Usage**:

.. code-block:: python

    from dmf.env import env

    # Load an existing environment variable
    env.getenv('API_KEY') # Example output: '12345'

    # Set a variable, saving in the file '.env'
    setenv('SLACK_KEY', '12346', scope='project')

    # Set a variable in the user file '~/.env.dmf'
    setenv('USER_SETTING', 'enabled', scope='user')

    # Set an environment variable during the execution
    setenv('TEMPORAL_VAR', True)

    import os

    # All the environment variables are available in the os.environ
    print(os.getenv('TEMPORAL_VAR'))  # Output: 'True'

**Working with custom .env files**:

.. code-block:: python

    from dmf.env import setup, env

    # Set ap a custom project env file
    setup("custom.env")

    # List all variables
    env.all()

    # All variables that starts with DMF
    env.all("DMF_*")

**Loading Environment Variables from a String**:

.. code-block:: python

    from dmf.env import env, load_from_str

    dotenv_str = """
    API_KEY=12345
    DATABASE_URL=sqlite:///mydb.db
    """

    # Load environment variables from a string
    load_from_str(dotenv_str)

    # Verify that the variables are set
    print(env.getenv('API_KEY'))  # Output: '12345'
    print(env.getenv('DATABASE_URL'))  # Output: 'sqlite:///mydb.db'

**Loading var from multiple files**:

.. code-block:: python

    from dmf.env import env

    env.load("file1.env")
    env.load("file2.env")