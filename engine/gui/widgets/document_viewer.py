from PySide6.QtWidgets import QTextEdit, QWidget, QVBoxLayout


class DocumentViewer(QWidget):
    """Viewer widget for displaying the content of a document."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.viewer = QTextEdit(self)
        self.viewer.setReadOnly(True)
        self.viewer.setPlainText("Selecione um documento para visualizar.")

        layout = QVBoxLayout(self)
        layout.addWidget(self.viewer)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_content(self, content: str) -> None:
        self.viewer.setPlainText(content)

    def clear(self) -> None:
        self.viewer.setPlainText("Selecione um documento para visualizar.")
