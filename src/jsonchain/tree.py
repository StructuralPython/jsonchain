from copy import copy
from typing import Hashable, Union, Optional, Any
import operator
import deepmerge

def compare_tree_values(
    tree_a: dict | list,
    tree_b: dict | list,
    levels_a: list[Hashable | None],
    levels_b: list[Hashable | None],
    leaf_a: Union[Hashable, list[Hashable]],
    leaf_b: Union[Hashable, list[Hashable]],
    compare_func: Union[str, callable],
    compared_key: Optional[Hashable]= None,
    *args,
    **kwargs,
) -> dict:
    """
    Returns a dictionary tree keyed according to 
    'tree_a': the first tree to compare
    'tree_b': the second tree to compare
    'levels_a': The levels to iterate through in order to access the leaf keys in
        'leaves_a'. If a level is listed is None, then all keys at that level will
        be iterated over.
    'levels_b': The levels to iterate through in order to access the leaf keys in
        'leaves_b'. If a level is listed is None, then all keys at that level will
        be iterated over.
    'leaves_a': a list of leaf keys to compare. Must be same length as 'leaves_b'.
    'leaves_b': a list of leaf keys to compare. Must be same length as 'leaves_a'.
    'compare_func': Either one of 
        {'div', 'sub', 'add', 'mult', 'ge', 'le', 'lt', 'gt', 'eq', 'ne'} or a 
        user-supplied callable whos call signature takes the values of the individul
        elements of 'leaves_a' as the first param, the individual elements of 'leaves_b'
        as the second param. Optionally, args and kwargs can be passed and they
        will be passed on to the callable.
    """
    ops = {
        "div": operator.truediv,
        "sub": operator.sub,
        "add": operator.add,
        "mul": operator.mul,
        "ge": operator.ge,
        "le": operator.le,
        "lt": operator.lt,
        "gt": operator.gt,
        "eq": operator.eq,
        "ne": operator.ne,
    }
    env_acc = {}
    # If we are at the last branch...
    subtree_a = retrieve_leaves(tree_a, levels_a, leaf_a)
    subtree_b = retrieve_leaves(tree_b, levels_b, leaf_b)

    branch_a = trim_branches(subtree_a, levels_a)
    branch_b = trim_branches(subtree_b, levels_b)

    for trunk in branch_a.keys():
        value_a = branch_a[trunk]
        value_b = branch_b[trunk]
        comparison_operator = ops.get(compare_func, compare_func)
        compared_value = comparison_operator(value_a, value_b)
        env_acc.setdefault(trunk, {})
        env_acc[trunk].setdefault(leaf_a, value_a)
        env_acc[trunk].setdefault(leaf_b, value_b)
        if compared_key is None:
            compared_key = str(compare_func)
        env_acc[trunk].setdefault(compared_key, compared_value)
    return env_acc


def trim_branches(
    tree: dict | list,
    levels: list[Hashable | None],
):
    """
    Returns a copy of the 'tree' but with the branches in 
    'levels' trimmed off.
    """
    trimmed = tree.copy()
    for i in range(len(levels)):
        leaf = levels.pop()
        trimmed = retrieve_leaves(trimmed, levels, leaf=leaf)
    return trimmed


def retrieve_leaves(
    tree: dict | list, 
    levels: list[Hashable | None], 
    leaf: list[Hashable] | Hashable | None,
) -> dict:
    """
    Envelopes the tree at the leaf node with 'agg_func'.
    """
    env_acc = {}
    key_error_msg = (
        "Key '{level}' does not exist at this level. Available keys: {keys}. "
        "Perhaps not all of your tree elements have the same keys. Try enveloping over trees "
        "that have the same branch structure and leaf names."
    )
    # If we are at the last branch...
    if not levels:
        if leaf is None:
            return tree
        if isinstance(leaf, list):
            leaf_values = {}
            for leaf_elem in leaf:
                try:
                    tree[leaf_elem]
                except KeyError:
                    raise KeyError(key_error_msg.format(level=leaf_elem, keys=list(tree.keys())))
                leaf_values.update({leaf_elem: tree[leaf_elem]})
        else:
            try:
                tree[leaf]
            except KeyError:
                raise KeyError(key_error_msg.format(level=leaf, keys=list(tree.keys())))
            leaf_values = tree[leaf]
        return leaf_values
    else:
        # Otherwise, pop the next level and dive into the tree on that branch
        level = levels[0]
        if level is not None:
            try:
                tree[level]
            except KeyError:
                raise KeyError(key_error_msg.format(level=level, keys=list(tree.keys())))
            env_acc.update({level: retrieve_leaves(tree[level], levels[1:], leaf)})
            return env_acc
        else:
            # If None, then walk all branches of this node of the tree
            if isinstance(tree, list):
                tree = {idx: leaf for idx, leaf in enumerate(tree)}
            for k, v in tree.items():
                env_acc.update({k: retrieve_leaves(v, levels[1:], leaf)})
            return env_acc
        

def extract_keys(
        object: dict[str, Any], 
        key_name: str,
        include_startswith: Optional[str] = None,
        exclude_startswith: Optional[str] = None,
    ) -> list[dict[str, Any]]:
    """
    Returns a list of dicts where each dict has a key of 'key_name'
    and a value of one of the keys of 'object'.

    e.g.
    object = {"key1": value, "key2": value, "key3": value}
    key_name = "label"

    extract_keys(object, key_name) # [{"label": "key1"}, {"label": "key2"}, {"label": "key3"}]

    'include_startswith': If provided, will only include keys that start with this string.
    'exclude_startswith': If provided, will exclude all keys that start with this string.

    If both 'include_startswith' and 'exclude_startswith' are provided, exclude is executed
    first.
    """
    shortlist = []
    for key in object.keys():
        if exclude_startswith is not None and key.startswith(exclude_startswith):
            continue
        else:
            shortlist.append(key)

    acc = []
    for key in shortlist:
        if include_startswith is not None and key.startswith(include_startswith):
            acc.append({key_name: key})
        elif include_startswith is None:
            acc.append({key_name: key})

    return acc

    

def merge_trees(trees: list[dict[str, dict]]) -> dict[str, dict]:
    """
    Merges all of the tress (dictionaries) in 'result_trees'. 

    This is different than a typical dictionary merge (e.g. a | b)
    which will merge dictionaries with different keys but will over-
    write values if two keys are the same.

    Instead, it crawls each branch of the tree and merges the data
    within each branch, no matter how deep the branches go.
    """
    acc = {}
    for result_tree in trees:
        acc = deepmerge.always_merger.merge(acc, result_tree)
    return acc