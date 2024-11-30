class Stack:
    def __init__(self) -> None:
        self.stack = []
    
    def push(self, value):
        self.stack.append(value)
    
    def show(self):
        return self.stack

    def pop(self):
        if len(self.stack) == 0:
            return 
        else:
            return self.stack.pop()
    
    def peek(self):
        return self.stack[-1]
    
    
