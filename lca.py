import timeit
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

    if (node1.first_visit < node2.first_visit):
        min_index = pm_rmq_query(preprocessed_pm_arr, node1.first_visit, node2.first_visit)
        return node_arr[min_index]
    else:
        min_index = pm_rmq_query(preprocessed_pm_arr, node2.first_visit, node1.first_visit)
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

# Single traversal of Binary tree, without extra storage for path arrays
def lca_recursive(root, n1, n2):
    # Base Case
    if root is None:
        return None
 
    # If either n1 or n2 matches with root's key, report
    #  the presence by returning root (Note that if a key is
    #  ancestor of other, then the ancestor key becomes LCA
    if root.data == n1 or root.data == n2:
        return root
 
    # Look for keys in left and right subtrees
    left_lca = lca_recursive(root.left, n1, n2)
    right_lca = lca_recursive(root.right, n1, n2)
 
    # If both of the above calls return Non-NULL, then one key
    # is present in once subtree and other is present in other,
    # So this node is the LCA
    if left_lca and right_lca:
        return root
 
    # Otherwise check if left subtree or right subtree is LCA
    return left_lca if left_lca is not None else right_lca

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
    d.right = e
    e.left = f
    e.right = g
    d.left = h
    #c.right = Node(25)
    #b.right = Node(7)

    start_p = timeit.default_timer()
    preprocessed_tree = lca_preprocessing(a)
    end_p = timeit.default_timer()
    node = lca_query(h, c, preprocessed_tree)
    end_q = timeit.default_timer()
    print("Example:")
    print("LCA of {} and {} is {}".format(h.data, c.data, node.data))
    print("preprocessing:", end_p - start_p, "\tquery:", end_q - end_p)

    start2 = timeit.default_timer()
    r = lca_recursive(a, 1, 22)
    end2 = timeit.default_timer()
    print("LCA of 1 and 22 is {}".format(r.data))
    print(end2-start2)
