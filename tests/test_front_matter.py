import unittest

from engine.parsers.front_matter import FrontMatterParser


class FrontMatterParserTestCase(unittest.TestCase):
    def test_no_front_matter_returns_original(self) -> None:
        content = "# Title\n\nContent"
        front_matter, body = FrontMatterParser.parse(content)

        self.assertIsNone(front_matter)
        self.assertEqual(body, content)

    def test_simple_key(self) -> None:
        content = "---\ntitle: Test\n---\n# Title"
        front_matter, body = FrontMatterParser.parse(content)

        self.assertEqual(front_matter, {"title": "Test"})
        self.assertEqual(body, "# Title")

    def test_multiple_keys(self) -> None:
        content = "---\ntitle: Test\ndescription: Example\n---\n# Title"
        front_matter, body = FrontMatterParser.parse(content)

        self.assertEqual(
            front_matter,
            {
                "title": "Test",
                "description": "Example",
            },
        )
        self.assertEqual(body, "# Title")

    def test_list_values(self) -> None:
        content = (
            "---\ntags:\n  - python\n  - ai\n---\n# Title"
        )
        front_matter, body = FrontMatterParser.parse(content)

        self.assertEqual(front_matter, {"tags": ["python", "ai"]})
        self.assertEqual(body, "# Title")

    def test_front_matter_removed_from_content(self) -> None:
        content = (
            "---\ntitle: Test\ntags:\n  - python\n  - ai\n---\n# Title\n\nContent"
        )
        front_matter, body = FrontMatterParser.parse(content)

        self.assertEqual(body, "# Title\n\nContent")


if __name__ == "__main__":
    unittest.main()
