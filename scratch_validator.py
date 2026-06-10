from typed_etl import (
    ValidationConfig,
    bind_correlation_id,
    configure_logging,
    read_file,
    validate_dataframe,
)

configure_logging()

bind_correlation_id()

df = read_file("data/valid_employees.csv")

validation_config = ValidationConfig(
    required_columns=[
        "employee_id",
        "name",
        "salary",
    ],
    non_nullable_columns=[
        "employee_id",
        "name",
    ],
    unique_columns=[
        "employee_id",
    ],
    expected_schema={
        "employee_id": "Int64",
        "name": "String",
        "salary": "Int64",
    },
)

validate_dataframe(
    df,
    validation_config,
)

print("Validation Passed")
