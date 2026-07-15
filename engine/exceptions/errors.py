class EngineError(Exception):
    """Base exception for all Liceu Engine errors."""


class RepositoryError(EngineError):
    """Raised when a repository operation fails."""


class DatabaseError(RepositoryError):
    """Raised when a database operation cannot be completed."""


class KnowledgeNotFoundError(RepositoryError):
    """Raised when a requested knowledge item does not exist."""


class ValidationError(EngineError):
    """Raised when input validation fails in the engine."""
