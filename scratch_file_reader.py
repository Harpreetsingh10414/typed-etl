from typed_etl import (
    bind_correlation_id,
    configure_logging,
    read_file,
)

configure_logging()

bind_correlation_id()

csv_df = read_file("data/employees.csv")

print(csv_df)

json_df = read_file("data/employees.json")

print(json_df)
