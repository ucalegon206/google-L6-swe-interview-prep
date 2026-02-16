"""
PROBLEM: Sliding Window Maximum
DIFFICULTY: Hard
TIME LIMIT: 35 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Monotonic Queue): https://www.youtube.com/watch?v=DfljaUwZsOk
- Geekific (Deque Explained): https://www.youtube.com/watch?v=LiNtADMqTfg
- Tushar Roy (Brute Force to Optimal): https://www.youtube.com/watch?v=J6o_Wz-UGvc

You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left 
of the array to the very right. You can only see the `k` numbers in the window. 
Each time the sliding window moves right by one position.

Return the max sliding window.

Example 1:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation: 
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

APPROACH: Monotonic Queue (Decreasing Deque)
--------------------------------------------
**The "Big Fish" Analogy:**
Imagine the sliding window is a pond.
- When a new fish (number) comes in, it eats all the smaller fish that were there before it.
  Why? Because the new fish is Big AND Younger (will stay in the window longer).
  The smaller fish that came before are now useless; they can never be the maximum again.
- If a fish comes in that is smaller than the current biggest fish, it survives (for now).
  Why? Because the big fish might leave the window (get too old), and this small fish might eventually become the biggest remaining fish.

**Data Structure: Deque (Double-Ended Queue)**
We need a structure that allows us to:
1. Pop small elements from the **Back** (when a big fish comes in).
2. Pop old elements from the **Front** (when they slide out of the window).
3. Access the current max at the **Front**.

**Algorithm Walkthrough:**
Input: nums = [1, 3, -1, -3, 5], k = 3
Deque stores INDICES: `q`

i=0, num=1:
- Empty q. Push 1.
- q = [0] (val: 1)

i=1, num=3:
- 3 > 1. 3 eats 1. Pop 0.
- Push 1.
- q = [1] (val: 3)

i=2, num=-1:
- -1 < 3. -1 survives.
- Push 2.
- q = [1, 2] (vals: 3, -1)
- Window size reached (3). Max is nums[q[0]] = 3. Result: [3]

i=3, num=-3:
- -3 < -1. -3 survives.
- Push 3.
- q = [1, 2, 3] (vals: 3, -1, -3)
- Check age: Index 1 is still valid (3-3+1 = 1).
- Max is nums[q[0]] = 3. Result: [3, 3]

i=4, num=5:
- 5 > -3. Pop 3.
- 5 > -1. Pop 2.
- 5 > 3. Pop 1.
- Push 4.
- q = [4] (val: 5)
- Max is nums[q[0]] = 5. Result: [3, 3, 5]

**Key "Invariant":**
The deque is always sorted in **Strictly Decreasing Order** of values.
The front always holds the index of the largest element in the current window.

Time Complexity: O(N). Each element is added once and removed at most once.
Space Complexity: O(k). The deque stores at most k elements.
"""

from typing import List
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums:
            return []
            
        # Deque will store INDICES, not values.
        # Storing indices allows us to easily check if an element is out of the window.
        q = deque()
        result = []
        
        for i in range(len(nums)):
            # Step 1: Remove indices that are out of the current window from the LEFT
            # The window range is [i - k + 1, i]
            # If the index at the front (q[0]) is < i - k + 1, it's too old.
            if q and q[0] < i - k + 1:
                q.popleft()
            
            # Step 2: Maintain the "Decreasing" property
            # [PITFALL] Monotonic Property.
            # While the value at the BACK (q[-1]) is smaller than current value (nums[i]),
            # remove it. It will never be the max because nums[i] is larger and lasts longer.
            while q and nums[q[-1]] < nums[i]:
                q.pop()
            
            # Step 3: Add current index
            q.append(i)
            
            # Step 4: Add to result if window size is reached
            # The first max is available when i == k - 1 (0-indexed)
            if i >= k - 1:
                # The front of the deque always has the index of the maximum element
                result.append(nums[q[0]])
                
        return result

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    nums = [1,3,-1,-3,5,3,6,7]
    k = 3
    print(f"Test 1: {solver.maxSlidingWindow(nums, k)} (Expected: [3,3,5,5,6,7])")
    
    # Test 2
    nums = [1]
    k = 1
    print(f"Test 2: {solver.maxSlidingWindow(nums, k)} (Expected: [1])")
    
    # Test 3: Decreasing Array (Maximum is always the first element of window)
    nums = [9, 8, 7, 6, 5]
    k = 3
    print(f"Test 3: {solver.maxSlidingWindow(nums, k)} (Expected: [9,8,7])")
    
    # Test 4: Increasing Array (Maximum is always the last element of window)
    nums = [1, 2, 3, 4, 5]
    k = 3
    print(f"Test 4: {solver.maxSlidingWindow(nums, k)} (Expected: [3,4,5])")
