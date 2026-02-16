import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _01_trapping_rain_water import Solution

class TestTrappingRainWater:
    def setup_method(self):
        self.solver = Solution()

    def test_standard_case(self):
        height = [0,1,0,2,1,0,1,3,2,1,2,1]
        assert self.solver.trap(height) == 6

    def test_bowl_shape(self):
        height = [4,2,0,3,2,5]
        assert self.solver.trap(height) == 9

    def test_mountain_shape(self):
        # No water trapped
        height = [0, 2, 5, 2, 0]
        assert self.solver.trap(height) == 0

    def test_ascending(self):
        height = [1, 2, 3, 4, 5]
        assert self.solver.trap(height) == 0

    def test_descending(self):
        height = [5, 4, 3, 2, 1]
        assert self.solver.trap(height) == 0

    def test_flat(self):
        height = [3, 3, 3, 3]
        assert self.solver.trap(height) == 0

    def test_empty(self):
        assert self.solver.trap([]) == 0

    def test_single_element(self):
        assert self.solver.trap([1]) == 0

    def test_two_elements(self):
        assert self.solver.trap([1, 2]) == 0

    def test_w_shape(self):
        # Water trapped in middle
        height = [5, 1, 5]
        assert self.solver.trap(height) == 4

    def test_large_input(self):
        # Performance check with 20,000 elements
        # A simple pattern: 10, 0, 10, 0, ... which traps 10 units in every gap
        # [10, 0, 10] -> traps 10
        # [10, 0, 10, 0, 10] -> traps 20
        # ...
        n = 20000
        height = []
        expected_water = 0
        for i in range(n):
            if i % 2 == 0:
                height.append(10)
            else:
                height.append(0)
                # If we have a sequence 10, 0, ... the next 10 closes the trap
                # Each '0' between '10's traps 10 units.
                # However, the last element might be 0, which wouldn't trap anything if no closing wall.
                # But n is 20000, so last index is 19999 (odd) -> 0.
                # The last 10 is at index 19998.
                # So we have pairs (10, 0), (10, 0) ... (10, 0).
                # The trailing 0 is not trapped because there is no wall after it.
                # Wait, let's trace:
                # [10, 0, 10] -> traps 10
                # [10, 0, 10, 0] -> traps 10 (last 0 spills)
                # [10, 0, 10, 0, 10] -> traps 20
                pass

        # Let's construct a cleaner large input: [0, 1, 0, 1, ...] is tricky.
        # Let's do a big bowl: [10000, 0, 0, ..., 0, 10000]
        # Traps 10000 * (n-2)
        height = [10000] + [0] * (n - 2) + [10000]
        assert self.solver.trap(height) == 10000 * (n - 2)

    def test_alternating_heights(self):
        # [0, 100, 0, 100, 0, 100]
        # Indices: 0(0), 1(100), 2(0), 3(100), 4(0), 5(100)
        # At 2: min(100, 100) - 0 = 100
        # At 4: min(100, 100) - 0 = 100
        # Total = 200
        height = [0, 100, 0, 100, 0, 100]
        assert self.solver.trap(height) == 200

    def test_plateau(self):
        # Wide flat top
        # [0, 5, 5, 5, 5, 0] -> No water
        height = [0, 5, 5, 5, 5, 0]
        assert self.solver.trap(height) == 0

    def test_plateau_trapping(self):
        # [5, 0, 0, 0, 5] -> Traps 5*3 = 15
        height = [5, 0, 0, 0, 5]
        assert self.solver.trap(height) == 15
        
        # [5, 2, 2, 2, 5] -> Traps (5-2)*3 = 9
        height = [5, 2, 2, 2, 5]
        assert self.solver.trap(height) == 9

    def test_stairs_with_gaps(self):
        # [5, 0, 4, 0, 3, 0, 2, 0, 1]
        # Water levels:
        # pos 1 (0): bounded by 5 and 4 -> 4
        # pos 3 (0): bounded by 4 and 3 -> 3
        # pos 5 (0): bounded by 3 and 2 -> 2
        # pos 7 (0): bounded by 2 and 1 -> 1
        # Total: 4 + 3 + 2 + 1 = 10
        height = [5, 0, 4, 0, 3, 0, 2, 0, 1]
        assert self.solver.trap(height) == 10

    def test_pyramid(self):
        # [0, 1, 2, 3, 2, 1, 0] -> No water
        height = [0, 1, 2, 3, 2, 1, 0]
        assert self.solver.trap(height) == 0

    def test_inverse_pyramid(self):
        # [3, 2, 1, 0, 1, 2, 3]
        # Water level will be 3 everywhere ideally, minus height
        # 0(3): full
        # 1(2): 3-2=1
        # 2(1): 3-1=2
        # 3(0): 3-0=3
        # 4(1): 3-1=2
        # 5(2): 3-2=1
        # 6(3): full
        # Total: 1 + 2 + 3 + 2 + 1 = 9
        height = [3, 2, 1, 0, 1, 2, 3]
        assert self.solver.trap(height) == 9

    def test_random_cases(self):
        # Reproducible random cases using specific seeds logic implies fixed input here
        
        # Case 1: Random small values
        height = [4, 9, 4, 5, 3, 2, 5]
        # max_l: 4, 9, 9, 9, 9, 9, 9
        # max_r: 9, 9, 5, 5, 5, 5, 5
        # min_max: 4, 9, 5, 5, 5, 5, 5
        # wat_lvl: 4, 9, 5, 5, 5, 5, 5
        # height : 4, 9, 4, 5, 3, 2, 5
        # diff   : 0, 0, 1, 0, 2, 3, 0 = 6
        assert self.solver.trap(height) == 6
