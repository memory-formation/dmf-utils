
# DMF Utils

![Python Versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue)
[![Documentation Status](https://readthedocs.org/projects/dmf-utils/badge/?version=latest)](https://dmf-utils.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/memory-formation/dmf-utils/blob/main/LICENSE)

DMF Utils is a Python package that provides a collection of utility functionalities to simplify common tasks in experiment and data analysis workflows. The package contains modules used by our group to facilitate tasks in neuroscience and artificial intelligence research.

## Quick Start

This package is designed in a modular way, with some functionalities included in this repository and others in separate packages that can be called from here. This allows for installing only the components needed for a specific project, aiming to maintain the broadest compatibility with different Python versions.

You can install **all modules** with pip or other package managers by running:

```bash
pip install dmf-utils[all]
```

See the [documentation](https://dmf-utils.readthedocs.io/) for more installation options and help, including how to use it in environments without internet access.

## Modules

* [Alerts](#alerts): Get notified when a function finishes running and send messages or files to Slack and Telegram.

### Alerts

Send messages or files to Slack and Telegram, and get notified when a function finishes running.

```bash
pip install dmf-utils[alerts]
```

```python
from dmf.alerts import alert

@alert
def my_function(name):
    sleep(5)
    return f"Hello, {name}!"

my_function("World")
```

Or as a command-line tool:

```bash
./my_function > output.txt
dmf-alert "Execution finished" -a output.txt
```

See the documentation for more information on how to set up the messaging service and additional functionalities.

## Documentation

For full documentation, visit [Read the Docs](https://dmf-utils.readthedocs.io/).

## Contributing

This package is maintained by the [Dynamics of Memory Formation (DMF) Group at the University of Barcelona](https://brainvitge.org/groups/memory_formation/). We welcome contributions from the community. If you would like to contribute, please open an issue or a pull request.

## License

DMF Utils is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
