"""Configuration management utilities."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Singleton configuration manager."""

    _instance: Optional["Config"] = None
    _config: Dict[str, Any] = {}

    def __new__(cls, config_path: Optional[str] = None) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load(config_path or "configs/config.yaml")
        return cls._instance

    def _load(self, path: str) -> None:
        base_path = Path(__file__).parent.parent.parent
        full_path = base_path / path

        with open(full_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        # Load model config
        model_path = base_path / "configs/model_config.yaml"
        if model_path.exists():
            with open(model_path, "r", encoding="utf-8") as f:
                model_cfg = yaml.safe_load(f)
                if model_cfg and "models" in model_cfg:
                    self._config["models"] = model_cfg["models"]

        # Resolve env vars
        self._config = self._resolve_env_vars(self._config)

    def _resolve_env_vars(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._resolve_env_vars(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._resolve_env_vars(i) for i in obj]
        if isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            env_var = obj[2:-1]
            default = None
            if ":" in env_var:
                env_var, default = env_var.split(":", 1)
            return os.getenv(env_var, default)
        return obj

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    @property
    def raw(self) -> Dict[str, Any]:
        return self._config


def get_config() -> Config:
    return Config()
