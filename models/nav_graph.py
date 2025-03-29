import json
import networkx as nx

class NavGraph:
    def __init__(self, json_path):
        with open(json_path) as f:
            self.data = json.load(f)
        self.graph = nx.Graph()
        self.build_graph()

    def build_graph(self):
        # Add vertices (nodes)
        vertices = self.data["levels"]["level1"]["vertices"]
        for idx, (x, y, attrs) in enumerate(vertices):
            self.graph.add_node(idx, pos=(x, y), **attrs)

        # Add lanes (edges)
        lanes = self.data["levels"]["level1"]["lanes"]
        for start, end, attrs in lanes:
            self.graph.add_edge(start, end, **attrs)

    def get_shortest_path(self, start, end):
        return nx.shortest_path(self.graph, start, end)