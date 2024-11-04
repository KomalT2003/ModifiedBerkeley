# code1: Berkely failure when master node fails

import random
import time

class BerkeleyAlgorithm:
    def __init__(self, nodes):
        self.nodes = nodes

    def synchronize_clocks(self, master_node_id):
        
        master_node = self.nodes[master_node_id]
        master_time = master_node.get_current_time()

        
        time_diffs = [master_time - node.get_current_time() for node in self.nodes if node.node_id != master_node_id]

        
        avg_time_diff = sum(time_diffs) / len(time_diffs)

        
        master_node.adjust_time(-avg_time_diff)

        
        for node in self.nodes:
            if node.node_id != master_node_id:
                node.set_time(master_node.get_current_time())

    def print_clocks(self):
        for node in self.nodes:
            timestamp = time.strftime("%H:%M:%S:%f", time.localtime(node.get_current_time()))
            print(f"Node {node.node_id}: {timestamp}")

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = time.time() + random.uniform(-5, 5)  # Initialize local clock with random deviation

    def get_current_time(self):
        return self.clock

    def adjust_time(self, time_diff):
        self.clock += time_diff

    def set_time(self, new_time):
        self.clock = new_time

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    nodes = [Node(i) for i in range(num_nodes)]

    master_node_id = int(input(f"Enter the master node ID (0 to {num_nodes - 1}): "))
    if master_node_id < 0 or master_node_id >= num_nodes:
        print("Invalid master node ID.")
        exit()


    algorithm = BerkeleyAlgorithm(nodes)
    print("\n-------------- Initial Clock Times:--------------\n")
    algorithm.print_clocks()

    #  breakdown
    breakdown=random.random()
    print(f"Breakdown: {breakdown}")
    if breakdown<0.5: # 50% chance of master node breakdown
        print(f"\nMaster node {master_node_id} has broken down during time adjustment process.")
        algorithm.print_clocks()
    else:
        algorithm.synchronize_clocks(master_node_id)
        print("\n-------------- Final Clock Times:--------------\n")
        algorithm.print_clocks()
