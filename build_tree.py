"""
Build the tree used to scan figures
"""
from functools import reduce
from solver.build_level import get_node_changes
from solver.tree_utils import prune_tree


def new_tree(tree):
    """
    Wrap grow_tree in prune tree in set_pents
    """
    return prune_tree(grow_tree(tree))


def grow_tree(tree, level=0):
    """
    Start with a single square.  Generate four more generations
    of squares to create all possible five square layouts.
    """
    if level == 4:
        return tree
    return grow_tree(fix_tree_links(grow_level(tree)), level + 1)


def grow_level(tree):
    """
    Fill out the tree with a level (based on distance from the origin point)
    """
    return make_node_changes(tree, get_node_changes(tree))


def set_offspring_values(tree):
    """
    Add the offspring information as a list of link indices into the tree
    """
    def internal_offspring_func(indx):
        tree[indx[1]]['new_offspring'] = len(indx[0])
        return tree
    return internal_offspring_func


def add_on_new_nodes(changes):
    """
    Take the offspring links added and convert that information to
    new nodes to tack onto the end of the tree.
    """
    return [item for sublist in
            ([list({'point': node, 'prev_gen': change[1], 'offspring': []}
                   for node in change[0])
              for change in changes]) for item in sublist]


def make_node_changes(tree, changes):
    """
    Combine the setting of offspring nodes and the adding
    of new nodes together into one function
    """
    return list(map(set_offspring_values(tree),
                    changes))[-1] + add_on_new_nodes(changes)


def afunc(arg1, arg2):
    """
    Used to concatenate two lists inside a reduce call
    """
    return arg1 + arg2


def nmap(arg):
    """
    Used by map call to return offspring field
    """
    return arg['offspring']


def scan_for_snumb(tree):
    """
    Scan the tree for the highest number offspring link
    """
    return max(reduce(afunc, list(map(nmap, tree))) + [0]) + 1


def gen_off_list(sindx):
    """
    Given a starting index and size, return a list of numbered
    links in that range.
    """
    def gen_link_olist(osize):
        return list(range(sindx, sindx + osize))
    return gen_link_olist


def fix_tree_links(tree):
    """
    Wrapper around fix_a_link to call it for each node
    """
    return list(map(fix_a_link(tree), tree))


def fix_a_link(tree):
    """
    Add the offspring links for nodes just added to the tree.
    """
    def ifunc(node):
        if 'new_offspring' not in node:
            return node
        node['offspring'] = gen_off_list(scan_for_snumb(tree)
                                         )(node['new_offspring'])
        node.pop('new_offspring')
        return node
    return ifunc
