"""
Figure out where to place pentominos
"""
from rect_chk_symmetry import bad_sym


def find_placements(rectangle, tree, irow, icol, sym_info):
    """
    Return end points in tree that are possible figures in a solution.
    """
    return filter(_chk_placement(rectangle)(tree)(irow)(icol)(sym_info),
                  _gen_placements(rectangle, [irow, icol], tree, 0, []))


def _chk_placement(rectangle):
    """
    General test wrapper so that checks can be called from a filter call.
    """
    def _inner1(tree):
        def _inner2(irow):
            def _inner3(icol):
                def _inner4(sym_info):
                    def _chk_placement1(node):
                        return _general_test(rectangle, tree, [irow, icol],
                                             sym_info, node)
                    return _chk_placement1
                return _inner4
            return _inner3
        return _inner2
    return _inner1


def _general_test(rectangle, tree, sqloc, sym_info, node):
    """
    General test to fail a pentomino if it is already in use, does not fit,
    or results in a symetry error.
    """
    if _fig_used(rectangle, tree[node]['pent_type']):
        return False
    if not _fig_is_okay(tree, rectangle, sqloc[0], sqloc[1], node):
        return False
    if bad_sym(rectangle, sym_info):
        return False
    return True


def _gen_placements(rectangle, sqloc, tree, last, retv):
    """
    Return list of all pentomino leaf nodes in tree that fit into the
    location specified
    """
    while last >= 0:
        while tree[last]['offspring']:
            if not _square_is_okay(rectangle,
                                   sqloc[1] + tree[last]['point'][0],
                                   sqloc[0] + tree[last]['point'][1]):
                last = _get_backup_path(last, tree)
                if last == -1:
                    break
            else:
                last = tree[last]['offspring'][0]
        if 'pent_type' in tree[last]:
            retv.append(last)
        last = _get_backup_path(last, tree)
    return retv


def _fig_used(rectangle, value):
    """
    Return true if the figure is already in use
    """
    return any(map(_chk_fig(value), rectangle))


def _fig_is_okay(tree, rectangle, irow, icol, last):
    """
    True if the figure checked fits into the rectangle
    """
    if last < 0:
        return True
    if not _square_is_okay(rectangle,
                           icol + tree[last]['point'][0],
                           irow + tree[last]['point'][1]):
        return False
    return _fig_is_okay(tree, rectangle, irow, icol,
                        tree[last]['prev_gen'])


def _chk_fig(value):
    """
    Check a fig for _fig_used mapping
    """
    def _innerf(in_data):
        if value in in_data:
            return True
        return False
    return _innerf


def _square_is_okay(rectangle, xval, yval):
    """
    Return true if location is in the rectangle and not used.
    """
    if xval < 0:
        return False
    if yval < 0:
        return False
    if xval >= len(rectangle[0]):
        return False
    if yval >= len(rectangle):
        return False
    if rectangle[yval][xval] != 0:
        return False
    return True


def _get_backup_path(last, tree):
    """
    From a leaf node, generate the path up the tree
    """
    if last < 0:
        return last
    return _gbp_withp(last, tree[last]['prev_gen'], tree)


def _gbp_withp(last, parent, tree):
    """
    Recursively support _get_backup_path searching
    """
    if parent < 0:
        return -1
    if tree[parent]['offspring'].index(last) + 1 < len(tree[
            parent]['offspring']):
        return tree[parent]['offspring'][
            tree[parent]['offspring'].index(last) + 1]
    return _gbp_withp(parent, tree[parent]['prev_gen'], tree)
