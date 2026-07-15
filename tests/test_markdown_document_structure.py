import unittest
from pathlib import Path

from engine.parsers import MarkdownDocument


class MarkdownDocumentStructureTestCase(unittest.TestCase):
    def test_default_structure_fields_are_empty(self) -> None:
        path = Path("/tmp/document.md")
        document = MarkdownDocument(path=path, content="# Title\nBody")

        self.assertEqual(document.headings, [])
        self.assertEqual(document.tags, [])
        self.assertEqual(document.wikilinks, [])
        self.assertEqual(document.images, [])
        self.assertEqual(document.tables, [])
        self.assertEqual(document.code_blocks, [])
        self.assertIsNone(document.front_matter)
        self.assertEqual(document.path, path)
        self.assertEqual(document.content, "# Title\nBody")


if __name__ == "__main__":
    unittest.main()
