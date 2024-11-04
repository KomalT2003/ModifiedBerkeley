# code 2: berkley failure when the master node has wrong time 
import random
import time

class BerkeleyAlgorithm:
    def __init__(self, nodes):
        self.nodes = nodes

    def synchronize_clocks(self, master_node_id):
        master_node = self.nodes[master_node_id]
        master_time = master_node.get_current_time()

        # time differences with master
        time_diffs = [master_time - node.get_current_time() for node in self.nodes if node.node_id != master_node_id]

        
        avg_time_diff = sum(time_diffs) / len(time_diffs)

        
        for node in self.nodes:
            if node.node_id != master_node_id:
                node.adjust_time(avg_time_diff)

    def print_clocks(self):
        for node in self.nodes:
            print(f"Node {node.node_id}: {node.get_current_time_readable()}")

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = time.time() + random.uniform(-5, 5)  #  random deviation

    def get_current_time(self):
        return self.clock

    def get_current_time_readable(self):
        time_str = time.strftime("%H:%M:%S", time.localtime(self.clock))
        microsec = int((self.clock % 1) * 1000000)
        return f"{time_str}:{microsec:06d}"

    def adjust_time(self, time_diff):
        self.clock += time_diff

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    nodes = [Node(i) for i in range(num_nodes)]

    master_node_id = int(input(f"Enter the master node ID (0 to {num_nodes - 1}): "))
    if master_node_id < 0 or master_node_id >= num_nodes:
        print("Invalid master node ID.")
        exit()

    
    master_node = nodes[master_node_id]
    master_node.clock += 14 * 60 * 60  # delay add karo

    algorithm = BerkeleyAlgorithm(nodes)
    print("\n-------------- Initial Clock Times:--------------\n")
    algorithm.print_clocks()
    algorithm.synchronize_clocks(master_node_id)
    print("\n-------------- Final Clock Times:--------------\n")
    algorithm.print_clocks()
