import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class EngineTestCase(unittest.TestCase):
    def test_engine_adds_and_lists_markdown(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            markdown_path = Path(temp_dir) / "sample.md"
            markdown_path.write_text("# Sample Title\n\nThis is the sample content.\n")

            knowledge = engine.add_markdown(markdown_path)

            self.assertEqual(knowledge.title, "Sample Title")
            self.assertIn("sample content", knowledge.content)
            self.assertEqual(engine.count(), 1)

            items = engine.list()
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].id, knowledge.id)

            results = engine.search("sample")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].id, knowledge.id)

    def test_engine_search_returns_empty_for_unknown_query(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            markdown_path = Path(temp_dir) / "sample.md"
            markdown_path.write_text("# Sample Title\n\nThis is the sample content.\n")

            engine.add_markdown(markdown_path)
            results = engine.search("missing")

            self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
