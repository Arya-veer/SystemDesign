from abc import ABC, abstractmethod
import uuid

class ServerNode(ABC):
    
    @abstractmethod
    def store(self, key, value):
        pass
    
    @abstractmethod
    def retrieve(self, key):
        pass
    
    @abstractmethod
    def remove(self, key):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def get_id(self):
        pass
    
    def __str__(self):
        return f"{self.get_id()}"
    
    def __repr__(self):
        return self.__str__()
    

class StorageNode(ServerNode):
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.virtual_nodes = []

    def store(self, key, value):
        self.data[key] = value

    def retrieve(self, key):
        return self.data.get(key)
    
    def remove(self, key):
        if key in self.data:
            del self.data[key]
            
    def get_data(self):
        return self.data
    
    def add_virtual_node(self, virtual_node):
        self.virtual_nodes.append(virtual_node)
        
    def get_id(self):
        return self.node_id
    
    def __str__(self):
        return super().__str__()
    
    def __len__(self):
        return len(self.data)
    

class VirtualNode(ServerNode):
    
    def __init__(self, storage_node):
        self.node_id = f"virtual-{uuid.uuid4()}-{storage_node.get_id()}"
        self.storage_node = storage_node
        
    def store(self, key, value):
        self.storage_node.store(key, value)
    
    def retrieve(self, key):
        return self.storage_node.retrieve(key)
    
    def remove(self, key):
        self.storage_node.remove(key)
        
    def get_data(self):
        return self.storage_node.get_data()
    
    def get_id(self):
        return self.node_id
    
    def __str__(self):
        return super().__str__()