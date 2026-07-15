import unittest

from engine.core import Knowledge, KnowledgeRepository, KnowledgeService


class KnowledgeServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = KnowledgeRepository()
        self.service = KnowledgeService(self.repository)

    def test_create_knowledge(self) -> None:
        knowledge = self.service.create(
            title="Sample Title",
            content="Sample content",
            tags=["tag1", "tag2"],
        )

        self.assertIsInstance(knowledge, Knowledge)
        self.assertEqual(knowledge.title, "Sample Title")
        self.assertEqual(knowledge.content, "Sample content")
        self.assertEqual(knowledge.tags, ["tag1", "tag2"])
        self.assertEqual(self.repository.get(knowledge.id), knowledge)

    def test_list_knowledge(self) -> None:
        first = self.service.create("First", "First content")
        second = self.service.create("Second", "Second content")

        items = self.service.list()

        self.assertEqual(items, [first, second])

    def test_get_knowledge_by_id(self) -> None:
        knowledge = self.service.create("Title", "Content")

        result = self.service.get(knowledge.id)

        self.assertEqual(result, knowledge)

    def test_update_knowledge(self) -> None:
        knowledge = self.service.create("Old", "Old content", ["old"])

        updated = self.service.update(
            knowledge.id,
            title="New",
            content="New content",
            tags=["new"],
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, knowledge.id)
        self.assertEqual(updated.title, "New")
        self.assertEqual(updated.content, "New content")
        self.assertEqual(updated.tags, ["new"])
        self.assertGreater(updated.updated_at, knowledge.updated_at)
        self.assertEqual(self.repository.get(knowledge.id), updated)

    def test_delete_knowledge(self) -> None:
        knowledge = self.service.create("Title", "Content")

        result = self.service.delete(knowledge.id)

        self.assertTrue(result)
        self.assertIsNone(self.repository.get(knowledge.id))


if __name__ == "__main__":
    unittest.main()
