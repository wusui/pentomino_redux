"""
Tree pruner
"""
from tree_utils import extract_path, fig_comp


def prune_tree(tree):
    """
    Given a tree, remove all figures that are duplicates
    of previous figures
    """
    return _get_result(_get_unique_figs(tree))()


def _get_unique_figs(tree):
    """
    Extract duplicate figures from the tree
    """
    return _find_unique_figures_wrap(list(map(_get_fig_values(tree),
                                              tree)), [])


def _get_result(tree):
    """
    Get indices of nodes not being kept, and delete those nodes.
    """
    def _innerf():
        return list(map(_do_node_delete(tree),
                        list(map(_get_indices,
                                 _get_nokeep(tree)))))[-1]
    return _innerf


def _get_indices(element):
    """
    Return first element
    """
    return element[0]


def _do_node_delete(tree):
    """
    Delete a node from the tree.
    """
    def _innerf(indx):
        tree[tree[indx]['prev_gen']]['offspring'].remove(indx)
        tree[indx] = {}
        return tree
    return _innerf


def _get_nokeep(tree):
    """
    Wrap _find_nonkeepers, Return list of nodes not to keep.
    """
    return list(filter(_find_nonkeepers, enumerate(tree)))


def _find_nonkeepers(node):
    """
    Return True for nodes we will delete.
    """
    if 'fig_value' in node[1]:
        if 'dont_delete_me' not in node[1]:
            return True
    return False


def _find_unique_figures_wrap(tree, figs_so_far):
    """
    Find_unique_figures simplification wrapper
    """
    return _find_unique_figures(figs_so_far)(tree)


def _find_unique_figures(figs_so_far):
    """
    Keep track of unique figures so dupicates can be removed
    """
    def _innerf(tree):
        return list(map(_get_figs_so_far, tree))

    def _get_figs_so_far(node):
        if 'fig_value' in node:
            if node['fig_value'] not in figs_so_far:
                figs_so_far.append(node['fig_value'])
                node['dont_delete_me'] = True
        return node
    return _innerf


def _get_fig_values(tree):
    """
    Given a node in a tree set 'fig_value' for that node.
    """
    def _innerf(node):
        if node['offspring'] == []:
            node['fig_value'] = fig_comp(extract_path(node, tree))
        return node
    return _innerf
