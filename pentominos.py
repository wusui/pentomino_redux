"""
Top level function calls for pentomino solver
"""
from tree_find_pents import build_pent_tree
from rect_find_x import solve_case


def fill_rectangles_with_pentominos(io_obj=print, low=3, high=7):
    """
    Loop through rectangle sizes and solve for each.  build_pent_tree
    is called to initialize the tree.  Io_obj is a routine to be used
    to display or store results.  It defaults to a straight print in
    python3, but can be overridden.
    """
    _solve_rectangles(build_pent_tree(), tuple(range(low, high)), io_obj)


def _solve_rectangles(tree, zrange, io_obj):
    """
    Call wrap_rectangle for all values inside the range of rectangle heights
    """
    tuple(map(_wrap_rectangle(tree)(io_obj), zrange))


def _wrap_rectangle(tree):
    """
    Curry process_rectangle calls (called from inside a map function)
    """
    def _inner0(io_obj):
        def _inner1(ysize):
            _process_rectangle(tree, ysize, io_obj)
        return _inner1
    return _inner0


def _process_rectangle(tree, ysize, io_obj):
    """
    Call solve case.  Generate layout of the rectangle first (ysize rows each
    of which are 60 // ysize squares long)
    """
    solve_case([[0 for _ in range(60 // ysize)]
                for _ in range(ysize)], tree, io_obj)


if __name__ == "__main__":
    fill_rectangles_with_pentominos()
