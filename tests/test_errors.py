import unittest

from engine.exceptions import (
    DatabaseError,
    EngineError,
    KnowledgeNotFoundError,
    RepositoryError,
    ValidationError,
)


class ErrorsTestCase(unittest.TestCase):
    def test_inheritance(self) -> None:
        self.assertTrue(issubclass(RepositoryError, EngineError))
        self.assertTrue(issubclass(DatabaseError, RepositoryError))
        self.assertTrue(issubclass(KnowledgeNotFoundError, RepositoryError))
        self.assertTrue(issubclass(ValidationError, EngineError))

    def test_capture_by_base_class(self) -> None:
        with self.assertRaises(EngineError):
            raise ValidationError("Invalid data")

        with self.assertRaises(RepositoryError):
            raise DatabaseError("DB failed")

    def test_capture_by_specific_class(self) -> None:
        with self.assertRaises(DatabaseError):
            raise DatabaseError("DB failed")

        with self.assertRaises(KnowledgeNotFoundError):
            raise KnowledgeNotFoundError("Missing knowlege")

    def test_isinstance_for_all_exceptions(self) -> None:
        self.assertIsInstance(EngineError("error"), EngineError)
        self.assertIsInstance(RepositoryError("error"), RepositoryError)
        self.assertIsInstance(DatabaseError("error"), DatabaseError)
        self.assertIsInstance(KnowledgeNotFoundError("error"), KnowledgeNotFoundError)
        self.assertIsInstance(ValidationError("error"), ValidationError)


if __name__ == "__main__":
    unittest.main()
