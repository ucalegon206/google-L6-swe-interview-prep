"""
PROBLEM: Regular Expression Matching
DIFFICULTY: Hard
TIME LIMIT: 30 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Dynamic Programming): https://www.youtube.com/watch?v=l3hda49XcDE
- Tushar Roy (DP - Top Down & Bottom Up): https://www.youtube.com/watch?v=l3hda49XcDE
- CS Dojo (Recursive & DP): https://www.youtube.com/watch?v=l3hda49XcDE

Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".

Constraints:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.

APPROACH: Dynamic Programming (Top-Down or Bottom-Up)
-----------------------------------------------------
Let dp[i][j] be true if s[i:] matches p[j:].

Base Cases:
1. If p is exhausted (j == len(p)), then s must also be exhausted (i == len(s)).

Recursive Step (comparing s[i] and p[j]):
1. First, check if the first characters match:
   `first_match = (i < len(s) and (p[j] == s[i] or p[j] == '.'))`
   
2. If the next character in pattern is '*' (p[j+1] == '*'):
   We have two choices:
   a. Ignore the '*' and its preceding element (effectively matching 0 times).
      - Recurse on (i, j+2)
   b. Use the '*' to match the current character in s (only if `first_match` is true).
      - Recurse on (i+1, j) -- note we keep j at the '*' to allow matching MORE instances of the preceding element.
      
3. Else (no '*'):
   - Simply proceed if `first_match` is true.
   - Recurse on (i+1, j+1)

We use memoization to store results of (i, j) to avoid re-computation.
Time Complexity: O(T * P) where T is length of string and P is length of pattern.
Space Complexity: O(T * P) for memoization table.
"""

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        memo = {}
        
        def dp(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Base Case: Pattern exhausted
            if j == len(p):
                result = i == len(s)
            else:
                # Check if current characters match
                first_match = i < len(s) and p[j] in {s[i], '.'}
                
                # Check for '*' wildcard
                if j + 1 < len(p) and p[j+1] == '*':
                    # Two options:
                    # 1. Skip the '*' (match 0 times) -> dp(i, j+2)
                    # 2. Use the '*' (match 1+ times) -> dp(i+1, j) if first_match is true
                    # [PITFALL] The '*' Logic.
                    # Option 1: Match ZERO occurrences. Skip pattern char and '*' -> j+2.
                    # Option 2: Match ONE or MORE. Consume string char (i+1) but KEEP pattern (j) to allow more matches.
                    #           Only valid if the current chars match.
                    result = dp(i, j+2) or (first_match and dp(i+1, j))
                else:
                    # Standard matching
                    result = first_match and dp(i+1, j+1)
            
            memo[(i, j)] = result
            return result
            
        return dp(0, 0)

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    s1 = "aa"
    p1 = "a"
    print(f"Test 1 ('aa', 'a'): {solver.isMatch(s1, p1)} (Expected: False)")
    
    # Test 2
    s2 = "aa"
    p2 = "a*"
    print(f"Test 2 ('aa', 'a*'): {solver.isMatch(s2, p2)} (Expected: True)")
    
    # Test 3
    s3 = "ab"
    p3 = ".*"
    print(f"Test 3 ('ab', '.*'): {solver.isMatch(s3, p3)} (Expected: True)")
    
    # Test 4
    s4 = "aab"
    p4 = "c*a*b"
    print(f"Test 4 ('aab', 'c*a*b'): {solver.isMatch(s4, p4)} (Expected: True)")
    # 'c*' matches 0 'c's. 'a*' matches 2 'a's. 'b' matches 'b'.
    
    # Test 5
    s5 = "mississippi"
    p5 = "mis*is*p*."
    print(f"Test 5 ('mississippi', 'mis*is*p*.'): {solver.isMatch(s5, p5)} (Expected: False)")
