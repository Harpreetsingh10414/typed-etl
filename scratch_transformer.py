import polars as pl

from typed_etl import (
    bind_correlation_id,
    cast_columns,
    configure_logging,
    drop_duplicates,
    fill_nulls,
    read_file,
    rename_columns,
    select_columns,
)

configure_logging()

bind_correlation_id()

df = read_file("data/transform_employees.csv")

print("\nOriginal\n")
print(df)

df = rename_columns(
    df,
    {
        "emp_id": "employee_id",
    },
)

df = drop_duplicates(
    df,
    subset=["employee_id"],
)

df = fill_nulls(
    df,
    {
        "department": "Unknown",
    },
)

df = cast_columns(
    df,
    {
        "salary": pl.Int64,
    },
)

df = select_columns(
    df,
    [
        "employee_id",
        "name",
        "salary",
        "department",
    ],
)

print("\nTransformed\n")
print(df)
