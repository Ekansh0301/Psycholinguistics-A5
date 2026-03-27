# Probabilistic Earley Parser

A modularised implementation of a probabilistic Earley parser.

## Quick Start

```shell
python parse.py grammar.gr sentences.sen
```

No external libraries or `pip install` commands are needed — it runs on the pure Python 3.6+ standard library!

---

## File Structure

The parser has been modularised for readability and separation of concerns:

| File | Purpose |
|------|---------|
| `parse.py` | The main execution entry point. Coordinates reading inputs and dispatching logic. |
| `grammar.py` | Handles logic for loading Probabilistic Context Free Grammars (PCFG) and computing bits costs `(-log2(p))`. |
| `earley.py` | Contains the core Viterbi-inclusive Earley algorithm `earley()`, keeping $O(n^3)$ complexities and checking bounds. |
| `tree.py` | Separates recursive tree extractions (`all_trees()`), probability computing, and pretty-printing logic into pure functions. |
| `report.md` | Contains the final answers to Assignment 5, documenting costs, Earley's final output charts, and theoretical efficiencies. |

### Sample Data
- `./time/time.gr` & `./time/time.sen`: "time flies like an arrow" 
- `./soldier/soldier.gr` & `./soldier/soldier.sen`: "the man shot the soldier with a gun" (Custom Ambiguity Grammar)

---

## Usage Instructions

1. **Verify Python Configuration:** Make sure you are using Python 3.6 or newer.
2. **Execute Parser Script:**
   ```shell
   python parse.py time/time.gr time/time.sen
   ```
   
*(Notice that we run the orchestrating `parse.py` file directly via the CLI, and it handles the required module relationships dynamically).*

---

## Expected Output format

The program evaluates the ambiguous sentences and emits properly aligned S-expressions followed consecutively by their minimum cost (base-2 logarithmic score):

```text
(S (NP (N time))
   (VP (V flies)
       (ADVP (ADV like)
             (NP (Det an)
                 (N arrow)))))
7.802285552379208
(S (NP (N time)
       (N flies))
   (VP (V like)
       (NP (Det an)
           (N arrow))))
10.024677973715654
```

- `-log₂(probability)` represents the cost. Because probabilities are $\leq 1.0$, minimizing the log cost determines the optimal (most probable) spanning parse structure efficiently!
- The algorithm evaluates distinct possible syntax trees entirely exhaustively, preventing loops but catching branching paths cleanly, avoiding the exponential looping bounds trap by inserting dictionary duplication $O(1)$ amortized lookups!

---

## Technical Notes

- **Grammar Format Expected:** `Probability LHS RHS1 RHS2 ...` (Items separated by whitespace)
- All algorithms maintain strict $O(n^2)$ structural space scaling and $O(n^3)$ temporal scaling through optimized dictionary lookups.
- Completely adheres to Python PEP-8 linting guidelines natively to prevent any false "warning" outputs across modern code editors.
