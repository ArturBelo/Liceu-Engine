from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog

from engine import LiceuEngine
from engine.gui.widgets import BacklinksPanel, DocumentListPanel, DocumentViewer, RelatedPanel, SearchBar, StatisticsPanel


class MainWindow(QMainWindow):
    """Main window for the Liceu Engine GUI."""

    def __init__(self, engine: LiceuEngine | None = None) -> None:
        super().__init__()
        self.engine = engine or LiceuEngine()
        self._documents: list = []

        self.setWindowTitle("Liceu Engine")
        self.resize(1200, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.document_list_panel = DocumentListPanel(self)
        self.document_list_widget = self.document_list_panel.list_widget
        self.document_list_widget.currentRowChanged.connect(self.display_selected_document)
        main_layout.addWidget(self.document_list_panel)

        viewer_panel = QWidget(self)
        viewer_layout = QVBoxLayout(viewer_panel)

        self.title_label = QLabel("Liceu Engine", self)
        viewer_layout.addWidget(self.title_label)

        self.search_bar = SearchBar(self)
        self.search_input = self.search_bar.input
        self.search_input.textChanged.connect(self.handle_search)
        viewer_layout.addWidget(self.search_bar)

        self.import_button = QPushButton("Importar Vault", self)
        self.import_button.clicked.connect(self.import_vault)
        viewer_layout.addWidget(self.import_button)

        self.status_label = QLabel("Nenhum Vault carregado.", self)
        viewer_layout.addWidget(self.status_label)

        self.document_viewer = DocumentViewer(self)
        self.content_viewer = self.document_viewer.viewer
        viewer_layout.addWidget(self.document_viewer)

        viewer_layout.addStretch()
        main_layout.addWidget(viewer_panel)

        self.statistics_panel = StatisticsPanel(self)
        viewer_layout.addWidget(self.statistics_panel)

        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)

        self.related_panel = RelatedPanel(self)
        self.related_list_widget = self.related_panel.list_widget
        self.related_list_widget.itemClicked.connect(self.open_related_document)
        right_layout.addWidget(self.related_panel)

        self.backlinks_panel = BacklinksPanel(self)
        self.backlinks_list_widget = self.backlinks_panel.list_widget
        self.backlinks_list_widget.itemClicked.connect(self.open_backlink_document)
        right_layout.addWidget(self.backlinks_panel)

        right_layout.addStretch()
        main_layout.addWidget(right_panel)

    def import_vault(self) -> None:
        """Import a vault directory using the LiceuEngine facade."""
        directory = QFileDialog.getExistingDirectory(self, "Selecione o Vault")
        if not directory:
            return

        imported = self.engine.import_directory(Path(directory))
        self.status_label.setText(f"{len(imported)} documentos importados.")
        self.update_document_list()
        self.statistics_panel.set_stats(self.engine.stats())

    def update_document_list(self) -> None:
        """Refresh the displayed document list from the engine."""
        self.document_list_widget.clear()
        self.related_list_widget.clear()
        self.backlinks_list_widget.clear()
        self.search_input.blockSignals(True)
        self.search_input.setText("")
        self.search_input.blockSignals(False)
        self._documents = self.engine.list(order_by="title")
        for knowledge in self._documents:
            self.document_list_widget.addItem(knowledge.title)
        if not self._documents:
            self.content_viewer.setPlainText("Selecione um documento para visualizar.")
            self.related_list_widget.addItem("No related documents.")
            self.backlinks_list_widget.addItem("No backlinks.")
            self.statistics_panel.set_stats({"documents": 0, "links": 0, "orphans": 0})

    def handle_search(self, query: str) -> None:
        """Search documents through the engine and update the displayed list."""
        self.document_list_widget.clear()
        self.document_list_widget.clear()
        self.related_list_widget.clear()
        self.backlinks_list_widget.clear()
        if not query:
            self._documents = self.engine.list(order_by="title")
        else:
            self._documents = self.engine.search(query)
        for knowledge in self._documents:
            self.document_list_widget.addItem(knowledge.title)
        self.content_viewer.setPlainText("Selecione um documento para visualizar.")
        self.related_list_widget.addItem("No related documents.")
        self.backlinks_list_widget.addItem("No backlinks.")

    def display_selected_document(self, current_row: int) -> None:
        """Display the content of the selected document."""
        if current_row < 0 or current_row >= len(getattr(self, "_documents", [])):
            self.content_viewer.setPlainText("Selecione um documento para visualizar.")
            self.related_list_widget.clear()
            self.related_list_widget.addItem("No related documents.")
            self.backlinks_list_widget.clear()
            self.backlinks_list_widget.addItem("No backlinks.")
            return

        knowledge = self._documents[current_row]
        self.content_viewer.setPlainText(knowledge.content)
        self.update_related_list(knowledge.title)
        self.update_backlinks_list(knowledge.title)

    def update_related_list(self, title: str) -> None:
        """Update the related document list based on the selected title."""
        self.related_list_widget.clear()
        related_documents = self.engine.related(title)
        if not related_documents:
            self.related_list_widget.addItem("No related documents.")
            return

        for knowledge in related_documents:
            self.related_list_widget.addItem(knowledge.title)

    def update_backlinks_list(self, title: str) -> None:
        """Update the backlinks panel based on the selected title."""
        self.backlinks_list_widget.clear()
        backlinks_documents = self.engine.backlinks(title)
        if not backlinks_documents:
            self.backlinks_list_widget.addItem("No backlinks.")
            return

        for knowledge in backlinks_documents:
            self.backlinks_list_widget.addItem(knowledge.title)

    def open_related_document(self, item) -> None:
        """Open a related document when clicked in the related list."""
        if item is None:
            return

        title = item.text()
        if title == "No related documents.":
            return

        target_row = next((index for index, doc in enumerate(self._documents) if doc.title == title), None)
        if target_row is None:
            self.update_document_list()
            target_row = next((index for index, doc in enumerate(self._documents) if doc.title == title), None)
            if target_row is None:
                return

        self.document_list_widget.setCurrentRow(target_row)
        self.update_backlinks_list(self._documents[target_row].title)

    def open_backlink_document(self, item) -> None:
        """Open a backlink document when clicked in the backlinks list."""
        if item is None:
            return

        title = item.text()
        if title == "No backlinks.":
            return

        target_row = next((index for index, doc in enumerate(self._documents) if doc.title == title), None)
        if target_row is None:
            self.update_document_list()
            target_row = next((index for index, doc in enumerate(self._documents) if doc.title == title), None)
            if target_row is None:
                return

        self.document_list_widget.setCurrentRow(target_row)
