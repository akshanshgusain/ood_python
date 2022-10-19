from src.algorithms.DLL import DLL
from src.algorithms.DLLNode import DLLNode
from src.policies.iEvectionPolicy import iEvectionPolicy


class LRUEvictionPolicy(iEvectionPolicy):

    def __init__(self):
        self.dll: DLL = DLL()
        self.mapper: dict = {}

    def key_accessed(self, key):
        if key in self.mapper:
            self.dll.detach_node(self.mapper.get(key))
            self.dll.add_node_at_last(self.mapper.get(key))
        else:
            new_node: DLLNode = self.dll.add_element_at_last(key)
            self.mapper[key] = new_node

    def evict_key(self):
        first: DLLNode = self.dll.get_first_node()
        if first is None:
            return None
        self.dll.detach_node(first)
        return first.element
