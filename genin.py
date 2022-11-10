import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import math


class Tree:
    T = None
    root = None
    leaves = None
    leafe_capacity = None

def init_tree(root_to_leaves, root):
    T = nx.DiGraph()

    # build edges
    for path in root_to_leaves:
        for index in range(0,len(path)-1):
            T.add_edge(path[index], path[index+1])

    # set capacity
    for path in root_to_leaves:
        for node in path:
            T.nodes[node]["capacity"] = 0

    capacity_by_server = math.ceil(len(instances) / len(root_to_leaves))
    leaves = [x for x in T.nodes() if T.out_degree(x)==0 and T.in_degree(x)==1]

    for node in leaves:
        T.nodes[node]["capacity"] = capacity_by_server
        parent = node

        while parent != root:
            for parent,_ in T.in_edges(node):
                T.nodes[parent]["capacity"] += capacity_by_server
            node = parent

    tree = Tree()
    tree.T = T
    tree.root = root
    tree.leaves = leaves
    tree.leafe_capacity = capacity_by_server
    return tree

def spread_instances(instances, tree):
    for instance in instances:
        node = root

        while node not in tree.leaves:
            max_cap = 0
            for _,child in tree.T.out_edges(node):
                if tree.T.nodes[child]["capacity"] > max_cap:
                    max_cap = tree.T.nodes[child]["capacity"]
                    node = child

        tree.T.add_edge(node, instance)
        tree.T.nodes[instance]["order"] = tree.leafe_capacity - tree.T.nodes[node]["capacity"]
        tree.T.nodes[node]["capacity"] -= 1

        parent = node

        while parent != root:
            for parent,_ in tree.T.in_edges(node):
                tree.T.nodes[parent]["capacity"] -= 1
            node = parent

        # print_tree(tree.T)

def print_tree(T):
    pos = graphviz_layout(T, prog="dot")
    labels = nx.get_node_attributes(T, 'capacity')
    labels_order = nx.get_node_attributes(T, 'order')

    nx.draw(T, pos, with_labels = True, node_size=1000)
    nx.draw_networkx_edges(T, pos, edge_color='r', arrows = True)
    # shift capacity to print
    pos_attrs = {}
    for node, coords in pos.items():
        pos_attrs[node] = (coords[0]+30, coords[1]-10)
    nx.draw_networkx_labels(T, pos_attrs, labels, font_color="blue")
    nx.draw_networkx_labels(T, pos_attrs, labels_order, font_color="red")

    plt.show()

instances = [
    "r-1", "r-2", "r-3", "r-4",
    "s-1-1", "s-1-2", "s-1-3", "s-1-4",
    "s-2-1", "s-2-2", "s-2-3", "s-2-4"
]
root = "cluster"
# root_to_leaves = [
#     [root, "dc-1", "region_a", "server-1"],
#     [root, "dc-1", "region_a", "server-2"],
#     [root, "dc-1", "region_b", "server-3"],
#     [root, "dc-1", "region_b", "server-4"],
#     [root, "dc-2", "region_c", "server-5"]
# ]
root_to_leaves = [
    [root, "dc-1", "server-1"],
    [root, "dc-1", "server-2"],
    [root, "dc-2", "server-3"],
    [root, "dc-2", "server-4"],
    [root, "dc-2", "server-5"]
]

tree = init_tree(root_to_leaves, root)
spread_instances(instances, tree)
print_tree(tree.T)