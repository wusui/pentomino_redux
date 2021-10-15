"""
Check for symmetrical duplicates
"""


def bad_sym(rectangle, sym_info):
    """
    Return False if this layout is symetrical to a flipped layout
    """
    if any(map(_chk_sym(_find_x_mid(rectangle))(sym_info),
               [[1, 1, 0], [3, 0, 2]])):
        return False
    if _get_w_score(rectangle, sym_info, 1, 0) > 0:
        return True
    if _get_w_score(rectangle, sym_info, 3, 0) > 0:
        return True
    return False


def _chk_sym(xlyst):
    """
    Check symetry at a pentomino level
    """
    def _innerf0(sym_info):
        def _innerf1(vals):
            return (sym_info[vals[0]] == 1 and
                    xlyst[vals[1]] != sym_info[vals[2]])
        return _innerf1
    return _innerf0


def _find_x_mid(rectangle):
    """
    Find midldle point of the X-pentomino
    """
    return tuple(filter(_filter_x_only, map(_get_xloc(rectangle),
                                            range(0, 60))))[2]


def _filter_x_only(value):
    """
    Check for invalid Marker
    """
    if value != [-1, -1]:
        return True
    return False


def _get_xloc(rectangle):
    """
    Get location of the X-pentominno
    """
    def _innerf(value):
        if rectangle[value % len(rectangle)][value //
                                             len(rectangle)] == 29:
            return [value // len(rectangle), value % len(rectangle)]
        return [-1, -1]
    return _innerf


def _get_w_score(rectangle, sym_info, indx, count=0):
    """
    Check location of the w-pentomino
    """
    if count == 60:
        return 0
    return _get_w_square(rectangle, sym_info, count) + _get_w_score(
        rectangle, sym_info, indx, count+1)


def _get_w_square(rectangle, sym_info, count):
    """
    Check a square in the w-pentomino
    """
    return sum(tuple(map(_get_score(rectangle)(sym_info)(count), [3, 1])))


def _get_score(rectangle):
    """
    Get count of locations above vs below or left vs right in order to do
    symetry checks.
    """
    def _get_row(xrow):
        return xrow // len(rectangle)

    def _get_rot_row(xrow):
        return xrow % len(rectangle)

    def _local_op(indx):
        return [_get_rot_row, _get_row][indx // 2]

    def _inner1(sym_info):
        def _inner2(count):
            def _inner3(dirv):
                if rectangle[_get_rot_row(count)][_get_row(count)] == 135:
                    if sym_info[dirv] == 1:
                        if _local_op(dirv)(count) < sym_info[dirv - 1]:
                            return 1
                        if _local_op(dirv)(count) > sym_info[dirv - 1]:
                            return -1
                return 0
            return _inner3
        return _inner2
    return _inner1
