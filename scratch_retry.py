from typed_etl import (
    bind_correlation_id,
    configure_logging,
    retry,
)

configure_logging()

bind_correlation_id()

counter = 0


@retry(
    max_attempts=5,
    wait_min=1,
    wait_max=10,
)
def unstable_api() -> str:
    global counter

    counter += 1

    print(f"Attempt {counter}")

    if counter < 3:
        raise ConnectionError("Temporary API issue")

    return "Success"


result = unstable_api()

print(result)
