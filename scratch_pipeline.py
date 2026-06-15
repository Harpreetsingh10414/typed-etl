import polars as pl

from typed_etl import (
    ETLPipeline,
    ValidationConfig,
    bind_correlation_id,
    cast_columns,
    configure_logging,
    drop_duplicates,
    fill_nulls,
    rename_columns,
)

configure_logging()

bind_correlation_id()

validation_config = ValidationConfig(
    required_columns=[
        "emp_id",
        "name",
        "salary",
    ],
    non_nullable_columns=[
        "emp_id",
        "name",
    ],
    unique_columns=[],
    expected_schema={
        "emp_id": "Int64",
        "name": "String",
        "salary": "Int64",
        "department": "String",
    },
)

pipeline = ETLPipeline(
    input_path="data/transform_employees.csv",
    output_path="output/pipeline_output.parquet",
    validation_config=validation_config,
    overwrite=True,
)


def standardize_columns(
    df: pl.DataFrame,
) -> pl.DataFrame:
    return rename_columns(
        df,
        {
            "emp_id": "employee_id",
        },
    )


def clean_duplicates(
    df: pl.DataFrame,
) -> pl.DataFrame:
    return drop_duplicates(
        df,
        subset=["employee_id"],
    )


def fill_missing(
    df: pl.DataFrame,
) -> pl.DataFrame:
    return fill_nulls(
        df,
        {
            "department": "Unknown",
        },
    )


def cast_types(
    df: pl.DataFrame,
) -> pl.DataFrame:
    return cast_columns(
        df,
        {
            "salary": pl.Int64,
        },
    )


pipeline.add_transformation(standardize_columns)

pipeline.add_transformation(clean_duplicates)

pipeline.add_transformation(fill_missing)

pipeline.add_transformation(cast_types)

result = pipeline.run()

print("\nPipeline Result:\n")

print(result)
