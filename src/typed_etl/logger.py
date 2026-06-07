import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import cast
from uuid import uuid4

import structlog
from structlog.stdlib import BoundLogger


def configure_logging(
    level: str = "INFO",
    json_output: bool = True,
) -> None:
    """
    Configure structured logging for the application.

    Args:
        level: Logging level.
        json_output: Whether to emit JSON logs.
    """

    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
    )

    renderer = (
        structlog.processors.JSONRenderer() if json_output else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            renderer,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger() -> BoundLogger:
    """
    Return configured logger.

    Returns:
        BoundLogger instance.
    """
    return cast(
        BoundLogger,
        structlog.get_logger(),
    )


def bind_correlation_id(
    correlation_id: str | None = None,
) -> str:
    """
    Bind a correlation ID to the current context.

    Args:
        correlation_id: Optional correlation ID.

    Returns:
        Correlation ID used.
    """

    if correlation_id is None:
        correlation_id = str(uuid4())

    structlog.contextvars.bind_contextvars(
        correlation_id=correlation_id,
    )

    return correlation_id


@contextmanager
def log_context(
    **kwargs: object,
) -> Generator[None, None, None]:
    """
    Bind contextual values to logs.

    Example:
        with log_context(job="employee_load"):
            logger.info("started")
    """

    structlog.contextvars.bind_contextvars(
        **kwargs,
    )

    try:
        yield

    finally:
        structlog.contextvars.clear_contextvars()
