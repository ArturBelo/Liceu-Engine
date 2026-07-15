import io
import logging
import unittest

from engine.logging import Logger


class LoggerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = Logger()
        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s %(message)s"))
        self.logger._logger.addHandler(self.handler)

    def tearDown(self) -> None:
        self.logger._logger.removeHandler(self.handler)
        self.handler.close()

    def test_logger_creation(self) -> None:
        self.assertIsInstance(self.logger, Logger)

    def test_info_logs_message(self) -> None:
        self.logger.info("info message")
        self.handler.flush()
        output = self.stream.getvalue()
        self.assertIn("[INFO]", output)
        self.assertIn("info message", output)

    def test_warning_logs_message(self) -> None:
        self.logger.warning("warning message")
        self.handler.flush()
        output = self.stream.getvalue()
        self.assertIn("[WARNING]", output)
        self.assertIn("warning message", output)

    def test_error_logs_message(self) -> None:
        self.logger.error("error message")
        self.handler.flush()
        output = self.stream.getvalue()
        self.assertIn("[ERROR]", output)
        self.assertIn("error message", output)

    def test_debug_logs_message_when_level_debug(self) -> None:
        self.logger._logger.setLevel(logging.DEBUG)
        self.logger.debug("debug message")
        self.handler.flush()
        output = self.stream.getvalue()
        self.assertIn("[DEBUG]", output)
        self.assertIn("debug message", output)
        self.logger._logger.setLevel(logging.INFO)

    def test_singleton_internal_logger(self) -> None:
        other_logger = Logger()
        self.assertIs(self.logger._logger, other_logger._logger)


if __name__ == "__main__":
    unittest.main()
