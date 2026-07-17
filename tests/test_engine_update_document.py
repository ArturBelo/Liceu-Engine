import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class EngineUpdateDocumentTestCase(unittest.TestCase):
    def test_update_document_overwrites_file_and_repository(self):
        with TemporaryDirectory() as temp_dir:
            sample_path = Path(temp_dir) / "sample.md"
            sample_path.write_text("# Sample\n\nOriginal content.\n")

            engine = LiceuEngine()
            engine.import_directory(Path(temp_dir))

            # ensure initial state
            docs = engine.list()
            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0].title, "Sample")
            self.assertIn("Original content", docs[0].content)

            # update through engine
            updated = engine.update_document("Sample", "# Sample\n\nUpdated content.\n")

            # verify the returned knowledge has updated content
            self.assertIn("Updated content", updated.content)

            # repository/list reflects update
            docs_after = engine.list()
            self.assertEqual(len(docs_after), 1)
            self.assertIn("Updated content", docs_after[0].content)

            # file on disk updated
            disk = sample_path.read_text()
            self.assertIn("Updated content", disk)


if __name__ == "__main__":
    unittest.main()
