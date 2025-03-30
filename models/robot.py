from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QBrush, QColor, QPen, QFont
import math

class Robot:
    _instances = []
    
    def __init__(self, node_id, x, y, scale_factor=50.0):
        self.node_id = node_id
        self.robot_id = f"robot_{len(Robot._instances)}"
        self.scale_factor = scale_factor
        Robot._instances.append(self)
        
        # Movement properties
        self.path = []
        self.speed = 2.0  # pixels per frame
        self.moving = False
        
        # Visual elements
        self._init_visuals(x, y)
    
    def _init_visuals(self, x, y):
        """Initialize visual components"""
        self.graphics_item = QGraphicsEllipseItem(
            x * self.scale_factor - 8,
            -y * self.scale_factor - 8,
            16, 16
        )
        self.label = QGraphicsTextItem(self.robot_id)
        
        # Appearance
        self.graphics_item.setBrush(QBrush(self.assign_color()))
        self.graphics_item.setPen(QPen(Qt.black, 2))
        self.graphics_item.setZValue(10)
        
        self.label.setPos(x * self.scale_factor + 10, -y * self.scale_factor - 10)
        self.label.setFont(QFont("Arial", 8, QFont.Bold))
        self.label.setDefaultTextColor(Qt.white)
        self.label.setZValue(11)
    
    def assign_color(self):
        colors = [
            QColor(255, 0, 0),    # Red
            QColor(0, 150, 0),    # Green
            QColor(0, 0, 255),    # Blue
            QColor(255, 165, 0)   # Orange
        ]
        return colors[len(Robot._instances) % len(colors)]
    
    def assign_path(self, path):
        """Set navigation path"""
        self.path = path
        self.moving = bool(path)
        
    def move_step(self):
        """Move one step along path"""
        if not self.moving or not self.path:
            return False
            
        current_center = QPointF(
            self.graphics_item.rect().x() + 8,
            self.graphics_item.rect().y() + 8
        )
        target_pos = self.path[0]
        
        # Create QLineF for distance calculation
        movement_line = QLineF(current_center, target_pos)
        distance = movement_line.length()
        
        if distance <= self.speed:
            # Reached target point
            self.graphics_item.setRect(
                target_pos.x() - 8,
                target_pos.y() - 8,
                16, 16
            )
            self.path.pop(0)
            if not self.path:
                self.moving = False
            return True
        else:
            # Move toward target
            direction_x = (target_pos.x() - current_center.x()) / distance
            direction_y = (target_pos.y() - current_center.y()) / distance
            
            new_x = current_center.x() + direction_x * self.speed
            new_y = current_center.y() + direction_y * self.speed
            
            self.graphics_item.setRect(
                new_x - 8,
                new_y - 8,
                16, 16
            )
            self.label.setPos(new_x + 10, new_y - 10)
            return True