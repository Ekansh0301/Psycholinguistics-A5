def all_trees(key, col, chart, rules, words, path=None):
    """Yield all distinct parse trees to reconstruct derivations."""
    path = path or frozenset()
    state = (key, col)

    if state in path:
        return

    new_path = path | {state}
    ridx, _, _ = key
    _, lhs, _ = rules[ridx]

    entry = chart[col].get(key)
    if not entry:
        return

    backs = entry['backs']
    if not backs:
        yield (lhs, [])
        return

    for back in backs:
        kind = back[0]
        if kind == 'scan':
            _, prev_key = back
            terminal = words[col - 1]
            children_gen = all_trees(
                prev_key, col - 1, chart, rules, words, new_path
            )
            for partial in children_gen:
                yield (partial[0], partial[1] + [terminal])

        elif kind == 'complete':
            _, left_key, right_key, mid = back
            left_gen = all_trees(left_key, mid, chart, rules, words, new_path)
            for partial in left_gen:
                right_gen = all_trees(
                    right_key, col, chart, rules, words, new_path
                )
                for sub in right_gen:
                    yield (partial[0], partial[1] + [sub])


def tree_cost(tree, rule_map):
    """Calculate total base-2 cost for a single parse tree."""
    lhs, children = tree
    if not children:
        return 0.0

    child_syms = tuple(c if isinstance(c, str) else c[0] for c in children)
    cost = rule_map.get((lhs, child_syms), float('inf'))

    for child in children:
        if isinstance(child, tuple):
            cost += tree_cost(child, rule_map)

    return cost


def tree_to_str(tree, indent=0):
    """Format tree as an S-expression string."""
    lhs, children = tree

    if not children:
        return f"({lhs})"

    if len(children) == 1 and isinstance(children[0], str):
        return f"({lhs} {children[0]})"

    prefix = f"({lhs} "
    child_indent = indent + len(prefix)

    lines = []
    for i, child in enumerate(children):
        if isinstance(child, str):
            child_str = child
        else:
            child_str = tree_to_str(child, child_indent)

        prefix_str = prefix if i == 0 else " " * child_indent
        lines.append(prefix_str + child_str)

    lines[-1] += ")"
    return "\n".join(lines).rstrip('\n')
