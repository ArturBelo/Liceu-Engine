import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class ImportDirectoryTestCase(unittest.TestCase):
    def test_import_directory_empty_folder(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            imported = engine.import_directory(Path(temp_dir))

            self.assertEqual(imported, [])
            self.assertEqual(engine.count(), 0)

    def test_import_directory_single_file(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            markdown_path = Path(temp_dir) / "single.md"
            markdown_path.write_text("# Single File\n\nContent here.\n")

            imported = engine.import_directory(Path(temp_dir))

            self.assertEqual(len(imported), 1)
            self.assertEqual(imported[0].title, "Single File")
            self.assertEqual(engine.count(), 1)

    def test_import_directory_multiple_files_and_subfolders(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            root_file = Path(temp_dir) / "root.md"
            nested_dir = Path(temp_dir) / "nested"
            nested_dir.mkdir()
            nested_file = nested_dir / "nested.md"
            ignored_file = Path(temp_dir) / "ignore.txt"

            root_file.write_text("# Root File\n\nRoot content.\n")
            nested_file.write_text("# Nested File\n\nNested content.\n")
            ignored_file.write_text("This should be ignored.\n")

            imported = engine.import_directory(Path(temp_dir))

            self.assertEqual(len(imported), 2)
            self.assertEqual(imported[0].title, "Nested File")
            self.assertEqual(imported[1].title, "Root File")
            self.assertEqual(engine.count(), 2)

    def test_import_directory_ignores_non_markdown_files(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            (Path(temp_dir) / "valid.md").write_text("# Valid\n\nYes\n")
            (Path(temp_dir) / "invalid.txt").write_text("# Invalid\n\nNo\n")

            imported = engine.import_directory(Path(temp_dir))

            self.assertEqual(len(imported), 1)
            self.assertEqual(imported[0].title, "Valid")
            self.assertEqual(engine.count(), 1)


if __name__ == "__main__":
    unittest.main()
