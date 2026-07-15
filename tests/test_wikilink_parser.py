import unittest
from pathlib import Path

from engine.parsers import MarkdownDocument, WikiLinkParser


class WikiLinkParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = WikiLinkParser()

    def test_document_without_links(self) -> None:
        document = MarkdownDocument(path=Path("/tmp/doc.md"), content="No links here.")

        result = self.parser.process(document)

        self.assertEqual(result.wikilinks, [])
        self.assertEqual(result.content, document.content)

    def test_single_link(self) -> None:
        document = MarkdownDocument(path=Path("/tmp/doc.md"), content="This is [[Python]].")

        result = self.parser.process(document)

        self.assertEqual(result.wikilinks, ["Python"])

    def test_multiple_links(self) -> None:
        document = MarkdownDocument(
            path=Path("/tmp/doc.md"),
            content="Link [[Python]] and [[AI]].",
        )

        result = self.parser.process(document)

        self.assertEqual(result.wikilinks, ["Python", "AI"])

    def test_repeated_links(self) -> None:
        document = MarkdownDocument(
            path=Path("/tmp/doc.md"),
            content="[[Python]] [[Python]]",
        )

        result = self.parser.process(document)

        self.assertEqual(result.wikilinks, ["Python", "Python"])

    def test_links_with_alias(self) -> None:
        document = MarkdownDocument(
            path=Path("/tmp/doc.md"),
            content="[[Programação|Prog]] [[Python|Py]]",
        )

        result = self.parser.process(document)

        self.assertEqual(result.wikilinks, ["Programação", "Python"])


if __name__ == "__main__":
    unittest.main()
