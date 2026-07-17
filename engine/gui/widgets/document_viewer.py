from PySide6.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QStackedWidget, QTextBrowser
from typing import Callable
import re


class DocumentViewer(QWidget):
    """Viewer widget that supports edit and preview modes.

    Exposes editor and preview widgets and helper methods so the MainWindow
    can coordinate saving, focus and mode toggling without moving business
    logic into the widget.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.stack = QStackedWidget(self)

        # editor
        self.editor = QTextEdit(self)
        self.editor.setPlainText("Selecione um documento para visualizar.")

        # preview (read-only HTML)
        self.preview = QTextBrowser(self)
        self.preview.setOpenExternalLinks(True)

        self.stack.addWidget(self.editor)
        self.stack.addWidget(self.preview)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        layout.setContentsMargins(0, 0, 0, 0)

    # content management
    def set_markdown(self, content: str) -> None:
        """Set the markdown content into the editor and update preview."""
        self.editor.setPlainText(content)
        self._render_preview(content)

    def set_preview(self, html: str) -> None:
        """Directly set HTML in the preview pane."""
        self.preview.setHtml(html)

    def get_markdown(self) -> str:
        return self.editor.toPlainText()

    def clear(self) -> None:
        self.editor.setPlainText("Selecione um documento para visualizar.")
        self.preview.setHtml("")

    # edit controls
    def set_editable(self, editable: bool) -> None:
        self.editor.setReadOnly(not editable)

    def is_modified(self) -> bool:
        return self.editor.document().isModified()

    def set_modified(self, modified: bool) -> None:
        self.editor.document().setModified(modified)

    # mode management
    def toggle_preview(self) -> None:
        """Toggle between editor (index 0) and preview (index 1).

        When switching to preview, ensure the preview is up to date with the
        editor content.
        """
        if self.stack.currentIndex() == 0:
            content = self.get_markdown()
            self._render_preview(content)
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def is_preview_active(self) -> bool:
        return self.stack.currentIndex() == 1

    # rendering
    def _render_preview(self, markdown_text: str) -> None:
        """Render markdown_text into HTML for the preview pane.

        Prefer the 'markdown' package when available. As a fallback, apply a
        minimal set of replacements to provide basic rendering for tests. Wiki
        links of the form [[Title]] are converted to internal links using the
        liceu:// scheme so they appear as clickable hyperlinks.
        """
        # convert wikilinks to inline markdown links to a liceu scheme
        def wikilink_sub(m: re.Match) -> str:
            target = m.group(1).strip()
            # escape parentheses in target
            return f"[{target}](liceu://{target})"

        preprocessed = re.sub(r"\[\[(.+?)\]\]", wikilink_sub, markdown_text)

        try:
            # prefer external markdown library if available
            import markdown as md

            html = md.markdown(preprocessed, extensions=["extra", "tables", "fenced_code"])
        except Exception:
            # minimal fallback renderer (not a full markdown parser)
            import html

            escaped = html.escape(preprocessed)
            # headings
            escaped = re.sub(r'(?m)^### (.+)$', r'<h3>\1</h3>', escaped)
            escaped = re.sub(r'(?m)^## (.+)$', r'<h2>\1</h2>', escaped)
            escaped = re.sub(r'(?m)^# (.+)$', r'<h1>\1</h1>', escaped)
            # bold/italic
            escaped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)
            escaped = re.sub(r'\*(.+?)\*', r'<em>\1</em>', escaped)
            # code fences
            escaped = re.sub(r'(?s)```(.+?)```', r'<pre><code>\1</code></pre>', escaped)
            # links from wikilink conversion: [text](liceu://text)
            escaped = re.sub(r'\[(.+?)\]\(liceu://(.+?)\)', r'<a href="liceu://\2">\1</a>', escaped)
            # line breaks
            escaped = escaped.replace('\n\n', '<br/><br/>')
            html = f"<div>{escaped}</div>"

        self.preview.setHtml(html)
