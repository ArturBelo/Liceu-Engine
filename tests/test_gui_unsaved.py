import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow
from engine.gui.utils import ConfirmResult


class GuiUnsavedProtectionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.window = MainWindow()

    def tearDown(self) -> None:
        try:
            self.window.close()
        except Exception:
            pass

    def test_select_another_document_no_edits(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                self.window.import_button.click()

            # select first then second
            self.window.document_list_widget.setCurrentRow(0)
            self.assertEqual(self.window.document_list_widget.currentRow(), 0)

            self.window.document_list_widget.setCurrentRow(1)
            self.assertEqual(self.window.document_list_widget.currentRow(), 1)

    def test_select_with_unsaved_shows_dialog_cancel(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                self.window.import_button.click()

            # select first
            self.window.document_list_widget.setCurrentRow(0)
            # mark as modified
            self.window.document_viewer.set_modified(True)

            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.CANCEL):
                # attempt to select second
                self.window.document_list_widget.setCurrentRow(1)
                # selection should be reverted
                self.assertEqual(self.window.document_list_widget.currentRow(), 0)

    def test_select_with_unsaved_save(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                self.window.import_button.click()

            self.window.document_list_widget.setCurrentRow(0)
            self.window.document_viewer.set_modified(True)

            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.SAVE), \
                 patch.object(MainWindow, 'handle_save_document', MagicMock(name='save')) as mock_save:
                self.window.document_list_widget.setCurrentRow(1)
                mock_save.assert_called()
                self.assertEqual(self.window.document_list_widget.currentRow(), 1)

    def test_select_with_unsaved_discard(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                self.window.import_button.click()

            self.window.document_list_widget.setCurrentRow(0)
            self.window.document_viewer.set_modified(True)

            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.DISCARD):
                self.window.document_list_widget.setCurrentRow(1)
                self.assertEqual(self.window.document_list_widget.currentRow(), 1)
                self.assertFalse(self.window.document_viewer.is_modified())

    def test_new_document_respects_unsaved(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                self.window.import_button.click()

            self.window.document_list_widget.setCurrentRow(0)
            self.window.document_viewer.set_modified(True)

            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.CANCEL):
                # NewDocumentDialog should not be shown
                with patch('engine.gui.widgets.NewDocumentDialog.get_document') as mock_dialog:
                    self.window.handle_new_document()
                    mock_dialog.assert_not_called()

            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.DISCARD), \
                 patch('engine.gui.widgets.NewDocumentDialog.get_document', return_value=("T","")):
                # now should open dialog and create
                self.window.handle_new_document()
                # list should contain new doc
                titles = [self.window.document_list_widget.item(i).text() for i in range(self.window.document_list_widget.count())]
                self.assertIn("T", titles)

    def test_import_vault_respects_unsaved(self):
        with TemporaryDirectory() as temp_dir1, TemporaryDirectory() as temp_dir2:
            Path(temp_dir1, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir2, "b.md").write_text("# B\n\nContent B.\n")

            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir1):
                self.window.import_button.click()

            self.window.document_list_widget.setCurrentRow(0)
            self.window.document_viewer.set_modified(True)

            # CANCEL should abort opening new vault
            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.CANCEL), \
                 patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir2) as get_dir_mock:
                self.window.import_vault()
                # file dialog not called because we aborted
                # (import_vault calls confirm before showing dialog)
                # ensure currently still using first vault's list
                titles = [self.window.document_list_widget.item(i).text() for i in range(self.window.document_list_widget.count())]
                self.assertIn("A", titles)

            # DISCARD should proceed and import new vault
            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.DISCARD), \
                 patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir2):
                self.window.import_vault()
                titles = [self.window.document_list_widget.item(i).text() for i in range(self.window.document_list_widget.count())]
                self.assertIn("B", titles)

    def test_close_event_respects_unsaved(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                self.window.import_button.click()

            self.window.document_list_widget.setCurrentRow(0)
            self.window.document_viewer.set_modified(True)

            # ensure window is visible for close tests
            self.window.show()

            # CANCEL -> window remains visible
            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.CANCEL):
                self.window.close()
                self.assertTrue(self.window.isVisible())

            # DISCARD -> window closes
            with patch('engine.gui.utils.confirm_unsaved_changes', return_value=ConfirmResult.DISCARD):
                # show again to close
                self.window.show()
                self.window.close()
                self.assertFalse(self.window.isVisible())


if __name__ == "__main__":
    unittest.main()
