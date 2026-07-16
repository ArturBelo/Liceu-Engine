from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout


class StatisticsPanel(QWidget):
    """Panel that displays knowledge vault statistics."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.documents_label = QLabel("Documents: 0", self)
        self.links_label = QLabel("Links: 0", self)
        self.orphans_label = QLabel("Orphans: 0", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.documents_label)
        layout.addWidget(self.links_label)
        layout.addWidget(self.orphans_label)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_stats(self, stats: dict[str, int]) -> None:
        self.documents_label.setText(f"Documents: {stats.get('documents', 0)}")
        self.links_label.setText(f"Links: {stats.get('links', 0)}")
        self.orphans_label.setText(f"Orphans: {stats.get('orphans', 0)}")
