"""Structured logging for Tablint.

Provides a package-level logger that callers can use via get_logger().
By default, logs at WARNING level so end users don't see noise.
Library consumers can adjust via standard logging configuration.
"""

import logging

LOGGER_NAME = "tablint"


def get_logger(module_name: str = "") -> logging.Logger:
    """Get a logger scoped to a tablint submodule.

    Args:
        module_name: Dot-separated submodule path (e.g. "checks.correlations").
                     If empty, returns the root tablint logger.
    """
    name = f"{LOGGER_NAME}.{module_name}" if module_name else LOGGER_NAME
    return logging.getLogger(name)


# Configure root tablint logger with NullHandler (library best practice).
# This prevents "No handlers could be found" warnings when tablint is used
# as a library. End users or the CLI can attach their own handlers.
_root_logger = logging.getLogger(LOGGER_NAME)
_root_logger.addHandler(logging.NullHandler())
