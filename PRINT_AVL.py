from AVLTree import AVLTree


def avl_to_str(avl_or_root, show_values=False, show_height=True):
    """
    Return an ASCII drawing of the AVL tree.

    Assumes your implementation:
    - AVLTree has .root
    - AVLNode has .key, .value, .left, .right
    - Virtual nodes: is_real_node() == False (or key is None)
    - Height stored on node as .height (common). If not found, tries .h.
    """

    # Accept either an AVLTree or an AVLNode
    root = avl_or_root.root if hasattr(avl_or_root, "root") else avl_or_root

    def is_real(node):
        if node is None:
            return False
        if hasattr(node, "is_real_node"):
            return node.is_real_node()
        return getattr(node, "key", None) is not None

    def get_height(node):
        # Prefer stored AVL height fields
        if hasattr(node, "height"):
            return node.height
        if hasattr(node, "h"):
            return node.h

        # Fallback: compute height (only if your nodes truly don't store it)
        def rec(n):
            if n is None or not is_real(n):
                return -1
            return 1 + max(rec(getattr(n, "left", None)), rec(getattr(n, "right", None)))

        return rec(node)

    def node_label(node):
        parts = []
        # key / key:value
        if show_values:
            parts.append(f"{node.key}:{node.value}")
        else:
            parts.append(str(node.key))
        # add height
        if show_height:
            parts.append(f"h={get_height(node)}")
        return "(" + ",".join(parts) + ")"

    def left_child(node):
        c = getattr(node, "left", None)
        return c if is_real(c) else None

    def right_child(node):
        c = getattr(node, "right", None)
        return c if is_real(c) else None

    def build(node):
        if node is None or not is_real(node):
            return ["#"]

        label = node_label(node)
        left = build(left_child(node))
        right = build(right_child(node))

        lwid = len(left[-1])
        rwid = len(right[-1])
        rootwid = len(label)

        result = [(lwid + 1) * " " + label + (rwid + 1) * " "]

        ls = len(left[0].rstrip())
        rs = len(right[0]) - len(right[0].lstrip())
        result.append(
            ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " "
        )

        for i in range(max(len(left), len(right))):
            row = ""
            row += left[i] if i < len(left) else lwid * " "
            row += (rootwid + 2) * " "
            row += right[i] if i < len(right) else rwid * " "
            result.append(row)

        return result

    return "\n".join(build(root))


def print_avl(avl_or_root, show_values=False, show_height=True):
    print(avl_to_str(avl_or_root, show_values=show_values, show_height=show_height))


def main():
    t = AVLTree()
    t.insert(3, "e")
    t.insert(22, "f")
    t.insert(7, "g")
    t.insert(18, "h")
    t.insert(1, "i")
    t.insert(30, "j")
    t.insert(14, "k")
    t.insert(9, "l")
    t.insert(25, "m")
    t.insert(6, "n")

    print_avl(t)  # prints keys
    print_avl(t, show_values=True)

    # prints key:value

    print(t.tree_size)


if __name__ == "__main__":
    main()
