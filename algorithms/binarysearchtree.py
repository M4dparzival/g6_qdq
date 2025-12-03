class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return node
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children: Get the inorder successor
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def preorder_traversal(self, node=None, traversal=""):
        if node is None:
            node = self.root
        if node:
            traversal += str(node.value) + " "
            traversal = self.preorder_traversal(node.left, traversal)
            traversal = self.preorder_traversal(node.right, traversal)
        return traversal

    def inorder_traversal(self, node=None, traversal=""):
        if node is None:
            node = self.root
        if node:
            traversal = self.inorder_traversal(node.left, traversal)
            traversal += str(node.value) + " "
            traversal = self.inorder_traversal(node.right, traversal)
        return traversal

    def postorder_traversal(self, node=None, traversal=""):
        if node is None:
            node = self.root
        if node:
            traversal = self.postorder_traversal(node.left, traversal)
            traversal = self.postorder_traversal(node.right, traversal)
            traversal += str(node.value) + " "
        return traversal
