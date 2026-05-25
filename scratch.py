from pathlib import Path

from typed_etl.config_loader import load_config
from typed_etl.models import RetryPolicy

config = load_config(
    Path("config.yaml"),
    RetryPolicy,
)

print(config)
print(config.max_attempts)
