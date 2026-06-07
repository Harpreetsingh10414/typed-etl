from typed_etl import (
    bind_correlation_id,
    configure_logging,
    get_logger,
    log_context,
)

configure_logging()

correlation_id = bind_correlation_id()

print(f"Correlation ID: {correlation_id}")

logger = get_logger()

logger.info(
    "pipeline_started",
    source_file="employees.csv",
)

with log_context(
    job_name="employee_ingestion",
    source_system="naukri",
):
    logger.info(
        "reading_file",
        filename="employees.csv",
    )

    logger.info(
        "transforming_data",
        rows=1200,
    )
