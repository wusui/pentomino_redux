"""
Solve pentomino filling of a rectangle
"""
from rect_place import find_placements
from rect_check_areas import areas_ok_size
from rect_translate import translate


def set_fig_in_pt_set(rectangle, value, points):
    """
    General routine to set tiles found in points to value
    """
    if not points:
        return rectangle
    rectangle[points[0][0]][points[0][1]] = value
    set_fig_in_pt_set(rectangle, value, points[1:])
    return rectangle


def scan_pent(rectangle, sym_info, tree, io_obj):
    """
    Call _solver if blank squares are all valid
    """
    if not areas_ok_size(rectangle[:]):
        return None
    return _solver(rectangle, tree, sym_info, io_obj)


def _solver(rectangle, tree, sym_info, output):
    """
    Main recursive solution routine
    """
    def _curry_node(rectangle):
        def _inner1(tree):
            def _inner2(sqloc):
                def _inner3(sym_info):
                    def _inner4(output):
                        def _inner5(node):
                            _resolve(tree, [sqloc, sym_info], output,
                                     _set_fig(tree, rectangle[:], sqloc, node,
                                              tree[node]['pent_type'])[:],
                                     node)
                            return ''
                        def _resolve(tree, sqloc_sym_info, output,
                                     new_rect, node):
                            if areas_ok_size(new_rect[:]):
                                _solver(new_rect[:], tree, sqloc_sym_info[1],
                                        output)
                            _set_fig(tree, new_rect, sqloc_sym_info[0], node,
                                     0)
                        return _inner5
                    return _inner4
                return _inner3
            return _inner2
        return _inner1

    def _curry_sqloc(sqloc):
        def _inner1(output):
            def _inner2(rectangle):
                if sqloc[0] >= 0:
                    tuple(map(_curry_node(rectangle)(tree)(sqloc)(sym_info)
                              (output), find_placements(rectangle, tree,
                                                        sqloc[0], sqloc[1],
                                                        sym_info)))
                else:
                    output(translate(rectangle))
            return _inner2
        return _inner1
    return _curry_sqloc(_get_sq_loc(rectangle, 0))(output)(rectangle)


def _get_sq_loc(rectangle, value, count=0):
    """
    Find starting square at which to try next pentomino
    """
    if count == 60:
        return -1, -1
    if _curry_point(rectangle)(value, count):
        return count % len(rectangle), count // len(rectangle)
    return _get_sq_loc(rectangle, value, count+1)


def _curry_point(rectangle):
    """
    Check if point in rectangle is value expected
    """
    def _innerf(value, count):
        return rectangle[count % len(rectangle)][count //
                                                 len(rectangle)] == value
    return _innerf


def _set_fig(tree, rectangle, sqloc, node, fig):
    """
    Set figure in rectangle
    """
    return set_fig_in_pt_set(rectangle, fig,
                             _fig_nset(tree, rectangle, sqloc, node, []))


def _fig_nset(tree, rectangle, sqloc, node, nlyst):
    """
    Set node value in rectangle
    """
    if node < 0:
        return nlyst
    nlyst.append([sqloc[0] + tree[node]['point'][1],
                  sqloc[1] + tree[node]['point'][0]])
    return _fig_nset(tree, rectangle, sqloc, tree[node]['prev_gen'], nlyst)
