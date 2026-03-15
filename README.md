# AVL Tree — Python Implementation

A fully functional AVL Tree (self-balancing BST) implemented from scratch in Python, including advanced operations, ASCII visualizer, and empirical performance benchmarks.

## Features

- **Core AVL operations** — insert, delete, search with automatic rebalancing
- **Finger Search** — O(log k) search starting from the max node, where k is the rank distance
- **Join** — merges two AVL trees in O(log n)
- **Split** — splits a tree at a given node in O(log n)
- **ASCII Tree Visualizer** — prints the tree structure in the terminal
- **Performance Benchmarks** — empirical analysis of search and balancing costs across input types

---

## Project Structure

```
avl-tree-python/
├── AVLTree.py          # Core implementation (AVLNode + AVLTree classes)
├── visualizer.py       # ASCII tree printer for debugging and demos
├── benchmark.py        # Empirical experiments: sorted / random / reversed / swapped inputs
├── student_tester.py   # Basic unit tests: insert, delete, search, max_node
├── avl_tester_v2.py    # Extended stress tester with edge cases
└── README.md
```

---

## How to Run

**Requirements:** Python 3.x — no external libraries needed.

### Run unit tests
```bash
python student_tester.py
```
```
Running Student Tester...
✅ All tests passed!
Grade: 10 / 10
```

### Visualize the tree
```bash
python visualizer.py
```
```
             (9,h=3)
            /        \
      (3,h=2)          (22,h=2)
      /      \          /      \
  (1,h=0)  (7,h=1)  (18,h=1)  (30,h=0)
            /    \    /
        (6,h=0)(#)(14,h=0)
```

### Run performance benchmarks
```bash
python benchmark.py
```

---

## API Reference

```python
tree = AVLTree()

tree.insert(key, value)       # Insert key-value pair
tree.delete(node)             # Delete a node
tree.search(key)              # → (node, edges) — search from root
tree.finger_search(key)       # → (node, edges) — search from max node, O(log k)
tree.max_node()               # → AVLNode with the largest key, O(1)
tree.size()                   # → int, number of nodes, O(1)
tree.avl_to_array()           # → sorted list of (key, value) tuples
tree.join(tree2, key, val)    # Merge two trees with a separating key, O(log n)
tree.split(node)              # → (left_tree, right_tree), O(log n)
```

---

## Time Complexity

| Operation       | Complexity   | Notes                                      |
|-----------------|--------------|--------------------------------------------|
| `search`        | O(log n)     | Standard BST descent from root             |
| `finger_search` | O(log k)     | k = rank distance from max node to target  |
| `insert`        | O(log n)     | BST insert + rebalance up to root          |
| `delete`        | O(log n)     | BST delete + rebalance up to root          |
| `max_node`      | O(1)         | Maintained as a pointer field              |
| `size`          | O(1)         | Maintained as a counter field              |
| `join`          | O(log n)     | Walk one spine by height difference        |
| `split`         | O(log n)     | Climb from node to root using join         |
| `avl_to_array`  | O(n)         | In-order traversal                         |

---

## Benchmark Results

`benchmark.py` measures **total search cost** (edges traversed) and **total balancing cost** (promotions/rotations) for inserting n = 300 × 2^i elements across four input types:

| Input type   | Description                                      |
|--------------|--------------------------------------------------|
| Sorted       | 1, 2, 3, ..., n                                  |
| Reverse      | n, n-1, ..., 1                                   |
| Random       | uniformly shuffled (averaged over 20 runs)        |
| Adj. Swaps   | sorted with random adjacent swaps, p=0.5          |

**Key finding:** Finger insert on nearly-sorted inputs (Adj. Swaps) achieves significantly lower search cost than on random inputs, consistent with the O(log k) theoretical bound.

---

## Rebalancing Cases

The tree handles all four AVL violation cases after every insert and delete:

| Case | Condition                        | Fix                          |
|------|----------------------------------|------------------------------|
| L-L  | BF(x) = +2, BF(x.left) ≥ 0      | Right rotation               |
| R-R  | BF(x) = -2, BF(x.right) ≤ 0     | Left rotation                |
| L-R  | BF(x) = +2, BF(x.left) = -1     | Left on child, right on x    |
| R-L  | BF(x) = -2, BF(x.right) = +1    | Right on child, left on x    |

---

## Tech Stack

- **Language:** Python 3
- **Testing:** `unittest` (standard library)
- **No external dependencies**
