from typing import Tuple

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QWidget,
)


class NewDocumentDialog(QDialog):
    """Dialog to collect a new document title and initial content."""

    @staticmethod
    def get_document(parent: QWidget | None = None) -> Tuple[str | None, str | None]:
        dialog = QDialog(parent)
        dialog.setWindowTitle("New Document")

        layout = QFormLayout(dialog)

        title_input = QLineEdit(dialog)
        content_input = QTextEdit(dialog)

        layout.addRow("Title:", title_input)
        layout.addRow("Content:", content_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=dialog)
        layout.addRow(buttons)

        result = {"accepted": False}

        def on_accept():
            result["accepted"] = True
            dialog.accept()

        def on_reject():
            dialog.reject()

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(on_reject)

        accepted = dialog.exec()
        if result["accepted"]:
            return title_input.text().strip() or None, content_input.toPlainText()
        return None, None
