"""
PROBLEM: Largest Rectangle in Histogram
DIFFICULTY: Hard
TIME LIMIT: 45 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Monotonic Stack): https://www.youtube.com/watch?v=zx5Sw9130L0
- Tech Dose (Stack Solution): https://www.youtube.com/watch?v=J2X70jj_I1o
- Tushar Roy (Detailed Walkthrough): https://www.youtube.com/watch?v=ZmnqCZp9bBs

Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, 
return the area of the largest rectangle in the histogram.

Example 1:
Input: heights = [2,1,5,6,2,3]
Output: 10
Explanation: The largest rectangle has an area = 10 units.
It is formed by the bars of height 5 and 6. The min height is 5, and width is 2, so 5 * 2 = 10.

Example 2:
Input: heights = [2,4]
Output: 4

Constraints:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4


APPROACH: Monotonic Stack
To find the largest rectangle, we need to know for each bar `i` with height `h`:
1. The **Left Boundary**: The index of the first bar to the left that is shorter than `h`.
2. The **Right Boundary**: The index of the first bar to the right that is shorter than `h`.
(Because if a bar is shorter, it cuts off the rectangle.)

Width = (Right Boundary - Left Boundary - 1)
Area = `h * Width`

We can find these boundaries efficiently in O(N) using a Monotonic Stack optimization.
A **Monotonic INCREASING Stack** stores indices such that the corresponding heights are always increasing.

Algorithm:
1. Iterate through the histogram heights.
2. While the current bar is SHORTER than the bar at the top of the stack:
   - This means the current bar is the **Right Boundary** for the stack top.
   - Pop the top index (`h_idx`) from the stack. The height of the rectangle is `heights[h_idx]`.
   - The **Left Boundary** is strictly the new top of the stack (after popping).
     (Because elements in the stack are always increasing, the new top is the closest smaller element to the left).
   - Calculate Area: `height * (current_i - stack_top_i - 1)`
   - Update max_area.
3. Push the current index onto the stack.

Edge Case:
- After iterating through all bars, the stack might not be empty (e.g., if heights are increasing [1,2,3]).
- We process the remaining bars as if they extend to the very end of the array (Right Boundary = len(heights)).

Time Complexity: O(N). Each element is pushed and popped at most once.
Space Complexity: O(N). Stack size.

Industry Nomenclature:
- **Monotonic Stack**: A stack that maintains elements in a sorted order.
- **Previous Less Element / Next Less Element**: The nearest elements that bound the rectangle size.
"""

from typing import List

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        # Stack will store indices
        stack = []
        max_area = 0
        
        # We append a 0-height bar at the end.
        # This forces the stack to empty completely at the end of the loop,
        # processing all remaining potential rectangles.
        # Because 0 is smaller than any valid height (assuming non-negative),
        # it acts as the "Right Boundary" for all remaining increasing bars.
        heights.append(0)
        
        for i, h in enumerate(heights):
            # While the current bar is LOWER than the bar at the stack top,
            # we demonstrate that 'i' is the right boundary for the bar at stack top.
            while stack and h < heights[stack[-1]]:
                # This height was a potential candidate for a tall rectangle.
                height = heights[stack.pop()]
                
                # Determine width:
                # If stack is empty, it means this bar was the smallest so far,
                # so it extends all the way to the left (current index i).
                # If stack is not empty, the left boundary is the previous index in stack.
                # [PITFALL] Width Calculation.
                # Right boundary is 'i' (exclusive, since it's smaller).
                # Left boundary is 'stack[-1]' (exclusive, since it's the previous smaller element).
                # Width = (Right - 1) - (Left + 1) + 1 = Right - Left - 1.
                # If stack is empty, it means this bar is smaller than everything before it, so Left = -1.
                width = i if not stack else i - stack[-1] - 1
                
                max_area = max(max_area, height * width)
            
            stack.append(i)
        
        return max_area

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    heights = [2,1,5,6,2,3]
    print(f"Test 1: {solver.largestRectangleArea(heights)} (Expected: 10)") # 5 and 6 form 5*2=10
    
    # Test 2
    heights = [2,4]
    print(f"Test 2: {solver.largestRectangleArea(heights)} (Expected: 4)") # 2*2=4 or 4*1=4
    
    # Test 3: Increasing logic
    heights = [1, 2, 3]
    print(f"Test 3: {solver.largestRectangleArea(heights)} (Expected: 4)") # 2*2 for [2,3] -> 4. 1*3 -> 3. 3*1 -> 3.
