"""
Get the information needed to build a level
"""
from get_offspring import get_complete_gen


def find_next(tree):
    """
    Return a bunch of True/False values.  Each entry will correspond to
    a node in tree.  Offspring values that will be updated at this
    level are True.
    """
    return map(get_changed_nodes, tree)


def get_added_links(tree):
    """
    Return new tuple of information about nodes to be added.

    Returns:
       tuple of tuples zipped together.  Each top level element consists
       of three fields:
           1. True or False depending on if this node is changing.
           2. A set of point representing offspring values.
           3. An index into tree for this node
    """
    return tuple(zip(
        find_next(tree),
        get_complete_gen(tree),
        range(len(tree))))


def get_link_info(tree):
    """
    Add on indices to links to get full information on a new node
    """
    return add_indices(get_added_links(tree))


def add_indices(base_data, pstart=0):
    """
    Add on index values for the new nodes
    """
    if not base_data:
        return base_data
    return [[base_data[0], pstart],
            add_indices(base_data[1:],
                        pstart + len(base_data[0]))]


def get_changed_nodes(node):
    """
    Tester used inside map calls to see if offspring data is empty
    """
    return node['offspring'] == []


def flatten_nodes(node_info):
    """
    Reformat node data that was formerly nested into one flat array.
    """
    if not node_info:
        return []
    return [node_info[0]] + flatten_nodes(node_info[1])


def old_node_test(node_info):
    """
    Test the first entry of the first tuple in the tuple
    """
    return node_info[0][0]


def remove_old_nodes(node_info):
    """
    Remove nodes from tuple that do not have their offspring field changed
    """
    return tuple(filter(old_node_test, node_info))


def format_node_info(node_info):
    """
    Extract just the information we need

    Args:
        node_info (tuple): tuple of node information

    Returns:
        tuple whose entries are:
            - a tuple of points to be added
            - the index in tree where the offspring field will be updated
            - the index in tree where the new nodes will start to be added
    """
    return tuple([node_info[0][1], node_info[0][2], node_info[1]])


def get_just_node_info(node_info):
    """
    Call format_node_name for each entry in node_info
    """
    return tuple(map(format_node_info, node_info))


def get_set_of_node_changes(tree):
    """
    Extract node change information from tree and convert into
    one set of changes.
    """
    return flatten_nodes(get_link_info(tree))


def get_only_changed_nodes(tree):
    """
    Make sure nodes not changing are removed from change array
    """
    return remove_old_nodes(get_set_of_node_changes(tree))


def get_node_changes(tree):
    """
    Get node changes in tree when new level is added.

    Returns:
        new node changes.  Format described by format_node_info
    """
    return get_just_node_info(get_only_changed_nodes(tree))
