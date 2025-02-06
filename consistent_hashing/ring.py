from node import ServerNode, StorageNode, VirtualNode
from typing import List
import hashlib
from sortedcontainers import SortedDict, SortedList
import random
def generate_hash(key,mod):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)%mod


STORAGE_NODES = [
    StorageNode("105.10.56.250"),
    StorageNode("105.10.56.251"),
    StorageNode("105.10.56.252"),
]



class HashRing:
    
    def __init__(self, size:int, replication_factor:int):
        self.tree = SortedDict()
        self.size = size
        self.replication_factor = replication_factor
    
    def initialize(self, server_nodes:List[ServerNode])->None:
        for node in server_nodes:
            self.tree[generate_hash(node.get_id(),mod=self.size)] = node
            for i in range(self.replication_factor):
                virtual_node = VirtualNode(node)
                node.add_virtual_node(virtual_node)
                self.tree[generate_hash(virtual_node.get_id(),mod=self.size)] = virtual_node
    
    def next_node(self, key)->"ServerNode":
        hash_code = generate_hash(key,mod=self.size)

        index = SortedList(self.tree.keys()).bisect_right(hash_code) 
        if index == len(self.tree):
            return self.tree[SortedList(self.tree.keys())[0]]
        if SortedList(self.tree.keys())[index] == hash_code:
            index += 1
        return self.tree[SortedList(self.tree.keys())[index]]
           
        
    def add_data(self, key, value)->None:
        print("Adding data",value," with key ",key)
        node = self.next_node(key)
        if node is None:
            raise Exception("Node not found")
        node.store(key, value)
        
    def get_data(self, key)->"ServerNode":
        print("Retrieving data with key ",key)
        node = self.next_node(key)
        if node is None:
            raise Exception("Data not found")
        print("Retrieving data",node.retrieve(key),"from node",node.get_id())
        return node.retrieve(key)
    
    def remove_data(self, key)->None:
        print("Removing data with key ",key)
        node = self.next_node(key)
        if node is None:
            raise Exception("Data not found")
        node.remove(key)
    
    def delete_server(self, node_id)->None:
        print("Deleting server ",node_id)
        storage_node = self.tree.get(generate_hash(node_id,mod=self.size))
        if storage_node is None:
            raise Exception("Node not found")
        for virtual_node in storage_node.virtual_nodes:
            self.tree.pop(generate_hash(virtual_node.get_id(),mod=self.size))
        
        self.tree.pop(generate_hash(node_id,mod=self.size))
        data = storage_node.get_data()
        for key in data:
            self.add_data(key, data[key])  
    
    def _move_data(self, next_node, storage_node)->None:
        keys_to_move = []
        for key in next_node.get_data():
            if generate_hash(storage_node.get_id(),mod=self.size) > generate_hash(key,mod=self.size):
                print("Moving key ",key)
                storage_node.store(key, next_node.retrieve(key))
                keys_to_move.append(key)
        for key in keys_to_move:
            next_node.remove(key)
     
            
    def add_server(self, storage_node)->None:
        print("Adding server ",storage_node.get_id())
        self.tree[generate_hash(storage_node.get_id(),mod=self.size)] = storage_node
        next_node = self.next_node(storage_node.get_id())
        self._move_data(next_node, storage_node)
        
        for i in range(self.replication_factor):
            virtual_node = VirtualNode(storage_node)
            storage_node.add_virtual_node(virtual_node)
            self.tree[generate_hash(virtual_node.get_id(),mod=self.size)] = virtual_node
            next_node = self.next_node(virtual_node.get_id())
            self._move_data(next_node, virtual_node)
            
        
        
            
        
def run():
    ring = HashRing(67, 1)
    ring.initialize(STORAGE_NODES)
    print(len(ring.tree))
    print(ring.tree)
    for node in STORAGE_NODES:
        print(node,len(node))
    keys = (random.sample(range(1000000), 30))
    keys = [str(key) for key in keys]
    for i,key in enumerate(keys):
        ring.add_data(key, f"value_{i}")
    for i,key in enumerate(keys):
        ring.get_data(key)
    
    for node in STORAGE_NODES:
        print(node,len(node))
    ring.delete_server("105.10.56.250")
    STORAGE_NODES.pop(0)
    print(len(ring.tree))
    print(ring.tree)
    for i,key in enumerate(keys):
        ring.get_data(key)
    for node in STORAGE_NODES:
        print(node,len(node))
    new_node = StorageNode("102.12.18.201")
    ring.add_server(new_node)
    STORAGE_NODES.append(new_node)
    print(len(ring.tree))
    print(ring.tree)
    for i,key in enumerate(keys):
        ring.get_data(key)
    total_nodes = 0
    for node in STORAGE_NODES:
        print(node,len(node))
        total_nodes += len(node)
    print("Total nodes",total_nodes)

if __name__ == "__main__":
    run()