import tempfile
import unittest
from pathlib import Path

from engine.core import KnowledgeFactory
from engine.parsers import MarkdownDocument


class KnowledgeFactoryTestCase(unittest.TestCase):
    def test_title_from_front_matter(self) -> None:
        path = Path("/tmp/doc.md")
        document = MarkdownDocument(
            path=path,
            content="# Heading\nContent",
            front_matter={"title": "Front Title", "tags": ["tag1"]},
            headings=["Heading"],
            wikilinks=["Python"],
        )

        knowledge = KnowledgeFactory.from_markdown(document)

        self.assertEqual(knowledge.title, "Front Title")
        self.assertEqual(knowledge.metadata, {"title": "Front Title", "tags": ["tag1"]})
        self.assertEqual(knowledge.headings, ["Heading"])
        self.assertEqual(knowledge.wikilinks, ["Python"])
        self.assertEqual(knowledge.tags, [])

    def test_title_from_first_heading(self) -> None:
        path = Path("/tmp/doc.md")
        document = MarkdownDocument(
            path=path,
            content="# Heading\nContent",
            front_matter=None,
            headings=["Heading"],
            wikilinks=["Python"],
        )

        knowledge = KnowledgeFactory.from_markdown(document)

        self.assertEqual(knowledge.title, "Heading")
        self.assertEqual(knowledge.metadata, {})
        self.assertEqual(knowledge.headings, ["Heading"])
        self.assertEqual(knowledge.wikilinks, ["Python"])

    def test_title_from_filename_when_no_heading(self) -> None:
        path = Path("/tmp/document.md")
        document = MarkdownDocument(
            path=path,
            content="Content without heading",
            front_matter=None,
            headings=[],
            wikilinks=[],
        )

        knowledge = KnowledgeFactory.from_markdown(document)

        self.assertEqual(knowledge.title, "document")
        self.assertEqual(knowledge.metadata, {})

    def test_tags_and_metadata_preserved(self) -> None:
        path = Path("/tmp/doc.md")
        document = MarkdownDocument(
            path=path,
            content="# Heading\nContent",
            front_matter={"category": "test"},
            headings=["Heading"],
            wikilinks=["Python"],
            tags=["tag1"],
        )

        knowledge = KnowledgeFactory.from_markdown(document)

        self.assertEqual(knowledge.tags, ["tag1"])
        self.assertEqual(knowledge.metadata, {"category": "test"})
