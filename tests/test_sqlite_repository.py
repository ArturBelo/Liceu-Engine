import sqlite3
import tempfile
import unittest
from pathlib import Path
from uuid import UUID

from engine.config import Settings
from engine.core import Knowledge, SQLiteKnowledgeRepository


class SQLiteKnowledgeRepositoryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test_engine.db"
        settings = Settings(database_path=self.database_path)
        self.repository = SQLiteKnowledgeRepository(settings=settings)

    def tearDown(self) -> None:
        self.repository._connection.close()
        self.temp_dir.cleanup()

    def test_add_and_get(self) -> None:
        knowledge = Knowledge(title="Title", content="Content", tags=["tag"])
        self.repository.add(knowledge)

        loaded = self.repository.get(knowledge.id)

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.id, knowledge.id)
        self.assertEqual(loaded.title, "Title")
        self.assertEqual(loaded.content, "Content")
        self.assertEqual(loaded.tags, ["tag"])
        self.assertEqual(loaded.created_at, knowledge.created_at)
        self.assertEqual(loaded.updated_at, knowledge.updated_at)

    def test_list(self) -> None:
        first = Knowledge(title="First", content="First content")
        second = Knowledge(title="Second", content="Second content")
        self.repository.add(first)
        self.repository.add(second)

        items = self.repository.list()

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].id, first.id)
        self.assertEqual(items[1].id, second.id)

    def test_update(self) -> None:
        knowledge = Knowledge(title="Old", content="Old content", tags=["old"])
        self.repository.add(knowledge)

        updated = Knowledge(
            id=knowledge.id,
            title="New",
            content="New content",
            tags=["new"],
            created_at=knowledge.created_at,
            updated_at=knowledge.updated_at,
        )
        updated = updated.__class__(
            id=knowledge.id,
            title="New",
            content="New content",
            tags=["new"],
            created_at=knowledge.created_at,
            updated_at=knowledge.updated_at,
        )

        success = self.repository.update(updated)
        loaded = self.repository.get(knowledge.id)

        self.assertTrue(success)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.title, "New")
        self.assertEqual(loaded.content, "New content")
        self.assertEqual(loaded.tags, ["new"])

    def test_remove(self) -> None:
        knowledge = Knowledge(title="Title", content="Content")
        self.repository.add(knowledge)

        removed = self.repository.remove(knowledge.id)
        loaded = self.repository.get(knowledge.id)

        self.assertTrue(removed)
        self.assertIsNone(loaded)

    def test_remove_nonexistent_returns_false(self) -> None:
        removed = self.repository.remove(UUID(int=0))

        self.assertFalse(removed)

    def test_update_nonexistent_returns_false(self) -> None:
        knowledge = Knowledge(title="New", content="New content")

        self.assertFalse(self.repository.update(knowledge))

    def test_database_file_created(self) -> None:
        self.assertTrue(self.database_path.exists())
        conn = sqlite3.connect(self.database_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge'")
        row = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(row)
