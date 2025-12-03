from algorithms.binarysearchtree import BinarySearchTree, Node

# Manually create BST nodes
bst = BinarySearchTree()
bst.root = Node(10)
bst.root.left = Node(5)
bst.root.left.left = Node(3)
bst.root.left.right = Node(7)
bst.root.right = Node(15)

# Test search(node, value)
print("Search root for 10:", bst.search(bst.root, 10))  # True
print("Search root for 20:", bst.search(bst.root, 20))  # False
print("Search root.left for 3:", bst.search(bst.root.left, 3))  # True
print("Search None for 10:", bst.search(None, 10))  # False

# Test get_max_value(node)
print("Max value in tree:", bst.get_max_value(bst.root))  # 15
print("Max value in left subtree:", bst.get_max_value(bst.root.left))  # 7
print("Max value None:", bst.get_max_value(None))  # None

# Test find_height(node)
print("Height of tree:", bst.find_height(bst.root))  # 2
print("Height of left subtree:", bst.find_height(bst.root.left))  # 1
print("Height of None:", bst.find_height(None))  # -1

# Test delete(node, value)
# Before delete 5: 3,5,7,10,15
print("Before delete 5, manual inorder: 3 5 7 10 15")
bst.root = bst.delete(bst.root, 5)
# After: 3,7,10,15
print("After delete 5, expected: 3 7 10 15")

# Delete leaf 3
bst.root = bst.delete(bst.root, 3)
# After: 7,10,15
print("After delete 3, expected: 7 10 15")

# Delete None
result = bst.delete(None, 10)
print("Delete on None:", result)  # None

print("All tests completed.")
