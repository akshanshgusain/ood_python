class DLLNode:
    def __init__(self, element):
        self.element = element
        self.next: DLLNode = None
        self.prev: DLLNode = None
