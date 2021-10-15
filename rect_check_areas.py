"""
Check to make sure that layout still has valid open areas
"""
from collections import Counter


def areas_ok_size(rectangle):
    """
    find a blank area and make sure it has a valid size
    """
    rectangle = _find_blank_area(rectangle, 0, -1)
    return _cleanup_signs(_validate_all_blank_sizes(rectangle), rectangle)


def _find_blank_area(rectangle, indx, marker):
    """
    Find blank area (used for testing if all blank partitions of a rectangle
    are valid)
    """
    if indx == 60:
        return rectangle
    if rectangle[indx % len(rectangle)][indx // len(rectangle)] == 0:
        _mark_up(rectangle, indx % len(rectangle), indx // len(rectangle),
                 marker)
        rectangle = _find_blank_area(rectangle, indx + 1, marker - 1)
    else:
        rectangle = _find_blank_area(rectangle, indx + 1, marker)
    return rectangle


def _mark_up(rectangle, irow, icol, checkr):
    """
    Given a square in an area, make sure all blank neighbors get
    similarly marked
    """
    rectangle[irow][icol] = checkr
    if irow > 0 and rectangle[irow - 1][icol] == 0:
        _mark_up(rectangle, irow - 1, icol, checkr)
    if icol > 0 and rectangle[irow][icol - 1] == 0:
        _mark_up(rectangle, irow, icol - 1, checkr)
    if irow < len(rectangle) - 1 and rectangle[irow + 1][icol] == 0:
        _mark_up(rectangle, irow + 1, icol, checkr)
    if icol < len(rectangle[0]) - 1 and rectangle[irow][icol + 1] == 0:
        _mark_up(rectangle, irow, icol + 1, checkr)


def _validate_all_blank_sizes(rectangle):
    """
    Make sure all blank areas are fillable
    """
    return all(tuple(map(_get_pent_size, _get_hole_hist(rectangle))))


def _get_pent_size(count):
    """
    Return true if pentominos can fill the number of squares passed
    """
    return count % 5 == 0


def _get_hole_hist(rectangle):
    """
    Return histogram of areas of blank spaces
    """
    return tuple(dict(Counter(_get_linear(rectangle))).values())


def _get_linear(rectangle):
    """
    Make rectangle data a single list
    """
    return tuple(map(_make_linear(rectangle), range(0, 60)))


def _make_linear(rectangle):
    """
    Extract single tile for _get_linear support
    """
    def _inner(coord):
        return rectangle[coord // len(rectangle[0])][coord % len(rectangle[0])]
    return _inner


def _cleanup_signs(value, rectangle):
    """
    Set marked squares to 0
    """
    rectangle = _reset_negative_rectangle_values(rectangle, 0)
    return value


def _reset_negative_rectangle_values(rectangle, count):
    """
    Clean up negative marks used in area checking
    """
    if count == 60:
        return rectangle
    if rectangle[count % len(rectangle)][count // len(rectangle)] < 0:
        rectangle[count % len(rectangle)][count // len(rectangle)] = 0
    return _reset_negative_rectangle_values(rectangle, count + 1)
