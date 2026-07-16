import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class AnalyzerTestCase(unittest.TestCase):
    def test_document_count(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            engine.add_markdown(Path(temp_dir, "a.md"))
            engine.add_markdown(Path(temp_dir, "b.md"))
            stats = engine.stats()

            self.assertEqual(stats["documents"], 2)

    def test_link_count(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_a.write_text("# A\n\nLink to [[B]].\n")
            file_b.write_text("# B\n\nContent B.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            stats = engine.stats()

            self.assertEqual(stats["links"], 1)

    def test_orphan_count(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_c = Path(temp_dir) / "c.md"
            file_a.write_text("# A\n\nLink to [[B]].\n")
            file_b.write_text("# B\n\nContent B.\n")
            file_c.write_text("# C\n\nContent C.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            engine.add_markdown(file_c)
            stats = engine.stats()

            self.assertEqual(stats["orphans"], 1)

    def test_stats_consistency_with_graph(self):
        with TemporaryDirectory() as temp_dir:
            engine = LiceuEngine()
            file_a = Path(temp_dir) / "a.md"
            file_b = Path(temp_dir) / "b.md"
            file_a.write_text("# A\n\nLink to [[B]].\n")
            file_b.write_text("# B\n\nContent B.\n")

            engine.add_markdown(file_a)
            engine.add_markdown(file_b)
            graph = engine.build_graph()
            stats = engine.stats()

            self.assertEqual(stats["documents"], len(engine.list()))
            self.assertEqual(stats["links"], len(graph.list_edges()))
            self.assertEqual(stats["orphans"], 0)


if __name__ == "__main__":
    unittest.main()
