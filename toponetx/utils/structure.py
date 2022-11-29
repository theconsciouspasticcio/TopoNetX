from collections import defaultdict
from typing import Dict, List, Tuple, Union


def sparse_array_to_neighborhood_list(
    sparse_array, src_dict=None, dst_dict=None
) -> zip:
    r"""Convert sparse array to neighborhood list for arbitrary higher order structures.
    .. note::
        neighborhood list is a list of tuples such that each tuple has the form (s,t), s and t
        are indices representing a cell in a higher order structure.
        this structure can be converted to a matrix of size |S|X|T| where |S| is
        the size of the source cells and |T| is the size of the target cells.
    Args:
        ``sparse_array``:  sparse array representing the higher order structure between S and T cells
    """
    src_idx, dst_idx = sparse_array.nonzero()

    if src_dict is None and dst_dict is None:
        return zip(dst_idx, src_idx)
    elif src_dict is not None and dst_dict is not None:
        src_list = [src_dict[i] for i in src_idx]
        dest_list = [dst_dict[i] for i in dst_idx]
        return zip(dest_list, src_list)
    else:
        raise ValueError("src_dict and dst_dict must be either None or both not None")


def neighborhood_list_to_neighborhood_dict(
    n_list: List[Tuple[int, int]], src_dict=None, dst_dict=None
) -> Dict[int, List[int]]:
    r"""Convert neighborhood list to neighborhood dictionary for arbitrary higher order structures.
    .. note::
        for every cell i, neighborhood_dict[i] is describe all cells j that are in the neighborhood to j
    Args:
        ``n_list`` (``List[Tuple[int, int]]``): neighborhood list.
    """
    if src_dict is None and dst_dict is None:
        neighborhood_dict = defaultdict(list)
        for src_idx, dst_idx in n_list:
            neighborhood_dict[src_idx].append(dst_idx)
        return neighborhood_dict
    elif src_dict is not None and dst_dict is not None:
        for src_idx, dst_idx in n_list:
            neighborhood_dict[src_dict[src_idx]].append(dst_dict[dst_idx])
        return neighborhood_dict
    else:
        raise ValueError("src_dict and dst_dict must be either None or both not None")


def sparse_array_to_neighborhood_dict(
    sparse_array, src_dict=None, dst_dict=None
) -> Dict[int, List[int]]:
    r"""Convert sparse array to neighborhood dictionary for arbitrary higher order structures.
    .. note::
        neighborhood list is a list of tuples such that each tuple has the form (s,t), s and t
        are indices representing a cell in a higher order structure.
        this structure can be converted to a matrix of size |S|X|T| where |S| is
        the size of the source cells and |T| is the size of the target cells.
    Args:
        ``sparse_array``:  sparse array representing the higher order structure between S and T cells
    """
    return neighborhood_list_to_neighborhood_dict(
        sparse_array_to_neighborhood_list(sparse_array, src_dict, dst_dict)
    )
