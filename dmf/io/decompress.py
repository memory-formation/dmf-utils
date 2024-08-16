from pathlib import Path
from typing import Optional, Union, Tuple

# Define valid compression formats
VALID_COMPRESSION_FORMATS = (
     "zip", "tar.gz", "tar.bz2", "tar.xz", "gz", "tar", "bz2", "xz", "7z", "tgz", 
)
ERROR_PASSWORD = "Password protection is not supported for {compression} format. Supported only for ZIP and 7z formats."
NOT_SUPPORTED = "Compression format {compression} is not supported. Use one of {formats}."


def decompress(
    input_file: Union[str, Path],
    output_dir: Union[str, Path] = "./",
    compression: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs,
) -> Path:
    """
    Decompress a compressed file.

    Args:
        input_file (Union[str, Path]): The compressed input file path.
        output_dir (Union[str, Path]): The directory where files should be extracted.
        compression (Optional[str]): The compression format. Optional.
        password (Optional[str]): Password for the archive. Supported only for ZIP and 7z formats.
        kwargs: Additional keyword arguments to pass to the decompression function.

    Returns:
        Path: The path to the decompressed files.

    Raises:
        ValueError: If the input is invalid or incompatible.
        NotImplementedError: If the specified compression format does not support password protection.
    """
    # Parse and validate the decompression arguments
    input_file, output_dir, compression = _parse_decompression_args(
        input_file=input_file, output_dir=output_dir, compression=compression
    )
    
    if compression in {"gz", "bz2", "xz"}:
        if password:
            raise NotImplementedError(ERROR_PASSWORD.format(compression=compression))
        _decompress_gzip_bzip2_xz(input_file, output_dir, compression, **kwargs)
    elif compression == "zip":
        _decompress_zip(input_file, output_dir, password, **kwargs)
    elif compression in {"tar", "tgz", "tar.gz", "tar.bz2", "tar.xz"}:
        if password:
            raise NotImplementedError(ERROR_PASSWORD.format(compression=compression))
        _decompress_tar(input_file, output_dir, compression, **kwargs)
    elif compression == "7z":
        _decompress_7z(input_file, output_dir, password, **kwargs)

    return output_dir


def _decompress_gzip_bzip2_xz(input_file: Path, output_dir: Path, compression: str, **kwargs) -> None:
    """Decompress a gzip, bzip2, or xz file."""
    import shutil

    if compression == "gz":
        import gzip
        decompressor = gzip.open
    elif compression == "bz2":
        import bz2
        decompressor = bz2.open
    elif compression == "xz":
        import lzma
        decompressor = lzma.open
    else:
        raise ValueError(NOT_SUPPORTED.format(compression=compression, formats=list(VALID_COMPRESSION_FORMATS)))

    with decompressor(input_file, "rb") as f_in, open(output_dir / input_file.stem, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def _decompress_zip(input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs) -> None:
    """Decompress a zip file."""
    import zipfile

    with zipfile.ZipFile(input_file, "r") as zipf:
        if password:
            zipf.setpassword(password.encode())
        zipf.extractall(output_dir)


def _decompress_7z(input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs) -> None:
    """Decompress a 7z file."""
    try:
        import py7zr
    except ImportError:
        raise ImportError("py7zr package is required for 7z decompression. Install it using `pip install py7zr`.")

    with py7zr.SevenZipFile(input_file, 'r', password=password, **kwargs) as archive:
        archive.extractall(output_dir)


def _decompress_tar(input_file: Path, output_dir: Path, compression: str, **kwargs) -> None:
    """Decompress a tar file."""
    import tarfile

    with tarfile.open(input_file, "r") as tar:
        tar.extractall(output_dir)


def _parse_decompression_args(
    input_file: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    compression: Optional[str] = None,
) -> Tuple[Path, Path, str]:
    """Parse and validate the decompression arguments."""
    # Convert input to Path if it's a string
    input_file = Path(input_file)

    # Check if the input file exists and is a file
    if not input_file.exists() or not input_file.is_file():
        raise ValueError(f"Input file does not exist or is not a valid file: {input_file}")

    # If compression is specified, ensure it's valid
    if compression:
        if compression not in VALID_COMPRESSION_FORMATS:
            raise ValueError(NOT_SUPPORTED.format(compression=compression, formats=list(VALID_COMPRESSION_FORMATS)))
    else:
        # Infer compression from input_file extension
        compression = next(
            (ext for ext in VALID_COMPRESSION_FORMATS if str(input_file).endswith(f".{ext}")),
            None
        )
        if not compression:
            raise ValueError("Unable to infer compression format from the input file extension.")

    
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    print("The compression format is: ", compression)

    return input_file, output_dir, compression
