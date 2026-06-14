import polars as pl

from typed_etl import (
    bind_correlation_id,
    cast_columns,
    configure_logging,
    drop_duplicates,
    fill_nulls,
    read_file,
    rename_columns,
    write_file,
)

configure_logging()

bind_correlation_id()

df = read_file("data/transform_employees.csv")

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

print("\nFinal DataFrame:\n")
print(df)

write_file(
    df,
    "output/employees.parquet",
    overwrite=True,
)

write_file(
    df,
    "output/employees.csv",
    overwrite=True,
)

write_file(
    df,
    "output/employees.json",
    overwrite=True,
)

print("\nFiles written successfully!")
