from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, 
                            QGraphicsEllipseItem, QGraphicsLineItem,
                            QGraphicsTextItem)
from PyQt5.QtCore import Qt, QRectF
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
        # Draw lanes (edges) first (z-value 0)
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
            line.setZValue(0)
            self.scene.addItem(line)

        # Draw vertices (nodes) with guaranteed clickability
        for node in self.nav_graph.graph.nodes():
            x, y = self.nav_graph.graph.nodes[node]["pos"]
            attrs = self.nav_graph.graph.nodes[node]
            
            # Create vertex with explicit properties
            vertex = self._create_vertex(node, x, y, attrs)
            self.scene.addItem(vertex)
            
            # Add label if named
            if "name" in attrs and attrs["name"]:
                self._add_vertex_label(x, y, attrs["name"])
                
            print(f"Vertex {node} created at ({x:.2f}, {y:.2f})")  # Debug output
        
        # Add path preview
        if hasattr(self, 'preview_path'):
            for i in range(len(self.preview_path)-1):
                start = self.preview_path[i]
                end = self.preview_path[i+1]
                line = QGraphicsLineItem(
                    start.x(), start.y(),
                    end.x(), end.y()
                )
                line.setPen(QPen(Qt.green, 1, Qt.DashLine))
                line.setZValue(5)
                self.scene.addItem(line)

    def _create_vertex(self, node_id, x, y, attrs):
        """Creates a properly configured vertex item"""
        vertex = QGraphicsEllipseItem(
            x * self.scale_factor - 10,
            -y * self.scale_factor - 10,
            20, 20,
            parent=None  # Critical for proper behavior
        )
        
        # Set identification data
        vertex.setData(0, node_id)  # Primary key - node ID
        vertex.setData(1, "vertex")  # Type marker
        
        # Visual styling
        color = QColor(70, 130, 180) if attrs.get("is_charger") else QColor(220, 20, 60)
        vertex.setBrush(QBrush(color))
        vertex.setPen(QPen(Qt.black, 1))
        vertex.setZValue(1)  # Above lanes
        
        # Enable interaction
        vertex.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        vertex.setFlag(QGraphicsEllipseItem.ItemIsFocusable)
        
        return vertex

    def _add_vertex_label(self, x, y, name):
        """Adds text label to a vertex"""
        label = QGraphicsTextItem(name)
        label.setFont(QFont("Arial", 10))
        label.setPos(
            x * self.scale_factor + 15,
            -y * self.scale_factor - 15
        )
        label.setZValue(1)  # Same as vertex
        self.scene.addItem(label)

    def print_click_debug(self, pos):
        """Enhanced debugging tool"""
        scene_pos = self.mapToScene(pos)
        items = self.scene.items(scene_pos)
        
        print("\n=== CLICK DEBUG ===")
        print(f"Click at screen: ({pos.x()}, {pos.y()})")
        print(f"Scene coordinates: ({scene_pos.x():.2f}, {scene_pos.y():.2f})")
        print(f"Items at position ({len(items)}):")
        
        for i, item in enumerate(items):
            print(f"[{i}] {type(item).__name__}: "
                  f"NodeID={item.data(0)}, "
                  f"Type={item.data(1)}")
        
        print("==================\n")