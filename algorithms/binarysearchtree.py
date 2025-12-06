class Node:
    """A node in the Binary Search Tree."""

    def __init__(self, value, left=None, right=None):
        """Initialize a node with value and optional left/right children."""
        self.value = value
        self.left = left
        self.right = right


class BST:
    """A Binary Search Tree implementation."""

    def __init__(self, root_value=None):
        """Initialize the BST with an optional root value."""
        self.root = Node(root_value) if root_value is not None else None

    def insert(self, data, node=None):
        """Insert a value into the BST."""
        if node is None:
            node = self.root
        if node is None:
            self.root = Node(data)
            return self.root

        if data < node.value:
            node.left = self.insert(data, node.left)
        else:
            node.right = self.insert(data, node.right)
        return node

    def search(self, target, node=None):
        """Search for a target value in the BST."""
        if node is None:
            node = self.root
        if node is None:
            return None

        if node.value == target:
            return node

        elif node.value < target:
            return self.search(target, node.right)
        else:
            return self.search(target, node.left)

    def get_min(self, node=None):
        """Get the minimum value in the BST or subtree."""
        if node is None:
            node = self.root
        if node is None:
            return None

        current = node
        while current.left:
            current = current.left
        return current.value

    def get_max(self, node=None):
        """Get the maximum value in the BST or subtree."""
        if node is None:
            node = self.root
        if node is None:
            return None

        current = node
        while current.right:
            current = current.right
        return current.value

    def find_height(self, node=None):
        """Find the height of the BST or subtree."""
        if node is None:
            node = self.root
        if node is None:
            return -1

        left_height = self.find_height(node.left)
        right_height = self.find_height(node.right)

        return 1 + max(left_height, right_height)

    def get_min_node(self, node=None):
        """Get the node with the minimum value in the BST or subtree."""
        if node is None:
            node = self.root
        if node is None:
            return None

        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, value, node=None):
        """Delete a value from the BST using inorder successor."""
        if node is None:
            node = self.root
        if node is None:
            return None

        if value < node.value:
            node.left = self.delete(value, node.left)
        elif value > node.value:
            node.right = self.delete(value, node.right)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Find inorder successor
                succ = self.get_min_node(node.right)
                node.value = succ.value
                node.right = self.delete(succ.value, node.right)
        return node

    def preorder_traversal(self, start, traversal=""):
        """Perform preorder traversal and return as string."""
        if start:
            traversal += str(start.value) + " "
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal

    def inorder_traversal(self, start, traversal=""):
        """Perform inorder traversal and return as string."""
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += str(start.value) + " "
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal

    def postorder_traversal(self, start, traversal=""):
        """Perform postorder traversal and return as string."""
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += str(start.value) + " "
        return traversal
