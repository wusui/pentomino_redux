"""
_get_offspring and associated functions
"""


def get_complete_gen(tree):
    """
    Given a tree, return a list of lists indexed by node number.
    Each list entry is a set of points that can be added
    as an offspring node to that node
    """
    return map(_get_new_points(tree), range(len(tree)))


def _get_new_points(tree):
    """
    Gen_offspring_points wrapper
    """
    def _func1(node):
        return _gen_offspring_points(_get_parents(tree, node))
    return _func1


def _get_parents(tree, node, plist=None):
    """
    Recursively look for parent nodes
    """
    if plist is None:
        plist = []
    plist.append(tree[node]['point'])
    if tree[node]['prev_gen'] < 0:
        return list(_uniqify(plist))
    return _get_parents(tree, tree[node]['prev_gen'], plist)


def _gen_offspring_points(parents):
    """
    Wrapper to return T/F value frsom _make_one_list calls
    """
    def _check_dupe(point):
        return point not in parents
    return list(filter(_check_dupe, _make_one_list(parents)))


def _make_one_list(points):
    """
    Return one list of unique points
    """
    return _uniqify(_combined_lists(_get_all_possible_points(points)))


def _uniqify(alist):
    """
    Given a list, return a list with duplicates removed.
    """
    return list(map(list, set(list(map(tuple, alist)))))


def _combined_lists(alist, total=None):
    """
    Given a list of lists, make that set of lists one list
    """
    if total is None:
        total = []
    if not alist:
        return total
    return _combined_lists(alist[1:], total + alist[0])


def _get_all_possible_points(points):
    """
    Given a list of points, for each point return a list of all
    possible new neighbor points that can be added.
    """
    return list(map(_get_next_points, points))


def _get_next_points(points):
    """
    Return valid next points (yet unused neighbors to points passed)
    """
    return list(filter(_is_configurable, _get_points(points)))


def _get_points(point):
    """
    Return list of possible neighbor points to a given point
    """
    return [[point[0], point[1] + 1],
            [point[0], point[1] - 1],
            [point[0] + 1, point[1]],
            [point[0] - 1, point[1]]
            ]


def _is_configurable(point):
    """
    Filter comparison function to make sure point is in valid range
    """
    return point[0] >= 0 and (point[1] >= 0 or point[0] > 0)
