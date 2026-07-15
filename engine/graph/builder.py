from engine.core import Knowledge
from .edge import KnowledgeEdge
from .graph import KnowledgeGraph
from .node import KnowledgeNode


class GraphBuilder:
    """Builds a knowledge graph from a list of Knowledge entities."""

    def __init__(self, knowledges: list[Knowledge]) -> None:
        self._knowledges = knowledges

    def build(self) -> KnowledgeGraph:
        graph = KnowledgeGraph()
        title_to_id: dict[str, str] = {}

        for knowledge in self._knowledges:
            node = KnowledgeNode(
                id=str(knowledge.id),
                title=knowledge.title,
                knowledge=knowledge.content,
            )
            graph.add_node(node)
            if knowledge.title not in title_to_id:
                title_to_id[knowledge.title] = node.id

        for knowledge in self._knowledges:
            source_id = str(knowledge.id)
            for target_title in knowledge.wikilinks:
                target_id = title_to_id.get(target_title)
                if target_id is None:
                    continue
                graph.add_edge(
                    KnowledgeEdge(source=source_id, target=target_id, relation="wikilink")
                )

        return graph
