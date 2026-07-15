import unittest

from engine.graph import KnowledgeEdge, KnowledgeGraph, KnowledgeNode


class KnowledgeGraphTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = KnowledgeGraph()
        self.node_a = KnowledgeNode(id="a", title="Node A", knowledge="Content A")
        self.node_b = KnowledgeNode(id="b", title="Node B", knowledge="Content B")

    def test_add_nodes(self) -> None:
        self.graph.add_node(self.node_a)
        self.graph.add_node(self.node_b)

        self.assertEqual(self.graph.get_node("a"), self.node_a)
        self.assertEqual(self.graph.get_node("b"), self.node_b)

    def test_add_edges(self) -> None:
        self.graph.add_node(self.node_a)
        self.graph.add_node(self.node_b)
        edge = KnowledgeEdge(source="a", target="b", relation="related")

        self.graph.add_edge(edge)

        self.assertEqual(self.graph.list_edges(), [edge])

    def test_get_node_returns_none_for_missing(self) -> None:
        self.assertIsNone(self.graph.get_node("missing"))

    def test_list_nodes(self) -> None:
        self.graph.add_node(self.node_a)
        self.graph.add_node(self.node_b)

        self.assertEqual(self.graph.list_nodes(), [self.node_a, self.node_b])

    def test_list_edges(self) -> None:
        self.graph.add_node(self.node_a)
        self.graph.add_node(self.node_b)
        edge = KnowledgeEdge(source="a", target="b", relation="related")
        self.graph.add_edge(edge)

        self.assertEqual(self.graph.list_edges(), [edge])


if __name__ == "__main__":
    unittest.main()
