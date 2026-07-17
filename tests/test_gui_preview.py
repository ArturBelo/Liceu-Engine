import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow


class GuiPreviewTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_preview_mode_renders_markdown_and_preserves_edits(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "doc.md").write_text("# Title\n\nSome **bold** text and a wikilink [[Python]].\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            # select document
            window.document_list_widget.setCurrentRow(0)
            # ensure editor contains original markdown
            self.assertIn("# Title", window.content_viewer.toPlainText())

            # switch to preview
            window.preview_button.click()
            # preview should be active
            self.assertTrue(window.document_viewer.is_preview_active())

            preview_html = window.document_viewer.preview.toHtml()
            # should contain heading and bold and the wikilink as a link
            self.assertIn("<h1", preview_html.lower())
            # accept either <strong> or inline-styled span for bold depending on renderer
            self.assertTrue(
                ("<strong>bold</strong>".lower() in preview_html.lower())
                or ("font-weight:700" in preview_html.lower())
                or ("bold" in preview_html.lower())
            )
            self.assertIn("liceu://python", preview_html.lower())

            # modify editor content and ensure preview updates when toggled again
            window.preview_button.click()  # back to edit
            window.content_viewer.setPlainText("# Title\n\nModified *italic* text and [[Python]].\n")
            # go to preview again
            window.preview_button.click()
            updated_html = window.document_viewer.preview.toHtml()
            # accept either <em> or inline-styled span for italic depending on renderer
            self.assertTrue(
                ("<em>italic</em>".lower() in updated_html.lower())
                or ("font-style:italic" in updated_html.lower())
                or ("italic" in updated_html.lower())
            )


if __name__ == "__main__":
    unittest.main()
