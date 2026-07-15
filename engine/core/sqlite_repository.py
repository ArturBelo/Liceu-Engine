import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from ..config import Settings
from .interfaces import IKnowledgeRepository
from .knowledge import Knowledge


class SQLiteKnowledgeRepository(IKnowledgeRepository):
    """SQLite implementation of the Knowledge repository."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or Settings()
        self._database_path: Path = self._settings.database_path
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(
            self._database_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self._connection.row_factory = sqlite3.Row
        self._ensure_table()

    def _ensure_table(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def _row_to_knowledge(self, row: sqlite3.Row) -> Knowledge:
        return Knowledge(
            id=UUID(row["id"]),
            title=row["title"],
            content=row["content"],
            tags=json.loads(row["tags"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def add(self, knowledge: Knowledge) -> None:
        self._connection.execute(
            "INSERT INTO knowledge (id, title, content, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(knowledge.id),
                knowledge.title,
                knowledge.content,
                json.dumps(knowledge.tags),
                knowledge.created_at.isoformat(),
                knowledge.updated_at.isoformat(),
            ),
        )
        self._connection.commit()

    def get(self, id: UUID) -> Knowledge | None:
        cursor = self._connection.execute(
            "SELECT * FROM knowledge WHERE id = ?",
            (str(id),),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_knowledge(row)

    def list(
        self,
        limit: int | None = None,
        offset: int = 0,
        order_by: str = "created_at",
        descending: bool = False,
    ) -> list[Knowledge]:
        valid_order_fields = {"created_at", "updated_at", "title"}
        if order_by not in valid_order_fields:
            order_by = "created_at"

        order_direction = "DESC" if descending else "ASC"
        query = f"SELECT * FROM knowledge ORDER BY {order_by} {order_direction}"

        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params = (limit, max(offset, 0))
        else:
            query += " LIMIT -1 OFFSET ?"
            params = (max(offset, 0),)

        cursor = self._connection.execute(query, params)
        return [self._row_to_knowledge(row) for row in cursor.fetchall()]

    def remove(self, id: UUID) -> bool:
        cursor = self._connection.execute(
            "DELETE FROM knowledge WHERE id = ?",
            (str(id),),
        )
        self._connection.commit()
        return cursor.rowcount > 0

    def update(self, knowledge: Knowledge) -> bool:
        cursor = self._connection.execute(
            """
            UPDATE knowledge
            SET title = ?, content = ?, tags = ?, created_at = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                knowledge.title,
                knowledge.content,
                json.dumps(knowledge.tags),
                knowledge.created_at.isoformat(),
                knowledge.updated_at.isoformat(),
                str(knowledge.id),
            ),
        )
        self._connection.commit()
        return cursor.rowcount > 0

    def search(self, query: str) -> list[Knowledge]:
        query_text = f"%{query}%"
        cursor = self._connection.execute(
            """
            SELECT * FROM knowledge
            WHERE title LIKE ? COLLATE NOCASE
               OR content LIKE ? COLLATE NOCASE
            ORDER BY created_at ASC
            """,
            (query_text, query_text),
        )
        return [self._row_to_knowledge(row) for row in cursor.fetchall()]

    def __del__(self) -> None:
        try:
            self._connection.close()
        except Exception:
            pass
