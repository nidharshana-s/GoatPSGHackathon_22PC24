from src.models.traffic_manager import TrafficManager

class Robot:
    robot_count = 0
    
    STATUS_IDLE = "IDLE"
    STATUS_MOVING = "MOVING"
    STATUS_WAITING = "WAITING"
    STATUS_CHARGING = "CHARGING"
    STATUS_COMPLETE = "COMPLETE"
    STATUS_BLOCKED = "BLOCKED"  # New status for when robot is blocked by traffic

    def __init__(self, x, y):
        Robot.robot_count += 1
        self.id = f"R{Robot.robot_count}"
        self.x = x
        self.y = y
        self.status = self.STATUS_IDLE
        self.previous_status = self.STATUS_IDLE
        self.current_vertex = None
        self.destination_vertex = None
        self.path = []
        self.original_path_length = 0  # Store original path length
        self.speed = 2  # pixels per update
        self.wait_time = 0
        self.previous_location = None
        self.initial_location = None  # Store the initial spawn location
        self.source_vertex = None  # Store the source vertex when task is assigned
        self.has_moved_from_spawn = False  # Track if robot has moved from spawn location
        self.spawn_x = x  # Store spawn coordinates
        self.spawn_y = y
        self.has_completed_first_move = False  # Track if first movement is complete
        self.current_lane = None  # Current lane being used
        self.waiting_for_lane = None  # Lane the robot is waiting for
        self.waiting_for_vertex = None  # Vertex the robot is waiting for
        self.blocked_reason = None  # Reason for being blocked

    def assign_task(self, destination_vertex, path=None):
        """Assign a navigation task to the robot"""
        self.destination_vertex = destination_vertex
        self.previous_status = self.status
        self.status = self.STATUS_MOVING
        if path:
            self.path = path.copy()  # Make a copy of the path
            # Path length is number of edges (vertices - 1)
            self.original_path_length = len(path) - 1 if len(path) > 0 else 0
            self.source_vertex = self.current_vertex  # Store current vertex as source

    def update(self, traffic_manager: TrafficManager):
        """Update robot state with traffic management"""
        if self.status == self.STATUS_MOVING:
            if self.path:
                # Get next vertex in path
                next_x, next_y = self.path[0]
                next_vertex = self.find_next_vertex(next_x, next_y)
                
                if next_vertex is not None:
                    # Request permission to use the lane
                    if self.current_vertex is not None:
                        lane = (self.current_vertex, next_vertex)
                        if not traffic_manager.request_lane(self.id, self.current_vertex, next_vertex):
                            self.status = self.STATUS_BLOCKED
                            self.waiting_for_lane = lane
                            self.blocked_reason = f"Lane {lane} is occupied"
                            traffic_manager.log_collision(self.id, f"Lane {lane}", "WAITING")
                            return
                    
                    # Request permission to occupy next vertex
                    if not traffic_manager.request_vertex(self.id, next_vertex):
                        self.status = self.STATUS_BLOCKED
                        self.waiting_for_vertex = next_vertex
                        self.blocked_reason = f"Vertex {next_vertex} is occupied"
                        traffic_manager.log_collision(self.id, f"Vertex {next_vertex}", "WAITING")
                        return
                
                # Move towards next point in path
                dx = next_x - self.x
                dy = next_y - self.y
                distance = (dx**2 + dy**2)**0.5
                
                if distance < self.speed:
                    # Release previous vertex if exists
                    if self.current_vertex is not None:
                        traffic_manager.release_vertex(self.id, self.current_vertex)
                    
                    # Release previous lane if exists
                    if self.current_lane is not None:
                        traffic_manager.release_lane(self.id, self.current_lane[0], self.current_lane[1])
                    
                    self.previous_location = (self.x, self.y)
                    self.x = next_x
                    self.y = next_y
                    self.current_vertex = next_vertex
                    self.current_lane = (self.current_vertex, next_vertex)
                    
                    if not self.has_moved_from_spawn and (self.x != self.spawn_x or self.y != self.spawn_y):
                        self.has_moved_from_spawn = True
                    
                    self.path.pop(0)
                    if not self.path:
                        self.previous_status = self.status
                        self.status = self.STATUS_COMPLETE
                        if not self.has_completed_first_move:
                            self.has_completed_first_move = True
                else:
                    self.x += (dx/distance) * self.speed
                    self.y += (dy/distance) * self.speed
                    if not self.has_moved_from_spawn and (abs(self.x - self.spawn_x) > self.speed or abs(self.y - self.spawn_y) > self.speed):
                        self.has_moved_from_spawn = True
            else:
                self.previous_status = self.status
                self.status = self.STATUS_COMPLETE
                if not self.has_completed_first_move:
                    self.has_completed_first_move = True
        elif self.status == self.STATUS_WAITING:
            if self.wait_time > 0:
                self.wait_time -= 1
            else:
                self.previous_status = self.status
                self.status = self.STATUS_MOVING
        elif self.status == self.STATUS_BLOCKED:
            # Check if we can proceed
            if self.waiting_for_lane:
                if traffic_manager.request_lane(self.id, self.waiting_for_lane[0], self.waiting_for_lane[1]):
                    self.status = self.STATUS_MOVING
                    self.waiting_for_lane = None
                    self.blocked_reason = None
            elif self.waiting_for_vertex:
                if traffic_manager.request_vertex(self.id, self.waiting_for_vertex):
                    self.status = self.STATUS_MOVING
                    self.waiting_for_vertex = None
                    self.blocked_reason = None
        elif self.status == self.STATUS_COMPLETE:
            # Release any remaining resources
            if self.current_vertex is not None:
                traffic_manager.release_vertex(self.id, self.current_vertex)
            if self.current_lane is not None:
                traffic_manager.release_lane(self.id, self.current_lane[0], self.current_lane[1])
            
            self.destination_vertex = None
            self.previous_status = self.status
            self.status = self.STATUS_IDLE

    def find_next_vertex(self, x, y):
        """Find the vertex ID for given coordinates"""
        # This should be implemented based on your graph structure
        # For now, return None as placeholder
        return None

    def has_moved(self):
        """Check if robot has moved to a new location"""
        if self.previous_location:
            return (self.x, self.y) != self.previous_location
        return False

    def has_status_changed(self):
        """Check if robot's status has changed"""
        return self.status != self.previous_status

    def set_initial_location(self, vertex):
        """Set the initial spawn location of the robot"""
        self.initial_location = vertex
        self.current_vertex = vertex  # Also set as current vertex

    def get_path_length(self):
        """Get the original path length"""
        return self.original_path_length

    def should_be_removed(self):
        """Check if robot should be removed"""
        return self.has_completed_first_move and self.status == self.STATUS_IDLE

    def get_status_details(self):
        """Get detailed status information"""
        details = {
            'id': self.id,
            'status': self.status,
            'current_vertex': self.current_vertex,
            'destination_vertex': self.destination_vertex,
            'waiting_for_lane': self.waiting_for_lane,
            'waiting_for_vertex': self.waiting_for_vertex,
            'blocked_reason': self.blocked_reason
        }
        return details
