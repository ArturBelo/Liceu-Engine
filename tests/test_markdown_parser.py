import tempfile
import unittest
from pathlib import Path

from engine.parsers import MarkdownParser, MarkdownDocument
from engine.exceptions import EngineError, ValidationError


class MarkdownParserTestCase(unittest.TestCase):
    def test_parse_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "doc.md"
            path.write_text("# Title\n\nContent", encoding="utf-8")

            parser = MarkdownParser(path)
            document = parser.parse()

            self.assertIsInstance(document, MarkdownDocument)
            self.assertEqual(document.path, path)
            self.assertEqual(document.content, "# Title\n\nContent")
            self.assertIsNone(document.front_matter)

    def test_file_not_found_raises_engine_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing.md"
            parser = MarkdownParser(path)

            with self.assertRaises(EngineError):
                parser.parse()

    def test_invalid_extension_raises_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "doc.txt"
            path.write_text("content", encoding="utf-8")
            parser = MarkdownParser(path)

            with self.assertRaises(ValidationError):
                parser.parse()

    def test_parse_empty_file_returns_empty_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.md"
            path.write_text("", encoding="utf-8")
            parser = MarkdownParser(path)

            document = parser.parse()

            self.assertIsInstance(document, MarkdownDocument)
            self.assertEqual(document.content, "")
            self.assertEqual(document.path, path)
            self.assertIsNone(document.front_matter)


if __name__ == "__main__":
    unittest.main()
