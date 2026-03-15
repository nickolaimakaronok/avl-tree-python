import random
import sys
import time

# Increase recursion depth just in case (though AVL is balanced, useful for utility functions)
sys.setrecursionlimit(20000)

from AVLTree import AVLTree


# ==========================================
# Helper: Count Inversions (Merge Sort)
# ==========================================
def count_inversions(arr):
    """
    Counts inversions in O(n log n).
    """
    if len(arr) < 2:
        return 0, arr

    mid = len(arr) // 2
    left_inv, left_sorted = count_inversions(arr[:mid])
    right_inv, right_sorted = count_inversions(arr[mid:])

    merge_inv, merged = merge_and_count(left_sorted, right_sorted)

    return left_inv + right_inv + merge_inv, merged


def merge_and_count(left, right):
    i, j = 0, 0
    count = 0
    merged = []

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            count += (len(left) - i)
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return count, merged


# ==========================================
# Experiment Logic
# ==========================================

def run_experiment_on_array(arr):
    """
    Inserts all elements from arr into an AVLTree using finger_insert.
    Returns: (search_cost, balance_cost)
    """
    tree = AVLTree()
    total_search_cost = 0
    total_balance_cost = 0

    for key in arr:
        # finger_insert returns (node, search_edges, promote_count)
        # We store the result in dummy variables to avoid clutter
        _, edges, promotes = tree.finger_insert(key, str(key))

        if edges != -1:
            total_search_cost += edges
            total_balance_cost += promotes

    return total_search_cost, total_balance_cost


def generate_random_swapped(n):
    """
    Generates an array 1..n and performs adjacent swaps with p=0.5
    """
    arr = list(range(1, n + 1))
    for j in range(n - 1):
        if random.random() < 0.5:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def main():
    print("Starting experiments up to i=10...")
    print("Note: Higher values (i=8, 9, 10) will take longer to compute. Please wait.\n")

    results = {}

    # Loop from 1 to 10
    for i in range(1, 11):
        n = 300 * (2 ** i)
        print(f"[{time.strftime('%H:%M:%S')}] Processing i={i}, n={n}...")

        # --- 1. Sorted ---
        arr_sorted = list(range(1, n + 1))
        # Only count inversions if we need them for Table 2 (i <= 5)
        inv_sorted = 0
        if i <= 5:
            inv_sorted, _ = count_inversions(arr_sorted)

        s_sorted, b_sorted = run_experiment_on_array(arr_sorted)

        # --- 2. Reverse ---
        arr_reverse = list(range(n, 0, -1))
        inv_reverse = 0
        if i <= 5:
            # Formula for max inversions: n*(n-1)/2
            inv_reverse = n * (n - 1) // 2

        s_reverse, b_reverse = run_experiment_on_array(arr_reverse)

        # --- 3. Random (Avg of 20) ---
        s_rand_sum, b_rand_sum, inv_rand_sum = 0, 0, 0
        runs = 20
        for _ in range(runs):
            arr_rand = list(range(1, n + 1))
            random.shuffle(arr_rand)

            if i <= 5:
                curr_inv, _ = count_inversions(arr_rand)
                inv_rand_sum += curr_inv

            s, b = run_experiment_on_array(arr_rand)
            s_rand_sum += s
            b_rand_sum += b

        avg_rand = {
            's': s_rand_sum / runs,
            'b': b_rand_sum / runs,
            'inv': inv_rand_sum / runs if i <= 5 else 0
        }

        # --- 4. Swaps (Avg of 20) ---
        s_swap_sum, b_swap_sum, inv_swap_sum = 0, 0, 0
        for _ in range(runs):
            arr_swap = generate_random_swapped(n)

            if i <= 5:
                curr_inv, _ = count_inversions(arr_swap)
                inv_swap_sum += curr_inv

            s, b = run_experiment_on_array(arr_swap)
            s_swap_sum += s
            b_swap_sum += b

        avg_swap = {
            's': s_swap_sum / runs,
            'b': b_swap_sum / runs,
            'inv': inv_swap_sum / runs if i <= 5 else 0
        }

        results[i] = {
            'n': n,
            'Sorted': {'s': s_sorted, 'b': b_sorted, 'inv': inv_sorted},
            'Reverse': {'s': s_reverse, 'b': b_reverse, 'inv': inv_reverse},
            'Random': avg_rand,
            'Swaps': avg_swap
        }

    # ==========================================
    # PRINTING TABLES
    # ==========================================

    # Header Format
    # i | Sorted | Random | Swaps | Reverse
    header = "{:<5} | {:<15} | {:<15} | {:<20} | {:<20}".format(
        "i", "Sorted", "Random", "Adj. Swaps", "Reverse"
    )

    # --- TABLE 1: Balancing Costs (1 to 10) ---
    print("\n" + "=" * 90)
    print("Table 1: Total Balancing Cost — Promotions (i=1..10)")
    print("=" * 90)
    print(header)
    print("-" * 90)
    for i in range(1, 11):
        r = results[i]
        print("{:<5} | {:<15.0f} | {:<15.1f} | {:<20.1f} | {:<20.0f}".format(
            i,
            r['Sorted']['b'],
            r['Random']['b'],
            r['Swaps']['b'],
            r['Reverse']['b']
        ))

    # --- TABLE 2: Inversions (1 to 5 ONLY) ---
    # As per the assignment image text "sufficient up to i=5"
    print("\n\n" + "=" * 90)
    print("Table 2: Number of Inversions (i=1..5)")
    print("=" * 90)
    print(header)
    print("-" * 90)
    for i in range(1, 6):
        r = results[i]
        print("{:<5} | {:<15.0f} | {:<15.1f} | {:<20.1f} | {:<20.0f}".format(
            i,
            r['Sorted']['inv'],
            r['Random']['inv'],
            r['Swaps']['inv'],
            r['Reverse']['inv']
        ))

    # --- TABLE 3: Search Costs (1 to 10) ---
    print("\n\n" + "=" * 90)
    print("Table 3: Total Search Cost — Edges Traversed (i=1..10)")
    print("=" * 90)
    print(header)
    print("-" * 90)
    for i in range(1, 11):
        r = results[i]
        print("{:<5} | {:<15.0f} | {:<15.1f} | {:<20.1f} | {:<20.0f}".format(
            i,
            r['Sorted']['s'],
            r['Random']['s'],
            r['Swaps']['s'],
            r['Reverse']['s']
        ))
    print("=" * 90)


if __name__ == "__main__":
    main()
