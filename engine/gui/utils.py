from enum import Enum
from PySide6.QtWidgets import QMessageBox, QWidget


class ConfirmResult(Enum):
    SAVE = "save"
    DISCARD = "discard"
    CANCEL = "cancel"


def confirm_unsaved_changes(parent: QWidget | None = None) -> ConfirmResult:
    """Show a confirmation dialog for unsaved changes and return the user's choice.

    Returns one of ConfirmResult.SAVE, ConfirmResult.DISCARD, ConfirmResult.CANCEL.
    """
    dlg = QMessageBox(parent)
    dlg.setWindowTitle("Unsaved Changes")
    dlg.setText("The current document contains unsaved changes.\n\nWhat would you like to do?")
    save_btn = dlg.addButton("Save", QMessageBox.AcceptRole)
    discard_btn = dlg.addButton("Discard", QMessageBox.DestructiveRole)
    cancel_btn = dlg.addButton("Cancel", QMessageBox.RejectRole)
    dlg.setDefaultButton(save_btn)

    dlg.exec()

    clicked = dlg.clickedButton()
    if clicked == save_btn:
        return ConfirmResult.SAVE
    if clicked == discard_btn:
        return ConfirmResult.DISCARD
    return ConfirmResult.CANCEL
