from PySide6.QtWidgets import QListWidget, QWidget, QVBoxLayout


class DocumentListPanel(QWidget):
    """Panel that displays the list of available documents."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("documentList")

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_documents(self, titles: list[str]) -> None:
        self.list_widget.clear()
        for title in titles:
            self.list_widget.addItem(title)

    def clear(self) -> None:
        self.list_widget.clear()

    @property
    def current_row_changed(self):
        return self.list_widget.currentRowChanged

    def set_current_row(self, row: int) -> None:
        self.list_widget.setCurrentRow(row)

    @property
    def current_item(self):
        return self.list_widget.currentItem()
