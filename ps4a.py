# Problem Set 4A
# Name:
# Collaborators:

from tree import Node # Imports the Node object used to construct trees

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the test named test_data_representation should pass.
tree1 = Node(8,Node(2, Node(1),Node(6)), Node(10))

tree2 = Node(7,Node(2, Node(1),Node(5,Node(3),Node(6))),Node(9,Node(8),Node(10)))

tree3 = Node(5,Node(3,Node(2),Node(4)),Node(14,Node(12),Node(21,Node(20),Node(26))))

def find_tree_height(tree):
    '''
    Find the height of the given tree
    Input:
        tree: An element of type Node constructing a tree
    Output:
        The integer depth of the tree
    '''
    # Base case: empty tree
    if tree is None:
        return -1
    
    # Base case: leaf node
    if tree.get_left_child() is None and tree.get_right_child() is None:
        return 0
    
    # Recursive case: get height of left and right subtrees
    left_height = find_tree_height(tree.get_left_child())
    right_height = find_tree_height(tree.get_right_child())
    
    # Return max height + 1 for current level
    return max(left_height, right_height) + 1

def is_heap(tree, compare_func):
    '''
    Determines if the tree is a max or min heap depending on compare_func
    Inputs:
        tree: An element of type Node constructing a tree
        compare_func: a function that compares the child node value to the parent node value
            i.e. op(child_value,parent_value) for a max heap would return True if child_value < parent_value and False otherwise
                 op(child_value,parent_value) for a min heap would return True if child_value > parent_value and False otherwise
    Output:
        True if the entire tree satisfies the compare_func function; False otherwise
    '''
    # Base case: empty tree or leaf node is a heap
    if tree is None or (tree.get_left_child() is None and tree.get_right_child() is None):
        return True
    
    # Check left subtree
    left_child = tree.get_left_child()
    if left_child:
        if not compare_func(left_child.get_value(), tree.get_value()):
            return False
    
    # Check right subtree
    right_child = tree.get_right_child()
    if right_child:
        if not compare_func(right_child.get_value(), tree.get_value()):
            return False
    
    # Recursively check if left and right subtrees are heaps
    return is_heap(left_child, compare_func) and is_heap(right_child, compare_func)

if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # Example tests:
    print("Tree heights:")
    print("tree1:", find_tree_height(tree1))  # Should be 2
    print("tree2:", find_tree_height(tree2))  # Should be 3
    print("tree3:", find_tree_height(tree3))  # Should be 3
