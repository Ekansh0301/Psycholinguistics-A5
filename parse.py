"""
Probabilistic Earley Parser
Usage: python parse.py <grammar.gr> <sentences.sen>
"""

import sys

from grammar import load_grammar
from earley import earley
from tree import all_trees, tree_cost, tree_to_str


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python parse.py <grammar.gr> <sentences.sen>")

    rules, by_lhs, nts, rule_map = load_grammar(sys.argv[1])

    if 'ROOT' in by_lhs:
        start_sym = 'ROOT'
    elif 'S' in by_lhs:
        start_sym = 'S'
    else:
        start_sym = list(by_lhs.keys())[0]

    with open(sys.argv[2]) as fh:
        sentences = [line.split() for line in fh if line.strip()]

    # Parse inputs and reconstruct outputs
    for words in sentences:
        chart = earley(words, rules, by_lhs, nts, start=start_sym)
        n = len(words)

        complete_roots = [
            (ridx, len(rules[ridx][2]), 0)
            for ridx in by_lhs.get(start_sym, [])
            if (ridx, len(rules[ridx][2]), 0) in chart[n]
        ]

        if not complete_roots:
            print("NONE")
            continue

        valid_parses = []
        seen = set()

        for root_key in complete_roots:
            for tree in all_trees(root_key, n, chart, rules, words):
                ts = tree_to_str(tree)
                if ts not in seen:
                    seen.add(ts)
                    tc = tree_cost(tree, rule_map)
                    valid_parses.append((tc, ts))

        valid_parses.sort(key=lambda x: x[0])

        for cost, ts in valid_parses:
            print(ts)
            print(cost)


if __name__ == '__main__':
    main()