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
        print(self.data, end=" <- ")  # Visit the root first
        if self.left:              # Traverse the left subtree
            self.left.PrintTree()
        if self.right:             # Traverse the right subtree
            self.right.PrintTree()
        print("")

    def countLeftRightNodes(self):
        """
        Count all left and right nodes in preorder traversal, excluding the root.
        Returns:
            tuple: (left_count, right_count)
        """
        left_count = 0
        right_count = 0

        def traverse(node, is_left):
            nonlocal left_count, right_count
            if not node:
                return
            if is_left:
                left_count += 1
            else:
                right_count += 1
            traverse(node.left, True)
            traverse(node.right, False)

        # Start traversal from the root's children
        if self.left:
            traverse(self.left, True)
        if self.right:
            traverse(self.right, False)

        return left_count, right_count