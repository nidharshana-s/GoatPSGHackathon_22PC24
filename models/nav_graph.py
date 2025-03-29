import json
import networkx as nx

class NavGraph:
    def __init__(self, json_path):
        with open(json_path) as f:
            self.data = json.load(f)
        self.graph = nx.Graph()
        self.build_graph()

    def build_graph(self):
        
        level_key = next(iter(self.data["levels"]))  
        level_data = self.data["levels"][level_key]
        
        # Add vertices (nodes)
        vertices = level_data["vertices"]
        for idx, (x, y, attrs) in enumerate(vertices):
            self.graph.add_node(idx, pos=(x, y), **attrs)

        # Add lanes (edges)
        lanes = level_data["lanes"]
        for start, end, attrs in lanes:
            self.graph.add_edge(start, end, **attrs)

    def get_shortest_path(self, start, end):
        return nx.shortest_path(self.graph, start, end)