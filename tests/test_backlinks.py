import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class BacklinksTestCase(unittest.TestCase):
    def test_backlinks_without_backlinks(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_a.write_text("# A\n\nContent A.\n")

            engine.add_markdown(file_a)
            self.assertEqual(engine.backlinks("A"), [])

    def test_backlinks_single_backlink(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_a.write_text("# A\n\nLink to [[B]].\n")
            file_b.write_text("# B\n\nContent B.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            backlinks = engine.backlinks("B")

            self.assertEqual(len(backlinks), 1)
            self.assertEqual(backlinks[0].title, "A")

    def test_backlinks_multiple_backlinks(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_c = Path(temp_dir) / "c.md"
            file_a.write_text("# A\n\nLink to [[C]].\n")
            file_b.write_text("# B\n\nLink to [[C]].\n")
            file_c.write_text("# C\n\nContent C.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            engine.add_markdown(file_c)
            backlinks = engine.backlinks("C")

            self.assertEqual({item.title for item in backlinks}, {"A", "B"})

    def test_backlinks_title_not_found(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_a.write_text("# A\n\nContent A.\n")

            engine.add_markdown(file_a)
            self.assertEqual(engine.backlinks("Unknown"), [])

    def test_backlinks_consistency_with_build_graph(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_a.write_text("# A\n\nLink to [[B]].\n")
            file_b.write_text("# B\n\nContent B.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            graph = engine.build_graph()

            self.assertEqual(len(graph.list_nodes()), 2)
            self.assertEqual(len(graph.list_edges()), 1)
            backlinks = engine.backlinks("B")
            self.assertEqual(len(backlinks), 1)
            self.assertEqual(backlinks[0].title, "A")


if __name__ == "__main__":
    unittest.main()
