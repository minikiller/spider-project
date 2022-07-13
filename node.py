class NodeIter:
    def __init__(self, node):
        self.cur_node = node
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.cur_node is None:
            raise StopIteration
        else:
            node = self.cur_node
            self.cur_node = self.cur_node.next
            return node

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __iter__(self):
        return NodeIter(self)