import os
import logging
from datetime import datetime
import time

class RobotLogger:
    def __init__(self, log_dir="logs"):
        # Create logs directory if it doesn't exist
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create a new log file for each session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"robot_movements_{timestamp}.log")
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()  # Also print to console
            ]
        )
        self.logger = logging.getLogger("RobotLogger")
        
        self.start_time = time.time()

    def _get_timestamp(self):
        """Get current timestamp in a readable format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def _write_log(self, message):
        """Write a log message to the file"""
        with open(self.log_file, "a") as f:
            f.write(f"[{self._get_timestamp()}] {message}\n")
            
    def log_robot_spawn(self, robot_id, location):
        """Log when a robot is spawned"""
        self._write_log(f"Robot {robot_id} spawned at {location}")

    def log_destination_reached(self, robot_id, source_node, dest_node, path_length):
        """Log when a robot reaches its destination"""
        self._write_log(f"Robot {robot_id} completed journey from {source_node} to {dest_node} (Path Length: {path_length})")
        
    def log_collision(self, robot_id, location, event_type):
        """Log collision or waiting events"""
        self._write_log(f"TRAFFIC: Robot {robot_id} {event_type} at {location}")
        
    def log_lane_occupancy(self, lane, robot_id, action):
        """Log lane occupancy changes"""
        self._write_log(f"TRAFFIC: Lane {lane} {action} by Robot {robot_id}")
        
    def log_vertex_occupancy(self, vertex, robot_id, action):
        """Log vertex occupancy changes"""
        self._write_log(f"TRAFFIC: Vertex {vertex} {action} by Robot {robot_id}")
        
    def log_task_assignment(self, robot_id, destination):
        """Log when a task is assigned to a robot"""
        self._write_log(f"Task assigned to Robot {robot_id}: navigate to {destination}")
        
    def log_robot_status_change(self, robot_id, old_status, new_status, reason=None):
        """Log when a robot's status changes"""
        message = f"Robot {robot_id} status changed from {old_status} to {new_status}"
        if reason:
            message += f" (Reason: {reason})"
        self._write_log(message)
        
    def log_system_start(self):
        """Log system startup"""
        self._write_log("=== Fleet Management System Started ===")
        
    def log_system_end(self):
        """Log system shutdown"""
        duration = time.time() - self.start_time
        self._write_log(f"=== Fleet Management System Ended (Duration: {duration:.2f}s) ===") 