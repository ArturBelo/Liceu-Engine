from pathlib import Path
from uuid import UUID

from engine.analytics import VaultAnalyzer
from engine.core import KnowledgeFactory, KnowledgeRepository, KnowledgeService
from engine.graph import GraphBuilder
from engine.parsers import MarkdownParser


class LiceuEngine:
    """Facade for the Liceu Engine public API."""

    def __init__(self) -> None:
        self._repository = KnowledgeRepository()
        self._service = KnowledgeService(self._repository)
        self._graph = None
        self._vault_path: Path | None = None

    def add_markdown(self, path: Path):
        """Parse a Markdown file and add it to the knowledge repository."""
        document = MarkdownParser(path).parse()
        knowledge = KnowledgeFactory.from_markdown(document)
        return self._service.create(
            title=knowledge.title,
            content=knowledge.content,
            tags=knowledge.tags,
            headings=knowledge.headings,
            wikilinks=knowledge.wikilinks,
            metadata=knowledge.metadata,
        )

    def build_graph(self):
        """Build and store a KnowledgeGraph for the current knowledge items."""
        self._graph = GraphBuilder(self._service.list()).build()
        return self._graph

    def related(self, title: str):
        """Return knowledge items related to the given title via graph edges."""
        knowledges = self._service.list()
        target_knowledge = next((item for item in knowledges if item.title == title), None)
        if target_knowledge is None:
            return []

        if self._graph is None:
            self.build_graph()

        neighbors = self._graph.neighbors(str(target_knowledge.id))
        related_knowledges = []
        for node in neighbors:
            knowledge = self._repository.get(UUID(node.id))
            if knowledge is not None:
                related_knowledges.append(knowledge)
        return related_knowledges

    def backlinks(self, title: str):
        """Return knowledge items that link to the given title via graph edges."""
        knowledges = self._service.list()
        target_knowledge = next((item for item in knowledges if item.title == title), None)
        if target_knowledge is None:
            return []

        if self._graph is None:
            self.build_graph()

        neighbors = self._graph.incoming_neighbors(str(target_knowledge.id))
        backlinks = []
        for node in neighbors:
            knowledge = self._repository.get(UUID(node.id))
            if knowledge is not None:
                backlinks.append(knowledge)
        return backlinks

    def stats(self):
        """Return vault statistics computed by the analyzer."""
        if self._graph is None:
            self.build_graph()

        analyzer = VaultAnalyzer(self._repository, self._graph)
        return {
            "documents": analyzer.document_count(),
            "links": analyzer.link_count(),
            "orphans": analyzer.orphan_count(),
        }

    def create_document(self, title: str, content: str = ""):
        """Create a new Markdown document inside the currently opened vault.

        The new file name is derived from the title. The file is created on disk inside
        the last imported vault, then the existing import flow is used to parse and
        store the knowledge entity.
        """
        if not self._vault_path:
            from engine.exceptions.errors import ValidationError

            raise ValidationError("No vault is currently opened. Import a vault first.")

        # create a safe filename from the title
        safe = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in title).strip()
        safe = safe.replace(" ", "_") or "untitled"
        file_path = self._vault_path / f"{safe}.md"

        # avoid overwriting existing files: append a suffix if needed
        counter = 1
        base = safe
        while file_path.exists():
            file_path = self._vault_path / f"{base}-{counter}.md"
            counter += 1

        # write content
        file_path.write_text(content)

        # reuse add_markdown to parse and persist
        new_knowledge = self.add_markdown(file_path)

        # synchronize the graph after creating new knowledge
        try:
            self.build_graph()
        except Exception:
            # graph sync should not break creation — fail silently but could be logged
            pass

        return new_knowledge

    def update_document(self, title: str, content: str):
        """Update an existing Markdown document identified by title.

        Finds the corresponding file in the currently opened vault by parsing files
        and matching the produced title, overwrites its content, reparses and
        updates the repository via the service update flow.
        """
        if not self._vault_path:
            from engine.exceptions.errors import ValidationError

            raise ValidationError("No vault is currently opened. Import a vault first.")

        from engine.exceptions.errors import KnowledgeNotFoundError
        from engine.parsers import MarkdownParser
        from engine.core import KnowledgeFactory

        # find existing knowledge in repository
        existing = next((k for k in self._service.list() if k.title == title), None)
        if existing is None:
            raise KnowledgeNotFoundError(f"Knowledge with title '{title}' not found in repository")

        # search for the file in the vault that parses to the same title
        target_path = None
        for file in sorted(self._vault_path.rglob("*.md"), key=lambda p: str(p)):
            try:
                doc = MarkdownParser(file).parse()
            except Exception:
                continue
            k = KnowledgeFactory.from_markdown(doc)
            if k.title == title:
                target_path = file
                break

        if target_path is None:
            raise KnowledgeNotFoundError(f"Source Markdown file for '{title}' not found in vault")

        # overwrite file
        target_path.write_text(content)

        # reparse and update repository via service update
        new_doc = MarkdownParser(target_path).parse()
        new_k = KnowledgeFactory.from_markdown(new_doc)

        updated = self._service.update(
            existing.id,
            new_k.title,
            new_k.content,
            new_k.tags,
            headings=new_k.headings,
            wikilinks=new_k.wikilinks,
        )

        # synchronize the graph after updating knowledge
        try:
            self.build_graph()
        except Exception:
            # do not break the update flow if graph rebuild fails
            pass

        return updated

    def import_directory(self, path: Path):
        """Import all Markdown files from a directory recursively."""
        directory = Path(path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")
        if not directory.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")

        # remember the opened vault path
        self._vault_path = directory

        markdown_files = sorted(
            [file for file in directory.rglob("*") if file.is_file() and file.suffix.lower() == ".md"],
            key=lambda file: str(file),
        )

        imported = []
        for markdown_file in markdown_files:
            imported.append(self.add_markdown(markdown_file))

        return imported

    def list(self, limit: int | None = None, offset: int = 0, order_by: str = "created_at", descending: bool = False):
        """List knowledge items from the repository."""
        return self._service.list(limit=limit, offset=offset, order_by=order_by, descending=descending)

    def search(self, query: str):
        """Search knowledge items by query text."""
        return self._service.search(query)

    def count(self) -> int:
        """Return the number of knowledge items stored."""
        return len(self._service.list())
