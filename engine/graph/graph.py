from typing import Dict, List, Optional

from .edge import KnowledgeEdge
from .node import KnowledgeNode


class KnowledgeGraph:
    """Graph model for knowledge nodes and edges."""

    def __init__(self) -> None:
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._edges: List[KnowledgeEdge] = []

    def add_node(self, node: KnowledgeNode) -> None:
        """Add a node to the graph."""
        self._nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add an edge to the graph."""
        self._edges.append(edge)

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Return a node by its ID, or None if it does not exist."""
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[KnowledgeNode]:
        """Return a list of all nodes in the graph."""
        return list(self._nodes.values())

    def list_edges(self) -> List[KnowledgeEdge]:
        """Return a list of all edges in the graph."""
        return list(self._edges)
