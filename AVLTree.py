# id1: 345682645
# name1: Nickolai Makaronok
# username1: mikalaim
# id2: 213122625
# name2: Tal Samson
# username2: talsamson

"""A class represnting a node in an AVL tree"""


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
        if (self.key is None):
            return False
        return True


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

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key):
        if self.root is None:
            return (None, 0)

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

        return None, path_len

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def finger_search(self, key):

        if self.root is None:
            return (None, 0)

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

        return None, path_len

    def BF(self, nodeX):
        if nodeX is None:
            return 0
        return nodeX.left.height - nodeX.right.height


    def right_rotation(self, nodeX):
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

        if self.root is None:
            self.root = AVLNode(key, val)
            self.root.height = 0

            self.root.left = AVLNode(None, None)
            self.root.right = AVLNode(None, None)
            self.root.left.parent = self.root
            self.root.right.parent = self.root

            self.max_node_field = self.root

            return self.root, 0, 0

        curr = self.root
        path_len = 0

        while (curr.is_real_node()):
            path_len += 1
            if curr.key < key:
                curr = curr.right
            elif curr.key > key:
                curr = curr.left

        curr.key = key
        curr.value = val
        curr.height = 0

        new_node_left = AVLNode(None, None)
        new_node_right = AVLNode(None, None)

        curr.left = new_node_left
        curr.right = new_node_right

        new_node_right.parent = curr
        new_node_left.parent = curr

        if self.max_node_field is None or key > self.max_node_field.key:
            self.max_node_field = curr

        # "balancing"

        parent = curr.parent
        promotes = 0

        while (parent is not None):

            old_height = parent.height
            new_height = 1 + max(parent.left.height, parent.right.height)

            bf = parent.left.height - parent.right.height

            if abs(bf) < 2 and old_height == new_height:
                break
            elif abs(bf) < 2 and old_height != new_height:
                parent.height = new_height
                promotes += 1
                parent = parent.parent
            else:
                self.rebalance(parent)
                return curr, path_len, promotes

        return curr, path_len, promotes

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
        return None, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
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

    def join(self, tree2, key, val):
        return

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, node):
        return None, None

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        return None

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self):
        return self.max_node_field

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return -1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return None
