"""
Find the pentomino value for all leaf nodes in the tree
"""
from tree_build import new_tree
from tree_utils import extract_path, fig_comp


def build_pent_tree():
    """
    Build tree with pentomino information in pent_type field
    """
    return tuple(_set_pents(new_tree([{'point': [0, 0], 'prev_gen': -1,
                                       'offspring': []}])))


def _set_pents(tree):
    """
    Call _pent_chk for every node on the tree
    """
    return map(_pent_chk(tree), tree)


def _pent_chk(tree):
    """
    Get pent_type information
    """
    def _innerf(node):
        if 'fig_value' in node:
            node['pent_type'] = _find_pents(extract_path(node, tree))
        return node
    return _innerf


def _find_pents(path):
    """
    Find pentomino value by selecting the minimum fig_comp value for all
    orientations of the figure being checked
    """
    return min(map(_rotate_work(path), range(0, 8)))


def _rotate_work(path):
    """
    Get coordinates of a rotated figure
    """
    def _innerf(rot_type):
        return fig_comp(_rot_path_compute(_gen_new_path(rot_type)))

    def _gen_new_path(rot_type):
        return tuple(list(map(_gen_rotated_point(rot_type), path)) + [[0, 0]])
    return _innerf


def _gen_rotated_point(rot_type):
    """
    Get new coordinates of a tile based on rotation number
    """
    def _innerf(tile):
        return [tile[_get_rotx(rot_type)] * [1, 1, -1, -1][rot_type % 4],
                tile[_get_roty(rot_type)] * [1, -1, 1, -1][rot_type % 4]]
    return _innerf


def _rot_path_compute(rot_path):
    """
    Adjust x and y locations of rotated figure
    """
    return _wrap_remove(_ynorm(_xnorm(rot_path)))


def _xnorm(path):
    """
    line up rotated figure so minimum x value is 0
    """
    return tuple(map(_shiftx(min(map(_get_x_coord, path))), path))


def _ynorm(path):
    """
    Line up rotated figure so that minimum y value where x = 0 is 0
    """
    return tuple(map(_shifty(min(map(_get_y_coord,
                                     filter(_chk_y_path, path)))), path))


def _shiftx(offset):
    """
    Move rotated figure along x access to line up the origin point
    """
    def _innerf(tile):
        tile[0] -= offset
        return tile
    return _innerf


def _shifty(offset):
    """
    Move rotated figure along y access to line up the origin point
    """
    def _innerf(tile):
        tile[1] -= offset
        return tile
    return _innerf


def _get_x_coord(tile):
    """
    Return x coordinate of square
    """
    return tile[0]


def _get_y_coord(tile):
    """
    Return y coordinate of square
    """
    return tile[1]


def _chk_y_path(tile):
    """
    Check to make sure tile is among left most possible tiles
    """
    if tile[0] == 0:
        return True
    return False


def _get_rotx(rot_type):
    """
    Return x coordinate for this rotation
    """
    return 1 if rot_type >= 4 else 0


def _get_roty(rot_type):
    """
    Return y coordinate for this rotation
    """
    return 0 if rot_type >= 4 else 1


def _wrap_remove(rot_path):
    """
    Once the new figure has been lined up properly, get rid of origin
    """
    return filter(_remove_zeros, rot_path)


def _remove_zeros(point_value):
    """
    Don't check origin tile in some cases
    """
    if point_value == [0, 0]:
        return False
    return True
