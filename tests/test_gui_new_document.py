import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow


class GuiNewDocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_new_document_dialog_creates_and_selects(self):
        with TemporaryDirectory() as temp_dir:
            window = MainWindow()
            # set vault path
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            with patch("engine.gui.widgets.new_document_dialog.NewDocumentDialog.get_document", return_value=("My Note", "# My Note\n\nBody")):
                window.new_button.click()

            # verify created and selected
            self.assertEqual(window.document_list_widget.currentItem().text(), "My Note")
            self.assertEqual(window.content_viewer.toPlainText(), "# My Note\n\nBody")
            self.assertEqual(window.statistics_panel.documents_label.text(), "Documents: 1")

    def test_new_document_cancel_does_nothing(self):
        window = MainWindow()
        with patch("engine.gui.widgets.new_document_dialog.NewDocumentDialog.get_document", return_value=(None, None)):
            window.new_button.click()

        self.assertEqual(window.document_list_widget.count(), 0)


if __name__ == "__main__":
    unittest.main()
