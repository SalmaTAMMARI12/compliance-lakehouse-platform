"""Configuration centralisée du logging.

Tous les modules (domain, application, infrastructure, DAGs Airflow)
utilisent `get_logger(__name__)` plutôt que `logging.getLogger` directement,
pour garantir un format homogène et un point d'évolution unique
(ex. plus tard : export JSON structuré vers Loki).
"""

from __future__ import annotations

import logging
import sys

_CONFIGURED = False

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Configure le logging racine. Appelé une seule fois au démarrage de l'application."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=_FORMAT,
        stream=sys.stdout,
    )
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Retourne un logger nommé, en s'assurant que la config racine est initialisée."""
    if not _CONFIGURED:
        configure_logging()
    return logging.getLogger(name)