import json
from pathlib import Path

import yaml
from pydantic import ValidationError

from typed_etl.exceptions import ConfigValidationError
from typed_etl.models import BaseConfig


def load_config[T: BaseConfig](
    path: Path,
    model: type[T],
) -> T:
    """
    Load and validate config file.
    """

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if path.suffix == ".json":
        data = json.loads(path.read_text())

    elif path.suffix in [".yaml", ".yml"]:
        data = yaml.safe_load(path.read_text())

    else:
        raise ConfigValidationError(f"Unsupported config format: {path.suffix}")

    try:
        return model.model_validate(data)

    except ValidationError as exc:
        raise ConfigValidationError(str(exc)) from exc
