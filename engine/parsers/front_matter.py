from __future__ import annotations

from typing import Any

from engine.parsers.document import MarkdownDocument


class FrontMatterParser:
    """Parse YAML-like front matter from Markdown content."""

    @staticmethod
    def parse_text(text: str) -> tuple[dict[str, Any] | None, str]:
        lines = text.splitlines(True)
        if not lines or lines[0].strip() != "---":
            return None, text

        closing_index = None
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing_index = index
                break

        if closing_index is None:
            return None, text

        front_lines = [line.rstrip("\n") for line in lines[1:closing_index]]
        body = "".join(lines[closing_index + 1 :])
        front_matter: dict[str, Any] = {}
        current_key: str | None = None
        current_list: list[str] | None = None

        for line in front_lines:
            if not line.strip():
                continue

            stripped = line.lstrip()
            indent = len(line) - len(stripped)

            if stripped.startswith("-") and current_key is not None and indent >= 2:
                item = stripped[1:].strip()
                if current_list is None:
                    current_list = []
                current_list.append(item)
                front_matter[current_key] = current_list
                continue

            if ":" in stripped and indent == 0:
                if current_key is not None and current_list is not None:
                    current_list = None

                key, value = stripped.split(":", 1)
                key = key.strip()
                value = value.strip()
                if value == "":
                    current_key = key
                    current_list = []
                    front_matter[key] = current_list
                else:
                    current_key = None
                    current_list = None
                    front_matter[key] = value
                continue

            if current_key is not None and current_list is not None and stripped.startswith("-"):
                item = stripped[1:].strip()
                current_list.append(item)
                continue

        return front_matter, body

    parse = staticmethod(parse_text)

    def process(self, document: MarkdownDocument) -> MarkdownDocument:
        front_matter, content = self.parse_text(document.content)
        return MarkdownDocument(
            path=document.path,
            content=content,
            front_matter=front_matter,
        )

    parse = staticmethod(parse_text)
