import os
from pathlib import Path
from typing import Optional, Union, Tuple

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# Define valid compression formats
VALID_COMPRESSION_FORMATS = (
     "zip", "tar.gz", "tar.bz2", "tar.xz", "gz", "tar", "bz2", "xz", "7z", "tgz", 
)
DEFAULT_COMPRESSION = "zip"
ERROR_PASSWORD = "Password protection is not supported for {compression} format. Supported only for ZIP and 7z formats."
NOT_SUPPORTED = "Compression format {compression} is not supported. Use one of {formats}."
FOLDER_ERROR = "Format {compression} cannot compress directories. Use formats like .zip, .tar, or .7z."

def compress(
    input_file: Union[str, Path],
    compression: Optional[Literal[ "gz", "zip", "tar", "bz2", "xz", "7z", "tgz", "tar.gz"]] = None,
    output_file: Optional[Union[str, Path]] = None,
    password: Optional[str] = None,
    **kwargs,
) -> Path:
    """
    Compress a file or directory.

    Args:
        input_file (Union[str, Path]): The input file path or directory.
        compression (Optional[str]): The compression format. Optional.
        output_file (Optional[Union[str, Path]]): The output file path. Optional.
        password (Optional[str]): Password for the archive. Supported only for ZIP and 7z formats.
        kwargs: Additional keyword arguments to pass to the compression function.

    Returns:
        Path: The path to the compressed file.

    Raises:
        ValueError: If the input or output is invalid or incompatible.
        NotImplementedError: If the specified compression format does not support password protection.
    """
    # Parse and validate the compression arguments
    input_file, output_file, compression = _parse_compression_args(
        input_file=input_file, output_file=output_file, compression=compression
    )
    
    if compression in {"gz", "bz2", "xz"}:
        if password:
            raise NotImplementedError(ERROR_PASSWORD.format(compression=compression))
        _compress_gzip_bzip2_xz(input_file, output_file, compression, **kwargs)
    elif compression == "zip":
        _compress_zip(input_file, output_file, password, **kwargs)
    elif compression in {"tar", "tgz", "tar.gz", "tar.bz2", "tar.xz"}:
        if password:
            raise NotImplementedError(ERROR_PASSWORD.format(compression=compression))
        _compress_tar(input_file, output_file, compression, **kwargs)
    elif compression == "7z":
        _compress_7z(input_file, output_file, password, **kwargs)
    else:
        raise ValueError(NOT_SUPPORTED.format(compression=compression, formats=list(VALID_COMPRESSION_FORMATS)))

    return output_file

def _compress_gzip_bzip2_xz(input_file: Path, output_file: Path, compression: str, **kwargs) -> None:
    """Compress a file using gzip, bzip2, or xz."""
    import shutil

    if input_file.is_dir():
        raise ValueError(FOLDER_ERROR.format(compression=compression))

    if compression == "gz":
        import gzip
        compressor = gzip.open
    elif compression == "bz2":
        import bz2
        compressor = bz2.open
    elif compression == "xz":
        import lzma
        compressor = lzma.open
    else:
        raise ValueError(NOT_SUPPORTED.format(compression=compression, formats=list(VALID_COMPRESSION_FORMATS)))

    with open(input_file, "rb") as f_in, compressor(output_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

def _compress_zip(input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs) -> None:
    """Compress a file or directory using zip."""
    import zipfile

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        if input_file.is_dir():
            for root, _, files in os.walk(input_file):
                for file in files:
                    zipf.write(Path(root) / file, Path(root).relative_to(input_file) / file)
        else:
            zipf.write(input_file, input_file.name)

        if password:
            zipf.setpassword(password.encode())

def _compress_7z(input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs) -> None:
    """Compress a file or directory using 7z."""
    try:
        import py7zr
    except ImportError:
        raise ImportError("py7zr package is required for 7z compression. Install it using `pip install py7zr`.")

    with py7zr.SevenZipFile(output_file, 'w', password=password, **kwargs) as archive:
        if input_file.is_dir():
            archive.writeall(input_file, arcname=input_file.name)
        else:
            archive.write(input_file, arcname=input_file.name)

def _compress_tar(input_file: Path, output_file: Path, compression: str, **kwargs) -> None:
    """Compress a file or directory using tar."""
    import tarfile

    mode_mapping = {
        "tar": "w",
        "tgz": "w:gz",
        "tar.gz": "w:gz",
        "tar.bz2": "w:bz2",
        "tar.xz": "w:xz",
    }
    if input_file.is_dir() or input_file.is_file():
        with tarfile.open(output_file, mode_mapping[compression]) as tar:
            tar.add(input_file, arcname=input_file.name)
    else:
        raise ValueError("Invalid input for tar compression.")

def _parse_compression_args(
    input_file: Union[str, Path],
    output_file: Optional[Union[str, Path]] = None,
    compression: Optional[str] = None,
) -> Tuple[Path, Path, str]:
    """Parse and validate the compression arguments."""
    # Convert input to Path if it's a string
    input_file = Path(input_file)

    # If compression is specified, ensure it's valid
    if compression:
        if compression not in VALID_COMPRESSION_FORMATS:
            raise ValueError(NOT_SUPPORTED.format(compression=compression, formats=list(VALID_COMPRESSION_FORMATS)))

        # If output_file is not specified, derive it from input_file
        output_file = Path(output_file) if output_file else input_file.with_suffix(input_file.suffix + f".{compression}")

        # If output_file does not end with the specified compression, append it
        if not str(output_file).endswith(f".{compression}"):
            output_file = output_file.with_suffix(output_file.suffix + f".{compression}")

    # Infer compression from output_file if not explicitly specified
    else:
        output_file = Path(output_file) if output_file else input_file.with_suffix(input_file.suffix + f".{DEFAULT_COMPRESSION}")

        # Infer compression from output_file extension
        compression = next(
            (ext for ext in VALID_COMPRESSION_FORMATS if str(output_file).endswith(f".{ext}")),
            DEFAULT_COMPRESSION,
        )

    return input_file, output_file, compression
