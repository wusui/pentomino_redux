"""
Top level function calls for pentomino solver
"""
from find_pents import build_pent_tree
from find_solutions import solve_case


def fill_rectangles_with_pentominos(io_obj=print, low=3, high=7):
    """
    Loop through rectangle sizes and solve for each.  build_pent_tree
    is called to initialize the tree.  Use this for just printed solutions
    """
    return solve_rectangles(build_pent_tree(), tuple(range(low, high)),
                            io_obj)


def solve_rectangles(tree, zrange, io_obj):
    """
    Return tuple of solutions for pentomino filling for each rectangle
    height
    """
    return tuple(map(wrap_rectangle(tree)(io_obj), zrange))


def wrap_rectangle(tree):
    """
    Curry process_rectangle calls
    """
    def inner0(io_obj):
        def inner1(ysize):
            return process_rectangle(tree, ysize, io_obj)
        return inner1
    return inner0


def process_rectangle(tree, ysize, io_obj):
    """
    Call solve case.  Generate layout of the rectangle first
    """
    return solve_case([[0 for _ in range(60 // ysize)]
                       for _ in range(ysize)], tree, [], io_obj)


if __name__ == "__main__":
    fill_rectangles_with_pentominos()
