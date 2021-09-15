"""
Find the pentomino value for all leaf nodes in the tree
"""
from solver.build_tree import new_tree
from solver.tree_utils import extract_path, fig_comp


def set_pents(tree):
    """
    Call pent_chk for every node on the tree
    """
    return map(pent_chk(tree), tree)


def pent_chk(tree):
    """
    Get pent_type information
    """
    def innerf(node):
        if 'fig_value' in node:
            node['pent_type'] = find_pents(extract_path(node, tree))
        return node
    return innerf


def shiftx(offset):
    """
    Move rotated figure along x access to line up the origin point
    """
    def innerf(tile):
        tile[0] -= offset
        return tile
    return innerf


def shifty(offset):
    """
    Move rotated figure along y access to line up the origin point
    """
    def innerf(tile):
        tile[1] -= offset
        return tile
    return innerf


def get_x_coord(tile):
    """
    Return x coordinate of square
    """
    return tile[0]


def get_y_coord(tile):
    """
    Return y coordinate of square
    """
    return tile[1]


def chk_y_path(tile):
    """
    Check to make sure tile is among left most possible tiles
    """
    if tile[0] == 0:
        return True
    return False


def xnorm(path):
    """
    line up rotated figure so minimum x value is 0
    """
    return list(map(shiftx(min(map(get_x_coord, path))), path))


def ynorm(path):
    """
    Line up rotated figure so that minimum y value where x = 0 is 0
    """
    return list(map(shifty(min(map(get_y_coord, filter(chk_y_path, path)))),
                    path))


def rotate_work(path):
    """
    Get coordinates of a rotated figure
    """
    def innerf(rot_type):
        return fig_comp(rot_path_compute(gen_new_path(rot_type)))

    def gen_new_path(rot_type):
        return list(map(gen_rotated_point(rot_type), path)) + [[0, 0]]
    return innerf


def gen_rotated_point(rot_type):
    """
    Get new coordinates of a tile based on rotation number
    """
    def innerf(tile):
        return [tile[get_rotx(rot_type)] * [1, 1, -1, -1][rot_type % 4],
                tile[get_roty(rot_type)] * [1, -1, 1, -1][rot_type % 4]]
    return innerf


def get_rotx(rot_type):
    """
    Return x coordinate for this rotation
    """
    return 1 if rot_type >= 4 else 0


def get_roty(rot_type):
    """
    Return y coordinate for this rotation
    """
    return 0 if rot_type >= 4 else 1


def rot_path_compute(rot_path):
    """
    Adjust x and y locations of rotated figure
    """
    return wrap_remove(ynorm(xnorm(rot_path)))


def wrap_remove(rot_path):
    """
    Once the new figure has been lined up properly, get rid of origin
    """
    rot_path.remove([0, 0])
    return rot_path


def find_pents(path):
    """
    Find pentomino value by selecting the minimum fig_comp value for all
    orientations of the figure being checked
    """
    return min(map(rotate_work(path), range(0, 8)))


def get_origin():
    """
    Start with the [0, 0] square
    """
    return [{'point': [0, 0], 'prev_gen': -1, 'offspring': []}]


def build_pent_tree():
    """
    Build tree with pentomino information in pent_type field
    """
    return list(set_pents(new_tree(get_origin())))
