import logging

_logger = logging.getLogger("liceu_engine")
_logger.setLevel(logging.INFO)

if not _logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s %(message)s"))
    _logger.addHandler(handler)
    _logger.propagate = False


class Logger:
    """Singleton wrapper for the engine logger."""

    def __init__(self) -> None:
        self._logger = _logger

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)
