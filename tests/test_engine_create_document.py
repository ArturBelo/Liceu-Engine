import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine
from engine.exceptions.errors import ValidationError


class EngineCreateDocumentTestCase(unittest.TestCase):
    def test_create_document_without_vault_raises(self):
        engine = LiceuEngine()
        with self.assertRaises(ValidationError):
            engine.create_document("New", "# New")

    def test_create_document_creates_file_and_knowledge(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            engine.import_directory(Path(temp_dir))
            new = engine.create_document("Note One", "# Note One\n\nContent")

            # file should exist
            file_path = Path(temp_dir) / "Note_One.md"
            self.assertTrue(file_path.exists())

            self.assertEqual(engine.count(), 1)
            items = engine.list()
            self.assertEqual(items[0].title, "Note One")


if __name__ == "__main__":
    unittest.main()
