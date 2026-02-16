import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _11_sliding_window_maximum import Solution

class TestSlidingWindowMaximum:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
        # Output: [3,3,5,5,6,7]
        nums = [1,3,-1,-3,5,3,6,7]
        k = 3
        expected = [3,3,5,5,6,7]
        assert self.solver.maxSlidingWindow(nums, k) == expected

    def test_single_element(self):
        nums = [1]
        k = 1
        assert self.solver.maxSlidingWindow(nums, k) == [1]

    def test_decreasing_array(self):
        # [9, 8, 7, 6, 5], k=3
        # Window 1: [9,8,7] -> 9
        # Window 2: [8,7,6] -> 8
        # Window 3: [7,6,5] -> 7
        nums = [9, 8, 7, 6, 5]
        k = 3
        expected = [9, 8, 7]
        assert self.solver.maxSlidingWindow(nums, k) == expected

    def test_increasing_array(self):
        # [1, 2, 3, 4, 5], k=3
        # Window 1: [1,2,3] -> 3
        # Window 2: [2,3,4] -> 4
        # Window 3: [3,4,5] -> 5
        nums = [1, 2, 3, 4, 5]
        k = 3
        expected = [3, 4, 5]
        assert self.solver.maxSlidingWindow(nums, k) == expected

    def test_empty_input(self):
        nums = []
        k = 0
        assert self.solver.maxSlidingWindow(nums, k) == []

    def test_k_equals_length(self):
        nums = [1, -5, 10, -3]
        k = 4
        # Max is 10
        assert self.solver.maxSlidingWindow(nums, k) == [10]

    def test_k_is_1(self):
        # Output should be same as input
        nums = [4, 2, 10]
        k = 1
        assert self.solver.maxSlidingWindow(nums, k) == [4, 2, 10]

    def test_alternating_values(self):
        # [1, 5, 1, 5, 1], k=2
        # [1,5] -> 5
        # [5,1] -> 5
        # [1,5] -> 5
        # [5,1] -> 5
        nums = [1, 5, 1, 5, 1]
        k = 2
        assert self.solver.maxSlidingWindow(nums, k) == [5, 5, 5, 5]

    def test_large_negative_numbers(self):
        nums = [-100, -200, -50, -300]
        k = 2
        # [-100, -200] -> -100
        # [-200, -50] -> -50
        # [-50, -300] -> -50
        assert self.solver.maxSlidingWindow(nums, k) == [-100, -50, -50]
