# berkley with raft protocol
# raft protocol: helps to elect a leader among the nodes and get mutual consensus at each term with candidates and leaders
# berkley: helps to synchronize the clocks of the nodes

import random
import time
from threading import Thread
from datetime import datetime

class NodeState:
    FOLLOWER = 0
    CANDIDATE = 1
    LEADER = 2

# local clocks 
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = time.time() + random.uniform(-5, 5)  # Initialize local clock with random deviation
        self.state = NodeState.FOLLOWER
        self.term = 0
    def print_clock_time(self):
        dt_object = datetime.fromtimestamp(self.clock)
        print(f"Node {self.node_id}: {dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

    def synchronize(self, other_nodes, term):
        # Simulate message exchange with other nodes
        for other_node in other_nodes:
            if other_node.node_id != self.node_id:
                self.send_message(other_node, self.clock, term)

    def send_message(self, recipient, message, term):
        # Simulate message sending
        
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay) # delay 
        recipient.receive_message(self, message, term)

    def receive_message(self, sender, message, term):
        # Simulate message receiving
        if random.random() < 0.8:  # Simulate message delivery failure
            print(f"Node {self.node_id} failed to receive message from Node {sender.node_id} at term {term}")
            return
        self.clock = message

    def respond_to_vote_request(self, term):
        # Simulate response to vote request
        if self.state == NodeState.FOLLOWER:
            self.term = term
            print(f"Term {self.term}: Node {self.node_id} votes for the candidate")
            return True
        else:
            print(f"Term {self.term}: Node {self.node_id} rejects vote request (not a follower)")
            return False

# Raft consensus protocol
class RaftConsensus:
    def __init__(self, nodes):
        self.nodes = nodes
        self.leader = None

    def run_consensus(self, failed_node=None):
        print("Initial Clock Times:")
        for node in self.nodes:
            node.print_clock_time()

        term = 0
        while True:
            term += 1
            print(f"\n___________________________ Term {term} ___________________________\n")
            # Start election
            self.start_election()
            # Synchronize clocks
            self.synchronize_clocks()
            if term < 2:
                for node in self.nodes:
                    print(f"Node {node.node_id}: {node.clock}")
            else:
                # Eliminate failed node from the output
                for node in self.nodes:
                    if node.node_id == failed_node:
                        self.nodes.remove(node)
            print("\n^^^^^^^^^^^^^^^^^^^^^Updated Clock times:^^^^^^^^^^^\n")
            
            for node in self.nodes:
                node.print_clock_time()
            if all(abs(node.clock - self.nodes[0].clock) < 0.001 for node in self.nodes):
                print("\n___________________________ Synchronization Completed ___________________________")
                break
            if failed_node and self.leader.term == 2:
                print(f"******* Node {failed_node} failed at term {self.leader.term}********")
                self.nodes = [node for node in self.nodes if node.node_id != failed_node]
                failed_node = None
            

    def start_election(self):
        # Reset all nodes to follower state
        for node in self.nodes:
            node.state = NodeState.FOLLOWER

        # Randomly select a candidate
        candidate = random.choice(self.nodes)
        candidate.state = NodeState.CANDIDATE
        candidate.term += 1
        print(f"Node {candidate.node_id} initiates election for term {candidate.term}")

        # Simulate vote requests and responses
        votes_received = 0
        for node in self.nodes:
            if node != candidate:
                if random.random() < 0.8:  # Simulate message delivery success
                    print(f"Node {candidate.node_id} sends vote request to Node {node.node_id}")
                    if node.respond_to_vote_request(candidate.term):
                        votes_received += 1

        if votes_received >= len(self.nodes) // 2:
            candidate.state = NodeState.LEADER
            self.leader = candidate
            print(f"Node {candidate.node_id} becomes leader for term {candidate.term}")

    def synchronize_clocks(self):
        for node in self.nodes:
            if node != self.leader:
                print(f"Node {node.node_id} synchronizes time with Leader Node {self.leader.node_id}")
                node.synchronize(self.nodes, self.leader.term)

# Main function
if __name__ == "__main__":
    # Create nodes
    num_nodes = 5
    nodes = [Node(i) for i in range(num_nodes)]

    # Run Raft consensus algorithm
    failed_node = None
    while failed_node not in range(num_nodes):
        failed_node = int(input(f"Enter node number to fail (0 to {num_nodes-1}), or -1 to run without failure: "))
    if failed_node >= 0:
        print(f"Node {failed_node} will fail after term 2")

    consensus = RaftConsensus(nodes)
    consensus.run_consensus(failed_node)


    # # Print synchronized clock times
    print("\nSynchronized Clock Times:")
    for node in nodes:
        node.print_clock_time()
