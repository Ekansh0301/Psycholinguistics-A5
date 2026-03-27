def earley(words, rules, by_lhs, nts, start='ROOT'):
    """Execute Earley algorithm to build a parse chart."""
    n = len(words)
    chart = [{} for _ in range(n + 1)]
    agenda = [[] for _ in range(n + 1)]

    def add(col, ridx, dot, origin, cost, back=None):
        key = (ridx, dot, origin)
        if key not in chart[col]:
            backs_list = [] if back is None else [back]
            chart[col][key] = {'cost': cost, 'backs': backs_list}
            agenda[col].append(key)
        else:
            entry = chart[col][key]
            if cost < entry['cost']:
                entry['cost'] = cost
            if back is not None and back not in entry['backs']:
                entry['backs'].append(back)

    for ridx in by_lhs.get(start, []):
        add(0, ridx, 0, 0, rules[ridx][0])

    for j in range(n + 1):
        ptr = 0
        while ptr < len(agenda[j]):
            key = agenda[j][ptr]
            ptr += 1

            ridx, dot, origin = key
            _, lhs, rhs = rules[ridx]
            curr_cost = chart[j][key]['cost']

            if dot == len(rhs):
                for wkey, we in list(chart[origin].items()):
                    wridx, wdot, worigin = wkey
                    _, _, wrhs = rules[wridx]
                    if wdot < len(wrhs) and wrhs[wdot] == lhs:
                        new_cost = we['cost'] + curr_cost
                        back_ptr = ('complete', wkey, key, origin)
                        add(j, wridx, wdot + 1, worigin, new_cost, back_ptr)
            else:
                sym = rhs[dot]
                if sym in nts:
                    for r2 in by_lhs[sym]:
                        add(j, r2, 0, j, rules[r2][0])
                elif j < n and words[j] == sym:
                    add(j + 1, ridx, dot + 1, origin, curr_cost, ('scan', key))

    return chart
