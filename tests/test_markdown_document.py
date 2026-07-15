import unittest
from pathlib import Path

from engine.parsers import MarkdownDocument


class MarkdownDocumentTestCase(unittest.TestCase):
    def test_creation(self) -> None:
        path = Path("/tmp/document.md")
        document = MarkdownDocument(path=path, content="# Title\nBody")

        self.assertEqual(document.path, path)
        self.assertEqual(document.content, "# Title\nBody")
        self.assertIsNone(document.front_matter)
        self.assertEqual(document.headings, [])
        self.assertEqual(document.tags, [])
        self.assertEqual(document.wikilinks, [])
        self.assertEqual(document.images, [])
        self.assertEqual(document.tables, [])
        self.assertEqual(document.code_blocks, [])

    def test_front_matter_is_preserved(self) -> None:
        path = Path("/tmp/document.md")
        front_matter = {"title": "Test", "tags": ["a", "b"]}
        document = MarkdownDocument(path=path, content="# Title", front_matter=front_matter)

        self.assertEqual(document.path, path)
        self.assertEqual(document.content, "# Title")
        self.assertEqual(document.front_matter, front_matter)
        self.assertEqual(document.headings, [])
        self.assertEqual(document.tags, [])
        self.assertEqual(document.wikilinks, [])
        self.assertEqual(document.images, [])
        self.assertEqual(document.tables, [])
        self.assertEqual(document.code_blocks, [])


if __name__ == "__main__":
    unittest.main()
