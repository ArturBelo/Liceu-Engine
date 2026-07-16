import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow


class StatisticsPanelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_statistics_panel_updates_after_import(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")
            Path(temp_dir, "c.md").write_text("# C\n\nContent C.\n")

            window = MainWindow()
            with patch.object(QFileDialog, "getExistingDirectory", return_value=temp_dir):
                window.import_button.click()

            self.assertEqual(window.statistics_panel.documents_label.text(), "Documents: 3")
            self.assertEqual(window.statistics_panel.links_label.text(), "Links: 1")
            self.assertEqual(window.statistics_panel.orphans_label.text(), "Orphans: 1")


if __name__ == "__main__":
    unittest.main()
