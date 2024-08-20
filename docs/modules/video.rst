Video
=====

The `video` module in DMF Utils provides utilities for reading and writing video files. It offers functions to easily handle video frames, allowing you to write videos from frames and read videos into various formats such as NumPy arrays or PIL images.

This module is included in the base package:

.. code-block:: bash

    pip install dmf-utils[video]

Overview
--------

The `video` module allows you to:

- Write videos from frames using `VideoWriter` or the `write_video` function.
- Read videos into frames as either NumPy arrays or PIL images using `VideoReader` or the `read_video` function.
- Handle video processing tasks easily with support for common video formats.

Video Functions and Classes
---------------------------

Functions and classes included in this module:

.. autosummary::
   :toctree: autosummary

   dmf.video.write_video
   dmf.video.read_video
   dmf.video.VideoWriter
   dmf.video.VideoReader

Examples
--------

**Writing a Video**:

.. code-block:: python

    from dmf.video import write_video

    # Example: Writing a video from NumPy arrays
    import numpy as np
    frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) for _ in range(10)]
    write_video("output.mp4", frames, fps=30)

    # Example: Writing a video from image paths
    frames = ["frame1.png", "frame2.png", "frame3.png"]
    write_video("output.mp4", frames, fps=30)

**Reading a Video**:

.. code-block:: python

    from dmf.video import read_video

    # Example: Reading a video as a NumPy array
    frames = read_video("input.mp4", output_type="numpy")
    print(frames.shape)  # (num_frames, height, width, 3)

    # Example: Reading a video as a list of PIL images
    frames = read_video("input.mp4", output_type="pil")
    print(len(frames))  # Number of frames in the video

Classes
-------

**VideoWriter**:

.. code-block:: python

    from dmf.video import VideoWriter

    frames = ["frame1.png", "frame2.png", "frame3.png"]
    with VideoWriter("output.mp4", fps=30) as writer:
        for frame in frames:
            writer.add_frame(frame)

**VideoReader**:

.. code-block:: python

    from dmf.video import VideoReader

    with VideoReader("input.mp4", output_type="pil") as reader:
        for frame in reader:
            # Process each frame
            pass
