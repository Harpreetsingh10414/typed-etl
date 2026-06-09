from pathlib import Path

import polars as pl

from typed_etl.exceptions import (
    FileReadError,
    UnsupportedFileFormatError,
)
from typed_etl.logger import get_logger
from typed_etl.models import FileReaderConfig

SUPPORTED_FORMATS = {
    ".csv",
    ".json",
    ".parquet",
}


def read_file(
    path: str | Path,
    config: FileReaderConfig | None = None,
) -> pl.DataFrame:
    """
    Read a file into a Polars DataFrame.

    Args:
        path:
            Path to file.

        config:
            Optional reader configuration.

    Returns:
        Polars DataFrame.
    """

    logger = get_logger()

    file_path = Path(path)

    logger.info(
        "file_read_started",
        file=str(file_path),
    )

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_FORMATS:
        raise UnsupportedFileFormatError(f"Unsupported file format: {suffix}")

    config = config or FileReaderConfig()

    try:
        if suffix == ".csv":
            dataframe = pl.read_csv(
                file_path,
                separator=config.separator,
                has_header=config.has_header,
                null_values=config.null_values,
            )

        elif suffix == ".json":
            dataframe = pl.read_json(file_path)

        elif suffix == ".parquet":
            dataframe = pl.read_parquet(file_path)

        else:
            raise UnsupportedFileFormatError(f"Unsupported file format: {suffix}")

        logger.info(
            "file_read_completed",
            file=str(file_path),
            rows=dataframe.height,
            columns=dataframe.width,
        )

        return dataframe

    except Exception as exc:
        logger.exception(
            "file_read_failed",
            file=str(file_path),
            error=str(exc),
        )

        raise FileReadError(str(exc)) from exc
