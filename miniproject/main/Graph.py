import networkx as nx
import string
import random

class MallNavigator:
    def __init__(self):
        self.graph = nx.Graph()
        self.data = {"entrance": (12, 12,0), "toilet": (13, 13,0)}

    def add_location(self, name, x, y, z):
        self.graph.add_node(name, pos=(int(x), int(y), int(z)))

    def add_connection(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def create_connections(self):
        for name, coordinates in self.data.items():
            self.add_location(name, coordinates[0], coordinates[1], coordinates[2])
        self.add_connection("entrance", "toilet")


    def find_shortest_path(self, start, destination):
        shortest_path_nodes = nx.dijkstra_path(self.graph, start, destination)
        shortest_path_coordinates = [tuple(self.graph.nodes[node]['pos']) for node in shortest_path_nodes]
        return shortest_path_coordinates

    def find_path(self, start, destination):
        shortest_path = self.find_shortest_path(start, destination)
        return shortest_path

    def calculate_average_time(self, start, destination, average_speed):
        shortest_path = self.find_path(start, destination)
        total_distance = 0
        for i in range(len(shortest_path) - 1):
            current_pos = shortest_path[i]
            next_pos = shortest_path[i + 1]
            distance = ((next_pos[0] - current_pos[0]) ** 2 +
                        (next_pos[1] - current_pos[1]) ** 2 +
                        (next_pos[2] - current_pos[2]) ** 2) ** 0.5
            total_distance += distance

        average_time = total_distance / average_speed
        return average_time


# Example usage:
'''
navigator = MallNavigator()
navigator.create_connections()
start_location = "Entrance Hall"
end_location = "Data Center"
path = navigator.find_path(start_location, end_location)
average_time = navigator.calculate_average_time(start_location, end_location, average_speed=1.5)
print("Shortest Path:", path)
print("Estimated Average Time:", average_time)
'''