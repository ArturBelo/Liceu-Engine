from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QAction, QKeySequence
# Qt version will be obtained from the PySide6 package at runtime

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
        # handle selection changes with unsaved-changes protection
        self._current_row = -1
        self.document_list_widget.currentRowChanged.connect(self._on_document_selection_requested)
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

        self.new_button = QPushButton("New Document", self)
        self.new_button.clicked.connect(self.handle_new_document)
        viewer_layout.addWidget(self.new_button)

        self.status_label = QLabel("Nenhum Vault carregado.", self)
        viewer_layout.addWidget(self.status_label)

        self.document_viewer = DocumentViewer(self)
        # keep compatibility: content_viewer points to the QTextEdit editor
        self.content_viewer = self.document_viewer.editor
        viewer_layout.addWidget(self.document_viewer)

        # allow editing
        self.document_viewer.set_editable(True)
        self.content_viewer.textChanged.connect(self._on_content_changed)

        # preview toggle button
        self.preview_button = QPushButton("Preview", self)
        self.preview_button.setCheckable(True)
        self.preview_button.clicked.connect(self._toggle_preview_ui)
        viewer_layout.addWidget(self.preview_button)

        self.save_button = QPushButton("Save", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.handle_save_document)
        viewer_layout.addWidget(self.save_button)

        viewer_layout.addStretch()
        main_layout.addWidget(viewer_panel)

        self.statistics_panel = StatisticsPanel(self)
        viewer_layout.addWidget(self.statistics_panel)
        
        # ensure backlinks panel exists for earlier layout

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

        # create menus after UI widgets exist
        self._create_menus()

    def _create_menus(self) -> None:
        """Create the application menu bar and connect actions to existing handlers."""
        # File menu
        file_menu = self.menuBar().addMenu("File")

        new_action = QAction("New Document", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.handle_new_document)
        file_menu.addAction(new_action)

        open_action = QAction("Open Vault", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.import_vault)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.handle_save_document)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setEnabled(False)
        file_menu.addAction(save_as_action)

        export_action = QAction("Export...", self)
        export_action.setEnabled(False)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu - reuse QTextEdit actions where possible
        edit_menu = self.menuBar().addMenu("Edit")
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.content_viewer.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.content_viewer.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.content_viewer.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.content_viewer.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.content_viewer.paste)
        edit_menu.addAction(paste_action)

        select_all_action = QAction("Select All", self)
        select_all_action.triggered.connect(self.content_viewer.selectAll)
        edit_menu.addAction(select_all_action)

        # View menu
        view_menu = self.menuBar().addMenu("View")
        focus_search = QAction("Focus Search", self)
        focus_search.setShortcut(QKeySequence("Ctrl+F"))
        focus_search.triggered.connect(lambda: self.search_input.setFocus())
        view_menu.addAction(focus_search)

        focus_list = QAction("Focus Document List", self)
        focus_list.triggered.connect(lambda: self.document_list_widget.setFocus())
        view_menu.addAction(focus_list)

        focus_editor = QAction("Focus Editor", self)
        focus_editor.triggered.connect(lambda: self.content_viewer.setFocus())
        view_menu.addAction(focus_editor)

        # Graph menu (placeholders)
        graph_menu = self.menuBar().addMenu("Graph")
        open_graph = QAction("Open Graph View", self)
        open_graph.triggered.connect(self._open_graph_window)
        graph_menu.addAction(open_graph)
        refresh_graph = QAction("Refresh Graph", self)
        # refresh_graph will simply rebuild the engine graph when requested
        refresh_graph.triggered.connect(lambda: self.engine.build_graph())
        graph_menu.addAction(refresh_graph)

        # Help menu
        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About Liceu Engine", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

    def _show_about_dialog(self) -> None:
        """Show an About dialog with application and environment details."""
        try:
            from engine.version import __version__
        except Exception:
            __version__ = "unknown"

        import sys
        python_version = sys.version.split()[0]
        try:
            import PySide6
            qt_version = getattr(PySide6, "__version__", "unknown")
        except Exception:
            qt_version = "unknown"

        text = f"Liceu Engine\nVersion: {__version__}\nPython: {python_version}\nQt: {qt_version}"
        QMessageBox.information(self, "About Liceu Engine", text)

    def import_vault(self) -> None:
        """Import a vault directory using the LiceuEngine facade."""
        # protect from unsaved edits
        from engine.gui.utils import confirm_unsaved_changes, ConfirmResult

        if self.document_viewer.is_modified():
            choice = confirm_unsaved_changes(self)
            if choice == ConfirmResult.CANCEL:
                return
            if choice == ConfirmResult.SAVE:
                # save current before opening new vault
                self.handle_save_document()
            # if DISCARD, just continue

        directory = QFileDialog.getExistingDirectory(self, "Selecione o Vault")
        if not directory:
            return

        imported = self.engine.import_directory(Path(directory))
        self.status_label.setText(f"{len(imported)} documentos importados.")
        self.update_document_list()
        self.statistics_panel.set_stats(self.engine.stats())

    def handle_new_document(self) -> None:
        """Open the new document dialog and create the document through the engine."""
        # protect from unsaved edits
        from engine.gui.utils import confirm_unsaved_changes, ConfirmResult

        if self.document_viewer.is_modified():
            choice = confirm_unsaved_changes(self)
            if choice == ConfirmResult.CANCEL:
                return
            if choice == ConfirmResult.SAVE:
                self.handle_save_document()
            # DISCARD -> proceed without saving

        from engine.gui.widgets import NewDocumentDialog

        title, content = NewDocumentDialog.get_document(self)
        if not title:
            return

        new_knowledge = self.engine.create_document(title=title, content=content or "")
        # refresh UI and select created document
        self.update_document_list()
        # find the index of the created document
        index = next((i for i, k in enumerate(self._documents) if str(k.id) == str(new_knowledge.id)), None)
        if index is not None:
            self.document_list_widget.setCurrentRow(index)
            self.statistics_panel.set_stats(self.engine.stats())

    def _toggle_preview_ui(self) -> None:
        """Toggle the DocumentViewer preview and update the button label."""
        self.document_viewer.toggle_preview()
        if self.document_viewer.is_preview_active():
            self.preview_button.setText("Edit")
            # ensure preview is up to date with latest editor content
            self.document_viewer._render_preview(self.content_viewer.toPlainText())
        else:
            self.preview_button.setText("Preview")

    def _open_graph_window(self) -> None:
        """Open the GraphWindow to visualize relations."""
        from engine.gui.graph_window import GraphWindow

        self._graph_window = GraphWindow(self)
        self._graph_window.show()

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
            self._current_row = -1
            return

        knowledge = self._documents[current_row]
        self.content_viewer.setPlainText(knowledge.content)
        self.update_related_list(knowledge.title)
        self.update_backlinks_list(knowledge.title)
        self._current_row = current_row

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

    def _on_document_selection_requested(self, new_row: int) -> None:
        """Handle a requested document selection, protecting unsaved edits.

        This method is connected to the QListWidget.currentRowChanged signal which
        fires after the selection changes. To support Cancel, the method will
        restore the previous selection when needed.
        """
        from engine.gui.utils import confirm_unsaved_changes, ConfirmResult

        # if no prior selection or nothing modified, just display
        if not getattr(self, "document_viewer", None) or not self.document_viewer.is_modified():
            self.display_selected_document(new_row)
            return

        # there are unsaved changes
        choice = confirm_unsaved_changes(self)
        if choice == ConfirmResult.CANCEL:
            # revert to previous selection
            self.document_list_widget.blockSignals(True)
            self.document_list_widget.setCurrentRow(self._current_row)
            self.document_list_widget.blockSignals(False)
            return

        if choice == ConfirmResult.SAVE:
            # save current and then proceed to requested selection
            self.handle_save_document()
            # proceed
            self.display_selected_document(new_row)
            return

        # DISCARD: reload the currently selected knowledge from repository and proceed
        # revert in-memory edits by reloading current knowledge content (if any)
        if self._current_row is not None and self._current_row >= 0 and self._current_row < len(self._documents):
            current_k = self._documents[self._current_row]
            # reset editor content to stored content
            self.content_viewer.setPlainText(current_k.content)
            self.document_viewer.set_modified(False)

        # proceed to requested selection
        self.display_selected_document(new_row)

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

    def _on_content_changed(self) -> None:
        """Called when the content editor changes to enable Save button."""
        # enable save when content changes
        self.save_button.setEnabled(True)
        # forward modified flag to the DocumentViewer
        self.document_viewer.set_modified(True)

    def closeEvent(self, event) -> None:
        """Confirm unsaved changes when the user attempts to close the application."""
        from engine.gui.utils import confirm_unsaved_changes, ConfirmResult

        if self.document_viewer.is_modified():
            choice = confirm_unsaved_changes(self)
            if choice == ConfirmResult.CANCEL:
                event.ignore()
                return
            if choice == ConfirmResult.SAVE:
                self.handle_save_document()
                event.accept()
                return
            # DISCARD -> accept and close
            event.accept()
            return

        super().closeEvent(event)

    def handle_save_document(self) -> None:
        """Save the currently displayed document through the engine."""
        current_row = self.document_list_widget.currentRow()
        if current_row < 0 or current_row >= len(getattr(self, "_documents", [])):
            return

        knowledge = self._documents[current_row]
        new_content = self.content_viewer.toPlainText()

        # call only the engine to perform update
        updated = self.engine.update_document(title=knowledge.title, content=new_content)

        # refresh UI: list, selection, related, backlinks, statistics
        self.update_document_list()
        # find the updated document index
        index = next((i for i, k in enumerate(self._documents) if str(k.id) == str(updated.id)), None)
        if index is not None:
            self.document_list_widget.setCurrentRow(index)
        self.statistics_panel.set_stats(self.engine.stats())

        # reset modified state
        if hasattr(self, 'document_viewer') and self.document_viewer is not None:
            self.document_viewer.set_modified(False)
        self.save_button.setEnabled(False)
