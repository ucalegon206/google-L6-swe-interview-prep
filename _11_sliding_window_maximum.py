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

APPROACH: Monotonic Queue (Deque)
---------------------------------
A naive approach would be to iterate through all windows and find the max in each, taking O(N*k) time.
Given N=10^5, this is too slow (TLE). We need O(N).

We use a **Monotonic Queue** (implemented via a Deque - Double Ended Queue).
A Monotonic Queue maintains elements in a specific order (either increasing or decreasing).
Here, we want a **Decreasing Monotonic Queue**.

Invariant:
The queue will store **indices** (not values) of potential candidates for the maximum.
The elements in the queue will always be in **decreasing order of their values**.
Why? If `nums[i] <= nums[j]` and `i < j`, then `nums[i]` can NEVER be the maximum if `nums[j]` is in the window.
Basically, if a smaller number comes *before* a larger number, we can discard the smaller number because the larger number is "better" (larger) and "younger" (stays in window longer).

Algorithm:
1. Iterate through the array with index `i`.
2. **Remove Outdated indices**: Check if the front of the deque is out of the current window (`i - k + 1 > deque[0]`). If so, popleft.
3. **Maintain Monotonicity**: Before pushing `i`, remove all indices from the BACK of the deque whose values are smaller than `nums[i]`.
   (They are useless because `nums[i]` is larger and newer).
4. **Push**: Add current index `i` to the back.
5. **Record Result**: The front of the deque is the maximum for the current window. Add to results if the window is fully formed (`i >= k - 1`).

Time Complexity: O(N). Each element is added and removed at most once.
Space Complexity: O(k). The deque stores at most k elements.

Industry Nomenclature:
- **Deque (Double Ended Queue)**: A data structure that allows insertion and removal at both ends.
- **Monotonic Queue**: A queue where elements are always sorted.
- **Invariant**: A property that remains true throughout the execution of the algorithm.
- **Amortized Analysis**: Although the inner while loop runs multiple times, each element is processed a constant number of times on average.
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
