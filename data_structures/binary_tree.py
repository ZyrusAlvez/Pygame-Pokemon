class BinaryTreeNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data, direction):
        """
        Insert a new node explicitly in the specified direction.
        """
        if direction == "left":
            if self.left is None:
                self.left = BinaryTreeNode(data)
                print(f"Node with value \"{data}\" added to the left of \"{self.data}\"")
            else:
                self.left.insert(data, direction)
        elif direction == "right":
            if self.right is None:
                self.right = BinaryTreeNode(data)
                print(f"Node with value \"{data}\" added to the right of \"{self.data}\"")
            else:
                self.right.insert(data, direction)
        else:
            print("Invalid direction! Use 'left' or 'right'.")

    def PrintTree(self):
        """
        Print the tree in a preorder traversal.
        """
        print("Binary Tree")
        print(self.data, end=" <- ")  # Visit the root first
        if self.left:              # Traverse the left subtree
            self.left.PrintTree()
        if self.right:             # Traverse the right subtree
            self.right.PrintTree()
        print("")
