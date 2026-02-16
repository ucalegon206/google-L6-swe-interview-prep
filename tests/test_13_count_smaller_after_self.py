import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _13_count_smaller_after_self import Solution

class TestCountSmaller:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: nums = [5,2,6,1]
        # Output: [2,1,1,0]
        nums = [5, 2, 6, 1]
        expected = [2, 1, 1, 0]
        assert self.solver.countSmaller(nums) == expected

    def test_example_2_single_element(self):
        # Input: nums = [-1]
        # Output: [0]
        nums = [-1]
        expected = [0]
        assert self.solver.countSmaller(nums) == expected

    def test_example_3_duplicates(self):
        # Input: nums = [-1,-1]
        # Output: [0,0]
        nums = [-1, -1]
        expected = [0, 0]
        assert self.solver.countSmaller(nums) == expected

    def test_sorted_array(self):
        # [1, 2, 3, 4] -> [0, 0, 0, 0]
        nums = [1, 2, 3, 4]
        expected = [0, 0, 0, 0]
        assert self.solver.countSmaller(nums) == expected

    def test_reverse_sorted_array(self):
        # [4, 3, 2, 1] -> [3, 2, 1, 0]
        nums = [4, 3, 2, 1]
        expected = [3, 2, 1, 0]
        assert self.solver.countSmaller(nums) == expected

    def test_mixed_duplicates(self):
        # [5, 2, 6, 1, 2, 5]
        # 5: 2, 1, 2 -> 3
        # 2: 1 -> 1
        # 6: 1, 2, 5 -> 3
        # 1: 0
        # 2: 0
        # 5: 0
        # Wait, right of 5 (idx 0) are [2, 6, 1, 2, 5]. Smaller: 2, 1, 2. (3 check).
        # right of 2 (idx 1) are [6, 1, 2, 5]. Smaller: 1. (1 check).
        # right of 6 (idx 2) are [1, 2, 5]. Smaller: 1, 2, 5. (3 check).
        # right of 1 (idx 3) are [2, 5]. Smaller: 0.
        # right of 2 (idx 4) are [5]. Smaller: 0.
        # right of 5 (idx 5) are []. Smaller: 0.
        # Expected: [3, 1, 3, 0, 0, 0]
        nums = [5, 2, 6, 1, 2, 5]
        expected = [3, 1, 3, 0, 0, 0]
        assert self.solver.countSmaller(nums) == expected

    def test_empty_array(self):
        nums = []
        expected = []
        assert self.solver.countSmaller(nums) == expected
