from collections.abc import Sequence

import polars as pl

from typed_etl.exceptions import DataValidationError
from typed_etl.logger import get_logger
from typed_etl.models import ValidationConfig


def validate_required_columns(
    df: pl.DataFrame,
    required_columns: Sequence[str],
) -> None:
    """
    Validate required columns exist.
    """

    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise DataValidationError(f"Missing columns: {missing_columns}")


def validate_no_nulls(
    df: pl.DataFrame,
    columns: Sequence[str],
) -> None:
    """
    Validate columns contain no nulls.
    """

    for column in columns:
        null_count = df[column].is_null().sum()

        if null_count > 0:
            raise DataValidationError(f"Column '{column}' contains {null_count} null values")


def validate_unique(
    df: pl.DataFrame,
    columns: Sequence[str],
) -> None:
    """
    Validate uniqueness.
    """

    for column in columns:
        unique_count = df[column].n_unique()

        row_count = df.height

        if unique_count != row_count:
            raise DataValidationError(f"Column '{column}' contains duplicate values")


def validate_schema(
    df: pl.DataFrame,
    expected_schema: dict[str, str],
) -> None:
    """
    Validate dataframe schema.
    """

    actual_schema = {name: str(dtype) for name, dtype in df.schema.items()}

    for column, expected_type in expected_schema.items():
        actual_type = actual_schema.get(column)

        if actual_type != expected_type:
            raise DataValidationError(
                f"Column '{column}' expected type '{expected_type}' but found '{actual_type}'"
            )


def validate_dataframe(
    df: pl.DataFrame,
    config: ValidationConfig,
) -> None:
    """
    Run all configured validations.
    """

    logger = get_logger()

    logger.info(
        "validation_started",
        rows=df.height,
        columns=df.width,
    )

    validate_required_columns(
        df,
        config.required_columns,
    )

    validate_no_nulls(
        df,
        config.non_nullable_columns,
    )

    validate_unique(
        df,
        config.unique_columns,
    )

    validate_schema(
        df,
        config.expected_schema,
    )

    logger.info(
        "validation_passed",
        rows=df.height,
        columns=df.width,
    )
