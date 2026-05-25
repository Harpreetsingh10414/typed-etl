from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BaseConfig(BaseModel):
    """
    Base configuration model.

    Shared parent for all config models.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class RetryPolicy(BaseConfig):
    """
    Retry configuration for retry decorators.
    """

    max_attempts: Annotated[
        int,
        Field(gt=0, description="Maximum retry attempts"),
    ] = 3

    wait_min: Annotated[
        float,
        Field(gt=0, description="Minimum wait duration"),
    ] = 1.0

    wait_max: Annotated[
        float,
        Field(gt=0, description="Maximum wait duration"),
    ] = 60.0


class LogContext(BaseConfig):
    """
    Shared logging context.
    """

    service_name: str
    environment: str = "dev"


class FileReaderConfig(BaseConfig):
    """
    File reader configuration.
    """

    separator: str = ","

    has_header: bool = True

    null_values: list[str] | None = None

    schema_overrides: dict[str, str] | None = None
