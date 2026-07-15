import unittest
from datetime import datetime
from uuid import UUID

from engine.core import Knowledge


class KnowledgeTestCase(unittest.TestCase):
    def test_knowledge_creation(self):
        knowledge = Knowledge(title="Sample Title", content="Sample content")

        self.assertIsInstance(knowledge.id, UUID)
        self.assertEqual(knowledge.title, "Sample Title")
        self.assertEqual(knowledge.content, "Sample content")
        self.assertIsInstance(knowledge.created_at, datetime)
        self.assertIsInstance(knowledge.updated_at, datetime)
        self.assertEqual(knowledge.tags, [])


if __name__ == "__main__":
    unittest.main()
