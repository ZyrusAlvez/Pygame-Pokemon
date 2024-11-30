class Queue:
    def __init__(self):
        self.queue = []
    
    # Add an element
    def enqueue(self, item):
        self.queue.append(item)
    
    # Remove an element
    def dequeue(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)
    
    def size(self):
        return len(self.queue)