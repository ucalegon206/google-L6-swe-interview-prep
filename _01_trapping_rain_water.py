"""
PROBLEM: Trapping Rain Water
DIFFICULTY: Hard
TIME LIMIT: 30 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Python Two Pointers): https://www.youtube.com/watch?v=ZI2z5pq0TqA
- Tushar Roy (Stack & Two Pointers): https://www.youtube.com/watch?v=KV-Eq3wYFCI
- Take U Forward (Detailed Walkthrough): https://www.youtube.com/watch?v=m18Hntz4go8

Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it can trap after raining.

Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. 
In this case, 6 units of rain water (blue section) are being trapped.

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

APPROACH:
There are multiple approaches:
1. Dynamic Programming (Prefix/Suffix Max): O(N) Time, O(N) Space
   - Precompute `left_max` and `right_max` arrays.
   - Water at `i` = `min(left_max[i], right_max[i]) - height[i]`

2. Two Pointers: O(N) Time, O(1) Space (Optimal)
   - Maintain `left` and `right` pointers.
   - Also maintain `max_l` and `max_r`.
   - If `max_l < max_r`, we know the bottleneck is on the left side (or equal), so we can fill water at `left` based on `max_l`.
   - Move the pointer with the smaller max height inward.
"""

from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        """
        Calculates the amount of trapped water using the Two Pointers approach.
        
        This method computes the total amount of water that can be trapped between bars in an elevation map.
        It uses a two-pointer strategy to efficiently calculate the water level at each position in a single pass.
        
        Algorithm:
        ----------
        The core idea is that the amount of water trapped at any position `i` is determined by:
            water[i] = min(max_height_left[i], max_height_right[i]) - height[i]
            
        Instead of precomputing these max arrays (which takes O(N) space), we can use two pointers technique
        because we only need the *minimum* of the two maximums to know the water level.
        
        1. Initialize `left` pointer at the start (0) and `right` pointer at the end (n-1).
        2. Maintain `max_l` (maximum height seen from left) and `max_r` (maximum height seen from right).
        3. At each step, compare `max_l` and `max_r`:
            - If `max_l < max_r`: We know the water level at the `left` pointer is limited by `max_l` because 
              there is a taller barrier somewhere to the right (`max_r`). 
              So, water trapped = `max_l - height[left]`. Then move `left` forward.
            - Else (`max_l >= max_r`): The key constraint is `max_r`. 
              Water trapped = `max_r - height[right]`. Then move `right` backward.
        
        Time Complexity: O(N)
            - We process each element of the array exactly once using the two pointers.
            
        Space Complexity: O(1)
            - We only use a few variables (left, right, max_l, max_r, water) for storage.
            
        Args:
            height (List[int]): A list of non-negative integers representing the elevation map.
            
        Returns:
            int: The total amount of trapped water.
        """
        if not height:
            return 0
            
        left, right = 0, len(height) - 1
        max_l, max_r = height[left], height[right]
        water = 0
        
        while left < right:
            # We compare the MAX heights found so far on both ends.
            # The logic relies on the fact that water level at any index i is determined by:
            # min(max_height_to_left_of_i, max_height_to_right_of_i) - height[i]
            
            if max_l < max_r:
                # If left side max is smaller, then the water level at 'left' pointer position is bound by max_l.
                # Justification:
                # 1. We know max_l is the highest wall to the left of current `left`.
                # 2. We know max_r is *some* wall to the right of `left`.
                # 3. Since max_l < max_r, the actual max_right for `left` is at least max_r, so min(max_l, actual_max_right) = max_l.
                
                # [PITFALL] We MUST move the pointer BEFORE calculating water for that position.
                # Why? Because `max_l` initially includes `height[left]`. If we don't move, we are comparing the wall to itself.
                # We want to calculate water for the *inner* positions.
                left += 1
                current_height = height[left]
                
                # Update max_l if the new bar is taller
                # If the new bar is taller than previous max_l, it can't trap water relative to the left side,
                # but it becomes the new boundary for subsequent positions.
                max_l = max(max_l, current_height)
                
                # Add trapped water: (bounding height - current bar height)
                # Since max_l is updated to be at least current_height (line above), this is guaranteed to be >= 0.
                water += max_l - current_height
                
            else:
                # If right side max is smaller (or equal), then the water level at 'right' is bound by max_r.
                # Symmetric logic to the left side apply here.
                right -= 1
                current_height = height[right]
                
                # Update max_r
                max_r = max(max_r, current_height)
                
                # Add trapped water
                water += max_r - current_height
                
        return water

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1: Standard case
    h1 = [0,1,0,2,1,0,1,3,2,1,2,1]
    print(f"Test 1 Output: {solver.trap(h1)} (Expected: 6)")
    
    # Test 2: Bowl shape
    h2 = [4,2,0,3,2,5]
    print(f"Test 2 Output: {solver.trap(h2)} (Expected: 9)")
    
    # Test 3: No water possible (ascending)
    h3 = [1,2,3,4,5]
    print(f"Test 3 Output: {solver.trap(h3)} (Expected: 0)")
