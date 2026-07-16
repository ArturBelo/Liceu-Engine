import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class RelatedGraphTestCase(unittest.TestCase):
    def test_build_graph_without_relations(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_a.write_text("# A\n\nContent A.\n")
            file_b.write_text("# B\n\nContent B.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            graph = engine.build_graph()

            self.assertEqual(len(graph.list_nodes()), 2)
            self.assertEqual(len(graph.list_edges()), 0)
            self.assertEqual(engine.related("A"), [])

    def test_related_single_relation(self):
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
            related = engine.related("A")
            self.assertEqual(len(related), 1)
            self.assertEqual(related[0].title, "B")

    def test_related_multiple_relations(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_c = Path(temp_dir) / "c.md"
            file_a.write_text("# A\n\nLinks to [[B]] and [[C]].\n")
            file_b.write_text("# B\n\nContent B.\n")
            file_c.write_text("# C\n\nContent C.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            engine.add_markdown(file_c)
            related = engine.related("A")

            self.assertEqual({item.title for item in related}, {"B", "C"})

    def test_related_title_not_found(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_a.write_text("# A\n\nContent A.\n")

            engine.add_markdown(file_a)
            self.assertEqual(engine.related("Unknown"), [])


if __name__ == "__main__":
    unittest.main()
