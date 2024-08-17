Env
===

The `env` module in DMF Utils provides a flexible and powerful way to manage environment variables across different levels, including user, project, and system. This module simplifies the handling of environment variables by allowing you to load, set, unset, and retrieve variables from different sources, making it easy to manage configurations for your projects.

This module is included in the base package:

.. code-block:: bash

    pip install dmf-utils

Overview
--------

The `env` module allows you to:

- Load environment variables from user-level and project-level `.env` files.
- Set, get, and unset environment variables at different levels, ensuring your environment is configured correctly for your needs.
- Work with environment variables in a flexible manner, using either a global instance or custom `EnvManager` instances.
- Filter and retrieve all environment variables based on a specific scope or pattern.

This module is designed to integrate seamlessly into your existing workflows, providing a unified interface for managing environment variables in your projects.

Environment Management Functions
--------------------------------

The `env` module provides several key functions for environment management. These functions allow you to easily set up, retrieve, set, and unset environment variables, and load them from various sources.

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

    from dmf.env import env, setup, getenv, setenv, unsetenv

    # Setup the environment with default paths
    setup()

    # Set a variable in the project scope
    setenv('API_KEY', '12345', scope='project')

    # Get the value of an environment variable
    print(getenv('API_KEY'))  # Output: '12345'

    # Unset a variable from the environment
    unsetenv('API_KEY')

    # Set a variable in the user scope
    setenv('USER_SETTING', 'enabled', scope='user')

    # Load additional variables from a custom .env file
    env.load("custom.env")

**Working with a Custom EnvManager Instance**:

.. code-block:: python

    from dmf.env import EnvManager

    # Initialize a custom EnvManager
    custom_env = EnvManager().setup(project_env_path="my_project.env", user_env_path="~/.custom_env", override=True)

    # Set a variable in the user scope
    custom_env.setenv('SECRET_KEY', 'abcdef', scope='user')

    # Get the value of an environment variable
    print(custom_env.getenv('SECRET_KEY'))  # Output: 'abcdef'

    # Retrieve all environment variables in the project scope
    project_vars = custom_env.all(scope='project')
    print(project_vars)

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

**Filtering Environment Variables by Pattern**:

.. code-block:: python

    from dmf.env import env

    # Retrieve all environment variables containing 'API' in their names
    api_vars = env.all(pattern="API")
    print(api_vars)
