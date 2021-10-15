"""
Tree utilities
"""
from functools import reduce


def extract_path(node, tree):
    """
    Give a node, recursively generate a path of nodes
    back to the root of the tree, effectively generating
    the figure corresponding to this leaf node.
    """
    if node['point'] == [0, 0]:
        return []
    return [node['point']] + extract_path(tree[node['prev_gen']], tree)


def fig_comp(fig_pts):
    """
    Add numbers together to form unique figure number
    """
    return reduce(_do_sum, _comp_pow_numb(fig_pts))


def _do_sum(info1, info2):
    """
    reduce function used by fig_comp
    """
    return info1 + info2


def _comp_pow_numb(fig_pts):
    """
    Convert each figure into a number unique for that shape
    """
    return map(_math_func, fig_pts)


def _math_func(coord):
    """
    Calculate an index based on the distance a square is from 0,0
    """
    return _do_func(abs(coord[0]) + abs(coord[1]))(coord)


def _do_func(indx):
    """
    Form integer based on base 2 locations of each of the numbers
    mapped to a point
    """
    def _innerf(coord):
        return 2 ** ([0, 0, 2, 6, 12][indx] + indx + coord[1] - 1)
    return _innerf
