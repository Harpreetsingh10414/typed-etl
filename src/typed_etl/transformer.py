from collections.abc import Mapping, Sequence

import polars as pl

from typed_etl.exceptions import TransformationError
from typed_etl.logger import get_logger


def rename_columns(
    df: pl.DataFrame,
    mapping: Mapping[str, str],
) -> pl.DataFrame:
    """
    Rename dataframe columns.
    """

    logger = get_logger()

    logger.info(
        "rename_columns_started",
        mappings=len(mapping),
    )

    try:
        result = df.rename(
            dict(mapping),
        )

        logger.info(
            "rename_columns_completed",
            columns=result.width,
        )

        return result

    except Exception as exc:
        raise TransformationError(f"Failed to rename columns: {exc}") from exc


def select_columns(
    df: pl.DataFrame,
    columns: Sequence[str],
) -> pl.DataFrame:
    """
    Select columns from dataframe.
    """

    logger = get_logger()

    logger.info(
        "select_columns_started",
        columns=len(columns),
    )

    try:
        result = df.select(
            list(columns),
        )

        logger.info(
            "select_columns_completed",
            columns=result.width,
        )

        return result

    except Exception as exc:
        raise TransformationError(f"Failed to select columns: {exc}") from exc


def drop_duplicates(
    df: pl.DataFrame,
    subset: Sequence[str] | None = None,
) -> pl.DataFrame:
    """
    Remove duplicate rows.
    """

    logger = get_logger()

    logger.info(
        "drop_duplicates_started",
        rows=df.height,
    )

    try:
        result = df.unique(
            subset=list(subset) if subset else None,
            maintain_order=True,
        )

        logger.info(
            "drop_duplicates_completed",
            original_rows=df.height,
            remaining_rows=result.height,
        )

        return result

    except Exception as exc:
        raise TransformationError(f"Failed to drop duplicates: {exc}") from exc


def fill_nulls(
    df: pl.DataFrame,
    values: Mapping[str, str | int | float],
) -> pl.DataFrame:
    """
    Fill null values.
    """

    logger = get_logger()

    logger.info(
        "fill_nulls_started",
        columns=len(values),
    )

    try:
        result = df

        for column, value in values.items():
            result = result.with_columns(pl.col(column).fill_null(value))

        logger.info(
            "fill_nulls_completed",
        )

        return result

    except Exception as exc:
        raise TransformationError(f"Failed to fill nulls: {exc}") from exc


def cast_columns(
    df: pl.DataFrame,
    mapping: Mapping[str, pl.DataType],
) -> pl.DataFrame:
    """
    Cast dataframe columns.
    """

    logger = get_logger()

    logger.info(
        "cast_columns_started",
        columns=len(mapping),
    )

    try:
        result = df

        for column, dtype in mapping.items():
            result = result.with_columns(pl.col(column).cast(dtype))

        logger.info(
            "cast_columns_completed",
        )

        return result

    except Exception as exc:
        raise TransformationError(f"Failed to cast columns: {exc}") from exc
