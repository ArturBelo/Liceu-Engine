from PySide6.QtWidgets import QLineEdit, QWidget, QVBoxLayout


class SearchBar(QWidget):
    """Search bar widget for filtering documents."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._input = QLineEdit(self)
        self._input.setPlaceholderText("Buscar documentos...")

        layout = QVBoxLayout(self)
        layout.addWidget(self._input)
        layout.setContentsMargins(0, 0, 0, 0)

    @property
    def input(self) -> QLineEdit:
        return self._input

    def set_text(self, text: str) -> None:
        self._input.setText(text)

    def clear(self) -> None:
        self._input.clear()

    @property
    def text_changed(self):
        return self._input.textChanged
