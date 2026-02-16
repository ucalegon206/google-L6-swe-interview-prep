import pytest
import sys
import os
import heapq

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _03_merge_k_sorted_lists import Solution, ListNode, create_linked_list, print_linked_list

class TestMergeKSortedLists:
    def setup_method(self):
        self.solver = Solution()
        
    def list_to_vals(self, node):
        """Helper to convert linked list to list of values for easy assertion"""
        vals = []
        while node:
            vals.append(node.val)
            node = node.next
        return vals

    def test_example_1_standard(self):
        # Input: lists = [[1,4,5],[1,3,4],[2,6]]
        # Output: [1,1,2,3,4,4,5,6]
        l1 = create_linked_list([1, 4, 5])
        l2 = create_linked_list([1, 3, 4])
        l3 = create_linked_list([2, 6])
        result = self.solver.mergeKLists([l1, l2, l3])
        assert self.list_to_vals(result) == [1, 1, 2, 3, 4, 4, 5, 6]

    def test_example_2_empty_input(self):
        # Input: lists = []
        # Output: []
        result = self.solver.mergeKLists([])
        assert result is None

    def test_example_3_list_of_empties(self):
        # Input: lists = [[]]
        # Output: []
        l1 = create_linked_list([]) # Returns None
        result = self.solver.mergeKLists([l1])
        assert result is None
        
        # Multiple empty lists
        result = self.solver.mergeKLists([None, None, None])
        assert result is None

    def test_single_list(self):
        # Merge of one list is just the list itself
        l1 = create_linked_list([1, 2, 3])
        result = self.solver.mergeKLists([l1])
        assert self.list_to_vals(result) == [1, 2, 3]

    def test_disjoint_ranges(self):
        # Lists with completely different value ranges
        # [1, 2], [5, 6], [3, 4] -> [1, 2, 3, 4, 5, 6]
        l1 = create_linked_list([1, 2])
        l2 = create_linked_list([5, 6])
        l3 = create_linked_list([3, 4])
        result = self.solver.mergeKLists([l1, l2, l3])
        assert self.list_to_vals(result) == [1, 2, 3, 4, 5, 6]

    def test_lots_of_duplicates(self):
        # [1, 1], [1, 1], [1] -> [1, 1, 1, 1, 1]
        l1 = create_linked_list([1, 1])
        l2 = create_linked_list([1, 1])
        l3 = create_linked_list([1])
        result = self.solver.mergeKLists([l1, l2, l3])
        assert self.list_to_vals(result) == [1, 1, 1, 1, 1]

    def test_negative_numbers(self):
        # [-10, -5], [-7, 0] -> [-10, -7, -5, 0]
        l1 = create_linked_list([-10, -5])
        l2 = create_linked_list([-7, 0])
        result = self.solver.mergeKLists([l1, l2])
        assert self.list_to_vals(result) == [-10, -7, -5, 0]

    def test_different_lengths(self):
        # [1], [2, 3, 4, 5], []
        l1 = create_linked_list([1])
        l2 = create_linked_list([2, 3, 4, 5])
        l3 = create_linked_list([])
        result = self.solver.mergeKLists([l1, l2, l3])
        assert self.list_to_vals(result) == [1, 2, 3, 4, 5]

    def test_large_k_small_n(self):
        # Many lists, each with 1 element
        # k=1000 lists of [i]
        lists = []
        expected = []
        for i in range(100):
            lists.append(create_linked_list([i]))
            expected.append(i)
        
        result = self.solver.mergeKLists(lists)
        assert self.list_to_vals(result) == expected
