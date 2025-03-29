from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                            QLabel, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from .graph_view import GraphView
from models.robot import Robot

class FleetGUI(QMainWindow):
    def __init__(self, nav_graph):
        super().__init__()
        self.nav_graph = nav_graph
        self.setWindowTitle("Fleet Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Graph Visualization
        self.graph_view = GraphView(nav_graph)
        layout.addWidget(self.graph_view)

        # Robot Management
        self.robots = []
        
        # Status Bar
        self.statusBar().showMessage("Ready - Click on any vertex to spawn a robot")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.graph_view.mapToScene(event.pos())
            clicked_items = self.graph_view.scene.items(pos)
            
            for item in clicked_items:
                if isinstance(item, QGraphicsEllipseItem) and item.data(0) != "robot":
                    node_id = item.data(0)
                    x, y = self.nav_graph.graph.nodes[node_id]["pos"]
                    self.spawn_robot(node_id, x, y)
                    break
                    
    def spawn_robot(self, node_id, x, y):
        robot = Robot(node_id, x, y, self.graph_view.scale_factor)
        self.robots.append(robot)
        self.graph_view.scene.addItem(robot.graphics_item)
        self.statusBar().showMessage(f"Robot spawned at vertex {node_id}")