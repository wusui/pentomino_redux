"""
Solve pentomino filling of a rectangle
"""
from functools import reduce
from operator import iconcat
from rect_solutions import scan_pent, set_fig_in_pt_set


def solve_case(rectangle, tree, io_obj):
    """
    Main program to recursively fill a rectangle with pentominos
    """
    return tuple(map(_solve_rect_with_x(rectangle)(tree)([
        len(rectangle) // 2, len(rectangle) % 2,
        len(rectangle[0]) // 2, len(rectangle[0]) % 2])(io_obj),
                     tuple(_get_x_center_pts(len(rectangle) // 2 +
                                             len(rectangle) % 2,
                                             len(rectangle[0]) // 2
                                             + len(rectangle[0]) % 2))))


def _get_x_center_pts(halfway_x, halfway_y):
    """
    Find locations of x-pentomino center points
    """
    return reduce(iconcat, _get_pt_tuple(range(1, halfway_x),
                                         range(1, halfway_y)))


def _get_pt_tuple(pnt1, pnt2):
    """
    get ranges, return tuple of valid x-pentomino center points
    """
    return tuple(map(_map_x_dim(tuple(pnt1)), pnt2))


def _map_x_dim(xdim):
    """
    Get x-coordinate of x-pentomino center point
    """
    def _innerf(zdim):
        return tuple(map(_map_y_dim(zdim), xdim))
    return _innerf


def _map_y_dim(zdim):
    """
    Get y-coordinate of x-pentomino center point
    """
    def _innerf(xdim):
        return [zdim, xdim]
    return _innerf


def _solve_rect_with_x(rectangle):
    """
    Wrap solving code
    """
    def _inner1(tree):
        def _inner2(sym_info):
            def _inner4(io_obj):
                def _inner5(x_pent_coords):
                    return _manipulate_x_value(rectangle, [tree, sym_info],
                                               x_pent_coords, io_obj)
                return _inner5
            return _inner4
        return _inner2
    return _inner1


def _manipulate_x_value(rectangle, tree_sym_info, x_pent_coords, io_obj):
    """
    Set x-pentomino in rectangle, do scan, clear x-pentomino
    """
    rectangle = _set_x_rect(rectangle, x_pent_coords[1], x_pent_coords[0], 29)
    scan_pent(rectangle, tree_sym_info[1], tree_sym_info[0], io_obj)
    rectangle = _set_x_rect(rectangle, x_pent_coords[1], x_pent_coords[0], 0)


def _set_x_rect(rectangle, ycent, xcent, value):
    """
    Set the points in the x-pentomino
    """
    return set_fig_in_pt_set(rectangle, value,
                             tuple(map(_curry_point_pt([ycent, xcent]),
                                       [[0, 0], [1, 0], [-1, 0], [0, 1],
                                        [0, -1]])))


def _curry_point_pt(center_point):
    """
    Given center, set other points in x-pentomino
    """
    def _innerf1(offset):
        return [center_point[0] + offset[0], center_point[1] + offset[1]]
    return _innerf1
