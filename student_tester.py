'''
    In order to run the tester:
    1.  Make sure your AVLTree.py file and this file
        are both in the same directory.
    2.  Run: python3 student_tester.py
    3.  Your grade will be printed at the end.
        Only failed tests will be printed.
'''

import unittest
from AVLTree import AVLTree

GRADE = 0
MAX_GRADE = 10
TEST_COUNT = 4
POINTS_PER_TEST = MAX_GRADE / TEST_COUNT


class BasicStudentTester(unittest.TestCase):

    def setUp(self):
        self.T = AVLTree()

    def add_points(self):
        global GRADE
        GRADE += POINTS_PER_TEST

    def test_insert_small(self):
        self.T.insert(10, "10")
        self.T.insert(5, "5")
        self.T.insert(15, "15")

        self.assertEqual(self.T.size(), 3)
        self.assertIsNotNone(self.T.search(10)[0])
        self.assertIsNotNone(self.T.search(5)[0])
        self.assertIsNotNone(self.T.search(15)[0])

        self.add_points()

    def test_delete_small(self):
        for i in range(5):
            self.T.insert(i, str(i))

        self.assertEqual(self.T.size(), 5)

        self.T.delete(self.T.search(0)[0])
        self.T.delete(self.T.search(3)[0])

        self.assertEqual(self.T.size(), 3)

        self.add_points()

    def test_insert_delete_mix(self):
        nums = [7, 3, 9, 1, 5]
        for x in nums:
            self.T.insert(x, str(x))

        self.assertEqual(self.T.size(), 5)

        self.T.delete(self.T.search(5)[0])
        self.assertEqual(self.T.size(), 4)

        self.T.insert(20, "20")
        self.assertEqual(self.T.size(), 5)

        self.add_points()

    # ------------------------------------
    # NEW TEST: max_node() correctness
    # ------------------------------------
    def test_max_node(self):
        # Empty dictionary
        self.assertIsNone(self.T.max_node())

        # Insert values
        vals = [10, 4, 22, 8, 30, 1, 15]
        for x in vals:
            self.T.insert(x, str(x))

        # Max should be 30
        self.assertIsNotNone(self.T.max_node())
        self.assertEqual(self.T.max_node().key, 30)

        # Delete the max node
        self.T.delete(self.T.search(30)[0])

        # Max should now be 22
        self.assertEqual(self.T.max_node().key, 22)

        self.add_points()


# ------------------------
#   Custom Test Runner
# ------------------------

if __name__ == "__main__":
    print("Running Student Tester...\n")

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BasicStudentTester)
    result = unittest.TextTestRunner(verbosity=0).run(suite)

    print("\n==============================")
    print("       TESTER SUMMARY")
    print("==============================")

    if result.failures or result.errors:
        print("\n❌ Failed Tests:")
        for test, err in result.failures + result.errors:
            test_name = test.id().split(".")[-1]
            print(f"  - {test_name}")
            print(f"    {err.splitlines()[-1]}")
    else:
        print("\n✅ All tests passed!")

    print("\nGrade:", GRADE, "/", MAX_GRADE)
    print("==============================")

