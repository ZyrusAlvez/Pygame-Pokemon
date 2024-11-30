class LinkedList:
    def __init__(self):
        self.head = None
        
    def count(self):
        printmoko = self.head
        c = 0
        while printmoko is not None:
            c += 1
            printmoko = printmoko.next
        return c
    
    def show_data(self):
        iterative = []
        printmoko = self.head
        while printmoko is not None:
            iterative.append(printmoko.data)
            printmoko = printmoko.next
        return iterative
                
    def atend(self, newdata):
        Newnode = Node(newdata)
        if self.head is None:
            self.head = Newnode
            return
        lastnode = self.head
        while lastnode.next:
            lastnode = lastnode.next
        lastnode.next = Newnode
        
    def get_data_at(self, position):
        if position < 1:
            raise ValueError("Position must be 1 or greater.")
        
        current = self.head
        index = 1
        while current is not None:
            if index == position:
                return current.data
            current = current.next
            index += 1
        
        raise IndexError("Position out of range.")
        
        
class Node:
    def __init__(self, data = None):
        self.data = data
        self.next = None