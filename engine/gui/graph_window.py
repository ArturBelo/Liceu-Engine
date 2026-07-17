from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import QRectF, Qt

from engine import LiceuEngine


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id: str, title: str, rect: QRectF, parent_window: "GraphWindow") -> None:
        super().__init__(rect)
        self.node_id = node_id
        self.title = title
        self.parent_window = parent_window
        self.setBrush(QBrush(QColor("#99ccff")))
        self.setPen(QPen(QColor("#336699")))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, False)

        # label
        text = QGraphicsTextItem(title, parent=self)
        text.setDefaultTextColor(QColor("#003366"))
        # center the text
        tb = text.boundingRect()
        text.setPos(rect.width() / 2 - tb.width() / 2, rect.height() / 2 - tb.height() / 2)

    def mouseDoubleClickEvent(self, event):
        # delegate to parent to open document
        if self.parent_window:
            self.parent_window.open_document_by_node(self.node_id)
        super().mouseDoubleClickEvent(event)


class EdgeItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2) -> None:
        super().__init__(x1, y1, x2, y2)
        self.setPen(QPen(QColor("#888888"), 1))


class GraphWindow(QMainWindow):
    """Window to visualize the knowledge graph using QGraphicsView."""

    def __init__(self, main_window) -> None:
        super().__init__()
        self.setWindowTitle("Liceu Engine — Graph")
        self.resize(800, 600)

        self.main_window = main_window
        self.engine: LiceuEngine = main_window.engine

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # mapping
        self.node_items: dict[str, NodeItem] = {}
        self.edge_items: list[EdgeItem] = []

        # load graph on open
        self.populate_graph()

        # enable dragging background to pan
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setRenderHint(self.view.renderHints())
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # enable wheel zoom
        self.view.wheelEvent = self._wheel_zoom

    def populate_graph(self) -> None:
        """Fetch the latest graph from the engine and render it."""
        graph = self.engine.build_graph()
        nodes = graph.list_nodes()
        edges = graph.list_edges()

        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()

        # simple circular layout
        import math

        n = len(nodes)
        if n == 0:
            return

        cx = 300
        cy = 200
        radius = 150
        angle = 0
        step = 2 * math.pi / max(n, 1)

        node_positions = {}
        size = 80
        for i, node in enumerate(nodes):
            x = cx + radius * math.cos(angle) - size / 2
            y = cy + radius * math.sin(angle) - size / 2
            rect = QRectF(x, y, size, size)
            item = NodeItem(node.id, node.title, rect, parent_window=self)
            self.scene.addItem(item)
            self.node_items[node.id] = item
            node_positions[node.id] = (x + size / 2, y + size / 2)
            angle += step

        # edges
        for edge in edges:
            src = edge.source
            tgt = edge.target
            if src in node_positions and tgt in node_positions:
                x1, y1 = node_positions[src]
                x2, y2 = node_positions[tgt]
                line = EdgeItem(x1, y1, x2, y2)
                # put edges behind nodes
                line.setZValue(-1)
                self.scene.addItem(line)
                self.edge_items.append(line)

    def _wheel_zoom(self, event):
        # zoom in/out
        delta = event.angleDelta().y()
        factor = 1.001 ** delta
        self.view.scale(factor, factor)

    def open_document_by_node(self, node_id: str) -> None:
        """Open the document in the main window by selecting it in the document list.

        This reuses MainWindow's selection logic by setting the current row on the
        document list widget.
        """
        # find the index in main_window's documents
        docs = getattr(self.main_window, "_documents", [])
        target_row = next((i for i, d in enumerate(docs) if str(d.id) == str(node_id)), None)
        if target_row is None:
            # reload list and try again
            self.main_window.update_document_list()
            docs = getattr(self.main_window, "_documents", [])
            target_row = next((i for i, d in enumerate(docs) if str(d.id) == str(node_id)), None)
            if target_row is None:
                return

        # select in main window (triggers the same selection protections there)
        self.main_window.document_list_widget.setCurrentRow(target_row)
        # optionally close graph window
        self.close()
