import time
from pm_rmq import pm_rmq_query, pm_rmq_preprocess

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.first_visit = None
        self.data = data

### Least Common Ancestor ###

def lca_preprocessing(root):
    # E, L, R arrays made (LCA -> RMQ)
    depth_arr, node_arr = binary_tree_to_arr(root)
    preprocessed_pm_arr = pm_rmq_preprocess(depth_arr)
    return (preprocessed_pm_arr, depth_arr, node_arr)

def lca_query(node1, node2, preprocessed_tree):
    preprocessed_pm_arr, depth_arr, node_arr = preprocessed_tree

    start_index = min(node1.first_visit, node2.first_visit)
    end_index = max(node1.first_visit, node2.first_visit)
    min_index = pm_rmq_query(preprocessed_pm_arr, start_index, end_index)
    return node_arr[min_index]

def euler_tour(curr_node, curr_depth, depth_arr, node_arr):
    if curr_node is None:
        return
    else:
        # R array is stored inside the node
        if curr_node.first_visit is None:
            curr_node.first_visit = len(depth_arr)
        depth_arr.append(curr_depth)
        node_arr.append(curr_node)
        # recursively build the arrays
        if curr_node.left is not None:
            euler_tour(curr_node.left, curr_depth + 1, depth_arr, node_arr)
            depth_arr.append(curr_depth)
            node_arr.append(curr_node)
        if curr_node.right is not None:
            euler_tour(curr_node.right, curr_depth + 1, depth_arr, node_arr)
            depth_arr.append(curr_depth)
            node_arr.append(curr_node)

def binary_tree_to_arr(root):
    depth_arr = []
    node_arr = []
    euler_tour(root, 0, depth_arr, node_arr)
    return depth_arr, node_arr

def lca_recursive(root, n1, n2):
    # Base Case
    if root is None:
        return None
 
    # If both n1 and n2 are smaller than root, then LCA
    # lies in left
    if(root.data > n1 and root.data > n2):
        return lca(root.left, n1, n2)
 
    # If both n1 and n2 are greater than root, then LCA
    # lies in right
    if(root.data < n1 and root.data < n2):
        return lca(root.right, n1, n2)
 
    return root

if __name__ == '__main__':
    # Example tree from L15
    a = Node(20)
    b = Node(8)
    c = Node(22)
    d = Node(4)
    e = Node(12)
    f = Node(10)
    g = Node(14)
    h = Node(1)
    a.left = b
    b.left = c
    a.right = d
    d.left = e
    e.left = f
    e.right = g
    d.right = h

    preprocessed_tree = lca_preprocessing(a)
    print(preprocessed_tree)
    node = lca_query(h, c, preprocessed_tree)
    print("Example:")
    print("LCA of {} and {}".format(h.data, c.data))
    print("    {}".format(node.data))

    r = lca_recursive(a, 1, 22)
    print("LCA of 1 and 22 is {}".format(r.data))
