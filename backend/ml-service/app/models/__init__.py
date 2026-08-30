"""Models package — ML model artifacts storage and registry."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Default model directory
MODEL_DIR = Path("/app/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


class ModelRegistry:
    """Simple file-based model registry.

    In production, use MLflow or similar. This is a minimal implementation
    for development that tracks which model version is currently active.
    """

    _registry: dict[str, dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, version: str, path: str, metadata: dict | None = None) -> None:
        """Register a new model version."""
        key = f"{name}:{version}"
        cls._registry[key] = {
            "name": name,
            "version": version,
            "path": path,
            "metadata": metadata or {},
            "active": False,
        }
        logger.info("Registered model %s", key)

    @classmethod
    def set_active(cls, name: str, version: str) -> None:
        """Set a model version as active."""
        for key, entry in cls._registry.items():
            if entry["name"] == name:
                entry["active"] = (entry["version"] == version)
        logger.info("Set active %s = %s", name, version)

    @classmethod
    def get_active(cls, name: str) -> dict[str, Any] | None:
        """Get the currently active model version for a given model name."""
        for entry in cls._registry.values():
            if entry["name"] == name and entry["active"]:
                return entry
        return None

    @classmethod
    def list_models(cls) -> list[dict[str, Any]]:
        """List all registered models."""
        return list(cls._registry.values())


__all__ = ["ModelRegistry", "MODEL_DIR"]
