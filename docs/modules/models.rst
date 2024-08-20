Models
======

The `dmf.models` module provides utilities for tasks related to PyTorch models.

This package is included in the `dmf-utils` core package and can be installed using the following command:

.. code-block:: bash

    pip install dmf-utils


Howeve, you need to have installed PyTorch to use the functionalities in this module. 
The installation instructions for PyTorch are provided below.

Content
---------

The `dmf.models` module includes the following functions:

.. autosummary::
   :toctree: autosummary

   dmf.models.free
   dmf.models.get_memory_stats
   dmf.models.get_device
   dmf.models.set_seed


Pytorch Installation
--------------------

For detailed information check the official `PyTorch installation guide <https://pytorch.org/get-started/locally/>`_.

Linux + CUDA
~~~~~~~~~~~~

1. First, check your cuda version by running:

.. code-block:: bash

    nvcc --version

If you dont have CUDA installed, you can install it by following the instructions on the `NVIDIA CUDA Toolkit <https://developer.nvidia.com/cuda-toolkit>`_ page.

To install the latest version of PyTorch for your CUDA support, run:

.. code-block:: bash

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

Make sure to replace `cu118` with the appropriate version matching your CUDA toolkit version.

macOS + MPS
~~~~~~~~~~~

On macOS systems, especially those with Apple Silicon (M1, M2 chips), 
you can use the Metal Performance Shaders (MPS) backend by installing PyTorch with:

.. code-block:: bash

    pip install torch torchvision torchaudio

The MPS backend is automatically enabled when using PyTorch on compatible macOS devices.

CPU-based
~~~~~~~~~

For environments without GPU support or when running on systems without CUDA or MPS capabilities,
 you can install the CPU-only version of PyTorch:

.. code-block:: bash

    pip install torch torchvision torchaudio