class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BST:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None
    
    def insert(self, data, node=None):
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
        if node is None:
            node = self.root
        if node is None:
            return None
        
        if node.value == target:
            return node
        
        elif node.value < target:
            return self.search(node.right, target)
        else:
            return self.search(node.left, target)
    
    def get_min(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        current = node
        while current.left:
            current = current.left
        return current.value

    def get_max(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        current = node
        while current.right:
            current = current.right
        return current.value
    
    def find_height(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return -1
        
        left_height = self.find_height(node.left)
        right_height = self.find_height(node.right)

        return 1+max(left_height, right_height)
    
    def get_min_node(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        
        current = node
        while current.left:
            current = current.left
        return current
    
    def delete(self, value, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None

        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
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
                node.right = self.delete(node.right, succ.value)
        return node
