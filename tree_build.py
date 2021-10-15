"""
Build the tree used to scan figures
"""
from functools import reduce
from tree_level import get_node_changes
from tree_prune import prune_tree


def new_tree(tree):
    """
    Wrap _grow_tree in prune tree
    """
    return prune_tree(_grow_tree(tree))


def _grow_tree(tree, level=0):
    """
    Start with a single square.  Generate four more generations
    of squares to create all possible five square layouts.
    """
    if level == 4:
        return tree
    return _grow_tree(_fix_tree_links(_grow_level(tree)), level + 1)


def _grow_level(tree):
    """
    Fill out the tree with a level (based on distance from the origin point)
    """
    return _make_node_changes(tree, get_node_changes(tree))


def _make_node_changes(tree, changes):
    """
    Combine the setting of offspring nodes and the adding
    of new nodes together into one function
    """
    return tuple(map(_set_offspring_values(tree),
                     changes))[-1] + _add_on_new_nodes(changes)


def _set_offspring_values(tree):
    """
    Add the offspring information as a list of link indices into the tree
    """
    def _internal_offspring_func(indx):
        tree[indx[1]]['new_offspring'] = len(indx[0])
        return tree
    return _internal_offspring_func


def _add_on_new_nodes(changes):
    """
    Take the offspring links added and convert that information to
    new nodes to tack onto the end of the tree.
    """
    return [item for sublist in
            ([list({'point': node, 'prev_gen': change[1], 'offspring': []}
                   for node in change[0])
              for change in changes]) for item in sublist]


def _fix_tree_links(tree):
    """
    Wrapper around _fix_a_link to call it for each node
    """
    return list(map(_fix_a_link(tree), tree))


def _fix_a_link(tree):
    """
    Add the offspring links for nodes just added to the tree.
    """
    def _ifunc(node):
        if 'new_offspring' not in node:
            return node
        node['offspring'] = _gen_off_list(_scan_for_snumb(tree))(
            node['new_offspring'])
        node.pop('new_offspring')
        return node
    return _ifunc


def _gen_off_list(sindx):
    """
    Given a starting index and size, return a list of numbered
    links in that range.
    """
    def _gen_link_olist(osize):
        return list(range(sindx, sindx + osize))
    return _gen_link_olist


def _scan_for_snumb(tree):
    """
    Scan the tree for the highest number offspring link
    """
    return max(reduce(_afunc, tuple(map(_nmap, tree))) + [0]) + 1


def _afunc(arg1, arg2):
    """
    Used to concatenate two lists inside a reduce call
    """
    return arg1 + arg2


def _nmap(arg):
    """
    Used by map call to return offspring field
    """
    return arg['offspring']
