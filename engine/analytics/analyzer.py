from engine.core import KnowledgeRepository
from engine.graph import KnowledgeGraph


class VaultAnalyzer:
    """Analyze the knowledge vault using repository and graph structures."""

    def __init__(self, repository: KnowledgeRepository, graph: KnowledgeGraph) -> None:
        self._repository = repository
        self._graph = graph

    def document_count(self) -> int:
        """Return the number of documents in the repository."""
        return len(self._repository.list())

    def link_count(self) -> int:
        """Return the total number of wiki links represented in the graph."""
        return len(self._graph.list_edges())

    def orphan_count(self) -> int:
        """Return the number of documents with no outgoing and no incoming links."""
        orphan_count = 0
        for knowledge in self._repository.list():
            if knowledge.wikilinks:
                continue
            incoming = self._graph.incoming_neighbors(str(knowledge.id))
            if not incoming:
                orphan_count += 1
        return orphan_count
