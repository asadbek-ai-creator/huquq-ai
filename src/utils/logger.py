"""
Logging utilities for huquqAI system
"""

import sys
from pathlib import Path
from loguru import logger
from src.core.config import get_config


def setup_logging():
    """Setup logging configuration"""
    config = get_config()
    log_config = config.logging

    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stderr,
        format=log_config.get("format", "{time} | {level} | {message}"),
        level=log_config.get("level", "INFO"),
        colorize=True
    )

    # File handler
    log_file = log_config.get("file", "logs/huquqai.log")
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_file,
        format=log_config.get("format", "{time} | {level} | {message}"),
        level=log_config.get("level", "INFO"),
        rotation=log_config.get("rotation", "10 MB"),
        retention=log_config.get("retention", "30 days"),
        compression="zip"
    )

    logger.info("Logging initialized")


def get_logger(name: str):
    """Get logger instance"""
    return logger.bind(name=name)
