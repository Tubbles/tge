#!/usr/bin/env python3


def mapping_from_rule(rule):
    """
    >>> mapping_from_rule(30)
    [False, False, False, True, True, True, True, False]
    >>> mapping_from_rule(110)
    [False, True, True, False, True, True, True, False]
    """
    return [bool(int(char)) for char in list(f"{rule:08b}")]


def elementary_cellular_automata(prev_cells, rule_mapping) -> bool:
    """
    >>> elementary_cellular_automata([True, True, True], mapping_from_rule(110))
    False
    >>> elementary_cellular_automata([True, True, False], mapping_from_rule(110))
    True
    >>> elementary_cellular_automata([True, False, True], mapping_from_rule(110))
    True
    >>> elementary_cellular_automata([True, False, False], mapping_from_rule(110))
    False
    >>> elementary_cellular_automata([False, True, True], mapping_from_rule(110))
    True
    >>> elementary_cellular_automata([False, True, False], mapping_from_rule(110))
    True
    >>> elementary_cellular_automata([False, False, True], mapping_from_rule(110))
    True
    >>> elementary_cellular_automata([False, False, False], mapping_from_rule(110))
    False
    """
    if prev_cells == [True, True, True]:
        return rule_mapping[0]
    elif prev_cells == [True, True, False]:
        return rule_mapping[1]
    elif prev_cells == [True, False, True]:
        return rule_mapping[2]
    elif prev_cells == [True, False, False]:
        return rule_mapping[3]
    elif prev_cells == [False, True, True]:
        return rule_mapping[4]
    elif prev_cells == [False, True, False]:
        return rule_mapping[5]
    elif prev_cells == [False, False, True]:
        return rule_mapping[6]
    elif prev_cells == [False, False, False]:
        return rule_mapping[7]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
