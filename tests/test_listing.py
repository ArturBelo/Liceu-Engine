import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from engine.config import Settings
from engine.core import (
    Knowledge,
    KnowledgeRepository,
    KnowledgeService,
    SQLiteKnowledgeRepository,
)


class ListingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = KnowledgeRepository()
        self.service = KnowledgeService(self.repository)

        self.first = Knowledge(
            title="Alpha",
            content="First content",
            created_at=datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 2, 0, 0, tzinfo=timezone.utc),
        )
        self.second = Knowledge(
            title="Beta",
            content="Second content",
            created_at=datetime(2024, 1, 3, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 4, 0, 0, tzinfo=timezone.utc),
        )
        self.third = Knowledge(
            title="Gamma",
            content="Third content",
            created_at=datetime(2024, 1, 5, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 6, 0, 0, tzinfo=timezone.utc),
        )

        self.repository.add(self.first)
        self.repository.add(self.second)
        self.repository.add(self.third)

    def test_order_by_created_at(self) -> None:
        results = self.repository.list(order_by="created_at")

        self.assertEqual(results, [self.first, self.second, self.third])

    def test_order_by_updated_at(self) -> None:
        results = self.repository.list(order_by="updated_at")

        self.assertEqual(results, [self.first, self.second, self.third])

    def test_order_by_title(self) -> None:
        results = self.repository.list(order_by="title")

        self.assertEqual(results, [self.first, self.second, self.third])

    def test_descending(self) -> None:
        results = self.repository.list(order_by="created_at", descending=True)

        self.assertEqual(results, [self.third, self.second, self.first])

    def test_limit(self) -> None:
        results = self.repository.list(limit=2)

        self.assertEqual(results, [self.first, self.second])

    def test_offset(self) -> None:
        results = self.repository.list(offset=1)

        self.assertEqual(results, [self.second, self.third])

    def test_limit_and_offset(self) -> None:
        results = self.repository.list(limit=1, offset=1)

        self.assertEqual(results, [self.second])

    def test_invalid_order_by_uses_created_at(self) -> None:
        results = self.repository.list(order_by="invalid")

        self.assertEqual(results, [self.first, self.second, self.third])

    def test_service_list_delegates(self) -> None:
        results = self.service.list(limit=2, offset=1, order_by="created_at")
        self.assertEqual(results, [self.second, self.third])


class SQLiteListingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "listing_test.db"
        settings = Settings(database_path=self.database_path)
        self.repository = SQLiteKnowledgeRepository(settings=settings)

        self.first = Knowledge(
            title="Alpha",
            content="First content",
            created_at=datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 2, 0, 0, tzinfo=timezone.utc),
        )
        self.second = Knowledge(
            title="Beta",
            content="Second content",
            created_at=datetime(2024, 1, 3, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 4, 0, 0, tzinfo=timezone.utc),
        )
        self.third = Knowledge(
            title="Gamma",
            content="Third content",
            created_at=datetime(2024, 1, 5, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 6, 0, 0, tzinfo=timezone.utc),
        )

        self.repository.add(self.first)
        self.repository.add(self.second)
        self.repository.add(self.third)

    def tearDown(self) -> None:
        try:
            self.repository._connection.close()
        except Exception:
            pass
        self.temp_dir.cleanup()

    def test_order_by_created_at(self) -> None:
        results = self.repository.list(order_by="created_at")
        self.assertEqual([item.id for item in results], [self.first.id, self.second.id, self.third.id])

    def test_order_by_updated_at(self) -> None:
        results = self.repository.list(order_by="updated_at")
        self.assertEqual([item.id for item in results], [self.first.id, self.second.id, self.third.id])

    def test_order_by_title(self) -> None:
        results = self.repository.list(order_by="title")
        self.assertEqual([item.id for item in results], [self.first.id, self.second.id, self.third.id])

    def test_descending(self) -> None:
        results = self.repository.list(order_by="created_at", descending=True)
        self.assertEqual([item.id for item in results], [self.third.id, self.second.id, self.first.id])

    def test_limit(self) -> None:
        results = self.repository.list(limit=2)
        self.assertEqual([item.id for item in results], [self.first.id, self.second.id])

    def test_offset(self) -> None:
        results = self.repository.list(offset=1)
        self.assertEqual([item.id for item in results], [self.second.id, self.third.id])

    def test_limit_and_offset(self) -> None:
        results = self.repository.list(limit=1, offset=1)
        self.assertEqual([item.id for item in results], [self.second.id])

    def test_invalid_order_by_uses_created_at(self) -> None:
        results = self.repository.list(order_by="invalid")
        self.assertEqual([item.id for item in results], [self.first.id, self.second.id, self.third.id])


if __name__ == "__main__":
    unittest.main()
