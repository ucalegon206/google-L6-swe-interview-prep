"""
PROBLEM: Median of Two Sorted Arrays
DIFFICULTY: Hard
TIME LIMIT: 40 Minutes

Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

VISUAL EXPLANATIONS:
- NeetCode (Excellent Visualization): https://www.youtube.com/watch?v=q6IEA26hvXc
- Take U Forward (Detailed Walkthrough): https://www.youtube.com/watch?v=NTop3VTjmxk
- Tushar Roy (Logical Breakdown): https://www.youtube.com/watch?v=LPFhl65R7ww

Example 1:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

Example 3:
Input: nums1 = [0,0], nums2 = [0,0]
Output: 0.00000

Example 4:
Input: nums1 = [], nums2 = [1]
Output: 1.00000

Example 5:
Input: nums1 = [2], nums2 = []
Output: 2.00000

Constraints:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

APPROACH: Binary Search on Partition
To achieve O(log(min(m, n))) complexity, we cannot simply merge the arrays (which would be O(m+n)).
Instead, we need to find a partition point in both arrays such that:
1. The left half of the combined array has the same number of elements as the right half (or one more).
2. All elements on the left side (from both arrays) are <= all elements on the right side.

Let's say we cut `nums1` at index `i` (meaning `nums1[0]...nums1[i-1]` are in the left half)
and `nums2` at index `j` (meaning `nums2[0]...nums2[j-1]` are in the left half).

The condition for a valid partition is:
nums1[i-1] <= nums2[j]  AND  nums2[j-1] <= nums1[i]

We perform binary search on the smaller array to find the correct `i`. `j` is then calculated based on `i` and the total length.
"""

from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Step 1: Ensure nums1 is the smaller array to minimize binary search range.
        if len(nums1) > len(nums2):
            return self.findMedianSortedArrays(nums2, nums1)

        x, y = len(nums1), len(nums2)
        low, high = 0, x
        
        while low <= high:
            partitionX = (low + high) // 2
            # partitionY is calculated such that the left half has (x + y + 1) // 2 elements.
            # This ensures that for odd total length, the median is the max of the left half.
            # [PITFALL] The +1 is critical! 
            # It ensures that for ODD total length (x+y), the "Left" side gets the extra element.
            # This makes the median logic consistent: median is max(Left) if odd.
            partitionY = (x + y + 1) // 2 - partitionX
            
            # Handling edge cases where partition is at the far left (0) or far right (length)
            # If partitionX is 0, it means nothing is there on left side. use -INF.
            # If partitionX is n, it means nothing is there on right side. use +INF.
            # [PITFALL] Boundary handling using Infinity.
            # If partitionX == 0, there is nothing on the left of X, so we use -infinity to "lose" any max comparisons.
            # If partitionX == x, there is nothing on the right of X, so we use +infinity to "lose" any min comparisons.
            maxLeftX = float('-inf') if partitionX == 0 else nums1[partitionX - 1]
            minRightX = float('inf') if partitionX == x else nums1[partitionX]
            
            maxLeftY = float('-inf') if partitionY == 0 else nums2[partitionY - 1]
            minRightY = float('inf') if partitionY == y else nums2[partitionY]
            
            # Step 2: Check if we have found the correct partition
            if maxLeftX <= minRightY and maxLeftY <= minRightX:
                # Partitions are correct!
                
                # If total length is even:
                if (x + y) % 2 == 0:
                    return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2
                # If total length is odd:
                else:
                    return max(maxLeftX, maxLeftY)
                    
            # Step 3: Adjust partition pointers
            elif maxLeftX > minRightY:
                # We are too far right in nums1. Move left.
                high = partitionX - 1
            else:
                # We are too far left in nums1. Move right.
                low = partitionX + 1
                
        raise ValueError("Input arrays are not sorted or invalid.")

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    nums1 = [1, 3]
    nums2 = [2]
    # Merged: [1, 2, 3], Median: 2
    print(f"Test 1: {solver.findMedianSortedArrays(nums1, nums2)} (Expected: 2.0)")

    # Test 2
    nums1 = [1, 2]
    nums2 = [3, 4]
    # Merged: [1, 2, 3, 4], Median: 2.5
    print(f"Test 2: {solver.findMedianSortedArrays(nums1, nums2)} (Expected: 2.5)")
    
    # Test 3
    nums1 = [0, 0]
    nums2 = [0, 0]
    print(f"Test 3: {solver.findMedianSortedArrays(nums1, nums2)} (Expected: 0.0)")
