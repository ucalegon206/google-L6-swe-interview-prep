import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _02_median_two_sorted_arrays import Solution

class TestMedianTwoSortedArrays:
    def setup_method(self):
        self.solver = Solution()

    def test_standard_odd(self):
        nums1 = [1, 3]
        nums2 = [2]
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 2.0

    def test_standard_even(self):
        nums1 = [1, 2]
        nums2 = [3, 4]
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 2.5

    def test_empty_first(self):
        nums1 = []
        nums2 = [1]
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 1.0

    def test_empty_second(self):
        nums1 = [2]
        nums2 = []
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 2.0

    def test_both_single(self):
        nums1 = [1]
        nums2 = [2]
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 1.5

    def test_disjoint_ranges(self):
        nums1 = [1, 2, 3]
        nums2 = [4, 5, 6]
        # Merged: 1, 2, 3, 4, 5, 6 -> Median is (3+4)/2 = 3.5
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 3.5

    def test_large_gap(self):
        nums1 = [1, 100]
        nums2 = [2, 99]
        # Merged: 1, 2, 99, 100 -> Median (2+99)/2 = 50.5
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 50.5

    def test_zeros(self):
        nums1 = [0, 0]
        nums2 = [0, 0]
        assert self.solver.findMedianSortedArrays(nums1, nums2) == 0.0
