from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, 
                            QGraphicsEllipseItem, QGraphicsLineItem,
                            QGraphicsTextItem)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont

class GraphView(QGraphicsView):
    def __init__(self, nav_graph):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.nav_graph = nav_graph
        self.scale_factor = 50.0
        
        # Set rendering hints
        self.setRenderHints(QPainter.Antialiasing | 
                          QPainter.TextAntialiasing |
                          QPainter.SmoothPixmapTransform)
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.draw_graph()
        
    def draw_graph(self):
        # Draw lanes (edges)
        for start, end in self.nav_graph.graph.edges():
            x1, y1 = self.nav_graph.graph.nodes[start]["pos"]
            x2, y2 = self.nav_graph.graph.nodes[end]["pos"]
            line = QGraphicsLineItem(
                x1 * self.scale_factor, 
                -y1 * self.scale_factor,
                x2 * self.scale_factor, 
                -y2 * self.scale_factor
            )
            line.setPen(QPen(Qt.darkGray, 2))
            self.scene.addItem(line)

        # Draw vertices (nodes)
        for node in self.nav_graph.graph.nodes():
            x, y = self.nav_graph.graph.nodes[node]["pos"]
            attrs = self.nav_graph.graph.nodes[node]
            
            # Draw vertex
            ellipse = QGraphicsEllipseItem(
                x * self.scale_factor - 10, 
                -y * self.scale_factor - 10, 
                20, 20
            )
            color = QColor(70, 130, 180) if attrs.get("is_charger") else QColor(220, 20, 60)
            ellipse.setBrush(QBrush(color))
            ellipse.setPen(QPen(Qt.black, 1))
            ellipse.setData(0, node)
            ellipse.setZValue(1)
            self.scene.addItem(ellipse)

            # Add labels
            if "name" in attrs and attrs["name"]:
                text = QGraphicsTextItem(attrs["name"])
                text.setFont(QFont("Arial", 10))
                text.setPos(
                    x * self.scale_factor + 15, 
                    -y * self.scale_factor - 15
                )
                self.scene.addItem(text)
    
    def wheelEvent(self, event):
        # Zoom with mouse wheel
        zoom_in = 1.25
        zoom_out = 1 / zoom_in
        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)