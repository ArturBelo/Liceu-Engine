import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from engine import LiceuEngine


class EngineGraphSyncTestCase(unittest.TestCase):
    def test_create_document_triggers_graph_update(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nContent A.\n")
            Path(temp_dir, "b.md").write_text("# B\n\nLink to [[A]].\n")

            engine = LiceuEngine()
            engine.import_directory(Path(temp_dir))

            # ensure initial backlinks
            backlinks = engine.backlinks("A")
            self.assertEqual(len(backlinks), 1)
            self.assertEqual(backlinks[0].title, "B")

            # create new document C linking to A
            engine.create_document("C", "# C\n\nLink to [[A]].\n")

            # after create, graph should be updated and backlinks should include C
            backlinks_after = engine.backlinks("A")
            titles = sorted([k.title for k in backlinks_after])
            self.assertIn("C", titles)

    def test_update_document_triggers_graph_update(self):
        with TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.md").write_text("# A\n\nLink to [[B]].\n")
            Path(temp_dir, "b.md").write_text("# B\n\nContent B.\n")

            engine = LiceuEngine()
            engine.import_directory(Path(temp_dir))

            # initial related from A should include B
            related = engine.related("A")
            self.assertEqual(len(related), 1)
            self.assertEqual(related[0].title, "B")

            # update A to remove link
            engine.update_document("A", "# A\n\nNo links.\n")

            # graph should be updated: related from A empty, backlinks for B empty
            related_after = engine.related("A")
            self.assertEqual(len(related_after), 0)

            backlinks_b = engine.backlinks("B")
            self.assertEqual(len(backlinks_b), 0)


if __name__ == "__main__":
    unittest.main()
