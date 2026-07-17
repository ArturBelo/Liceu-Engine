import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QFileDialog

from engine.gui.main_window import MainWindow


class GuiGraphTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_graph_window_opens_and_contains_nodes_edges(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            window = MainWindow()
            with patch.object(QFileDialog, 'getExistingDirectory', return_value=temp_dir):
                window.import_button.click()

            # open graph window
            window._open_graph_window()
            gw = window._graph_window
            self.assertTrue(hasattr(gw, 'scene'))

            # nodes should be present
            self.assertTrue(len(gw.node_items) >= 2)
            # edges should be present
            self.assertTrue(len(gw.edge_items) >= 1)

            # selecting a node by double-click should open document (simulate)
            # pick first node
            node_id = next(iter(gw.node_items.keys()))
            # simulate double click
            gw.open_document_by_node(node_id)
            # check that main window selection changed
            docs = window._documents
            titles = [d.title for d in docs]
            self.assertIn(window.document_list_widget.currentItem().text(), titles)


if __name__ == "__main__":
    unittest.main()
