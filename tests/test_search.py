import tempfile
import unittest
from pathlib import Path

from engine.config import Settings
from engine.core import (
    Knowledge,
    KnowledgeRepository,
    KnowledgeService,
    SQLiteKnowledgeRepository,
)


class InMemorySearchTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = KnowledgeRepository()
        self.service = KnowledgeService(self.repository)
        self.repository.add(Knowledge(title="Python Basics", content="Learn the syntax."))
        self.repository.add(Knowledge(title="Advanced SQL", content="Search using LIKE."))
        self.repository.add(Knowledge(title="Testing Guide", content="Unit tests and assertions."))

    def test_search_by_title(self) -> None:
        results = self.repository.search("python")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Basics")

    def test_search_by_content(self) -> None:
        results = self.repository.search("assertions")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Testing Guide")

    def test_search_case_insensitive(self) -> None:
        results = self.repository.search("sql")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Advanced SQL")

    def test_search_returns_empty_list_when_not_found(self) -> None:
        results = self.repository.search("not found")

        self.assertEqual(results, [])

    def test_service_search_delegates_to_repository(self) -> None:
        results = self.service.search("testing")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Testing Guide")


class SQLiteSearchTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "search_test.db"
        settings = Settings(database_path=self.database_path)
        self.repository = SQLiteKnowledgeRepository(settings=settings)
        self.repository.add(Knowledge(title="Python Basics", content="Learn the syntax."))
        self.repository.add(Knowledge(title="Advanced SQL", content="Search using LIKE."))
        self.repository.add(Knowledge(title="Testing Guide", content="Unit tests and assertions."))

    def tearDown(self) -> None:
        try:
            self.repository._connection.close()
        except Exception:
            pass
        self.temp_dir.cleanup()

    def test_search_by_title(self) -> None:
        results = self.repository.search("python")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Basics")

    def test_search_by_content(self) -> None:
        results = self.repository.search("assertions")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Testing Guide")

    def test_search_case_insensitive(self) -> None:
        results = self.repository.search("sql")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Advanced SQL")

    def test_search_returns_empty_list_when_not_found(self) -> None:
        results = self.repository.search("not found")

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
