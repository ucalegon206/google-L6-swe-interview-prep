import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _10_largest_rectangle_histogram import Solution

class TestLargestRectangleArea:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: heights = [2,1,5,6,2,3]
        # Output: 10 (bar 5 and 6, width 2, min_h 5 -> 10)
        heights = [2,1,5,6,2,3]
        assert self.solver.largestRectangleArea(heights) == 10

    def test_example_2_two_bars(self):
        # Input: heights = [2,4]
        # Output: 4 (bar 4, width 1, area 4 vs bar 2 and 4, width 2, min 2 -> 4)
        heights = [2,4]
        assert self.solver.largestRectangleArea(heights) == 4

    def test_increasing_order(self):
        # [1, 2, 3] -> areas: 1*3=3, 2*2=4, 3*1=3 -> Max 4
        heights = [1, 2, 3]
        assert self.solver.largestRectangleArea(heights) == 4

    def test_decreasing_order(self):
        # [3, 2, 1] -> areas: 3*1=3, 2*2=4, 1*3=3 -> Max 4
        heights = [3, 2, 1]
        assert self.solver.largestRectangleArea(heights) == 4

    def test_all_same_height(self):
        # [2, 2, 2] -> 2 * 3 = 6
        heights = [2, 2, 2]
        assert self.solver.largestRectangleArea(heights) == 6

    def test_single_bar(self):
        heights = [100]
        assert self.solver.largestRectangleArea(heights) == 100

    def test_empty_input(self):
        heights = []
        assert self.solver.largestRectangleArea(heights) == 0

    def test_jagged_array(self):
        # [2, 1, 2]
        # 2*1=2. 1*3=3. 2*1=2.
        # Max 3.
        heights = [2, 1, 2]
        assert self.solver.largestRectangleArea(heights) == 3

    def test_large_rectangle_at_end(self):
        # [0, 9] -> 9
        heights = [0, 9]
        assert self.solver.largestRectangleArea(heights) == 9
