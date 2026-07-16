import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow


class GuiImportTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_main_window_instantiates(self):
        window = MainWindow()
        self.assertIsNotNone(window)

    def test_main_window_contains_import_button(self):
        window = MainWindow()
        self.assertTrue(hasattr(window, "import_button"))
        self.assertEqual(window.import_button.text(), "Importar Vault")

    def test_main_window_contains_labels(self):
        window = MainWindow()
        self.assertTrue(hasattr(window, "title_label"))
        self.assertTrue(hasattr(window, "status_label"))
        self.assertEqual(window.title_label.text(), "Liceu Engine")
        self.assertEqual(window.status_label.text(), "Nenhum Vault carregado.")

    def test_document_list_starts_empty(self):
        window = MainWindow()
        self.assertTrue(hasattr(window, "document_list_widget"))
        self.assertEqual(window.document_list_widget.count(), 0)

    def test_viewer_starts_with_welcome_message(self):
        window = MainWindow()
        self.assertTrue(hasattr(window, "content_viewer"))
        self.assertEqual(window.content_viewer.toPlainText(), "Selecione um documento para visualizar.")

    def test_import_vault_updates_status_label(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "sample.md").write_text("# Sample\n\nContent\n")
            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            self.assertEqual(window.status_label.text(), "1 documentos importados.")
            self.assertEqual(window.engine.count(), 1)
            self.assertEqual(window.document_list_widget.count(), 1)
            self.assertEqual(window.document_list_widget.item(0).text(), "Sample")
            self.assertEqual(window.content_viewer.toPlainText(), "Selecione um documento para visualizar.")
            self.assertTrue(hasattr(window, "statistics_panel"))
            self.assertEqual(window.statistics_panel.documents_label.text(), "Documents: 1")
            self.assertEqual(window.statistics_panel.links_label.text(), "Links: 0")
            self.assertEqual(window.statistics_panel.orphans_label.text(), "Orphans: 1")

    def test_import_vault_populates_list_alphabetically(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "c.md").write_text("# C\n\nLink to [[A]].\n")
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            self.assertEqual(window.document_list_widget.count(), 3)
            titles = [window.document_list_widget.item(i).text() for i in range(3)]
            self.assertEqual(titles, ["A", "B", "C"])

    def test_selecting_document_displays_content(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            window.document_list_widget.setCurrentRow(1)
            self.assertEqual(window.content_viewer.toPlainText(), "# B\n\nContent B.\n")

    def test_related_documents_panel_updates(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            window.document_list_widget.setCurrentRow(0)
            self.assertEqual(window.related_list_widget.count(), 1)
            self.assertEqual(window.related_list_widget.item(0).text(), "B")

    def test_backlinks_panel_updates(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nLink to [[A]].\n")
            Path(temp_dir, "c.md").write_text("# C\n\nContent C.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            window.document_list_widget.setCurrentRow(0)
            self.assertEqual(window.backlinks_list_widget.count(), 1)
            self.assertEqual(window.backlinks_list_widget.item(0).text(), "B")

    def test_clicking_backlink_selects_and_displays(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nLink to [[A]].\n")
            Path(temp_dir, "c.md").write_text("# C\n\nContent C.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            window.document_list_widget.setCurrentRow(0)
            backlink_item = window.backlinks_list_widget.item(0)
            window.open_backlink_document(backlink_item)

            self.assertEqual(window.document_list_widget.currentItem().text(), "B")
            self.assertEqual(window.content_viewer.toPlainText(), "# B\n\nLink to [[A]].\n")
            self.assertEqual(window.related_list_widget.count(), 1)
            self.assertEqual(window.backlinks_list_widget.count(), 1)

    def test_clicking_backlink_shows_no_backlinks_when_none(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            window.document_list_widget.setCurrentRow(0)
            related_item = window.related_list_widget.item(0)
            window.open_related_document(related_item)

            self.assertEqual(window.document_list_widget.currentItem().text(), "B")
            self.assertEqual(window.content_viewer.toPlainText(), "# B\n\nContent B.\n")
            self.assertEqual(window.related_list_widget.count(), 1)
            self.assertEqual(window.related_list_widget.item(0).text(), "No related documents.")

    def test_search_filters_document_list(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")
            Path(temp_dir, "c.md").write_text("# C\n\nContent C.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            window.search_input.setText("b")
            self.assertEqual(window.document_list_widget.count(), 1)
            self.assertEqual(window.document_list_widget.item(0).text(), "B")

            window.search_input.setText("")
            self.assertEqual(window.document_list_widget.count(), 3)
            titles = [window.document_list_widget.item(i).text() for i in range(3)]
            self.assertEqual(titles, ["A", "B", "C"])

    def test_import_vault_cancel_keeps_status_label(self):
        window = MainWindow()
        initial_status = window.status_label.text()
        initial_viewer = window.content_viewer.toPlainText()
        with patch.object(QFileDialog, "getExistingDirectory", return_value=""):
            window.import_button.click()

        self.assertEqual(window.status_label.text(), initial_status)
        self.assertEqual(window.content_viewer.toPlainText(), initial_viewer)


if __name__ == "__main__":
    unittest.main()
