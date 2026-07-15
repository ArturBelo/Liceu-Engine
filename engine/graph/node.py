from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeNode:
    """Represents a node in the knowledge graph."""

    id: str
    title: str
    knowledge: str
