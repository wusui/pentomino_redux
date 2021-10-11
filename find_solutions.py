"""
Solve pentomino filling of a rectangle
"""
from functools import reduce
from operator import iconcat
from collections import Counter


def solve_case(rectangle, tree, ret_info, io_obj):
    """
    Main program to recursively fill a rectangle with pentominos
    """
    return tuple(map(solve_rect_with_x(rectangle)(tree)([
        len(rectangle) // 2, len(rectangle) % 2,
        len(rectangle[0]) // 2, len(rectangle[0]) % 2])(ret_info)(io_obj),
                     tuple(get_x_center_pts(len(rectangle) // 2 +
                                            len(rectangle) % 2,
                                            len(rectangle[0]) // 2
                                            + len(rectangle[0]) % 2))))


def map_x_dim(xdim):
    """
    Get x-coordinate of x-pentomino center point
    """
    def innerf(zdim):
        return tuple(map(map_y_dim(zdim), xdim))
    return innerf


def map_y_dim(zdim):
    """
    Get y-coordinate of x-pentomino center point
    """
    def innerf(xdim):
        return [zdim, xdim]
    return innerf


def get_pt_tuple(pnt1, pnt2):
    """
    get ranges, return tuple of valid x-pentomino center points
    """
    return tuple(map(map_x_dim(tuple(pnt1)), pnt2))


def get_x_center_pts(halfway_x, halfway_y):
    """
    Find locations of x-pentomino center points
    """
    return reduce(iconcat, get_pt_tuple(range(1, halfway_x),
                                        range(1, halfway_y)))


def manipulate_x_value(rectangle, tree_sym_info, ret_info, x_pent_coords,
                       io_obj):
    """
    Set x-pentomino in rectangle, do scan, clear x-pentomino
    """
    rectangle = set_x_rect(rectangle, x_pent_coords[1], x_pent_coords[0], 29)
    ret_info = accum_pents(scan_pent(rectangle, tree_sym_info[1],
                                     tree_sym_info[0], io_obj), ret_info)
    rectangle = set_x_rect(rectangle, x_pent_coords[1], x_pent_coords[0], 0)
    return ret_info


def solve_rect_with_x(rectangle):
    """
    Wrap solving code
    """
    def inner1(tree):
        def inner2(sym_info):
            def inner3(ret_info):
                def inner4(io_obj):
                    def inner5(x_pent_coords):
                        return manipulate_x_value(rectangle, [tree, sym_info],
                                                  ret_info, x_pent_coords,
                                                  io_obj)
                    return inner5
                return inner4
            return inner3
        return inner2
    return inner1


def accum_pents(result, ret_info):
    """
    Add result to return info list
    """
    if result:
        ret_info += [result]
    return ret_info


def set_x_rect(rectangle, ycent, xcent, value):
    """
    Set the points in the x-pentomino
    """
    return set_fig_in_pt_set(rectangle, value,
                             tuple(map(curry_point_pt([ycent, xcent]),
                                       [[0, 0], [1, 0], [-1, 0], [0, 1],
                                        [0, -1]])))


def set_fig_in_pt_set(rectangle, value, points):
    """
    General routine to set tiles found in points to value
    """
    if not points:
        return rectangle
    rectangle[points[0][0]][points[0][1]] = value
    set_fig_in_pt_set(rectangle, value, points[1:])
    return rectangle


def curry_point_pt(center_point):
    """
    Given center, set other points in x-pentomino
    """
    def innerf1(offset):
        return [center_point[0] + offset[0], center_point[1] + offset[1]]
    return innerf1


def scan_pent(rectangle, sym_info, tree, io_obj):
    """
    Call solver if blank squares are all valid
    """
    if not areas_ok_size(rectangle[:]):
        return None
    return solver(rectangle, tree, sym_info, io_obj)


def g_test(rectangle, tree, sqloc, sym_info, node):
    """
    General test to fail a pentomino if it is already in use, does not fit,
    or results in a symetry error.
    """
    if fig_used(rectangle, tree[node]['pent_type']):
        return False
    if not fig_is_okay(tree, rectangle, sqloc[0], sqloc[1], node):
        return False
    if bad_sym(rectangle, sym_info):
        return False
    return True


def chk_guess(rectangle):
    """
    General test wrapper so that checks can be called from a filter call.
    """
    def inner1(tree):
        def inner2(irow):
            def inner3(icol):
                def inner4(sym_info):
                    def chk_guess1(node):
                        return g_test(rectangle, tree, [irow, icol], sym_info,
                                      node)
                    return chk_guess1
                return inner4
            return inner3
        return inner2
    return inner1


def good_guesses(rectangle, tree, irow, icol, sym_info):
    """
    Return end points in tree that are possible figures in a solution.
    """
    return filter(chk_guess(rectangle)(tree)(irow)(icol)(sym_info),
                  gen_guesses(rectangle, [irow, icol], tree, 0, []))


def solver(rectangle, tree, sym_info, output):
    """
    Main recursive solution routine
    """
    def curry_node(rectangle):
        def inner1(tree):
            def inner2(sqloc):
                def inner3(sym_info):
                    def inner4(output):
                        def inner5(node):
                            resolve(tree, [sqloc, sym_info], output,
                                    set_fig(tree, rectangle[:], sqloc, node,
                                            tree[node]['pent_type'])[:], node)
                            return ''
                        def resolve(tree, sqloc_sym_info, output,
                                    new_rect, node):
                            if areas_ok_size(new_rect[:]):
                                solver(new_rect[:], tree, sqloc_sym_info[1],
                                       output)
                            set_fig(tree, new_rect, sqloc_sym_info[0], node, 0)
                        return inner5
                    return inner4
                return inner3
            return inner2
        return inner1

    def curry_sqloc(sqloc):
        def inner1(output):
            def inner2(rectangle):
                if sqloc[0] >= 0:
                    tuple(map(curry_node(rectangle)(tree)(sqloc)(sym_info)
                              (output), good_guesses(rectangle, tree, sqloc[0],
                                                     sqloc[1], sym_info)))
                else:
                    output(translate(rectangle))
            return inner2
        return inner1
    return curry_sqloc(get_sq_loc(rectangle, 0))(output)(rectangle)


def get_sq_loc(rectangle, value, count=0):
    """
    Find starting square at which to try next pentomino
    """
    if count == 60:
        return -1, -1
    if curry_point(rectangle)(value, count):
        return count % len(rectangle), count // len(rectangle)
    return get_sq_loc(rectangle, value, count+1)


def curry_point(rectangle):
    """
    Check if point in rectangle is value expected
    """
    def innerf(value, count):
        return rectangle[count % len(rectangle)][count //
                                                 len(rectangle)] == value
    return innerf


def gen_guesses(rectangle, sqloc, tree, last, retv):
    """
    Return list of all pentomino leaf nodes in tree that fit into the
    location specified
    """
    while last >= 0:
        while tree[last]['offspring']:
            if not square_is_okay(rectangle,
                                  sqloc[1] + tree[last]['point'][0],
                                  sqloc[0] + tree[last]['point'][1]):
                last = get_backup_path(last, tree)
                if last == -1:
                    break
            else:
                last = tree[last]['offspring'][0]
        if 'pent_type' in tree[last]:
            retv.append(last)
        last = get_backup_path(last, tree)
    return retv


def fig_is_okay(tree, rectangle, irow, icol, last):
    """
    True if the figure checked fits into the rectangle
    """
    if last < 0:
        return True
    if not square_is_okay(rectangle,
                          icol + tree[last]['point'][0],
                          irow + tree[last]['point'][1]):
        return False
    return fig_is_okay(tree, rectangle, irow, icol,
                       tree[last]['prev_gen'])


def fig_nset(tree, rectangle, sqloc, node, nlyst):
    """
    Set node value in rectangle
    """
    if node < 0:
        return nlyst
    nlyst.append([sqloc[0] + tree[node]['point'][1],
                  sqloc[1] + tree[node]['point'][0]])
    return fig_nset(tree, rectangle, sqloc, tree[node]['prev_gen'], nlyst)


def set_fig(tree, rectangle, sqloc, node, fig):
    """
    Set figure in rectangle
    """
    return set_fig_in_pt_set(rectangle, fig,
                             fig_nset(tree, rectangle, sqloc, node, []))


def fig_used(rectangle, value):
    """
    Return true if the figure is already in use
    """
    return any(map(chk_fig(value), rectangle))


def chk_fig(value):
    """
    Check a fig for fig_used mapping
    """
    def innerf(in_data):
        if value in in_data:
            return True
        return False
    return innerf


def square_is_okay(rectangle, xval, yval):
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


def gbp_withp(last, parent, tree):
    """
    Recursively support get_backup_path searching
    """
    if parent < 0:
        return -1
    if tree[parent]['offspring'].index(last) + 1 < len(tree[
            parent]['offspring']):
        return tree[parent]['offspring'][
            tree[parent]['offspring'].index(last) + 1]
    return gbp_withp(parent, tree[parent]['prev_gen'], tree)


def get_backup_path(last, tree):
    """
    From a leaf node, generate the path up the tree
    """
    if last < 0:
        return last
    return gbp_withp(last, tree[last]['prev_gen'], tree)


def find_blank_area(rectangle, indx, marker):
    """
    Find blank area (used for testing if all blank partitions of a rectangle
    are valid)
    """
    if indx == 60:
        return rectangle
    if rectangle[indx % len(rectangle)][indx // len(rectangle)] == 0:
        mark_up(rectangle, indx % len(rectangle), indx // len(rectangle),
                marker)
        rectangle = find_blank_area(rectangle, indx + 1, marker - 1)
    else:
        rectangle = find_blank_area(rectangle, indx + 1, marker)
    return rectangle


def make_linear(rectangle):
    """
    Extract single tile for get_linear support
    """
    def inner(coord):
        return rectangle[coord // len(rectangle[0])][coord % len(rectangle[0])]
    return inner


def get_linear(rectangle):
    """
    Make rectangle data a single list
    """
    return tuple(map(make_linear(rectangle), range(0, 60)))


def get_pent_size(count):
    """
    Return true if pentominos can fill the number of squares passed
    """
    return count % 5 == 0


def fix_negative_values(pent_tile):
    """
    Make sure marked blanks are counted as empty squares
    """
    if pent_tile < 0:
        return 0
    return pent_tile


def reset_negative_rectangle_values(rectangle, count):
    """
    Clean up negative marks used in area checking
    """
    if count == 60:
        return rectangle
    if rectangle[count % len(rectangle)][count // len(rectangle)] < 0:
        rectangle[count % len(rectangle)][count // len(rectangle)] = 0
    return reset_negative_rectangle_values(rectangle, count + 1)


def cleanup_signs(value, rectangle):
    """
    Set marked squares to 0
    """
    rectangle = reset_negative_rectangle_values(rectangle, 0)
    return value


def get_hole_hist(rectangle):
    """
    Return histogram of areas of blank spaces
    """
    return tuple(dict(Counter(get_linear(rectangle))).values())


def validate_all_blank_sizes(rectangle):
    """
    Make sure all blank areas are fillable
    """
    return all(tuple(map(get_pent_size, get_hole_hist(rectangle))))


def areas_ok_size(rectangle):
    """
    find a blank area and make sure it has a valid size
    """
    rectangle = find_blank_area(rectangle, 0, -1)
    return cleanup_signs(validate_all_blank_sizes(rectangle), rectangle)


def mark_up(rectangle, irow, icol, checkr):
    """
    Given a square in an area, make sure all blank neighbors get
    similarly marked
    """
    rectangle[irow][icol] = checkr
    if irow > 0 and rectangle[irow - 1][icol] == 0:
        mark_up(rectangle, irow - 1, icol, checkr)
    if icol > 0 and rectangle[irow][icol - 1] == 0:
        mark_up(rectangle, irow, icol - 1, checkr)
    if irow < len(rectangle) - 1 and rectangle[irow + 1][icol] == 0:
        mark_up(rectangle, irow + 1, icol, checkr)
    if icol < len(rectangle[0]) - 1 and rectangle[irow][icol + 1] == 0:
        mark_up(rectangle, irow, icol + 1, checkr)


def chk_sym(xlyst):
    """
    Check symetry at a pentomino level
    """
    def innerf0(sym_info):
        def innerf1(vals):
            return (sym_info[vals[0]] == 1 and
                    xlyst[vals[1]] != sym_info[vals[2]])
        return innerf1
    return innerf0


def bad_sym(rectangle, sym_info):
    """
    Return False if this layout is symetrical to a flipped layout
    """
    if any(map(chk_sym(find_x_mid(rectangle))(sym_info),
               [[1, 1, 0], [3, 0, 2]])):
        return False
    if get_w_score(rectangle, sym_info, 1, 0) > 0:
        return True
    if get_w_score(rectangle, sym_info, 3, 0) > 0:
        return True
    return False


def get_w_score(rectangle, sym_info, indx, count=0):
    """
    Check location of the w-pentomino
    """
    if count == 60:
        return 0
    return get_w_square(rectangle, sym_info, count) + get_w_score(
        rectangle, sym_info, indx, count+1)


def get_w_square(rectangle, sym_info, count):
    """
    Check a square in the w-pentomino
    """
    return sum(tuple(map(get_score(rectangle)(sym_info)(count), [3, 1])))


def get_score(rectangle):
    """
    Get count of locations above vs below or left vs right in order to do
    symetry checks.
    """
    def get_row(xrow):
        return xrow // len(rectangle)

    def get_rot_row(xrow):
        return xrow % len(rectangle)

    def local_op(indx):
        return [get_rot_row, get_row][indx // 2]

    def inner1(sym_info):
        def inner2(count):
            def inner3(dirv):
                if rectangle[get_rot_row(count)][get_row(count)] == 135:
                    if sym_info[dirv] == 1:
                        if local_op(dirv)(count) < sym_info[dirv - 1]:
                            return 1
                        if local_op(dirv)(count) > sym_info[dirv - 1]:
                            return -1
                return 0
            return inner3
        return inner2
    return inner1


def find_x_mid(rectangle):
    """
    Find midldle point of the X-pentomino
    """
    return tuple(filter(filter_x_only, map(get_xloc(rectangle),
                                           range(0, 60))))[2]


def filter_x_only(value):
    """
    Check for invalid Marker
    """
    if value != [-1, -1]:
        return True
    return False


def get_xloc(rectangle):
    """
    Get location of the X-pentominno
    """
    def innerf(value):
        if rectangle[value % len(rectangle)][value //
                                             len(rectangle)] == 29:
            return [value // len(rectangle), value % len(rectangle)]
        return [-1, -1]
    return innerf


def translate(rectangle):
    """
    Convert rectangle numbers to pentomino characters
    """
    return '\n'.join(tuple(map(line_conv, rectangle))) + '\n\n'


def line_conv(chars_to_conv):
    """
    Convert a row of the rectangle from numbers to pentomino characters
    """
    return ''.join(tuple(map(fconvert, chars_to_conv)))


def fconvert(value):
    """
    Convert one tile from a number to a pentomino character
    """
    table = {523: 'U', 39: 'N', 15: 'F', 135: 'W', 23: 'P', 267: 'L',
             139: 'Z', 77: 'T', 85: 'Y', 43: 'V', 33033: 'I', 29: 'X'}
    return table[value]
