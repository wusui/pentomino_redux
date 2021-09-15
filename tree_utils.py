"""
Tree utilities
"""
from functools import reduce


def prune_tree(tree):
    """
    Given a tree, remove all figures that are duplicates
    of previous figures
    """
    return get_result(get_unique_figs(tree))()


def get_result(tree):
    """
    Get indices of nodes not being kept, and delete those nodes.
    """
    def innerf():
        return list(map(do_node_delete(tree),
                        list(map(get_indices,
                                 get_nokeep(tree)))))[-1]
    return innerf


def get_unique_figs(tree):
    """
    Extract duplicate figures from the tree
    """
    return find_unique_figures_wrap(list(map(get_fig_values(tree), tree)), [])


def get_nokeep(tree):
    """
    Wrap find_nonkeepers, Return list of nodes not to keep.
    """
    return list(filter(find_nonkeepers, enumerate(tree)))


def get_indices(delete_tuple):
    """
    Return first element of tuple
    """
    return delete_tuple[0]


def find_nonkeepers(node):
    """
    Return True for nodes we will delete.
    """
    if 'fig_value' in node[1]:
        if 'dont_delete_me' not in node[1]:
            return True
    return False


def find_unique_figures_wrap(tree, figs_so_far):
    """
    Find_unique_figures simplification wrapper
    """
    return find_unique_figures(figs_so_far)(tree)


def find_unique_figures(figs_so_far):
    """
    Keep track of unique figures so dupicates can be removed
    """
    def innerf(tree):
        return list(map(get_figs_so_far, tree))

    def get_figs_so_far(node):
        if 'fig_value' in node:
            if node['fig_value'] not in figs_so_far:
                figs_so_far.append(node['fig_value'])
                node['dont_delete_me'] = True
        return node
    return innerf


def get_fig_values(tree):
    """
    Given a node in a tree set 'fig_value' for that node.
    """
    def innerf(node):
        if node['offspring'] == []:
            node['fig_value'] = fig_comp(extract_path(node, tree))
        return node
    return innerf


def do_node_delete(tree):
    """
    Delete a node fromthe tree.
    """
    def innerf(indx):
        tree[tree[indx]['prev_gen']]['offspring'].remove(indx)
        tree[indx] = {}
        return tree
    return innerf


def do_sum(info1, info2):
    """
    reduce function used by fig_comp
    """
    return info1 + info2


def fig_comp(fig_pts):
    """
    Ad numbers together to form unique figure number
    """
    return reduce(do_sum, comp_pow_numb(fig_pts))


def comp_pow_numb(fig_pts):
    """
    Convert each figure into a number unique for that shape
    """
    return map(math_func, fig_pts)


def math_func(coord):
    """
    Calculate an index based on the distance a square is from 0,0
    """
    return do_func(abs(coord[0]) + abs(coord[1]))(coord)


def do_func(indx):
    """
    Form integer based on base 2 locations of each of the numbers
    mapped to a point
    """
    def innerf(coord):
        return 2 ** ([0, 0, 2, 6, 12][indx] + indx + coord[1] - 1)
    return innerf


def extract_path(node, tree):
    """
    Give a node, recursively generate a path of nodes
    back to the root of the tree, effectively generating
    the figure corresponding to this leaf node.
    """
    if node['point'] == [0, 0]:
        return []
    return [node['point']] + extract_path(tree[node['prev_gen']], tree)
