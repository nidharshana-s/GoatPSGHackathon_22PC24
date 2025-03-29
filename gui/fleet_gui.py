from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                            QLabel, QStatusBar, QGraphicsEllipseItem, QGraphicsView)
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtGui import (QPainter,QBrush)
from .graph_view import GraphView
from models.robot import Robot

class FleetGUI(QMainWindow):
    def __init__(self, nav_graph):
        super().__init__()
        self.nav_graph = nav_graph
        self.setup_ui()
        self.graph_view.mousePressEvent = self.handle_view_click
        
    def setup_ui(self):
        # Window setup
        self.setWindowTitle("Fleet Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Graph view
        self.graph_view = GraphView(self.nav_graph)
        layout.addWidget(self.graph_view)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Robot tracking
        self.robots = []
        
        # Connect click debugger (temporary)
        self.graph_view.mousePressEvent = self.debug_click

    def debug_click(self, event):
        """Temporary debug method"""
        self.graph_view.print_click_debug(event.pos())
        
        # Forward to actual handler
        QGraphicsView.mousePressEvent(self.graph_view, event)
        self.mousePressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.graph_view.mapToScene(event.pos())
            items = self.graph_view.scene.items(scene_pos)
            
            for item in items:
                if isinstance(item, QGraphicsEllipseItem) and item.data(0) is not None:
                    self.handle_vertex_click(item)
                    break

    def handle_vertex_click(self, vertex_item):
        node_id = vertex_item.data(0)
        x, y = self.nav_graph.graph.nodes[node_id]["pos"]
        
        # Visual feedback
        original_brush = vertex_item.brush()
        vertex_item.setBrush(QBrush(Qt.yellow))
        QTimer.singleShot(200, lambda: vertex_item.setBrush(original_brush))
        
        # Spawn robot
        robot = Robot(node_id, x, y, self.graph_view.scale_factor)
        self.graph_view.scene.addItem(robot.graphics_item)
        self.graph_view.scene.addItem(robot.label)
        self.robots.append(robot)
        
        # Status update
        self.status_bar.showMessage(
            f"✅ Spawned {robot.robot_id} at Node {node_id}",
            3000  # Show for 3 seconds
        )
        
    def handle_view_click(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.graph_view.mapToScene(event.pos())
            items = self.graph_view.scene.items(scene_pos)
            
            for item in items:
                # More robust check using both data fields
                if (isinstance(item, QGraphicsEllipseItem) and 
                    item.data(0) is not None and 
                    item.data(1) == "vertex"):
                    
                    node_id = item.data(0)
                    print(f"Valid click on vertex {node_id}")  # Debug
                    self.spawn_robot_at_item(item)
                    break
        
    def spawn_robot_at_item(self, item):
        """Handle robot spawning at a clicked item"""
        node_id = item.data(0)
        x, y = self.nav_graph.graph.nodes[node_id]["pos"]
        
        # Visual feedback (flash)
        original_brush = item.brush()
        item.setBrush(QBrush(Qt.yellow))
        QTimer.singleShot(200, lambda: item.setBrush(original_brush))
        
        # Create and add robot
        robot = Robot(node_id, x, y, self.graph_view.scale_factor)
        self.graph_view.scene.addItem(robot.graphics_item)
        self.graph_view.scene.addItem(robot.label)
        self.robots.append(robot)
        
        # Update status
        self.status_bar.showMessage(f"Spawned {robot.robot_id} at Node {node_id}", 3000)