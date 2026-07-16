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

    def neighbors(self, node_id: str) -> List[KnowledgeNode]:
        """Return all nodes directly connected by outgoing edges from the given node."""
        if self.get_node(node_id) is None:
            return []

        neighbors: list[KnowledgeNode] = []
        for edge in self._edges:
            if edge.source == node_id:
                neighbor = self.get_node(edge.target)
                if neighbor is not None:
                    neighbors.append(neighbor)
        return neighbors

    def incoming_neighbors(self, node_id: str) -> List[KnowledgeNode]:
        """Return all nodes that point to the given node via incoming edges."""
        if self.get_node(node_id) is None:
            return []

        neighbors: list[KnowledgeNode] = []
        for edge in self._edges:
            if edge.target == node_id:
                neighbor = self.get_node(edge.source)
                if neighbor is not None:
                    neighbors.append(neighbor)
        return neighbors
