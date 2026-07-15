import unittest

from engine.core import Knowledge
from engine.graph import GraphBuilder, KnowledgeEdge, KnowledgeNode


class GraphBuilderTestCase(unittest.TestCase):
    def test_add_nodes(self) -> None:
        knowledge_a = Knowledge(title="A", content="Content A")
        knowledge_b = Knowledge(title="B", content="Content B")

        graph = GraphBuilder([knowledge_a, knowledge_b]).build()

        self.assertEqual(graph.get_node(str(knowledge_a.id)), KnowledgeNode(id=str(knowledge_a.id), title="A", knowledge="Content A"))
        self.assertEqual(graph.get_node(str(knowledge_b.id)), KnowledgeNode(id=str(knowledge_b.id), title="B", knowledge="Content B"))

    def test_add_edges(self) -> None:
        knowledge_a = Knowledge(title="A", content="See B", wikilinks=["B"])
        knowledge_b = Knowledge(title="B", content="Content B")

        graph = GraphBuilder([knowledge_a, knowledge_b]).build()

        self.assertEqual(graph.list_edges(), [KnowledgeEdge(source=str(knowledge_a.id), target=str(knowledge_b.id), relation="wikilink")])

    def test_ignore_nonexistent_links(self) -> None:
        knowledge_a = Knowledge(title="A", content="See Missing", wikilinks=["Missing"])
        knowledge_b = Knowledge(title="B", content="Content B")

        graph = GraphBuilder([knowledge_a, knowledge_b]).build()

        self.assertEqual(graph.list_edges(), [])

    def test_documents_without_links(self) -> None:
        knowledge_a = Knowledge(title="A", content="No links")
        knowledge_b = Knowledge(title="B", content="Also no links")

        graph = GraphBuilder([knowledge_a, knowledge_b]).build()

        self.assertEqual(graph.list_edges(), [])


if __name__ == "__main__":
    unittest.main()
