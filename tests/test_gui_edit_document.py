import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow


class GuiEditDocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_editing_and_saving_updates_engine_and_ui(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nOriginal A.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            # select document
            window.document_list_widget.setCurrentRow(0)
            self.assertEqual(window.content_viewer.toPlainText(), "# A\n\nOriginal A.\n")

            # modify content
            window.content_viewer.setPlainText("# A\n\nModified A.\n")
            # simulate user typing triggers
            window._on_content_changed()
            self.assertTrue(window.save_button.isEnabled())

            # click save
            window.save_button.click()

            # save button disabled after saving
            self.assertFalse(window.save_button.isEnabled())

            # content reflected in engine
            docs = window.engine.list()
            self.assertEqual(docs[0].content, "# A\n\nModified A.\n")

            # file on disk updated
            disk = Path(temp_dir, "a.md").read_text()
            self.assertIn("Modified A", disk)

            # statistics updated
            stats = window.engine.stats()
            self.assertIn("documents", stats)


if __name__ == "__main__":
    unittest.main()
