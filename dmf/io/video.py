from pathlib import Path
from typing import Iterable, Optional, Union, TYPE_CHECKING

try:
    import cv2
except ImportError:
    raise ImportError(
        "OpenCV is required for video writing. "
        "Install it using `pip install opencv-python`."
    )

try:
    import numpy as np
except ImportError:
    raise ImportError(
        "NumPy is required for video writing. Install it using `pip install numpy`."
    )

if TYPE_CHECKING:
    import numpy as np
    from PIL import Image
    import matplotlib.pyplot as plt

FrameType = Union["np.ndarray", "Image.Image", "plt.Figure", Path, str]

CODECS_MAPPING = {
    "mp4": "mp4v",
    "m4v": "mp4v",
    "avi": "MJPG",
    "mov": "avc1",
}


class VideoWriter:
    def __init__(
        self, file_path: Union[str, Path], codec: Optional[str] = None, fps: int = 30
    ):
        self.file_path = Path(file_path)
        self.codec = codec or self._get_codec()
        self.fps = fps
        self._writer = None
        self._initialized = False
        self.height = None
        self.width = None
        self.n_frames = 0

    def add_frame(self, frame: FrameType) -> int:
        """Add a frame to the video."""
        frame_data = self._get_frame_data(frame)

        if not self._initialized:
            self._initialize_writer(frame_data)

        self._writer.write(frame_data)
        self.n_frames += 1
        return self.n_frames

    def generate_video(self, frames: Iterable[FrameType]) -> Path:
        """Generate a video from a list of frames."""
        for frame in frames:
            self.add_frame(frame)
        return self.release()

    def _get_codec(self) -> str:
        ext = self.file_path.suffix.lstrip(".").lower()
        codec = CODECS_MAPPING.get(ext)
        if codec:
            return codec

        raise ValueError(
            f"Unsupported video extension '{ext}'. "
            "Please specify the codec in the initialization."
        )

    def _initialize_writer(self, frame_data: "np.array"):
        """Initialize the VideoWriter based on the first frame's dimensions."""
        self.height, self.width = frame_data.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self._writer = cv2.VideoWriter(
            str(self.file_path), fourcc, self.fps, (self.width, self.height)
        )
        self._initialized = True

    def _get_frame_data(self, frame: FrameType) -> "np.ndarray":
        """Convert the frame to a NumPy array if needed and handle any necessary conversions."""
        # Check if the object can be treated as a path (file path-like)

        if hasattr(frame, "canvas"):
            # Matplotlib figure
            frame = self._figure_to_array(frame)
        elif isinstance(frame, (Path, str)):
            frame_path = Path(frame)
            if frame_path.exists() and frame_path.is_file():
                frame = cv2.imread(str(frame_path))
            else:
                raise FileNotFoundError(f"File not found: {frame_path}")

        # Convert the frame to a NumPy array
        frame = np.asarray(frame)

        # Convert grayscale to BGR if needed
        if frame.ndim == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        # Convert RGBA to BGR if needed
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        return frame

    def _figure_to_array(self, figure: "plt.Figure") -> "np.ndarray":
        """Convert a Matplotlib figure to a NumPy array."""
        # Save the figure to a BytesIO buffer in RGBA format
        from io import BytesIO
        from PIL import Image

        io_buf = BytesIO()
        figure.savefig(io_buf, format="png", pad_inches=0)
        io_buf.seek(0)

        # Read the image from the buffer and convert to a NumPy array
        img = Image.open(io_buf)
        img_arr = np.asarray(img)

        # Close the buffer
        io_buf.close()

        return img_arr

    def _reset(self):
        """Reset the video writer."""
        self._writer = None
        self._initialized = False
        self.height = None
        self.width = None
        self.n_frames = 0

    def release(self) -> Path:
        """Release the video writer and finalize the video file."""
        if self._writer:
            self._writer.release()
            self._reset()
            return self.file_path
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
