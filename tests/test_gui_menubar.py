import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from engine.gui.main_window import MainWindow


class GuiMenuBarTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_menu_actions_exist_and_connected(self):
        window = MainWindow()

        # find File menu
        file_menu_action = next((a for a in window.menuBar().actions() if a.text() == "File"), None)
        self.assertIsNotNone(file_menu_action)
        file_menu = file_menu_action.menu()
        action_texts = [a.text() for a in file_menu.actions() if a.text()]
        # check expected entries exist
        self.assertIn("New Document", action_texts)
        self.assertIn("Open Vault", action_texts)
        self.assertIn("Save", action_texts)
        self.assertIn("Exit", action_texts)

    def test_shortcuts_and_handlers_trigger(self):
        window = MainWindow()

        # patch handlers to observe calls
        with patch.object(window, 'handle_new_document') as new_mock, \
             patch.object(window, 'import_vault') as import_mock, \
             patch.object(window, 'handle_save_document') as save_mock:

            # trigger actions via menu
            file_menu_action = next((a for a in window.menuBar().actions() if a.text() == "File"), None)
            file_menu = file_menu_action.menu()

            new_action = next(a for a in file_menu.actions() if a.text() == "New Document")
            open_action = next(a for a in file_menu.actions() if a.text() == "Open Vault")
            save_action = next(a for a in file_menu.actions() if a.text() == "Save")

            # activating the actions should call the patched handlers
            new_action.trigger()
            open_action.trigger()
            save_action.trigger()

            new_mock.assert_called()
            import_mock.assert_called()
            save_mock.assert_called()

    def test_view_focus_actions(self):
        window = MainWindow()

        view_menu_action = next((a for a in window.menuBar().actions() if a.text() == "View"), None)
        self.assertIsNotNone(view_menu_action)
        view_menu = view_menu_action.menu()

        focus_search = next(a for a in view_menu.actions() if a.text() == "Focus Search")
        focus_list = next(a for a in view_menu.actions() if a.text() == "Focus Document List")
        focus_editor = next(a for a in view_menu.actions() if a.text() == "Focus Editor")

        # trigger and ensure no exceptions and the actions exist
        focus_search.trigger()
        focus_list.trigger()
        focus_editor.trigger()


if __name__ == "__main__":
    unittest.main()
