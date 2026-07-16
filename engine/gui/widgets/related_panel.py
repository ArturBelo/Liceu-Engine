from PySide6.QtWidgets import QLabel, QListWidget, QWidget, QVBoxLayout


class RelatedPanel(QWidget):
    """Panel that displays related documents."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label = QLabel("Related Documents", self)
        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("relatedList")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_items(self, titles: list[str]) -> None:
        self.list_widget.clear()
        for title in titles:
            self.list_widget.addItem(title)

    def clear(self) -> None:
        self.list_widget.clear()

    @property
    def item_clicked(self):
        return self.list_widget.itemClicked

    @property
    def count(self) -> int:
        return self.list_widget.count()

    def set_placeholder(self, text: str) -> None:
        self.list_widget.clear()
        self.list_widget.addItem(text)
