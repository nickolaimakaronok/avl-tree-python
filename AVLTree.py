# id1: 345682645
# name1: Nickolai Makaronok
# username1: mikalaim
# id2: 213122625
# name2: Tal Samson
# username2: talsamson


"""A class represnting a node in an AVL tree"""


# ============================================================
# Complexity notes (worst-case, O(*))
# n = number of REAL nodes in the tree (self.tree_size).
# In an AVL tree, the height h satisfies: h = O(log n).
# So any walk up/down a single root --> leaf path is O(log n).
# ============================================================


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        # Worst-case time complexity: O(1)
        if (self.key is None):
            return False
        return True

    def update_height(self):
        # Worst-case time complexity: O(1)
        # Updates the height of the current node
        left_height = self.left.height if self.left and self.left.is_real_node() else -1
        right_height = self.right.height if self.right and self.right.is_real_node() else -1
        self.height = 1 + max(left_height, right_height)


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.root = None
        self.max_node_field = None
        self.tree_size = 0

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key):

        # Worst-case time complexity: O(log n)
        # (walks down at most the AVL height)

        if self.root is None:
            return (None, 1)

        curr = self.root

        path_len = 0

        while curr is not None and curr.is_real_node():
            path_len += 1

            if curr.key == key:
                return curr, path_len
            elif curr.key > key:
                curr = curr.left
            else:
                curr = curr.right

        return None, path_len + 1

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def finger_search(self, key):

        # Worst-case time complexity: O(log n)
        # (climb up from max at most O(log n), then descend O(log n))

        if self.root is None:
            return (None, 1)

        curr = self.max_node()
        path_len = 0

        while curr.parent is not None and curr.key > key:
            curr = curr.parent
            path_len += 1

        while curr is not None and curr.is_real_node():
            path_len += 1

            if curr.key == key:
                return curr, path_len
            elif curr.key > key:
                curr = curr.left
            else:
                curr = curr.right

        return None, path_len + 1

    def BF(self, nodeX):
        # Worst complexity O(1)
        # It returns the BF(Balance factor) of the given node(nodeX)

        if nodeX is None:
            return 0
        return nodeX.left.height - nodeX.right.height

    def right_rotation(self, nodeX):
        # Worst-case time complexity: O(1)

        nodeL = nodeX.left
        nodeP = nodeX.parent
        nodeLR = nodeL.right

        nodeL.right = nodeX
        nodeX.parent = nodeL

        nodeX.left = nodeLR
        nodeLR.parent = nodeX

        nodeL.parent = nodeP

        if nodeP is None:
            self.root = nodeL  # Case: X was the root
        elif nodeP.left is nodeX:
            nodeP.left = nodeL  # Case: X was a left child
        else:
            nodeP.right = nodeL  # Case: X was a right child

        nodeX.height = 1 + max(nodeX.left.height, nodeX.right.height)
        nodeL.height = 1 + max(nodeL.left.height, nodeL.right.height)

    def left_rotation(self, nodeX):
        # Worst-case time complexity: O(1)

        nodeR = nodeX.right
        nodeP = nodeX.parent
        nodeRL = nodeR.left

        nodeR.parent = nodeP
        nodeX.parent = nodeR
        nodeR.left = nodeX
        nodeRL.parent = nodeX
        nodeX.right = nodeRL

        if nodeP is None:
            self.root = nodeR  # Case: X was the root
        elif nodeP.left is nodeX:
            nodeP.left = nodeR  # Case: X was a left child
        else:
            nodeP.right = nodeR  # Case: X was a right child

        nodeX.height = 1 + max(nodeX.left.height, nodeX.right.height)
        nodeR.height = 1 + max(nodeR.left.height, nodeR.right.height)

    def rebalance(self, nodeX):

        # Worst-case time complexity: O(1)
        # (at most a constant number of rotations)

        # The first case L-L (Right Rotation) BF(nodeX) = 2,  BF(nodeX.left) >=0
        if (self.BF(nodeX) == 2 and self.BF(nodeX.left) >= 0):
            self.right_rotation(nodeX)

        # The second case R-R (Left Rotation) BF(nodeX) = -2 BF(nodex.right) <=0
        elif self.BF(nodeX) == -2 and self.BF(nodeX.right) <= 0:
            self.left_rotation(nodeX)

        # The third case L-R (Left Rotation on the left child, then Right Rotation on the node) BF(nodeX) = 2, BF(nodex.left) = -1
        elif self.BF(nodeX) == 2 and self.BF(nodeX.left) == -1:
            self.left_rotation(nodeX.left)
            self.right_rotation(nodeX)

        # The fourth case R-L (Right Rotation on the right child, then Left Rotation on the node) BF(nodeX) = -2 BF(node.right) = 1
        elif self.BF(nodeX) == -2 and self.BF(nodeX.right) == 1:
            self.right_rotation(nodeX.right)
            self.left_rotation(nodeX)

        return None

    def execute_insert(self, curr, key, val, path_len):

        # Worst-case time complexity: O(log n)
        # (rebalance-loop goes up to the root: at most AVL height)

        """
        Helper: turns the virtual node 'curr' into a real node,
        updates the max pointer, and performs rebalancing.
        """
        # Turning virtual node into real node
        curr.key = key
        curr.value = val
        curr.height = 0

        # Creating new virtual children
        curr.left = AVLNode(None, None)
        curr.right = AVLNode(None, None)
        curr.left.parent = curr
        curr.right.parent = curr

        self.tree_size += 1

        # Updating Max Node
        # Check if we need to update the max pointer
        if self.max_node_field is None or key > self.max_node_field.key:
            self.max_node_field = curr

        # Rebalancing
        parent = curr.parent
        promotes = 0

        while parent is not None:
            old_height = parent.height
            new_height = 1 + max(parent.left.height, parent.right.height)
            bf = parent.left.height - parent.right.height

            # Case 1: Stop
            if abs(bf) < 2 and old_height == new_height:
                break

            # Case 2: Promote
            elif abs(bf) < 2 and old_height != new_height:
                parent.height = new_height
                promotes += 1
                parent = parent.parent

            # Case 3: Rotate
            else:
                self.rebalance(parent)
                return curr, path_len, promotes

        return curr, path_len, promotes

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def insert(self, key, val):

        # Worst-case time complexity: O(log n)
        # (search for insertion place O(log n) + fix-up O(log n))

        # Handle empty tree case
        if self.root is None:
            self.root = AVLNode(key, val)
            self.root.height = 0
            self.root.left = AVLNode(None, None)
            self.root.right = AVLNode(None, None)
            self.root.left.parent = self.root
            self.root.right.parent = self.root
            self.max_node_field = self.root
            self.tree_size = 1
            return self.root, 1, 0

        curr = self.root
        path_len = 0
        while curr.is_real_node():
            path_len += 1
            if curr.key < key:
                curr = curr.right
            elif curr.key > key:
                curr = curr.left
            else:
                return None, -1, -1  # Key already exists

        # Helper function
        return self.execute_insert(curr, key, val, path_len + 1)

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def finger_insert(self, key, val):

        # Worst-case time complexity: O(log n)
        # (climb up from max O(log n) + descend O(log n) + fix-up O(log n))

        if self.max_node_field is None:
            return self.insert(key, val)

        curr = self.max_node_field
        path_len = 0

        # Climb Up
        while curr.parent is not None and curr.key > key:
            curr = curr.parent
            path_len += 1

        # Climb Down
        while curr.is_real_node():
            path_len += 1
            if curr.key < key:
                curr = curr.right
            else:
                curr = curr.left

        # Helper Function
        return self.execute_insert(curr, key, val, path_len + 1)

    def find_predecessor(self, node):

        # Worst-case time complexity: O(log n)
        # (either go down a subtree spine or climb up ancestors)

        if node is None or not node.is_real_node():
            return None

        # if there is a left sub tree
        if node.left.is_real_node():
            curr = node.left
            while curr.right.is_real_node():
                curr = curr.right
            return curr

        # if there is no left subtree we go up
        curr = node
        while curr.parent is not None:
            if curr is curr.parent.right:
                return curr.parent
            curr = curr.parent

        return None

    def find_successor(self, node):

        # Worst-case time complexity: O(log n)
        # (either go down a subtree spine or climb up ancestors)

        if node is None:
            return None

        curr = node

        if curr.right.is_real_node():
            if curr.right.left.is_real_node():
                curr = node.right.left
                while (curr.left.key != None):
                    curr = curr.left
                return curr
            else:
                return node.right
        else:
            while curr.parent is not None:
                if curr is curr.parent.left:
                    return curr.parent
                else:
                    curr = curr.parent

        return None

    """deletes node from the dictionary

       @type node: AVLNode
       @pre: node is a real pointer to a node in self
       """

    def delete(self, node):

        # Worst-case time complexity: O(log n)
        # (find successor/predecessor O(log n) + fix-up/rebalance up the tree O(log n))

        def fix_tree_after_deletion(curr):

            # Worst-case time complexity: O(log n)
            # (moves upward toward the root with O(1) work per level)

            while curr is not None and curr.is_real_node():

                old_height = curr.height

                curr.update_height()

                bf = self.BF(curr)

                # doing the algorithm for fixing a tree
                if abs(bf) < 2 and old_height == curr.height:
                    return
                elif abs(bf) < 2 and old_height != curr.height:
                    curr = curr.parent
                else:
                    old_parent = curr.parent
                    self.rebalance(curr)
                    curr = old_parent

        if node == self.max_node_field:
            self.max_node_field = self.find_predecessor(node)
        if node is None or not node.is_real_node():
            return

        self.tree_size -= 1
        p = node.parent

        # the first case the node is a leaf

        if not node.left.is_real_node() and not node.right.is_real_node():
            emptyNode = AVLNode(None, None)
            emptyNode.parent = p

            if p is None:
                self.root = None
            elif p.left is node:
                p.left = emptyNode
            else:
                p.right = emptyNode

            curr = p

            fix_tree_after_deletion(curr)

        # the second case only the left child exist

        elif node.left.is_real_node() and not node.right.is_real_node():
            child = node.left
            child.parent = p

            if p is None:
                self.root = child
                child.parent = None
            elif p.left is node:
                p.left = child
            else:
                p.right = child

            curr = p
            fix_tree_after_deletion(curr)
            return

        # the third case only the right child exist
        elif not node.left.is_real_node() and node.right.is_real_node():
            child = node.right
            child.parent = p

            if p is None:
                self.root = child
                child.parent = None
            elif p.left is node:
                p.left = child
            else:
                p.right = child

            curr = p
            fix_tree_after_deletion(curr)
            return

        # both children
        else:
            # successor
            successor_X = self.find_successor(node)

            successor_X_Original_Parent = successor_X.parent
            successor_X_Original_Child = successor_X.right

            # Successor is the immediate child of the node
            if successor_X == node.right:
                # Link successor to the parent of the deleted node
                successor_X.parent = node.parent
                if node.parent is None:
                    self.root = successor_X
                elif node.parent.left is node:
                    node.parent.left = successor_X
                else:
                    node.parent.right = successor_X

                # Link the left subtree of node to successor
                successor_X.left = node.left
                if successor_X.left and successor_X.left.is_real_node():
                    successor_X.left.parent = successor_X

                successor_X.height = node.height
                correction_start_node = successor_X



            # Successor is deeper in the tree
            else:
                # Cut successor out from its current location
                # Its parent takes its right child
                if successor_X_Original_Child:
                    successor_X_Original_Child.parent = successor_X_Original_Parent

                if successor_X_Original_Parent.left is successor_X:
                    successor_X_Original_Parent.left = successor_X_Original_Child
                else:
                    successor_X_Original_Parent.right = successor_X_Original_Child

                # Place successor in the spot of node

                # Link to node's parent
                successor_X.parent = node.parent
                if node.parent is None:
                    self.root = successor_X
                elif node.parent.left is node:
                    node.parent.left = successor_X
                else:
                    node.parent.right = successor_X

                # Take node's left subtree
                successor_X.left = node.left
                if successor_X.left and successor_X.left.is_real_node():
                    successor_X.left.parent = successor_X

                # Take node's right subtree
                successor_X.right = node.right
                if successor_X.right and successor_X.right.is_real_node():
                    successor_X.right.parent = successor_X

                # Rebalancing start point: the old parent of successor
                correction_start_node = successor_X_Original_Parent

            # for my bro GC
            node.parent = node.left = node.right = None

            successor_X.height = node.height

            # Rebalancing
            fix_tree_after_deletion(correction_start_node)
            return

    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """

    def is_empty(self):
        # Worst-case O(1)
        return self.root is None or (not self.root.is_real_node())

    def join(self, tree2, key, val):

        # Worst-case time complexity: O(log n)
        # where n = (size of self) + (size of tree2) + 1
        # (walk down one spine by height-difference, then fix-up to root)

        if tree2 is None or tree2.is_empty():
            self.insert(key, val)  # size += 1
            return

        if self.root is None:
            self.root = tree2.root
            self.tree_size = tree2.tree_size
            self.max_node_field = tree2.max_node_field
            self.insert(key, val)
            return

        if self.root.key < key:
            T1, T2 = self, tree2
        else:
            T1, T2 = tree2, self

        new_node = AVLNode(key, val)
        new_node.height = 0

        root1 = T1.root
        root2 = T2.root
        h1 = root1.height
        h2 = root2.height

        if abs(h1 - h2) <= 1:
            new_node.left = root1
            root1.parent = new_node
            new_node.right = root2
            root2.parent = new_node

            # Update the main tree root
            self.root = new_node
            new_node.update_height()

            # Max node is the max node of the right tree and updating size
            self.max_node_field = T2.max_node_field
            self.tree_size = T1.tree_size + T2.tree_size + 1
            return

        elif h1 > h2:
            # Go down the RIGHT spine of T1 until height <= h2 + 1
            b = root1
            while b.height > h2 + 1:
                b = b.right

            parent_b = b.parent

            # Insert x: x.left takes b, x.right takes the whole T2
            new_node.left = b
            b.parent = new_node

            new_node.right = root2
            root2.parent = new_node

            new_node.parent = parent_b

            # 2. Re-attach x to the main tree
            if parent_b is None:
                T1.root = new_node
            else:
                parent_b.right = new_node  # We went down the right spine

            # Balance upwards
            self.fix_up_join(new_node)
            self.root = T1.root

            # Right Tree (T2) is Taller (h2 > h1)
        else:  # h2 > h1
            # Go down the LEFT spine of T2 until height <= h1 + 1
            b = root2
            while b.height > h1 + 1:
                b = b.left

            parent_b = b.parent

            # Insert x: x.right takes b, x.left takes the whole T1
            new_node.right = b
            b.parent = new_node

            new_node.left = root1
            root1.parent = new_node

            new_node.parent = parent_b

            # Re-attach x to the main tree
            if parent_b is None:
                T2.root = new_node
            else:
                parent_b.left = new_node  # We went down the left spine

            # Balance upwards
            self.fix_up_join(new_node)
            self.root = T2.root

        # Final update of max_node and size
        self.max_node_field = T2.max_node_field
        self.tree_size = T1.tree_size + T2.tree_size + 1
        return

    # Helper function (MUST be defined within the AVLTree class scope)
    def fix_up_join(self, node):

        # Worst-case time complexity: O(log n)
        # (moves upward toward the root; at most AVL height)

        curr = node
        while curr is not None:
            old_height = curr.height
            curr.update_height()
            bf = abs(self.BF(curr))
            if bf < 2 and curr.height == old_height:
                return
            elif bf < 2 and curr.height != old_height:
                curr = curr.parent
            else:
                self.rebalance(curr)
                curr = curr.parent

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def recompute_max(self):

        # Worst-case time complexity: O(log n)
        # (walks down the right spine to the maximal key)

        if self.root is None or (not self.root.is_real_node()):
            self.max_node_field = None
            return
        curr = self.root
        while curr.right is not None and curr.right.is_real_node():
            curr = curr.right
        self.max_node_field = curr

    def split(self, node):

        # Worst-case time complexity: O(log n)
        # (climbs from node to root: O(log n), using AVL-join to assemble two trees)

        # Initialize the two result trees
        t1 = AVLTree()
        t1.root = node.left if (node.left is not None and node.left.is_real_node()) else None
        if t1.root is not None:
            t1.root.parent = None

        t2 = AVLTree()
        t2.root = node.right if (node.right is not None and node.right.is_real_node()) else None
        if t2.root is not None:
            t2.root.parent = None

        # Start climbing from the immediate parent
        parent = node.parent

        while parent is not None:
            grand_parent = parent.parent
            if parent.right is node:
                left_tree = AVLTree()
                left_tree.root = parent.left

                if left_tree.root is not None:
                    left_tree.root.parent = None

                t1.join(left_tree, parent.key, parent.value)
            elif parent.left is node:
                right_tree = AVLTree()
                right_tree.root = parent.right

                if right_tree.root is not None:
                    right_tree.root.parent = None

                t2.join(right_tree, parent.key, parent.value)

            node = parent
            parent = grand_parent

        t1.recompute_max()
        t2.recompute_max()

        return (t1, t2)

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def in_order_to_array(self, arr, node):

        # Worst-case time complexity: O(n)
        # (visits each real node exactly once; recursion depth is O(log n))

        if node is not None and node.is_real_node():
            self.in_order_to_array(arr, node.left)
            arr.append((node.key, node.value))
            self.in_order_to_array(arr, node.right)

    def avl_to_array(self):
        # Worst-case time complexity: O(n)
        # (in-order traversal over all nodes)
        arr = []
        self.in_order_to_array(arr, self.root)
        return arr

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self):
        # Worst-case time complexity: O(1)
        return self.max_node_field

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        # Worst-case time complexity: O(1)
        return self.tree_size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        # Worst-case time complexity: O(1)
        return self.root
