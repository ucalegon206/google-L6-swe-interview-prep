# Study Guide: Problems Grouped by Approach

To help you internalize the concepts, I've grouped your 16 practice problems by their **primary optimal approach**. This will help you recognize the "shape" of a problem when you see it in an interview.

## 1. Two Pointers / Sliding Window
*These problems involve maintaining a range or two references to solve in O(N).*
*   **_01_trapping_rain_water.py** (Two Pointers coming from variable ends)
*   **_07_minimum_window_substring.py** (Sliding Window with Hash Map)
*   **_11_sliding_window_maximum.py** (Sliding Window with Monotonic Deque)

## 2. Binary Search
*These problems require O(log N) or better, usually on sorted data or answer spaces.*
*   **_02_median_two_sorted_arrays.py** (Binary Search on Partition)
*   **_13_count_smaller_after_self.py** (Merge Sort / Binary Index Tree)

## 3. Heaps (Priority Queue)
*These problems deal with "Top K", "Median", or "Merging".*
*   **_03_merge_k_sorted_lists.py** (Min-Heap)
*   **_14_the_skyline_problem.py** (Max-Heap / Sweep Line)

## 4. DFS / BFS / Graph Search
*These problems involve exploring states, grids, or graphs.*
*   **_04_word_ladder_ii.py** (BFS for shortest path + DFS for reconstruction)
*   **_05_alien_dictionary.py** (Topological Sort / DFS)
*   **_06_serialize_deserialize_binary_tree.py** (DFS Preorder or BFS Level Order)
*   **_12_remove_invalid_parentheses.py** (BFS for minimum removals)
*   **_08_word_search_ii.py** (DFS + Trie)

## 5. Dynamic Programming
*These problems involve breaking down a complex problem into subproblems.*
*   **_09_regular_expression_matching.py** (DP on 2D Grid)

## 6. Stacks
*These problems use a LIFO structure to handle order dependencies.*
*   **_10_largest_rectangle_histogram.py** (Monotonic Stack)

## 7. Design / System
*These problems simulate a real-world component.*
*   **_15_lru_cache.py** (Doubly Linked List + Hash Map)
*   **_16_design_search_autocomplete_system.py** (Trie + Min-Heap)

---

### Suggested Order of Review
1.  **Two Pointers** (Start here, it's the most "visual")
2.  **Heaps** (Very common for L6 "scale" questions)
3.  **Graphs/Tries** (Critical for complexity)
