from src.algorithms.DLLNode import DLLNode
from src.algorithms.exceptions.InvalidElementException import InvalidElementException


class DLL:
    def __init__(self):
        # We can instantiate these by null, since we are never gonna use val for these dummyNodes
        self.dummy_head: DLLNode = DLLNode(None)
        self.dummy_tail: DLLNode = DLLNode(None)

        # Also Initially there are no items
        # so just join dummyHead and Tail, we can add items in between them easily.
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head

    '''
    * Method to detach a random node from the doubly linked list. The node itself will not be removed from the memory.
    * Just that it will be removed from the list and becomes orphaned.
    *
    * @param node Node to be detached.
    '''

    def detach_node(self, node: DLLNode):
        if node is not None:
            node.prev.next = node.next
            node.next.prev = node.prev

    '''Helper method to add a node at the end of the list.'''

    def add_node_at_last(self, node: DLLNode):
        tail_prev: DLLNode = self.dummy_tail.prev
        tail_prev.next = node
        node.next = self.dummy_tail
        self.dummy_tail.prev = node
        node.prev = tail_prev

    '''Helper method to add an element at the end.'''

    def add_element_at_last(self, element):
        if element is None:
            raise InvalidElementException()
        new_node: DLLNode = DLLNode(element)
        self.add_node_at_last(new_node)
        return new_node

    def is_item_present(self):
        return self.dummy_head.next != self.dummy_tail

    def get_first_node(self):
        item: DLLNode = None
        if not self.is_item_present():
            return None
        return self.dummy_head.next

    def get_last_node(self):
        item: DLLNode = None
        if not self.is_item_present():
            return None
        return self.dummy_tail.prev
