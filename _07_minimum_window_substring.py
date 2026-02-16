"""
PROBLEM: Minimum Window Substring
DIFFICULTY: Hard
TIME LIMIT: 40 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Sliding Window): https://www.youtube.com/watch?v=jSto0O4AJbM
- Tech Dose (Explained): https://www.youtube.com/watch?v=eS6PZLjoaq8
- Code in Motion (Animated): https://www.youtube.com/watch?v=U1q16AFcjKs

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. 
If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

Example 1:
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Example 2:
Input: s = "a", t = "a"
Output: "a"

Example 3:
Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return "".

Constraints:
- m == s.length
- n == t.length
- 1 <= m, n <= 10^5
- s and t consist of uppercase and lowercase English letters.
 
Follow up: Could you find an algorithm that runs in O(m + n) time?

APPROACH: Sliding Window Optimization (Two Pointers)
----------------------------------------------------
We need to find the smallest contiguous subarray (window) that satisfies a condition. This screams "Sliding Window".

Algorithm:
1. **Target Frequency Map**: First, count the frequency of each char in `t`. This tells us what we NEED.
2. **Current Window Map**: Maintain a frequency map of the current window in `s`.
3. **Expand (Right Pointer)**: Move the `right` pointer to include characters into the window.
   - Update the current window map.
   - Check if the added character satisfies a requirement (i.e., we have enough of that specific char).
   - Track `formed` variables: how many unique characters have met their target frequency.
4. **Contract (Left Pointer)**: Once the window is valid (i.e., `formed == required`), try to shrink it from the left to minimize size.
   - Record the current window size if it's the smallest seen so far.
   - Remove the character at `left` pointer from the window.
   - Update `formed` if the removal breaks a requirement.
   - Increment `left` pointer.

Time Complexity: O(M + N).
- We construct the frequency map: O(N).
- The sliding window pointers `left` and `right` each visit every character in `s` at most once: O(2M) = O(M).

Space Complexity: O(1) mostly, or O(26/52) since alphabet size is fixed.

Industry Nomenclature:
- **Frequency Map / Hash Map**: Data structure to count occurrences.
- **Two Pointers**: Technique using two indices to traverse data (often for subarrays).
- **Invariant**: The condition "window contains all chars of t" must hold true before we try to shrink.
"""

from typing import List
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""
            
        # Dictionary which keeps a count of all the unique characters in t.
        dict_t = Counter(t)
        
        # Number of unique characters in t, which need to be present in the desired window.
        required = len(dict_t)
        
        # Filter all the characters from s into a new list along with their index.
        # The filtering criteria is that the character should be present in t.
        # This is an optional optimization but helps visualize focusing only on relevant chars.
        # However, for generic implementation, we just iterate s directly.
        
        # 'l, r' denote the starting and ending indices of the window.
        l, r = 0, 0
        
        # `formed` is used to keep track of how many unique characters in t
        # are present in the current window in its desired frequency.
        # e.g., if t="AABC" then 'A' must appear twice. 'B' once, 'C' once.
        # satisfying 'A' (count >= 2) increments formed by 1.
        formed = 0
        
        # Dictionary which keeps a count of all the unique characters in the current window.
        window_counts = {}
        
        # ans tuple of the form (window length, left, right)
        # Initialize with infinity length
        ans = float("inf"), None, None
        
        while r < len(s):
            # Add character from the right to the window
            character = s[r]
            window_counts[character] = window_counts.get(character, 0) + 1
            
            # If the frequency of the current character added equals to the desired count in t
            # then increment the formed count by 1.
            # CAUTION: Only increment formed when it EXACTLY matches the requirement.
            # If we need 2 'A's and we now have 3 'A's, we don't increment formed again.
            # [PITFALL] Only increment formed when it EXACTLY matches the requirement.
            # If we need 2 'A's and we now have 3 'A's, we don't increment formed again.
            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1
                
            # Try and contract the window till the point where it ceases to be 'desirable'.
            while l <= r and formed == required:
                character = s[l]
                
                # Save the smallest window until now.
                if r - l + 1 < ans[0]:
                    ans = (r - l + 1, l, r)
                    
                # The character at the position pointed by the `left` pointer is no longer a part of the window.
                window_counts[character] -= 1
                
                # Check if removing this char breaks the "valid window" property
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1
                    
                # Move the left pointer ahead, this would help to look for a new window.
                l += 1    
                
            # Keep expanding the window once we are done contracting.
            r += 1
            
        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    s = "ADOBECODEBANC"
    t = "ABC"
    print(f"Test 1: {solver.minWindow(s, t)} (Expected: 'BANC')")
    
    # Test 2
    s = "a"
    t = "a"
    print(f"Test 2: {solver.minWindow(s, t)} (Expected: 'a')")
    
    # Test 3
    s = "a"
    t = "aa"
    print(f"Test 3: {solver.minWindow(s, t)} (Expected: '')")
