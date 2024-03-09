import networkx as nx
import string
import random

class MallNavigator:
    def __init__(self):
        self.graph = nx.Graph()
        self.data = {"entrance": (481,757 ,0), 
                     "toilet": (320, 76,0),
                     "food":(383,571,0),
                     "stationary":(269,692,0),
                     "hardware":(271,593,0),
                     "c1":(309,598,0),
                     "clothes":(70,607,0),
                     "fruits":(112,418,0),
                     "waiting room":(390,416,0),
                     "fountain":(458,397,0),
                     "c2":(206,412,0),
                     "vegetables":(190,194,0),
                     "stairs":(312,202,0),
                     "toilet":(315,85,0),
                     "c3":(408,250,0),
                     "c4":(291,246,0),
                     }

    def add_location(self, name, x, y, z):
        self.graph.add_node(name, pos=(int(x), int(y), int(z)))

    def add_connection(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def create_connections(self):
        for name, coordinates in self.data.items():
            self.add_location(name, coordinates[0], coordinates[1], coordinates[2])
        self.add_connection("entrance", "food")
        self.add_connection("entrance", "stationary")
        self.add_connection("entrance", "c1")
        self.add_connection("c1", "stationary")
        self.add_connection("c1", "food")
        self.add_connection("entrance", "hardware")
        self.add_connection("clothes", "hardware")
        self.add_connection("clothes", "fruits")
        self.add_connection("waiting room", "fruits")
        self.add_connection("waiting room", "c1")
        self.add_connection("cloth", "hardware")
        self.add_connection("fountain", "waiting room")
        self.add_connection("cloth", "hardware")
        self.add_connection("c2", "fruits")
        self.add_connection("c2", "waiting room")
        self.add_connection("c2", "vegetables")
        self.add_connection("vegetables", "stairs")
        self.add_connection("stairs", "toilet")
        self.add_connection("c3", "fountain")
        self.add_connection("c4", "c3")
        self.add_connection("c4", "toilet")
        self.add_connection("c4", "stairs")
        self.add_connection("c4", "vegetables")
        self.add_connection("toilet", "vegetables")





        


        

        

        



        


        


        

        

        



        
        
        
        
        


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