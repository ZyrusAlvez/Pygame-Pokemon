class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    # Preorder Traversal
    def traversePreOrder(self):
        results = [self.val]  # Start with the current node's value
        if self.left:  # Traverse left subtree
            results += self.left.traversePreOrder()
        if self.right:  # Traverse right subtree
            results += self.right.traversePreOrder()
        return results

def add_node(root, value, direction):
    """
    Add a node dynamically to the left or right of the tree.
    It will traverse until it finds an empty position.
    """
    current = root
    while True:
        if direction == "left":  # Add to left
            if not current.left:
                current.left = Node(value)  # Place the new node
                print(f"Node with value {value} added to the left of {current.val}")
                break
            current = current.left  # Traverse further down the left subtree
        elif direction == "right":  # Add to right
            if not current.right:
                current.right = Node(value)  # Place the new node
                print(f"Node with value {value} added to the right of {current.val}")
                break
            current = current.right  # Traverse further down the right subtree
        else:
            print("Invalid direction! Use 'L' for left and 'R' for right.")
            break