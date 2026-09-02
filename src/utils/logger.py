"""Logging utilities."""
import logging
import logging.config
from pathlib import Path
import yaml


def setup_logging(config_path: str = "configs/logging.yaml") -> None:
    base_path = Path(__file__).parent.parent.parent
    full_path = base_path / config_path
    if full_path.exists():
        with open(full_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Ensure any directories referenced by file handlers exist
        for handler in config.get("handlers", {}).values():
            filename = handler.get("filename")
            if filename:
                Path(filename).parent.mkdir(parents=True, exist_ok=True)

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


class MLFlowHandler(logging.Handler):
    """Custom handler to log to MLflow."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            import mlflow
            msg = self.format(record)
            mlflow.log_param("log_message", msg)
        except ImportError:
            pass


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
