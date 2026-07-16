from PySide6.QtWidgets import QLabel, QListWidget, QWidget, QVBoxLayout


class BacklinksPanel(QWidget):
    """Panel that displays backlinks for the currently selected document."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label = QLabel("Backlinks", self)
        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName("backlinksList")

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

    def set_placeholder(self, text: str) -> None:
        self.list_widget.clear()
        self.list_widget.addItem(text)

    @property
    def item_clicked(self):
        return self.list_widget.itemClicked
