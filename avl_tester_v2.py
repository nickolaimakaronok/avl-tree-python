"""Mega AVL Tester for TAU Data Structures Project 1 (AVL Tree).

How to use (recommended):
  1) Put this file next to your implementation file (usually: AVLTree.py)
  2) Run:
        python mega_avl_tester.py

If your implementation file has a different name/path:
        python mega_avl_tester.py --path /path/to/your_file.py

This tester checks:
  - Required API exists
  - BST + AVL invariants (balance factors, heights)
  - Parent pointers
  - Virtual children (leaves have 2 virtual nodes)
  - Correctness of search / finger_search return values (including path length e)
  - Correctness of insert / finger_insert return values (node, e, promote count h)
  - delete correctness
  - join correctness
  - split correctness
  - Random stress tests

NOTE: This is for *your* debugging only. Do not submit this tester.
"""

from __future__ import annotations

import argparse
import os
import importlib
import importlib.util
import math
import random
import sys
import traceback
import types
import unittest
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple


# -------------------------
# Module loading utilities
# -------------------------

def load_module(module_name: str | None, path: str | None) -> types.ModuleType:
    """Load student's module either by module name or by file path."""
    if path:
        spec = importlib.util.spec_from_file_location("student_avl", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module from path: {path}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]
        return mod

    name = module_name or "AVLTree"
    return importlib.import_module(name)


# -------------------------
# Helper: safe node checks
# -------------------------

def is_real(node: Any) -> bool:
    if node is None:
        return False
    fn = getattr(node, "is_real_node", None)
    if callable(fn):
        try:
            return bool(fn())
        except Exception:
            return False
    # Fallback: treat nodes with key None as virtual (common convention)
    return getattr(node, "key", None) is not None


def height(node: Any) -> int:
    if node is None or not is_real(node):
        return -1
    return int(getattr(node, "height"))


# -------------------------
# Invariant checks
# -------------------------

def inorder_collect(node: Any, out: List[Tuple[int, Any]]) -> None:
    if node is None or not is_real(node):
        return
    inorder_collect(getattr(node, "left", None), out)
    out.append((int(node.key), getattr(node, "value", None)))
    inorder_collect(getattr(node, "right", None), out)


def compute_true_height(node: Any) -> int:
    if node is None or not is_real(node):
        return -1
    hl = compute_true_height(node.left)
    hr = compute_true_height(node.right)
    return 1 + max(hl, hr)


def assert_avl_invariants(
    tree: Any,
    *,
    expected_items: Optional[Dict[int, Any]] = None,
    check_size: bool = True,
    check_max: bool = True,
    require_virtual_children: bool = True,
) -> None:
    """Raise AssertionError if tree violates expected AVL properties."""
    if not hasattr(tree, "get_root"):
        raise AssertionError("Tree missing get_root()")

    root = tree.get_root()
    if root is None or not is_real(root):
        # Empty tree
        if expected_items is not None:
            assert len(expected_items) == 0, f"Expected empty, got items={expected_items}"
        if check_size and hasattr(tree, "size"):
            assert tree.size() == 0, f"size() should be 0 for empty tree, got {tree.size()}"
        if check_max and hasattr(tree, "max_node"):
            assert tree.max_node() is None, "max_node() should be None for empty tree"
        return

    # DFS to validate structure
    visited: set[int] = set()

    def dfs(node: Any, lo: int, hi: int, parent: Any) -> int:
        if node is None:
            if require_virtual_children:
                raise AssertionError("Found None child where virtual node is required")
            return -1

        if not is_real(node):
            # virtual
            if require_virtual_children:
                # virtual nodes should have parent pointer set (common in the skeleton)
                p = getattr(node, "parent", None)
                assert p is parent, "Virtual node parent pointer is incorrect"
            # allow any negative height for virtual
            h = getattr(node, "height", -1)
            assert int(h) <= -1, f"Virtual node height should be <= -1, got {h}"
            return -1

        nid = id(node)
        if nid in visited:
            raise AssertionError("Cycle detected in pointers")
        visited.add(nid)

        k = int(node.key)
        assert lo < k < hi, f"BST order violation at key={k}, expected {lo} < key < {hi}"

        # Parent pointer
        assert getattr(node, "parent", None) is parent, f"Bad parent pointer at key={k}"

        # Children existence
        if require_virtual_children:
            assert getattr(node, "left", None) is not None, f"Missing left child at key={k}"
            assert getattr(node, "right", None) is not None, f"Missing right child at key={k}"

        hl = dfs(node.left, lo, k, node)
        hr = dfs(node.right, k, hi, node)

        # Height correctness
        expected_h = 1 + max(hl, hr)
        node_h = int(getattr(node, "height"))
        assert node_h == expected_h, f"Height wrong at key={k}: stored={node_h}, expected={expected_h}"

        # Balance factor
        bf = hl - hr
        assert abs(bf) <= 1, f"AVL balance violated at key={k}: BF={bf} (hl={hl}, hr={hr})"

        return expected_h

    dfs(root, -10**18, 10**18, None)

    # In-order must be sorted and match expected_items
    arr: List[Tuple[int, Any]] = []
    inorder_collect(root, arr)
    keys = [k for k, _ in arr]
    assert keys == sorted(keys), "In-order traversal is not sorted (BST property broken)"
    assert len(keys) == len(set(keys)), "Duplicate keys found in tree"

    if expected_items is not None:
        exp = sorted(expected_items.items(), key=lambda kv: kv[0])
        assert [(k, v) for k, v in arr] == exp, (
            "Tree contents mismatch.\n"
            f"Expected: {exp[:30]}{'...' if len(exp) > 30 else ''}\n"
            f"Got:      {arr[:30]}{'...' if len(arr) > 30 else ''}"
        )

    # size()
    if check_size and hasattr(tree, "size"):
        s = int(tree.size())
        assert s == len(arr), f"size() mismatch: got {s}, expected {len(arr)}"

    # avl_to_array()
    if hasattr(tree, "avl_to_array"):
        a2 = tree.avl_to_array()
        assert a2 == arr, "avl_to_array() mismatch with in-order traversal"

    # max_node()
    if check_max and hasattr(tree, "max_node"):
        mx = tree.max_node()
        assert mx is not None and is_real(mx), "max_node() returned None/virtual for non-empty tree"
        assert int(mx.key) == keys[-1], f"max_node() wrong: got {mx.key}, expected {keys[-1]}"


# -------------------------
# Expected path length (e)
# -------------------------

def expected_search_e_from(start: Any, key: int) -> int:
    """Expected e for search starting at a given node: edges traversed + 1."""
    if start is None or not is_real(start):
        return 1
    curr = start
    edges = 0
    while curr is not None and is_real(curr):
        if int(curr.key) == key:
            return edges + 1
        if key < int(curr.key):
            curr = curr.left
        else:
            curr = curr.right
        edges += 1
    return edges + 1


def expected_finger_search_e(tree: Any, key: int) -> int:
    """Expected e for finger_search as described in the assignment."""
    root = tree.get_root()
    if root is None or not is_real(root):
        return 1

    mx = tree.max_node()
    assert mx is not None and is_real(mx), "finger_search: tree.max_node() returned None/virtual"

    curr = mx
    edges = 0
    # climb up until first node with key <= target (or root)
    while getattr(curr, "parent", None) is not None and int(curr.key) > key:
        curr = curr.parent
        edges += 1

    # descend like normal search from curr
    while curr is not None and is_real(curr):
        if int(curr.key) == key:
            return edges + 1
        if key < int(curr.key):
            curr = curr.left
        else:
            curr = curr.right
        edges += 1

    return edges + 1


# -------------------------
# Shadow AVL insertion to compute expected promote count (h)
# -------------------------

@dataclass
class SNode:
    key: int
    height: int
    left: Optional["SNode"] = None
    right: Optional["SNode"] = None
    parent: Optional["SNode"] = None


def sn_h(n: Optional[SNode]) -> int:
    return -1 if n is None else n.height


def sn_update(n: SNode) -> None:
    n.height = 1 + max(sn_h(n.left), sn_h(n.right))


def sn_rotate_left(z: SNode) -> SNode:
    y = z.right
    assert y is not None
    T2 = y.left

    # rotation
    y.left = z
    z.right = T2

    # parents
    y.parent = z.parent
    z.parent = y
    if T2 is not None:
        T2.parent = z

    # fix parent's child pointer
    if y.parent is not None:
        if y.parent.left is z:
            y.parent.left = y
        elif y.parent.right is z:
            y.parent.right = y

    # heights (z first)
    sn_update(z)
    sn_update(y)
    return y


def sn_rotate_right(z: SNode) -> SNode:
    y = z.left
    assert y is not None
    T3 = y.right

    # rotation
    y.right = z
    z.left = T3

    # parents
    y.parent = z.parent
    z.parent = y
    if T3 is not None:
        T3.parent = z

    # fix parent's child pointer
    if y.parent is not None:
        if y.parent.left is z:
            y.parent.left = y
        elif y.parent.right is z:
            y.parent.right = y

    # heights
    sn_update(z)
    sn_update(y)
    return y


def sn_rebalance_at(z: SNode) -> SNode:
    bf = sn_h(z.left) - sn_h(z.right)
    if bf == 2:
        assert z.left is not None
        bf_l = sn_h(z.left.left) - sn_h(z.left.right)
        if bf_l >= 0:
            return sn_rotate_right(z)
        else:
            # LR
            z.left = sn_rotate_left(z.left)
            z.left.parent = z
            return sn_rotate_right(z)
    elif bf == -2:
        assert z.right is not None
        bf_r = sn_h(z.right.left) - sn_h(z.right.right)
        if bf_r <= 0:
            return sn_rotate_left(z)
        else:
            # RL
            z.right = sn_rotate_right(z.right)
            z.right.parent = z
            return sn_rotate_left(z)
    return z


def shadow_copy_from_student(node: Any, parent: Optional[SNode] = None) -> Optional[SNode]:
    if node is None or not is_real(node):
        return None
    sn = SNode(key=int(node.key), height=int(getattr(node, "height")), parent=parent)
    sn.left = shadow_copy_from_student(getattr(node, "left", None), sn)
    sn.right = shadow_copy_from_student(getattr(node, "right", None), sn)
    return sn


def shadow_insert_promotes(root: Optional[SNode], key: int) -> int:
    """Compute promote count for inserting key into a correct AVL tree (shadow copy)."""
    if root is None:
        return 0

    # BST insert
    curr = root
    parent: Optional[SNode] = None
    while curr is not None:
        parent = curr
        if key < curr.key:
            curr = curr.left
        else:
            curr = curr.right

    new_node = SNode(key=key, height=0, parent=parent)
    assert parent is not None
    if key < parent.key:
        parent.left = new_node
    else:
        parent.right = new_node

    promotes = 0
    z = parent
    while z is not None:
        old_h = z.height
        new_h = 1 + max(sn_h(z.left), sn_h(z.right))
        bf = sn_h(z.left) - sn_h(z.right)

        if abs(bf) < 2 and new_h == old_h:
            break
        if abs(bf) < 2 and new_h != old_h:
            z.height = new_h
            promotes += 1
            z = z.parent
            continue

        # rotation case
        new_sub_root = sn_rebalance_at(z)
        # after rotation, walk up to find true root for completeness
        while new_sub_root.parent is not None:
            new_sub_root = new_sub_root.parent
        break

    return promotes


# -------------------------
# Unittest suite
# -------------------------

class MegaAVLTests(unittest.TestCase):
    """The actual test cases. The module is injected via class variables."""

    MOD: types.ModuleType
    AVLTree: Any
    AVLNode: Any
    RAND_SEED: int = 12345
    STRESS_STEPS: int = 400

    @classmethod
    def setUpClass(cls) -> None:
        # If you run this file via a unittest runner (e.g., PyCharm's "Run tests"),
        # the `main()` function below is NOT executed, so `MOD` may not be injected.
        # In that case, we fall back to loading the implementation automatically.
        if not hasattr(cls, "MOD") or cls.MOD is None:  # type: ignore[attr-defined]
            module_name = os.environ.get("MEGA_AVL_MODULE", "AVLTree")
            path = os.environ.get("MEGA_AVL_PATH") or None
            try:
                cls.MOD = load_module(module_name, path)  # type: ignore[assignment]
            except Exception as e:
                raise AssertionError(
                    "Could not load your AVL implementation module.\n"
                    "Try running as a script:\n"
                    "  python mega_avl_tester.py\n"
                    "Or set env vars for your IDE test runner:\n"
                    "  MEGA_AVL_MODULE=<your module name>  (default: AVLTree)\n"
                    "  MEGA_AVL_PATH=<full path to your .py> (optional)\n"
                    f"Original error: {e}"
                ) from e

        # Required API
        for name in [
            "AVLTree",
            "AVLNode",
        ]:
            if not hasattr(cls.MOD, name):  # type: ignore[attr-defined]
                raise AssertionError(f"Module missing {name}")
        cls.AVLTree = getattr(cls.MOD, "AVLTree")  # type: ignore[attr-defined]
        cls.AVLNode = getattr(cls.MOD, "AVLNode")  # type: ignore[attr-defined]

        required_methods = [
            "search",
            "finger_search",
            "insert",
            "finger_insert",
            "delete",
            "join",
            "split",
            "avl_to_array",
            "max_node",
            "size",
            "get_root",
        ]
        missing = [m for m in required_methods if not hasattr(cls.AVLTree, m)]
        if missing:
            raise AssertionError(f"AVLTree missing required methods: {missing}")

    def mk(self) -> Any:
        return self.AVLTree()

    def test_empty_tree_api(self):
        t = self.mk()
        self.assertEqual(t.size(), 0)
        self.assertIsNone(t.get_root())
        self.assertIsNone(t.max_node())
        self.assertEqual(t.avl_to_array(), [])
        x, e = t.search(10)
        self.assertIsNone(x)
        self.assertEqual(e, 1)
        x, e = t.finger_search(10)
        self.assertIsNone(x)
        self.assertEqual(e, 1)

    def test_insert_search_basic_and_invariants(self):
        t = self.mk()
        model: Dict[int, str] = {}

        # Example from assignment: insert 3, 1, 2 promotes: 0,1,1
        for k, expected_promotes in [(3, 0), (1, 1), (2, 1)]:
            e_expected = expected_search_e_from(t.get_root(), k)
            root_shadow = shadow_copy_from_student(t.get_root())
            h_expected = shadow_insert_promotes(root_shadow, k)

            node, e, h = t.insert(k, str(k))
            model[k] = str(k)

            self.assertTrue(node is not None and is_real(node) and int(node.key) == k)
            self.assertEqual(e, e_expected)
            self.assertEqual(h, h_expected)
            self.assertEqual(h, expected_promotes)

            assert_avl_invariants(t, expected_items=model)

        # search existing
        node, e = t.search(2)
        self.assertTrue(node is not None and int(node.key) == 2)
        self.assertEqual(e, expected_search_e_from(t.get_root(), 2))

        # search missing
        node, e = t.search(999)
        self.assertIsNone(node)
        self.assertEqual(e, expected_search_e_from(t.get_root(), 999))

        # finger_search existing
        node, e = t.finger_search(2)
        self.assertTrue(node is not None and int(node.key) == 2)
        self.assertEqual(e, expected_finger_search_e(t, 2))

        # finger_search missing
        node, e = t.finger_search(-10)
        self.assertIsNone(node)
        self.assertEqual(e, expected_finger_search_e(t, -10))

    def test_finger_insert_path_and_promotes(self):
        t = self.mk()
        model: Dict[int, str] = {}

        # Build a tree
        for k in [10, 20, 30, 40, 50, 25]:
            node, _, _ = t.insert(k, f"v{k}")
            model[k] = f"v{k}"
            self.assertTrue(node is not None)
        assert_avl_invariants(t, expected_items=model)

        # Now finger_insert values near max should have short finger path
        k = 55
        e_expected = expected_finger_search_e(t, k)
        root_shadow = shadow_copy_from_student(t.get_root())
        h_expected = shadow_insert_promotes(root_shadow, k)

        node, e, h = t.finger_insert(k, f"v{k}")
        model[k] = f"v{k}"

        self.assertTrue(node is not None and is_real(node) and int(node.key) == k)
        self.assertEqual(e, e_expected)
        self.assertEqual(h, h_expected)
        assert_avl_invariants(t, expected_items=model)

    def test_delete_cases(self):
        t = self.mk()
        keys = [50, 30, 70, 20, 40, 60, 80, 35]
        model = {k: f"v{k}" for k in keys}
        for k in keys:
            t.insert(k, f"v{k}")
        assert_avl_invariants(t, expected_items=model)

        # delete leaf
        node, _ = t.search(20)
        self.assertIsNotNone(node)
        t.delete(node)
        model.pop(20)
        assert_avl_invariants(t, expected_items=model)

        # delete node with one child (35 is leaf now? depends; force)
        node, _ = t.search(40)
        self.assertIsNotNone(node)
        t.delete(node)
        model.pop(40)
        assert_avl_invariants(t, expected_items=model)

        # delete node with two children
        node, _ = t.search(30)
        self.assertIsNotNone(node)
        t.delete(node)
        model.pop(30)
        assert_avl_invariants(t, expected_items=model)

        # delete root
        root = t.get_root()
        self.assertTrue(root is not None and is_real(root))
        t.delete(root)
        model.pop(int(root.key))
        assert_avl_invariants(t, expected_items=model)

    def test_join_basic(self):
        # self keys < k < tree2 keys
        t1 = self.mk()
        t2 = self.mk()
        model: Dict[int, str] = {}

        for k in [10, 20, 30, 40]:
            t1.insert(k, f"a{k}")
            model[k] = f"a{k}"
        for k in [60, 70, 80]:
            t2.insert(k, f"b{k}")
            model[k] = f"b{k}"

        t1.join(t2, 50, "mid")
        model[50] = "mid"

        assert_avl_invariants(t1, expected_items=model)

        # opposite direction: tree2 keys < k < self keys
        t3 = self.mk()
        t4 = self.mk()
        model2: Dict[int, str] = {}

        for k in [100, 110, 120]:
            t3.insert(k, f"c{k}")
            model2[k] = f"c{k}"
        for k in [10, 20, 30, 40]:
            t4.insert(k, f"d{k}")
            model2[k] = f"d{k}"

        t3.join(t4, 50, "mid")
        model2[50] = "mid"

        assert_avl_invariants(t3, expected_items=model2)

    def test_split_basic(self):
        t = self.mk()
        keys = [10, 20, 30, 40, 50, 60, 70]
        model = {k: f"v{k}" for k in keys}
        for k in keys:
            t.insert(k, f"v{k}")
        assert_avl_invariants(t, expected_items=model)

        # split at 40
        node, _ = t.search(40)
        self.assertIsNotNone(node)
        left, right = t.split(node)

        left_expected = {k: v for k, v in model.items() if k < 40}
        right_expected = {k: v for k, v in model.items() if k > 40}

        # Size after split is allowed to be wrong by assignment; don't check size.
        assert_avl_invariants(left, expected_items=left_expected, check_size=False)
        assert_avl_invariants(right, expected_items=right_expected, check_size=False)

    def test_random_stress(self):
        rnd = random.Random(self.RAND_SEED)
        t = self.mk()
        model: Dict[int, str] = {}

        def do_insert(use_finger: bool):
            # choose new key
            while True:
                k = rnd.randint(-2000, 2000)
                if k not in model:
                    break
            v = f"v{k}"

            if use_finger:
                e_expected = expected_finger_search_e(t, k)
            else:
                e_expected = expected_search_e_from(t.get_root(), k)

            root_shadow = shadow_copy_from_student(t.get_root())
            h_expected = shadow_insert_promotes(root_shadow, k)

            if use_finger:
                node, e, h = t.finger_insert(k, v)
            else:
                node, e, h = t.insert(k, v)

            self.assertTrue(node is not None and is_real(node) and int(node.key) == k)
            self.assertEqual(e, e_expected)
            self.assertEqual(h, h_expected)
            model[k] = v

        def do_delete():
            k = rnd.choice(list(model.keys()))
            node, _ = t.search(k)
            self.assertTrue(node is not None and is_real(node) and int(node.key) == k)
            t.delete(node)
            model.pop(k)

        for step in range(self.STRESS_STEPS):
            if len(model) == 0 or (len(model) < 300 and rnd.random() < 0.65):
                do_insert(use_finger=(rnd.random() < 0.5))
            else:
                do_delete()

            # Validate invariants frequently
            assert_avl_invariants(t, expected_items=model)

            # Spot-check searches
            if rnd.random() < 0.2:
                q = rnd.randint(-2000, 2000)
                node, e = t.search(q)
                e_exp = expected_search_e_from(t.get_root(), q)
                self.assertEqual(e, e_exp)
                if q in model:
                    self.assertTrue(node is not None and int(node.key) == q)
                else:
                    self.assertIsNone(node)

            if rnd.random() < 0.2:
                q = rnd.randint(-2000, 2000)
                node, e = t.finger_search(q)
                e_exp = expected_finger_search_e(t, q)
                self.assertEqual(e, e_exp)
                if q in model:
                    self.assertTrue(node is not None and int(node.key) == q)
                else:
                    self.assertIsNone(node)


# -------------------------
# CLI
# -------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Mega AVL tester")
    p.add_argument("--module", default="AVLTree", help="Module name to import (default: AVLTree)")
    p.add_argument("--path", default=None, help="Path to the implementation .py file")
    p.add_argument("--seed", type=int, default=12345, help="Random seed for stress test")
    p.add_argument("--stress", type=int, default=400, help="Number of random operations")
    p.add_argument(
        "--no-virtual-check",
        action="store_true",
        help="Disable strict checking that every real node has non-None virtual children",
    )

    args, extra = p.parse_known_args()

    try:
        mod = load_module(args.module, args.path)
    except Exception as e:
        print("\nFAILED to load your AVL module.")
        print("Tried module:", args.module)
        if args.path:
            print("Tried path:", args.path)
        print("Error:", e)
        traceback.print_exc()
        return 2

    # Inject module + parameters into test class
    MegaAVLTests.MOD = mod
    MegaAVLTests.RAND_SEED = args.seed
    MegaAVLTests.STRESS_STEPS = args.stress

    # Control strictness (virtual children requirement)
    if args.no_virtual_check:
        global assert_avl_invariants
        _orig = assert_avl_invariants

        def assert_avl_invariants_relaxed(*a: Any, **kw: Any) -> None:
            kw.setdefault("require_virtual_children", False)
            return _orig(*a, **kw)

        assert_avl_invariants = assert_avl_invariants_relaxed  # type: ignore[assignment]

    # Run unittest
    unittest_args = [sys.argv[0]] + extra
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MegaAVLTests)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
