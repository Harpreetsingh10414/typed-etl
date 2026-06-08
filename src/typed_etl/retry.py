from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from tenacity import (
    RetryCallState,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_exponential_jitter,
)
from tenacity import (
    retry as tenacity_retry,
)

from typed_etl.exceptions import MaxRetriesExceededError
from typed_etl.logger import get_logger
from typed_etl.models import RetryPolicy

P = ParamSpec("P")
R = TypeVar("R")


def _log_before_sleep(
    retry_state: RetryCallState,
) -> None:
    """
    Log retry attempt information.
    """

    if retry_state.outcome is None:
        return

    logger = get_logger()

    exception = retry_state.outcome.exception()

    logger.warning(
        "retry_attempt",
        function_name=(retry_state.fn.__name__ if retry_state.fn is not None else "unknown"),
        attempt=retry_state.attempt_number,
        exception=str(exception),
    )


def retry(
    *,
    max_attempts: int = 3,
    wait_min: float = 1.0,
    wait_max: float = 60.0,
    reraise: bool = True,
    use_jitter: bool = True,
    retry_on: tuple[type[Exception], ...] = (Exception,),
    policy: RetryPolicy | None = None,
) -> Callable[
    [Callable[P, R]],
    Callable[P, R],
]:
    """
    Retry decorator.
    """

    if policy is not None:
        max_attempts = policy.max_attempts
        wait_min = policy.wait_min
        wait_max = policy.wait_max
        reraise = policy.reraise
        use_jitter = policy.use_jitter

    wait_strategy = (
        wait_exponential_jitter(
            initial=wait_min,
            max=wait_max,
        )
        if use_jitter
        else wait_exponential(
            min=wait_min,
            max=wait_max,
        )
    )

    def decorator(
        func: Callable[P, R],
    ) -> Callable[P, R]:
        tenacity_decorator = tenacity_retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_strategy,
            retry=retry_if_exception_type(retry_on),
            reraise=reraise,
            before_sleep=_log_before_sleep,
        )

        wrapped = tenacity_decorator(func)

        @wraps(func)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            try:
                return wrapped(
                    *args,
                    **kwargs,
                )

            except RetryError as exc:
                raise MaxRetriesExceededError(
                    function_name=func.__name__,
                    attempts=max_attempts,
                    original_exception=cast(
                        Exception,
                        exc.last_attempt.exception(),
                    ),
                ) from exc

        return wrapper

    return decorator
