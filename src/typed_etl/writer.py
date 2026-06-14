from pathlib import Path

import polars as pl

from typed_etl.exceptions import (
    FileWriteError,
    UnsupportedFileFormatError,
)
from typed_etl.logger import get_logger

SUPPORTED_WRITE_FORMATS = {
    ".csv",
    ".json",
    ".parquet",
}


def write_file(
    df: pl.DataFrame,
    path: str | Path,
    overwrite: bool = False,
) -> None:
    """
    Write dataframe to disk.

    Args:
        df:
            Dataframe to write.

        path:
            Output file path.

        overwrite:
            Whether existing file can be overwritten.
    """

    logger = get_logger()

    file_path = Path(path)

    logger.info(
        "file_write_started",
        file=str(file_path),
        rows=df.height,
        columns=df.width,
    )

    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_WRITE_FORMATS:
        raise UnsupportedFileFormatError(f"Unsupported output format: {suffix}")

    if file_path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {file_path}")

    try:
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if suffix == ".csv":
            df.write_csv(file_path)

        elif suffix == ".json":
            df.write_json(file_path)

        elif suffix == ".parquet":
            df.write_parquet(file_path)

        logger.info(
            "file_write_completed",
            file=str(file_path),
            rows=df.height,
            columns=df.width,
        )

    except Exception as exc:
        logger.exception(
            "file_write_failed",
            file=str(file_path),
            error=str(exc),
        )

        raise FileWriteError(str(exc)) from exc
