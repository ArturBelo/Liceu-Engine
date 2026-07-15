import unittest
from pathlib import Path

from engine.parsers import HeadingParser, MarkdownDocument


class HeadingParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = HeadingParser()

    def test_document_without_headings(self) -> None:
        document = MarkdownDocument(path=Path("/tmp/doc.md"), content="No headings here.")

        result = self.parser.process(document)

        self.assertEqual(result.headings, [])
        self.assertEqual(result.content, document.content)
        self.assertEqual(result.path, document.path)

    def test_single_heading(self) -> None:
        document = MarkdownDocument(path=Path("/tmp/doc.md"), content="# Title")

        result = self.parser.process(document)

        self.assertEqual(result.headings, ["Title"])

    def test_multiple_headings(self) -> None:
        document = MarkdownDocument(
            path=Path("/tmp/doc.md"),
            content="# First\n## Second\n### Third",
        )

        result = self.parser.process(document)

        self.assertEqual(result.headings, ["First", "Second", "Third"])

    def test_different_heading_levels(self) -> None:
        document = MarkdownDocument(
            path=Path("/tmp/doc.md"),
            content="# One\n## Two\n### Three\n#### Four\n##### Five\n###### Six",
        )

        result = self.parser.process(document)

        self.assertEqual(
            result.headings,
            ["One", "Two", "Three", "Four", "Five", "Six"],
        )

    def test_headings_with_extra_spaces(self) -> None:
        document = MarkdownDocument(
            path=Path("/tmp/doc.md"),
            content="#    Title   \n##   Subtitle  ",
        )

        result = self.parser.process(document)

        self.assertEqual(result.headings, ["Title", "Subtitle"])


if __name__ == "__main__":
    unittest.main()
