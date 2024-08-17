
IO (Input/Output)
=================

The IO module in DMF Utils provides tools for handling file operations, including saving, loading, compression, and decompression of various file formats. These utilities simplify working with different data formats, making it easier to manage files and directories in your data workflows.

This module is installed as part of the base package.

.. code-block:: bash

    pip install dmf-utils

However, there are additional external dependencies required for specific file formats and operations. For example, to work with HDF5 files, you may need to install the `h5py` package. An error will be raised when you need to install additional dependencies. However, you can install ALL dependencies by running:

.. code-block:: bash

    pip install dmf-utils[extra]

Overview
--------

The IO module allows you to:

- Save and load data in various formats, including CSV, JSON, HDF5, NumPy, and more.
- Compress and decompress files and directories with support for popular formats like ZIP, 7z, tar, gzip, etc.
- Other utilities like creating videos from image frames.

This module mainly contains wrappers for specific loaders and savers designed to facilitate common file operations in data processing.

Saving and Loading
------------------

The saving and loading functions in the IO module support a wide variety of formats, automatically inferring the appropriate format based on the file extension or allowing you to specify it explicitly.


.. autosummary::
   :toctree: autosummary

   dmf.io.save
   dmf.io.load


Supported File Formats
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Supported File Formats for Saving and Loading
   :header-rows: 1

   * - Loader / Saver
     - Extensions
   * - Pickle
     - .pkl, .pickle
   * - Joblib
     - .joblib
   * - HDF5
     - .h5, .hdf5, .hdf
   * - JSON
     - .json
   * - Text
     - .txt, .html, .log, .md, .rst
   * - NumPy
     - .npz, .npy
   * - Pandas
     - .csv, .parquet, .xlsx, .xls, .feather
   * - Pillow (Images)
     - .jpg, .jpeg, .png, .bmp, .gif, .tiff, .tif, .webp
   * - PyTorch
     - .pt, .pth
   * - YAML
     - .yaml, .yml
   * - INI
     - .ini, .cfg
   * - MATLAB (Scipy)
     - .mat
   * - Audio (Librosa)
     - .wav, .mp3, .flac, .ogg
   * - Video (OpenCV)
     - .mp4, .avi, .mov, .mkv


Examples
~~~~~~~~

**Saving a DataFrame to a CSV File**:

.. code-block:: python

    import pandas as pd
    from dmf.io import save

    df = pd.DataFrame({"a": [1, 2, 3]})
    save(df, "data.csv")

**Loading a DataFrame from a CSV File**:

.. code-block:: python

    from dmf.io import load

    df = load("data.csv")
    print(df)

Compression
-----------

The IO module provides easy-to-use tools for compressing and decompressing files and directories. Supported formats include gzip, bzip2, xz, zip, 7z, and various tar-based formats.

.. autosummary::
   :toctree: autosummary

   dmf.io.compress
   dmf.io.decompress


Compression Methods
~~~~~~~~~~~~~~~~~~~


.. list-table:: Supported Compression Methods
   :header-rows: 1

   * - Method
     - Extensions
     - Password
     - Folders
   * - gzip
     - .gz, .gzip
     - ❌
     - ❌
   * - bzip2
     - .bz2, .bzip2
     - ❌
     - ❌
   * - xz
     - .xz
     - ❌
     - ❌
   * - zip
     - .zip
     - ❌
     - ✅
   * - 7z (`py7zr <https://py7zr.readthedocs.io/en/latest/>`_)
     - .7z
     - ✅
     - ✅
   * - tar 
     - .tar
     - ❌
     - ✅
   * - tar  (+ compression)
     - .tar.gz, .tar.bz2, .tar.xz
     - ❌
     - ✅



Examples
~~~~~~~~

**Compressing a Directory**:

.. code-block:: python

    from dmf.io import compress

    compress("my_folder", compression="zip")

**Decompressing a File**:

.. code-block:: python

    from dmf.io import decompress

    decompress("my_folder.zip")

Other Utilities
---------------

In addition to saving, loading, and compression, the IO module includes utilities such as `VideoWriter`, which can be used to create videos from image frames.

.. autosummary::
   :toctree: autosummary

   dmf.io.VideoWriter


Examples
~~~~~~~~

**Creating a Video from Image Frames**:

.. code-block:: python

    import cv2
    from dmf.io.video import VideoWriter

    # Initialize the VideoWriter
    with VideoWriter("output.mp4", fps=30) as writer:
        for i in range 100):
            frame = cv2.imread(f"frame_{i}.png")
            writer.add_frame(frame)

This will create a video file `output.mp4` from a sequence of image frames.
