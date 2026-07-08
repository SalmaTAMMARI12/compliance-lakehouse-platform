"""Système de configuration centralisé.

Deux sources combinées :
- `.env` / variables d'environnement pour les secrets et paramètres d'infra
  (via pydantic-settings, typé et validé au démarrage) ;
- `config/settings/*.yaml` pour les paramètres non sensibles versionnés
  (noms de buckets, statuts du pipeline...).

Un seul point d'entrée : `get_settings()`. Personne d'autre dans le code
ne doit lire `os.environ` ou parser un YAML directement.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config" / "settings"


class Settings(BaseSettings):
    """Variables d'environnement typées — cf. .env.example pour la liste complète."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "dgssi"
    postgres_user: str = "dgssi"
    postgres_password: str = "changeme"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "changeme"
    minio_secret_key: str = "changeme"
    minio_bucket_bronze: str = "bronze"
    minio_bucket_silver: str = "silver"
    minio_bucket_gold: str = "gold"
    minio_bucket_logs: str = "logs"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def _load_yaml_config(app_env: str) -> dict[str, Any]:
    """Fusionne base.yaml avec le fichier spécifique à l'environnement (ex. dev.yaml)."""
    config: dict[str, Any] = {}
    for filename in ("base.yaml", f"{app_env}.yaml"):
        path = _CONFIG_DIR / filename
        if path.exists():
            with path.open(encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            _deep_merge(config, data)
    return config


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_yaml_config() -> dict[str, Any]:
    return _load_yaml_config(get_settings().app_env)