
"""
PROBLEM: Alien Dictionary
DIFFICULTY: Hard
TIME LIMIT: 35 Minutes

VISUAL EXPLANATIONS:
- NeetCode (DFS & BFS): https://www.youtube.com/watch?v=6kTZYvNNyps
- Take U Forward (Kahn's Algorithm): https://www.youtube.com/watch?v=U3N_je7tWAs
- Tech Dose (Topological Sort): https://www.youtube.com/watch?v=RIrTuf4DfYE

There is a new alien language that uses the English alphabet. However, the order among the letters is unknown to you.

You are given a list of strings `words` from the alien language's dictionary, where the strings in `words` 
are sorted lexicographically by the rules of this new language.

Return a string of the unique letters in the new alien language sorted in lexicographically increasing order 
by the new language's rules. If there is no solution, return "". If there are multiple solutions, return any of them.

Example 1:
Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"

Example 2:
Input: words = ["z","x"]
Output: "zx"

Example 3:
Input: words = ["z","x","z"]
Output: ""
Explanation: The order is invalid, so return "".

Constraints:
- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of only lowercase English letters.

APPROACH: Topological Sort (Kahn's Algorithm or DFS)
---------------------------------------------------
This is a classic graph problem. The precedence rules (character 'a' comes before 'b') form a Directed Acyclic Graph (DAG).
We need to find a linear ordering of nodes such that for every directed edge from u to v, node u comes before v in the ordering. This is exactly what **Topological Sorting** does.

Algorithm (Kahn's Algorithm - BFS):
1. **Build the Graph**:
   - Create an adjacency list `adj` where `adj[u]` contains all characters `v` that come *immediately after* `u`.
   - Compute `in_degree` for every unique character. `in_degree[v]` is the number of characters that must precede `v`.
   - Iterate through adjacent words in the input list. The FIRST differing character determines the order.
     - E.g., "wrt" vs "wrf" -> 't' comes before 'f'. Add edge t->f.
     - **Edge Case**: If "abc" comes before "ab", this is invalid in any dictionary (prefix must suffice). Return "".

2. **Initialize Queue**:
   - Add all nodes with `in_degree == 0` to a queue. These are characters with no prerequisites.

3. **Process Queue (BFS)**:
   - While queue is not empty:
     - Pop `u`. Add `u` to result.
     - For each neighbor `v` of `u`:
       - Decrement `in_degree[v]`.
       - If `in_degree[v]` becomes 0, push `v` to queue.

4. **Cycle Detection**:
   - If the result contains fewer characters than the total unique characters, it means there is a cycle (dependency loop like a < b < a). Return "".

Time Complexity: O(C)
- C is the total length of all words in the input list.
- We iterate through all words to build the graph (O(C)).
- V is number of unique characters (at most 26), E is edges (at most 26^2).
- Topo sort takes O(V + E). Since V and E are small constants, O(C) dominates.

Space Complexity: O(1) or O(U + min(U^2, N))
- We store the graph and degrees for U unique characters (at most 26).
- So O(1) effectively since alphabet size is fixed.
"""

from typing import List

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        # Step 0: Create data structures
        # Adjacency list: Initialize a adjacency list initially with just all the unique characters found in the words
        # Eventually we will Map each character to a set of characters that come AFTER it.
        adj = {c: set() for w in words for c in w}


        # In-degree count: Initialize a in-degree count initially with just all the unique characters found in the words
        # Eventually we will Map each character to the number of characters that come BEFORE it.
        in_degree = {c: 0 for c in adj}

        # Step 1: Build the Graph
        # We iterate through the sorted list of words and compare adjacent pairs.
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i+1]
            min_len = min(len(w1), len(w2))
            
            # Edge Case: Prefix Order Verification
            # If w2 is a prefix of w1 (e.g., ["apple", "app"]), this is invalid.
            # In a dictionary, the shorter prefix ("app") must always come BEFORE the longer word ("apple").
            if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
                # [PITFALL] Edge Case: "abc" before "ab" is invalid in a dictionary.
                # If the longer word is first, and it's a prefix of the later word, order is impossible.
                return ""
            
            # Find the first character difference to determine relative order.
            for j in range(min_len):
                if w1[j] != w2[j]:
                    char_out = w1[j]  # The character that comes first (source)
                    char_in = w2[j]   # The character that comes after (destination)
                    
                    # Add edge: char_out -> char_in
                    # This means char_out must come before char_in.
                    # We only add the edge if it doesn't already exist to avoid redundant processing.
                    if char_in not in adj[char_out]:
                        adj[char_out].add(char_in)
                        in_degree[char_in] += 1
                    
                    # CRITICAL: We only care about the FIRST difference.
                    # Subsequent characters do NOT imply order because the words are already sorted by this index.
                    break

        # Step 2: Kahn's Algorithm (Topological Sort via BFS)
        # Initialize queue with all characters that have NO incoming edges (in_degree == 0).
        # These characters can be the start of our alien alphabet.
        from collections import deque
        queue = deque([c for c in in_degree if in_degree[c] == 0])
        result = []
        
        while queue:
            char = queue.popleft()
            result.append(char)
            
            # "Remove" this character from the graph:
            # For each neighbor, decrement its in-degree since its prerequisite (char) is processed.
            for neighbor in adj[char]:
                in_degree[neighbor] -= 1
                # If a neighbor now has 0 incoming edges, it's free to be added to the queue.
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Step 3: Cycle Detection
        # If the result length is less than the total unique characters, it means there was a cycle.
        # Characters in a cycle (e.g., a->b->a) never reach in_degree == 0, so they are never added to result.
        if len(result) < len(in_degree):
            # [PITFALL] Cycle Detection.
            # If the result contains fewer characters than the total unique characters, 
            # it means some nodes were never added to the queue (incoming edges never became 0).
            # This implies a cycle exists (e.g., a < b < a).
            return ""
            
        return "".join(result)

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    words1 = ["wrt","wrf","er","ett","rftt"]
    # Possible valid outputs: "wertf"
    print(f"Test 1: {solver.alienOrder(words1)}")
    
    # Test 2
    words2 = ["z","x"]
    print(f"Test 2: {solver.alienOrder(words2)}")
    
    # Test 3 (Invalid)
    words3 = ["z","x","z"]
    print(f"Test 3: {solver.alienOrder(words3)}")
