import tkinter as tk
from tkinter import Canvas, Frame, Label, Button, Listbox, messagebox
from src.models.nav_graph import NavGraph
from src.models.robot import Robot
from src.models.traffic_manager import TrafficManager
from src.utils.logger import RobotLogger
import random
import time

class FleetGUI:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
        self.logger = RobotLogger()  # Initialize logger
        self.traffic_manager = TrafficManager()  # Initialize traffic manager
        
        # Define color scheme
        self.colors = {
            'background': '#F0F2F5',  # Light gray background
            'side_panel': '#FFFFFF',   # White side panel
            'text': '#1A1A1A',         # Dark gray text
            'primary': '#2196F3',      # Blue primary color
            'secondary': '#FFC107',    # Amber secondary color
            'success': '#4CAF50',      # Green success color
            'warning': '#FF9800',      # Orange warning color
            'danger': '#F44336',       # Red danger color
            'graph_edge': '#BDBDBD',   # Light gray for graph edges
            'graph_vertex': '#E3F2FD', # Light blue for vertices
            'graph_vertex_outline': '#1976D2',  # Dark blue for vertex outlines
            'robot_default': '#9C27B0', # Purple for default robot color
            'highlight': '#FFD700',     # Gold for highlighting
            'title_bg': '#1976D2',      # Dark blue for title bar
            'title_text': '#FFFFFF',    # White text for title
            'hover': '#E3F2FD',         # Light blue for hover effects
            'border': '#E0E0E0',        # Light gray for borders
            'blocked': '#FF5722',       # Deep orange for blocked robots
            'occupied': '#9E9E9E'       # Gray for occupied lanes/vertices
        }
        
        # Create title bar
        self.title_bar = Frame(root, bg=self.colors['title_bg'], height=40)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)
        self.title_bar.pack_propagate(False)
        Label(self.title_bar, 
              text="Fleet Management System", 
              font=("Arial", 14, "bold"),
              bg=self.colors['title_bg'],
              fg=self.colors['title_text']).pack(pady=8)
        
        # Create main container
        self.main_container = Frame(root, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas setup
        self.canvas_width = 800  
        self.canvas_height = 600  
        self.canvas = Canvas(self.main_container, 
                           width=self.canvas_width, 
                           height=self.canvas_height, 
                           bg=self.colors['background'], 
                           highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Side panel setup with border
        self.side_panel = Frame(self.main_container, 
                              width=250, 
                              bg=self.colors['side_panel'],
                              highlightthickness=1,
                              highlightbackground=self.colors['border'])
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.side_panel.pack_propagate(False)
        
        # Robot Info Section with border
        self.info_section = Frame(self.side_panel, 
                                bg=self.colors['side_panel'],
                                highlightthickness=1,
                                highlightbackground=self.colors['border'])
        self.info_section.pack(fill=tk.X, padx=10, pady=5)
        
        # Section title with modern styling
        Label(self.info_section, 
              text="Robot Information", 
              font=("Arial", 12, "bold"), 
              bg=self.colors['side_panel'],
              fg=self.colors['text']).pack(pady=5)
        
        # Robot info display
        self.robot_info_frame = Frame(self.info_section, bg=self.colors['side_panel'])
        self.robot_info_frame.pack(fill=tk.X)
        
        # Initialize robot info labels
        self.info_labels = {}
        self.create_info_labels()
        
        # Robot List Section with border
        self.list_section = Frame(self.side_panel, 
                                bg=self.colors['side_panel'],
                                highlightthickness=1,
                                highlightbackground=self.colors['border'])
        self.list_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Section title with modern styling
        Label(self.list_section, 
              text="Available Robots", 
              font=("Arial", 12, "bold"), 
              bg=self.colors['side_panel'],
              fg=self.colors['text']).pack(pady=5)
        
        # Robot listbox with custom style and hover effect
        self.robot_listbox = Listbox(self.list_section, 
                                   font=("Arial", 10),
                                   bg=self.colors['side_panel'],
                                   fg=self.colors['text'],
                                   selectmode=tk.SINGLE,
                                   selectbackground=self.colors['primary'],
                                   selectforeground='white',
                                   highlightthickness=0,
                                   activestyle='none')
        self.robot_listbox.pack(fill=tk.BOTH, expand=True)
        self.robot_listbox.bind('<<ListboxSelect>>', self.on_select_robot_from_list)
        self.robot_listbox.bind('<Enter>', lambda e: self.robot_listbox.config(bg=self.colors['hover']))
        self.robot_listbox.bind('<Leave>', lambda e: self.robot_listbox.config(bg=self.colors['side_panel']))
        
        # Delete button with hover effect
        self.delete_button = Button(self.list_section, 
                                  text="Delete Selected Robot",
                                  command=self.delete_selected_robot,
                                  bg=self.colors['danger'],
                                  fg='white',
                                  font=("Arial", 10),
                                  relief=tk.FLAT,
                                  padx=10,
                                  pady=5,
                                  cursor="hand2")
        self.delete_button.pack(pady=5)
        self.delete_button.bind('<Enter>', lambda e: self.delete_button.config(bg='#D32F2F'))
        self.delete_button.bind('<Leave>', lambda e: self.delete_button.config(bg=self.colors['danger']))
        
        # Add Traffic Info Section
        self.traffic_section = Frame(self.side_panel, 
                                   bg=self.colors['side_panel'],
                                   highlightthickness=1,
                                   highlightbackground=self.colors['border'])
        self.traffic_section.pack(fill=tk.X, padx=10, pady=5)
        
        Label(self.traffic_section, 
              text="Traffic Information", 
              font=("Arial", 12, "bold"), 
              bg=self.colors['side_panel'],
              fg=self.colors['text']).pack(pady=5)
        
        # Traffic info display
        self.traffic_info_frame = Frame(self.traffic_section, bg=self.colors['side_panel'])
        self.traffic_info_frame.pack(fill=tk.X)
        
        # Initialize traffic info labels
        self.traffic_labels = {}
        self.create_traffic_labels()
        
        # Notification system
        self.notifications = []
        self.notification_window = None
        self.last_notification_time = 0
        self.notification_cooldown = 3  # seconds
        
        # Rest of the initialization
        self.robots = []
        self.vertex_map = {}
        self.margin = 50 
        self.scale_factor, self.offset_x, self.offset_y = self.calculate_scaling()
        self.selected_robot = None
        self.robot_colors = {}
        self.draw_graph()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.update_robots()

    def create_info_labels(self):
        """Create labels for robot information display"""
        fields = ['ID', 'Status', 'Current Location', 'Destination', 'Path Length']
        for field in fields:
            frame = Frame(self.robot_info_frame, bg=self.colors['side_panel'])
            frame.pack(fill=tk.X, pady=2)
            
            Label(frame, text=f"{field}:", 
                  font=("Arial", 10, "bold"), 
                  bg=self.colors['side_panel'],
                  fg=self.colors['text']).pack(side=tk.LEFT)
            label = Label(frame, text="--", 
                         font=("Arial", 10), 
                         bg=self.colors['side_panel'],
                         fg=self.colors['text'])
            label.pack(side=tk.LEFT, padx=5)
            self.info_labels[field] = label

    def create_traffic_labels(self):
        """Create labels for traffic information display"""
        fields = ['Occupied Lanes', 'Waiting Robots', 'Blocked Robots']
        for field in fields:
            frame = Frame(self.traffic_info_frame, bg=self.colors['side_panel'])
            frame.pack(fill=tk.X, pady=2)
            
            Label(frame, text=f"{field}:", 
                  font=("Arial", 10, "bold"), 
                  bg=self.colors['side_panel'],
                  fg=self.colors['text']).pack(side=tk.LEFT)
            label = Label(frame, text="0", 
                         font=("Arial", 10), 
                         bg=self.colors['side_panel'],
                         fg=self.colors['text'])
            label.pack(side=tk.LEFT, padx=5)
            self.traffic_labels[field] = label

    def update_robot_info(self):
        """Update the side panel with robot information"""
        if self.selected_robot:
            robot = self.selected_robot
            current_vertex = self.find_nearest_vertex(robot.x, robot.y)
            current_name = self.graph.vertices[current_vertex][2] if current_vertex is not None else "Moving"
            
            dest_vertex = robot.destination_vertex
            dest_name = self.graph.vertices[dest_vertex][2] if dest_vertex is not None else "None"
            
            self.info_labels['ID'].config(text=robot.id)
            self.info_labels['Status'].config(text=robot.status)
            self.info_labels['Current Location'].config(text=current_name)
            self.info_labels['Destination'].config(text=dest_name)
            self.info_labels['Path Length'].config(text=str(robot.get_path_length()))
            
            # Update colors based on status
            status_color = {
                Robot.STATUS_IDLE: self.colors['success'],
                Robot.STATUS_MOVING: self.colors['primary'],
                Robot.STATUS_WAITING: self.colors['warning'],
                Robot.STATUS_CHARGING: self.colors['secondary'],
                Robot.STATUS_COMPLETE: '#9E9E9E'  # Gray
            }
            self.info_labels['Status'].config(fg=status_color.get(robot.status, self.colors['text']))
        else:
            for label in self.info_labels.values():
                label.config(text="--")

    def calculate_scaling(self):
        """ Calculate scaling factors to fit the graph within the canvas """
        min_x = min(v[0] for v in self.graph.vertices)
        max_x = max(v[0] for v in self.graph.vertices)
        min_y = min(v[1] for v in self.graph.vertices)
        max_y = max(v[1] for v in self.graph.vertices)

        graph_width = max_x - min_x
        graph_height = max_y - min_y

        scale_x = (self.canvas_width - 2 * self.margin) / graph_width if graph_width > 0 else 1
        scale_y = (self.canvas_height - 2 * self.margin) / graph_height if graph_height > 0 else 1
        scale = min(scale_x, scale_y)  

        offset_x = (self.canvas_width - (graph_width * scale)) / 2 - (min_x * scale)
        offset_y = (self.canvas_height - (graph_height * scale)) / 2 - (min_y * scale)

        return scale, offset_x, offset_y

    def transform_coordinates(self, x, y):
        """ Apply scaling and centering transformations """
        screen_x = x * self.scale_factor + self.offset_x
        screen_y = y * self.scale_factor + self.offset_y
        return screen_x, screen_y

    def draw_graph(self):
        # First create all vertex mappings
        for i, (x, y, name) in enumerate(self.graph.vertices):
            screen_x, screen_y = self.transform_coordinates(x, y)
            self.vertex_map[i] = (screen_x, screen_y)

        # Draw lanes first with traffic information
        for start, end in self.graph.lanes:
            x1, y1 = self.vertex_map[start]
            x2, y2 = self.vertex_map[end]
            
            # Check if lane is occupied
            lane = (start, end)
            if lane in self.traffic_manager.get_occupied_lanes():
                self.canvas.create_line(x1, y1, x2, y2, 
                                      fill=self.colors['occupied'], 
                                      width=3)
            else:
                self.canvas.create_line(x1, y1, x2, y2, 
                                      fill=self.colors['graph_edge'], 
                                      width=2)

        # Draw vertices with traffic information
        for i, (x, y, name) in enumerate(self.graph.vertices):
            screen_x, screen_y = self.vertex_map[i]
            
            # Check if vertex is occupied
            if i in self.traffic_manager.get_occupied_vertices():
                self.canvas.create_oval(screen_x - 8, screen_y - 8, 
                                      screen_x + 8, screen_y + 8, 
                                      fill=self.colors['occupied'], 
                                      outline=self.colors['graph_vertex_outline'])
            else:
                self.canvas.create_oval(screen_x - 8, screen_y - 8, 
                                      screen_x + 8, screen_y + 8, 
                                      fill=self.colors['graph_vertex'], 
                                      outline=self.colors['graph_vertex_outline'])
            
            # Draw vertex name with background
            text = self.canvas.create_text(screen_x, screen_y - 15, 
                                         text=name, 
                                         font=("Arial", 10, "bold"),
                                         fill=self.colors['text'])
            bbox = self.canvas.bbox(text)
            if bbox:
                self.canvas.create_rectangle(bbox[0]-2, bbox[1]-2, 
                                          bbox[2]+2, bbox[3]+2, 
                                          fill=self.colors['background'], 
                                          outline='')
                self.canvas.tag_raise(text)

    def get_random_color(self):
        """ Generate a random pastel color """
        colors = [
            '#FFB3BA',  # Pastel Pink
            '#BAFFC9',  # Pastel Green
            '#BAE1FF',  # Pastel Blue
            '#FFFFBA',  # Pastel Yellow
            '#FFE4BA',  # Pastel Orange
            '#E8BAFF',  # Pastel Purple
            '#BAE1FF',  # Pastel Sky Blue
            '#FFD1BA',  # Pastel Coral
        ]
        return random.choice(colors)

    def handle_click(self, event):
        # Check if clicked on a robot
        for robot in self.robots:
            if abs(event.x - robot.x) < 10 and abs(event.y - robot.y) < 10:
                self.select_robot(robot)
                return

        # Check if clicked on a vertex
        for i, (screen_x, screen_y) in self.vertex_map.items():
            if abs(event.x - screen_x) < 10 and abs(event.y - screen_y) < 10:
                if self.selected_robot:
                    self.assign_task(self.selected_robot, i)
                else:
                    self.spawn_robot(screen_x, screen_y)
                break

    def spawn_robot(self, x, y):
        robot = Robot(x, y)
        self.robots.append(robot)
        self.robot_colors[robot.id] = self.get_random_color()
        
        # Draw robot with unique color and status indicator
        self.canvas.create_oval(robot.x - 8, robot.y - 8, robot.x + 8, robot.y + 8, 
                              fill=self.robot_colors[robot.id], 
                              outline='black',
                              tags=f"robot_{robot.id}")
        
        # Add status indicator dot
        status_color = {
            Robot.STATUS_IDLE: self.colors['success'],
            Robot.STATUS_MOVING: self.colors['primary'],
            Robot.STATUS_WAITING: self.colors['warning'],
            Robot.STATUS_CHARGING: self.colors['secondary'],
            Robot.STATUS_COMPLETE: '#9E9E9E'
        }
        self.canvas.create_oval(robot.x - 3, robot.y - 3, robot.x + 3, robot.y + 3,
                              fill=status_color.get(robot.status, self.colors['text']),
                              outline='white',
                              tags=f"status_dot_{robot.id}")
        
        # Draw robot ID with modern styling
        text = self.canvas.create_text(robot.x, robot.y - 15, 
                                     text=robot.id, 
                                     font=("Arial", 8, "bold"),
                                     fill=self.colors['text'],
                                     tags=f"text_{robot.id}")
        bbox = self.canvas.bbox(text)
        if bbox:
            self.canvas.create_rectangle(bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2, 
                                      fill=self.colors['side_panel'], 
                                      outline=self.colors['border'],
                                      tags=f"background_{robot.id}")
            self.canvas.tag_raise(text)
            self.canvas.tag_raise(f"status_dot_{robot.id}")
        
        # Log robot spawn
        current_vertex = self.find_nearest_vertex(x, y)
        if current_vertex is not None:
            location = self.graph.vertices[current_vertex][2]
            robot.set_initial_location(current_vertex)
            self.logger.log_robot_spawn(robot.id, location)
        else:
            self.logger.log_robot_spawn(robot.id, "Unknown Location")

    def select_robot(self, robot):
        self.selected_robot = robot
        # Highlight selected robot with a glowing effect
        self.canvas.create_oval(robot.x - 12, robot.y - 12, 
                              robot.x + 12, robot.y + 12, 
                              outline=self.colors['highlight'], 
                              width=2)
        self.canvas.create_oval(robot.x - 14, robot.y - 14, 
                              robot.x + 14, robot.y + 14, 
                              outline=self.colors['highlight'], 
                              width=1)
        self.update_robot_info()

    def assign_task(self, robot, destination_vertex):
        """Assign a navigation task to the selected robot"""
        if robot.status == Robot.STATUS_IDLE:
            # Calculate path using navigation graph
            start_vertex = self.find_nearest_vertex(robot.x, robot.y)
            if start_vertex is not None and destination_vertex is not None:
                path = self.graph.find_path(start_vertex, destination_vertex)
                if path:
                    # Convert path vertices to screen coordinates
                    screen_path = [self.vertex_map[v] for v in path]
                    # Assign task with path
                    robot.assign_task(destination_vertex, screen_path)
                else:
                    robot.status = Robot.STATUS_WAITING
                    robot.wait_time = 30  # Wait for 3 seconds
        self.selected_robot = None
        # Remove highlight
        self.canvas.create_oval(robot.x - 10, robot.y - 10, robot.x + 10, robot.y + 10, 
                              outline='black', width=1)
        self.update_robot_info()

    def find_nearest_vertex(self, x, y):
        """Find the nearest vertex to given coordinates"""
        min_dist = float('inf')
        nearest_vertex = None
        for i, (vx, vy) in self.vertex_map.items():
            dist = ((x - vx)**2 + (y - vy)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                nearest_vertex = i
        return nearest_vertex

    def update_robot_list(self):
        """Update the robot list in the side panel"""
        self.robot_listbox.delete(0, tk.END)
        for robot in self.robots:
            current_vertex = self.find_nearest_vertex(robot.x, robot.y)
            location = self.graph.vertices[current_vertex][2] if current_vertex is not None else "Unknown"
            self.robot_listbox.insert(tk.END, f"{robot.id} - {location} - {robot.status}")

    def on_select_robot_from_list(self, event):
        """Handle robot selection from the list"""
        selection = self.robot_listbox.curselection()
        if selection:
            index = selection[0]
            selected_robot = self.robots[index]
            self.select_robot(selected_robot)

    def delete_selected_robot(self):
        """Delete the selected robot"""
        if self.selected_robot:
            # Remove all visual elements of the robot
            self.canvas.delete(f"robot_{self.selected_robot.id}")
            self.canvas.delete(f"status_dot_{self.selected_robot.id}")
            self.canvas.delete(f"status_{self.selected_robot.id}")
            self.canvas.delete(f"highlight_{self.selected_robot.id}")
            self.canvas.delete(f"background_{self.selected_robot.id}")
            self.canvas.delete(f"text_{self.selected_robot.id}")
            
            # Remove from lists and dictionaries
            self.robots.remove(self.selected_robot)
            del self.robot_colors[self.selected_robot.id]
            
            # Clear selection
            self.selected_robot = None
            self.update_robot_info()
            self.update_robot_list()

    def show_notification(self, message, level="info"):
        """Show a notification message"""
        current_time = time.time()
        if current_time - self.last_notification_time < self.notification_cooldown:
            return
            
        self.last_notification_time = current_time
        
        # Create notification window
        if self.notification_window:
            self.notification_window.destroy()
            
        self.notification_window = tk.Toplevel(self.root)
        self.notification_window.overrideredirect(True)  # Remove window decorations
        
        # Position window at top-right corner
        x = self.root.winfo_x() + self.root.winfo_width() - 300
        y = self.root.winfo_y() + 50
        self.notification_window.geometry(f"300x100+{x}+{y}")
        
        # Configure colors based on level
        colors = {
            "info": (self.colors['primary'], 'white'),
            "warning": (self.colors['warning'], 'white'),
            "error": (self.colors['danger'], 'white')
        }
        bg_color, fg_color = colors.get(level, colors["info"])
        
        # Create notification content
        frame = Frame(self.notification_window, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True)
        
        Label(frame, 
              text=message,
              font=("Arial", 10),
              bg=bg_color,
              fg=fg_color,
              wraplength=280).pack(pady=10)
        
        # Auto-close after 3 seconds
        self.notification_window.after(3000, self.notification_window.destroy)

    def update_traffic_info(self):
        """Update traffic information display"""
        occupied_lanes = len(self.traffic_manager.get_occupied_lanes())
        waiting_robots = len(self.traffic_manager.get_waiting_robots())
        blocked_robots = sum(1 for robot in self.robots if robot.status == Robot.STATUS_BLOCKED)
        
        self.traffic_labels['Occupied Lanes'].config(text=str(occupied_lanes))
        self.traffic_labels['Waiting Robots'].config(text=str(waiting_robots))
        self.traffic_labels['Blocked Robots'].config(text=str(blocked_robots))

    def update_robots(self):
        """Update robot positions and statuses"""
        for robot in self.robots:
            # Store previous position for movement detection
            prev_x, prev_y = robot.x, robot.y
            
            # Update robot state with traffic manager
            robot.update(self.traffic_manager)
            
            # Check for status changes and show notifications
            if robot.has_status_changed():
                if robot.status == Robot.STATUS_BLOCKED:
                    self.show_notification(f"Robot {robot.id} is blocked: {robot.blocked_reason}", "warning")
                elif robot.status == Robot.STATUS_COMPLETE:
                    self.show_notification(f"Robot {robot.id} completed its task", "info")
            
            # Update robot visualization
            self.canvas.delete(f"robot_{robot.id}")
            self.canvas.delete(f"status_dot_{robot.id}")
            
            # Draw robot with status-based color
            robot_color = self.robot_colors[robot.id]
            if robot.status == Robot.STATUS_BLOCKED:
                robot_color = self.colors['blocked']
            
            self.canvas.create_oval(robot.x - 8, robot.y - 8, robot.x + 8, robot.y + 8, 
                                  fill=robot_color, 
                                  outline='black',
                                  tags=f"robot_{robot.id}")
            
            # Update status indicator dot
            status_color = {
                Robot.STATUS_IDLE: self.colors['success'],
                Robot.STATUS_MOVING: self.colors['primary'],
                Robot.STATUS_WAITING: self.colors['warning'],
                Robot.STATUS_CHARGING: self.colors['secondary'],
                Robot.STATUS_COMPLETE: '#9E9E9E',
                Robot.STATUS_BLOCKED: self.colors['blocked']
            }
            self.canvas.create_oval(robot.x - 3, robot.y - 3, robot.x + 3, robot.y + 3,
                                  fill=status_color.get(robot.status, self.colors['text']),
                                  outline='white',
                                  tags=f"status_dot_{robot.id}")
            
            # Update status text
            status_text = f"{robot.id} - {robot.status}"
            if robot.blocked_reason:
                status_text += f" ({robot.blocked_reason})"
            
            self.canvas.delete(f"text_{robot.id}")
            self.canvas.delete(f"background_{robot.id}")
            
            text = self.canvas.create_text(robot.x, robot.y - 15, 
                                         text=status_text,
                                         font=("Arial", 8, "bold"),
                                         fill=self.colors['text'],
                                         tags=f"text_{robot.id}")
            bbox = self.canvas.bbox(text)
            if bbox:
                self.canvas.create_rectangle(bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2,
                                          fill=self.colors['side_panel'],
                                          outline=self.colors['border'],
                                          tags=f"background_{robot.id}")
                self.canvas.tag_raise(text)
                self.canvas.tag_raise(f"status_dot_{robot.id}")

        # Update traffic information
        self.update_traffic_info()
        
        # Update side panel information
        self.update_robot_info()
        self.update_robot_list()

        # Schedule next update
        self.root.after(100, self.update_robots)
