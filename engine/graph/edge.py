from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeEdge:
    """Represents a directional relationship between two knowledge nodes."""

    source: str
    target: str
    relation: str
