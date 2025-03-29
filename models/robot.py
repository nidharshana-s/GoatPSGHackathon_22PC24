from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen, QFont

class Robot:
    _instances = []  # Class variable to track all robot instances
    _next_id = 0     # Class variable to track IDs
    
    def __init__(self, node_id, x, y, scale_factor=50.0):
        self.node_id = node_id
        self.robot_id = f"robot_{Robot._next_id}"
        Robot._next_id += 1
        Robot._instances.append(self)
        
        # Position handling (scaled and y-inverted)
        self.x = x * scale_factor
        self.y = -y * scale_factor
        
        # Create visual elements
        self.graphics_item = QGraphicsEllipseItem(
            self.x - 8,  # x-position (center - offset)
            self.y - 8,  # y-position (center - offset)
            16,         # width
            16          # height
        )
        
        self.label = QGraphicsTextItem(self.robot_id)
        
        # Configure appearance
        self._setup_appearance()
    
    def _setup_appearance(self):
        """Initialize all visual properties"""
        # Configure robot circle
        self.graphics_item.setBrush(QBrush(self._assign_color()))
        self.graphics_item.setPen(QPen(Qt.black, 1))  # 1px black border
        self.graphics_item.setZValue(2)  # Render above lanes
        
        # Configure ID label
        self.label.setPos(self.x + 10, self.y - 10)  # Positioned to right of robot
        self.label.setFont(QFont("Arial", 8))
        self.label.setDefaultTextColor(Qt.black)
        self.label.setZValue(3)  # Render above robot
        
        # Ensure visible against background
        self.label.setOpacity(0.9)
    
    def _assign_color(self):
        """Returns a unique color for each robot"""
        colors = [
            QColor(255, 0, 0),    # Red
            QColor(0, 150, 0),    # Dark Green
            QColor(0, 0, 255),    # Blue
            QColor(255, 165, 0),  # Orange
            QColor(128, 0, 128),  # Purple
            QColor(0, 255, 255)   # Cyan
        ]
        return colors[len(Robot._instances) % len(colors)]