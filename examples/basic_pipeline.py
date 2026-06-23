from typed_etl import (
    ETLPipeline,
)

pipeline = ETLPipeline(
    input_path="employees.csv",
    output_path="employees.parquet",
)

pipeline.run()
