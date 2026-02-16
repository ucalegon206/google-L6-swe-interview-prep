"""
PROBLEM: Remove Invalid Parentheses
DIFFICULTY: Hard
TIME LIMIT: 50 Minutes

VISUAL EXPLANATIONS:
- NeetCode (BFS): https://www.youtube.com/watch?v=3eU0MAus0h8
- Tech Dose (Backtracking & BFS): https://www.youtube.com/watch?v=CbdoEz5peTE
- HappyGirlZT (Explanation): https://www.youtube.com/watch?v=2k_27C-P7Kg

Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.

Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.

Example 1:
Input: s = "()())()"
Output: ["(())()","()()()"]

Example 2:
Input: s = "(a)())()"
Output: ["(a())()","(a)()()"]

Example 3:
Input: s = ")("
Output: [""]

Constraints:
- 1 <= s.length <= 25
- s consists of lowercase English letters and parentheses '(' and ')'.
- There will be at most 20 parentheses in s.

APPROACH: Breadth-First Search (BFS)
------------------------------------
We are asked for the **minimum** number of removals.
This suggests a shortest-path problem on a graph where:
- Each node is a string state.
- Each edge is the removal of ONE parenthesis.
- The starting node is the input string `s`.
- The target nodes are any valid strings.

Algorithm:
1. Initialize a `queue` with the set {s} (using a set avoids duplicate states in the same level).
2. Initialize a `visited` set to track all processed strings.
3. While queue is not empty:
   - Check if any string in the current level is Valid.
     - If yes, filter ALL valid strings in this level and return them. (Because BFS guarantees minimal removals, the first level with solutions is the optimal level).
   - If no valid strings found in this level, generate the NEXT level:
     - For each string in current level:
       - Try removing valid characters (only '(' or ')') one by one.
       - Add resulting string to next level set if not visited.
   - Update `visited` with the items in the queue.
   - Move to next level.

Optimization:
- Using sets for levels automatically handles duplicates (e.g., removing different '(' might result in same string).
- We prune the search as soon as we find the first valid layer.

Industry Nomenclature:
- **BFS (Breadth-First Search)**: Algorithm for traversing tree or graph structures level by level.
- **State Space Search**: Exploring all possible configurations to find a goal state.
- **Pruning**: We prune the search as soon as we find the first valid layer.
"""

from typing import List
from collections import deque

class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        def isValid(string):
            count = 0
            for char in string:
                if char == '(':
                    count += 1
                elif char == ')':
                    count -= 1
                
                # If count goes negative, we have a closing parenthesis without a matching open one.
                if count < 0:
                    return False
            return count == 0

        # Queue for BFS and visited set
        queue = deque([s])
        visited = {s}
        found = False
        res = []

        while queue:
            # We process level by level
            # In Python, we can just process the queue as is, but we need to know when a level ends
            # to stop if we found a solution.
            
            # Since 'queue' changes size as we append, we snapshot current string count?
            # Or simpler:
            #   If we find a valid string in the *current* extracted item, 
            #   we know that *this level* is the target level.
            #   So we set 'found = True'. We continue to process the rest of the queue items 
            #   (which are at the same level) to find ALL solutions, but we DO NOT add their children to queue.
            
            curr = queue.popleft()
            
            if isValid(curr):
                res.append(curr)
                found = True
            
            # If we already found a valid string at this level (or previous processed node in same level),
            # we should NOT generate further children (next level would be n+1 removals).
            if found:
                continue
            
            # Generate next states
            for i in range(len(curr)):
                # We only remove parentheses
                if curr[i] not in ('(', ')'):
                    continue
                
                # Create optimization: Skip duplicates in the generated string
                # e.g. "((...)" -> removing first '(' vs second '(' might result in same string if adjacent.
                # Actually, duplicate strings are handled by `visited` set, so we don't need complex skipping logic here.
                
                next_str = curr[:i] + curr[i+1:]
                
                if next_str not in visited:
                    visited.add(next_str)
                    queue.append(next_str)
            
            # CRITICAL LOOP FIX:
            # The standard BFS loop above has a bug.
            # If queue has [A, B] (level 1).
            # We pop A. Invalid. We push A's children (Level 2). Queue is now [B, A_child1...].
            # We pop B. Valid! found=True.
            # But we already pushed A's children (Level 2) into the queue.
            # We will process B, find it is valid. Then next iteration we pop A_child1. 
            # `found` is True, so we don't generate children for A_child1, but A_child1 is definitely NOT minimal if B was valid (Level 1 vs Level 2).
            #
            # CORRECTION: We must process the ENTIRE level before moving to the next level.
        
        # Correct BFS Implementation using explicit levels
        queue = {s} # Use a set for the current level to automatically handle duplicates
        visited = set()
        
        while queue:
            # Check validity of all strings in this level
            valid_strings = [x for x in queue if isValid(x)]
            
            if valid_strings:
                # [PITFALL] Return immediately after the first valid level.
                # Since BFS guarantees shortest path (minimum removals),
                # the first level that contains ANY valid string contains ALL optimal solutions.
                return valid_strings
            
            # If no valid strings found, generate next level
            next_level = set()
            for curr in queue:
                for i in range(len(curr)):
                    if curr[i] in ('(', ')'):
                        next_str = curr[:i] + curr[i+1:]
                        if next_str not in visited:
                            next_level.add(next_str)
                            # visited.add(next_str) # Defer adding to visited until next level start? 
                            # Actually, efficient to just track global visited
            
            # Update visited
            visited.update(queue)
            queue = next_level
            
        return [""]

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    s1 = "()())()"
    print(f"Test 1: {solver.removeInvalidParentheses(s1)} (Expected: ['(())()', '()()()'])")
    
    # Test 2
    s2 = "(a)())()"
    print(f"Test 2: {solver.removeInvalidParentheses(s2)} (Expected: ['(a())()', '(a)()()'])")
    
    # Test 3
    s3 = ")("
    print(f"Test 3: {solver.removeInvalidParentheses(s3)} (Expected: [''])")
