"""
PROBLEM: Count of Smaller Numbers After Self
DIFFICULTY: Hard
TIME LIMIT: 45 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Merge Sort): https://www.youtube.com/watch?v=X0oXMdtUDwo
- Tushar Roy (Binary Indexed Tree): https://www.youtube.com/watch?v=2SVLYsq5W8M
- Aryan Mittal (Merge Sort & Fenwick): https://www.youtube.com/watch?v=_s4W1W2eA6M

You are given an integer array `nums` and you have to return a new counts array. 
The counts array has the property where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

Example 1:
Input: nums = [5,2,6,1]
Output: [2,1,1,0]
Explanation:
To the right of 5 there are 2 smaller elements (2 and 1).
To the right of 2 there is 1 smaller element (1).
To the right of 6 there is 1 smaller element (1).
To the right of 1 there is 0 smaller elements.

Example 2:
Input: nums = [-1]
Output: [0]

Example 3:
Input: nums = [-1,-1]
Output: [0,0]

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

APPROACH: Merge Sort (Divide and Conquer)
-----------------------------------------
This problem is related to finding **inversions** in an array.
A naive O(N^2) solution checking every pair is too slow. We need O(N log N).

We can modify Merge Sort.
In standard Merge Sort, we split the array into left and right halves and then merge them.
Counting Logic:
When we pick `left_val` to place in the sorted array, we want to know how many elements from the RIGHT subarray have *already* "jumped" ahead of it.

Correct Logic:
During merge, we have `left_part` and `right_part`.
We maintain pointers `i` (left) and `j` (right).
We want to place the smaller element into the merged result.

- If `right_part[j]` is smaller than `left_part[i]`:
  `right_part[j]` "jumps" ahead of `left_part[i]`.
  We increment `j` and place it in temp array.
  We count this jump. A variable `right_counter` tracks how many elements from right have been placed.
  
- If `left_part[i]` is smaller or equal to `right_part[j]`:
  We place `left_part[i]` into the temp array.
  At this moment, we know exactly how many elements from the `right_part` were smaller than `left_part[i]`—it's exactly `j`!
  Why? Because those `j` elements were already moved to the sorted array because they were smaller.
  So, we add `j` to the count of `left_part[i]`.

Important Implementation Detail:
Since we sort the array, the elements move indices. We need to track their *original indices* to update the `counts` array correctly.
So we store pairs `(value, original_index)`.

Industry Nomenclature:
- **Divide and Conquer**: Breaking a problem into subproblems, solving them, and combining results.
- **Inversion Count**: A measure of how far an array is from being sorted.
- **Stable Sort**: A sort that maintains the relative order of equal elements (important here).
"""

from typing import List

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # Store (val, original_index) to track where to add counts
        arr = [[v, i] for i, v in enumerate(nums)]
        result = [0] * n
        
        def merge_sort(enum):
            if len(enum) <= 1:
                return enum
            
            mid = len(enum) // 2
            left = merge_sort(enum[:mid])
            right = merge_sort(enum[mid:])
            
            return merge(left, right)
        
        def merge(left, right):
            merged = []
            i, j = 0, 0
            
            # During merge, we count how many elements from 'right' are smaller than 'left[i]'
            # But wait, to make it easier:
            # If we sort in ASCENDING order:
            # When we pick left[i], we want to know how many items from right were *already picked* (meaning they were smaller).
            num_elems_right_smaller_than_current_left = 0
            
            while i < len(left) and j < len(right):
                if left[i][0] <= right[j][0]:
                    # left[i] is smaller. It is placed in merged.
                    # At this point, 'j' elements from right have been processed.
                    # Those 'j' elements were all strictly smaller than left[i] (because they were picked first!).
                    # So we add 'j' to left[i]'s count.
                    # [PITFALL] Index Mapping.
                    # We must update the count for the *original* index of the element.
                    # 'j' represents the number of elements from the right subarray that jumped ahead.
                    result[left[i][1]] += j
                    merged.append(left[i])
                    i += 1
                else:
                    # right[j] is smaller. It "jumps" ahead.
                    # We don't update counts here because right elements don't care about left elements (problem is "smaller AFTER self").
                    merged.append(right[j])
                    j += 1
            
            # Remaining elements
            while i < len(left):
                # All remaining left elements are larger than ALL right elements processed so far.
                # So they effectively have 'len(right)' (or current j) smaller elements from the right side.
                result[left[i][1]] += j
                merged.append(left[i])
                i += 1
            
            while j < len(right):
                merged.append(right[j])
                j += 1
                
            return merged

        merge_sort(arr)
        return result

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    nums = [5, 2, 6, 1]
    # 5: [2, 1] -> 2
    # 2: [1] -> 1
    # 6: [1] -> 1
    # 1: [] -> 0
    print(f"Test 1: {solver.countSmaller(nums)} (Expected: [2, 1, 1, 0])")
    
    # Test 2
    nums = [-1]
    print(f"Test 2: {solver.countSmaller(nums)} (Expected: [0])")
    
    # Test 3
    nums = [-1, -1]
    print(f"Test 3: {solver.countSmaller(nums)} (Expected: [0, 0])")
