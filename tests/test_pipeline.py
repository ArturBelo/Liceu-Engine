import unittest

from engine.parsers import MarkdownDocument, ParserPipeline


class FirstParser:
    def parse(self, document: MarkdownDocument) -> MarkdownDocument:
        return MarkdownDocument(
            path=document.path,
            content=document.content + " first",
            front_matter=document.front_matter,
        )


class SecondParser:
    def parse(self, document: MarkdownDocument) -> MarkdownDocument:
        return MarkdownDocument(
            path=document.path,
            content=document.content + " second",
            front_matter=document.front_matter,
        )


class ParserPipelineTestCase(unittest.TestCase):
    def test_pipeline_empty_returns_document(self) -> None:
        document = MarkdownDocument(path="/tmp/doc.md", content="content")
        pipeline = ParserPipeline()

        result = pipeline.process(document)

        self.assertEqual(result, document)

    def test_pipeline_single_parser(self) -> None:
        document = MarkdownDocument(path="/tmp/doc.md", content="content")
        pipeline = ParserPipeline()
        pipeline.register(FirstParser())

        result = pipeline.process(document)

        self.assertEqual(result.content, "content first")
        self.assertEqual(result.path, document.path)

    def test_pipeline_multiple_parsers(self) -> None:
        document = MarkdownDocument(path="/tmp/doc.md", content="content")
        pipeline = ParserPipeline()
        pipeline.register(FirstParser())
        pipeline.register(SecondParser())

        result = pipeline.process(document)

        self.assertEqual(result.content, "content first second")
        self.assertEqual(result.path, document.path)

    def test_pipeline_returns_markdown_document(self) -> None:
        document = MarkdownDocument(path="/tmp/doc.md", content="content")
        pipeline = ParserPipeline()
        pipeline.register(FirstParser())

        result = pipeline.process(document)

        self.assertIsInstance(result, MarkdownDocument)


if __name__ == "__main__":
    unittest.main()
