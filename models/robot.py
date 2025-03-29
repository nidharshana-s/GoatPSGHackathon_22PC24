from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen

class Robot:
    def __init__(self, node_id, x, y, scale_factor=50.0):
        self.node_id = node_id
        self.x = x * scale_factor
        self.y = -y * scale_factor  # Invert y-axis
        self.status = "idle"
        self.scale_factor = scale_factor
        
        # Visual representation
        self.graphics_item = QGraphicsEllipseItem(
            self.x - 8, 
            self.y - 8, 
            16, 16
        )
        self.graphics_item.setBrush(QBrush(self.assign_color()))
        self.graphics_item.setPen(QPen(Qt.black, 1))
        self.graphics_item.setData(0, "robot")
        self.graphics_item.setZValue(2)  # Above other items
        
    def assign_color(self):
        colors = [
            QColor(255, 215, 0),   # Gold
            QColor(0, 255, 127),   # SpringGreen
            QColor(138, 43, 226),  # BlueViolet
            QColor(255, 69, 0)     # OrangeRed
        ]
        return colors[self.node_id % len(colors)]