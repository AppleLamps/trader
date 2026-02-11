"""
Logging setup for the bot.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(level: str = "INFO") -> logging.Logger:
    """Create and configure the bot logger."""
    logger = logging.getLogger("polyarb")
    logger.setLevel(getattr(logging, level, logging.INFO))

    if logger.handlers:
        return logger

    # Ensure console output can handle non-ASCII market names on Windows.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(
        log_dir / f"bot_{datetime.now().strftime('%Y%m%d')}.log",
        encoding="utf-8",
        errors="replace",
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
