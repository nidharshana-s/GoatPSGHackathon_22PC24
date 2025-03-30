from typing import Dict, List, Tuple, Set
import time

class TrafficManager:
    def __init__(self):
        self.occupied_lanes: Dict[Tuple[int, int], List[str]] = {}  # (start, end) -> [robot_ids]
        self.occupied_vertices: Dict[int, str] = {}  # vertex_id -> robot_id
        self.waiting_robots: Dict[str, Tuple[int, int]] = {}  # robot_id -> (start_vertex, end_vertex)
        self.collision_history: List[Tuple[str, str, str, float]] = []  # [(robot_id, location, event_type, timestamp)]
        
    def request_lane(self, robot_id: str, start_vertex: int, end_vertex: int) -> bool:
        """Request permission to use a lane"""
        lane = (start_vertex, end_vertex)
        if lane in self.occupied_lanes:
            # Lane is occupied, add to waiting list
            self.waiting_robots[robot_id] = lane
            return False
        else:
            # Lane is free, mark as occupied
            self.occupied_lanes[lane] = [robot_id]
            return True
            
    def request_vertex(self, robot_id: str, vertex_id: int) -> bool:
        """Request permission to occupy a vertex"""
        if vertex_id in self.occupied_vertices:
            # Vertex is occupied, add to waiting list
            self.waiting_robots[robot_id] = (vertex_id, vertex_id)
            return False
        else:
            # Vertex is free, mark as occupied
            self.occupied_vertices[vertex_id] = robot_id
            return True
            
    def release_lane(self, robot_id: str, start_vertex: int, end_vertex: int):
        """Release a lane after robot has passed through"""
        lane = (start_vertex, end_vertex)
        if lane in self.occupied_lanes:
            if robot_id in self.occupied_lanes[lane]:
                self.occupied_lanes[lane].remove(robot_id)
                if not self.occupied_lanes[lane]:
                    del self.occupied_lanes[lane]
                    
    def release_vertex(self, robot_id: str, vertex_id: int):
        """Release a vertex after robot has left"""
        if vertex_id in self.occupied_vertices and self.occupied_vertices[vertex_id] == robot_id:
            del self.occupied_vertices[vertex_id]
            
    def check_waiting_robots(self) -> List[str]:
        """Check if any waiting robots can proceed"""
        can_proceed = []
        for robot_id, lane in list(self.waiting_robots.items()):
            if lane not in self.occupied_lanes:
                can_proceed.append(robot_id)
                del self.waiting_robots[robot_id]
        return can_proceed
        
    def log_collision(self, robot_id: str, location: str, event_type: str):
        """Log a collision or waiting event"""
        timestamp = time.time()
        self.collision_history.append((robot_id, location, event_type, timestamp))
        
    def get_collision_history(self) -> List[Tuple[str, str, str, float]]:
        """Get the collision history"""
        return self.collision_history
        
    def get_waiting_robots(self) -> Dict[str, Tuple[int, int]]:
        """Get the list of waiting robots and their waiting locations"""
        return self.waiting_robots
        
    def get_occupied_lanes(self) -> Dict[Tuple[int, int], List[str]]:
        """Get the list of occupied lanes"""
        return self.occupied_lanes
        
    def get_occupied_vertices(self) -> Dict[int, str]:
        """Get the list of occupied vertices"""
        return self.occupied_vertices 