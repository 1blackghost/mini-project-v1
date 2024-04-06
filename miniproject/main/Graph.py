import networkx as nx
import string
import random

class MallNavigator:

    def __init__(self):
        self.graph = nx.Graph()
        original_width = 350
        original_height = 400

        new_width = 300
        new_height = 490

        width_ratio = new_width / original_width
        height_ratio = new_height / original_height

        data = {
            "entrance": (330, 32, 0),
            "c1": (202, 37, 0),
            "c2": (190, 100, 0),
            "c3": (190, 136, 0),
            "c4": (190, 176, 0),
            "c5": (190, 207, 0),
            "c5": (190, 245, 0),
            "c6": (190, 278, 0),
            "vegetables": (92, 100, 0),
            "cleaning":(300,102,0),
            "dairy":(102,137,0),
            "beverage":(280,136,0),
            "fruits":(108,173,0),
            "snacks":(289,175,0),
            "clothes":(100,206,0),
            "waiting":(272,206,0),
            "hardware":(80,240,0),
            "stationary":(272,246,0),
            "food":(109,275,0),
            "electronics":(302,279,0),
            "c7":(190,278,0),
            "ec":(190,203,0),
        }

        self.data = {}

        for key, value in data.items():
            resized_x = int(value[0] * width_ratio)
            resized_y = int(value[1] * height_ratio)
            self.data[key] = (resized_x, resized_y, value[2])

        for key, value in self.data.items():
            print(f"{key}: {value}")


    def add_location(self, name, x, y, z):
        self.graph.add_node(name, pos=(int(x), int(y), int(z)))

    def add_connection(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def create_connections(self):
        for name, coordinates in self.data.items():
            self.add_location(name, coordinates[0], coordinates[1], coordinates[2])
        self.add_connection("entrance", "c1") 
        self.add_connection("c1", "c2") 
        self.add_connection("c2", "c3") 
        self.add_connection("c3", "c4") 
        self.add_connection("c4", "c5") 
        self.add_connection("c5", "c6") 
        self.add_connection("c4","ec")
        self.add_connection("ec","c5")
        self.add_connection("c6", "c7") 
        self.add_connection("c2", "vegetables")
        self.add_connection("c2", "cleaning")  
        self.add_connection("c3", "dairy")  
        self.add_connection("c3", "beverage") 
        self.add_connection("c4", "fruits")  
        self.add_connection("c4", "snacks") 
        self.add_connection("ec", "clothes")  
        self.add_connection("ec", "waiting") 
        self.add_connection("c5", "hardware")  
        self.add_connection("c5", "stationary") 
        self.add_connection("c6", "food")  
        self.add_connection("c6", "electronics")

        
            
    
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