from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                            QStatusBar, QGraphicsEllipseItem, QGraphicsView, QGraphicsLineItem)
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor
from .graph_view import GraphView
from models.robot import Robot
import networkx as nx

class FleetGUI(QMainWindow):
    def __init__(self, nav_graph):
        super().__init__()
        self.nav_graph = nav_graph
        self.selected_robot = None
        self.setup_ui()
        
        # Movement animation timer
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.update_robot_movements)
        self.move_timer.start(50)  # 20 FPS

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
        
        # Set cursor
        self.graph_view.setCursor(Qt.CrossCursor)
        
        # Connect mouse events
        self.graph_view.mousePressEvent = self.handle_click

    def handle_click(self, event):
        """Handle all mouse clicks in the graph view"""
        # Debug output
        self.graph_view.print_click_debug(event.pos())
        
        scene_pos = self.graph_view.mapToScene(event.pos())
        items = self.graph_view.scene.items(scene_pos)
        
        if event.button() == Qt.LeftButton:
            for item in items:
                # Select robot
                if hasattr(item, 'robot'):
                    self.select_robot(item.robot)
                    break
                    
                # Assign destination to selected robot
                elif (isinstance(item, QGraphicsEllipseItem) and 
                      item.data(1) == "vertex" and 
                      self.selected_robot):
                    self.assign_destination(item.data(0))
                    break
                    
                # Spawn new robot
                elif (isinstance(item, QGraphicsEllipseItem) and 
                      item.data(1) == "vertex"):
                    self.spawn_robot_at_item(item)
                    break
        
        # Forward event to base class
        QGraphicsView.mousePressEvent(self.graph_view, event)

    def select_robot(self, robot):
        """Select a robot for task assignment"""
        # Deselect current robot
        if self.selected_robot:
            self.selected_robot.graphics_item.setPen(QPen(Qt.black, 1))
        
        # Select new robot
        self.selected_robot = robot
        robot.graphics_item.setPen(QPen(Qt.yellow, 3))  # Yellow border for selection
        self.status_bar.showMessage(f"Selected {robot.robot_id}", 2000)

    def spawn_robot_at_item(self, item):
        """Create new robot at clicked vertex"""
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
        
        # Store reference in graphics item
        robot.graphics_item.robot = robot
        
        # Update status
        self.status_bar.showMessage(f"Spawned {robot.robot_id} at Node {node_id}", 3000)

    def assign_destination(self, target_node_id):
        """Assign navigation task to selected robot"""
        if not self.selected_robot:
            return
            
        start_node = self.selected_robot.node_id
        end_node = target_node_id
        
        try:
            # Calculate path using networkx
            node_path = nx.shortest_path(
                self.nav_graph.graph, 
                source=start_node, 
                target=end_node
            )
            
            # Convert to scene coordinates
            scene_path = [
                QPointF(
                    self.nav_graph.graph.nodes[n]["pos"][0] * self.graph_view.scale_factor,
                    -self.nav_graph.graph.nodes[n]["pos"][1] * self.graph_view.scale_factor
                ) for n in node_path[1:]  # Skip current position
            ]
            
            # Assign path to robot
            self.selected_robot.assign_path(scene_path)
            
            # Visual feedback
            self.status_bar.showMessage(
                f"Assigned path to {self.selected_robot.robot_id}: "
                f"Node {start_node} → Node {end_node}",
                3000
            )
            
            # Draw path preview
            self.draw_path_preview(scene_path)
            
        except nx.NetworkXNoPath:
            self.status_bar.showMessage(
                f"No path from Node {start_node} to Node {end_node}",
                5000
            )

    def draw_path_preview(self, path):
        """Show temporary path visualization"""
        # Clear previous preview
        for item in self.graph_view.scene.items():
            if hasattr(item, 'is_path_preview'):
                self.graph_view.scene.removeItem(item)
        
        # Draw new path
        for i in range(len(path)-1):
            line = QGraphicsLineItem(
                path[i].x(), path[i].y(),
                path[i+1].x(), path[i+1].y()
            )
            line.setPen(QPen(Qt.green, 2, Qt.DashLine))
            line.setZValue(5)
            line.is_path_preview = True  # Mark for easy removal
            self.graph_view.scene.addItem(line)

    def update_robot_movements(self):
        """Update all robot positions each frame"""
        needs_update = False
        
        for robot in self.robots:
            if robot.move_step():  # Returns True if movement occurred
                needs_update = True
                
        if needs_update:
            self.graph_view.viewport().update()