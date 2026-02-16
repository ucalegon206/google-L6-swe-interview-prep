import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _14_the_skyline_problem import Solution

class TestSkylineProblem:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
        # Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
        buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
        expected = [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
        assert self.solver.getSkyline(buildings) == expected

    def test_example_2_flat(self):
        # Input: buildings = [[0,2,3],[2,5,3]]
        # Output: [[0,3],[5,0]]
        buildings = [[0,2,3],[2,5,3]]
        expected = [[0,3],[5,0]]
        assert self.solver.getSkyline(buildings) == expected

    def test_nested_buildings(self):
        # Tall building inside shorter building
        # [[0, 5, 10], [1, 4, 15]]
        # 0: +10. Max 10. -> [0, 10]
        # 1: +15. Max 15. -> [1, 15]
        # 4: -15. Max 10. -> [4, 10]
        # 5: -10. Max 0.  -> [5, 0]
        buildings = [[0, 5, 10], [1, 4, 15]]
        expected = [[0, 10], [1, 15], [4, 10], [5, 0]]
        assert self.solver.getSkyline(buildings) == expected

    def test_increasing_height(self):
        # [[0, 2, 5], [1, 3, 10], [2, 4, 15]]
        # 0: +5 -> [0, 5]
        # 1: +10 -> [1, 10]
        # 2: +15, -5 (irrelevant). Max 15 -> [2, 15]
        # 3: -10. Max 15. No change.
        # 4: -15. Max 0. -> [4, 0]
        buildings = [[0, 2, 5], [1, 3, 10], [2, 4, 15]]
        expected = [[0, 5], [1, 10], [2, 15], [4, 0]]
        assert self.solver.getSkyline(buildings) == expected

    def test_single_building(self):
        buildings = [[0, 2147483647, 2147483647]]
        expected = [[0, 2147483647], [2147483647, 0]]
        assert self.solver.getSkyline(buildings) == expected

    def test_empty_buildings(self):
        buildings = []
        expected = []
        # Code might return [] or handle empty
        # events = [] -> sort -> loop skip -> result [[0,0]]. 
        # return result[1:] -> []
        assert self.solver.getSkyline(buildings) == expected

    def test_separated_buildings(self):
        # [[0, 1, 10], [2, 3, 10]]
        # 0: +10 -> [0, 10]
        # 1: -10 -> [1, 0]
        # 2: +10 -> [2, 10]
        # 3: -10 -> [3, 0]
        buildings = [[0, 1, 10], [2, 3, 10]]
        expected = [[0, 10], [1, 0], [2, 10], [3, 0]]
        assert self.solver.getSkyline(buildings) == expected

    def test_same_start_different_height(self):
        # [[0, 5, 10], [0, 5, 20]]
        # Should just be [[0, 20], [5, 0]]
        buildings = [[0, 5, 10], [0, 5, 20]]
        expected = [[0, 20], [5, 0]]
        assert self.solver.getSkyline(buildings) == expected
