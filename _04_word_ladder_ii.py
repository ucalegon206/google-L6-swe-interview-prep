"""
PROBLEM: Word Ladder II
DIFFICULTY: Hard
TIME LIMIT: 50 Minutes

VISUAL EXPLANATIONS:
- TECH DOSE (BFS + DFS Explained): https://www.youtube.com/watch?v=mIZJIuMpI2M
- Happy Coding (Detailed Walkthrough): https://www.youtube.com/watch?v=DREVt7pMtrA
- Tushar Roy (Graph Construction): https://www.youtube.com/watch?v=PblfDYmlW87

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words 
beginWord -> s1 -> s2 -> ... -> sk such that:
1. Every adjacent pair of words differs by a single letter.
2. Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
3. sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return ALL the shortest transformation sequences 
from beginWord to endWord, or an empty list if no such sequence exists.

Example 1:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]

Example 2:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: []
Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.

Constraints:
- 1 <= beginWord.length <= 5
- endWord.length == beginWord.length
- 1 <= wordList.length <= 500
- wordList[i].length == beginWord.length
- wordList[i] consists of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.

APPROACH: BFS + DFS (Backtracking)
----------------------------------
This approach splits the problem into two distinct phases to handle the complexity efficiently.

Phase 1: BFS (Breadth-First Search)
- Goal: Find the shortest distance from `beginWord` to `endWord` AND build a directed graph (adjacency list).
- This graph represents the "layers" of the BFS. We only add edges from `wordA` -> `wordB` if `wordB` is in the *next* level of the BFS hierarchy.
- This ensures that when we traverse this graph later, we form ONLY shortest paths.
- Why BFS? BFS is guaranteed to find shortest paths in an unweighted graph.

Phase 2: DFS (Depth-First Search / Backtracking)
- Goal: Reconstruct all paths from `beginWord` to `endWord` using the graph built in Phase 1.
- We start at `beginWord` and recursively visit neighbors in our specific `adj` graph until we reach `endWord`.
- Since our graph only contains "shortest path" edges, any path from start to end in this graph IS a shortest path.

Key Optimization:
- "A-Z" Replacement: Instead of comparing every word against every other word (O(N^2 * L)), we generate all possible neighbors by changing each letter to 'a'-'z' (O(26 * L * L)).
  - Given N=500 and L=5:
  - N^2 * L = 250,000 * 5 = 1,250,000 ops.
  - N * 26 * L * L = 500 * 26 * 5 * 5 = 325,000 ops.
  - For small L, the generation method is significantly faster.

Time Complexity: O(N * 26 * L^2 + P * L)
- BFS Graph Build: O(N * 26 * L^2), where N is number of words, L is word length.
- DFS Reconstruction: O(P * L), where P is the number of shortest paths.
- In worst case, P can be exponential, but constraints (N=500) limit this.

Space Complexity: O(N * L + P * L)
- Adjacency list stores up to N words.
- Recursion stack for DFS.
- Storing all paths.
"""

from typing import List
from collections import deque, defaultdict

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        wordSet = set(wordList)
        if endWord not in wordSet:
            return []
            
        # BFS initialization
        # layer: Stores words in the current level of BFS
        layer = {beginWord}
        # adj: Stores the directed graph of shortest paths: parent -> list of children
        adj = defaultdict(list)
        
        while layer:
            next_layer = set()
            # Remove words in current layer from wordSet to prevent visiting them again in future layers
            # This ensures we don't have cycles and only move forward.
            # (Standard BFS usually marks visited immediately, but for *all* shortest paths, 
            # we might visit the same node from multiple parents in the SAME layer, so we remove AFTER processing the layer).
            for word in layer:
                if word in wordSet:
                    # [PITFALL] We remove words from wordSet only when we start processing the *next* layer, 
                    # OR we can remove them immediately if we track "current level visited".
                    # Better: remove all words in 'layer' from 'wordSet' at the start of the level processing
                    # to prevent finding them again in future levels.
                    # However, we must allow multiple parents in the CURRENT level to reach the same child in NEXT level.
                    wordSet.remove(word)
            
            # Since we removed them, if 'dog' is reached from 'dot' and 'log', it's fine because 
            # 'dog' is in the *next_layer* set, and we process 'dot' and 'log' in the *current* layer.
            # Wait, correcting logic: We must remove words from wordSet that are in the *current* layer 
            # so they aren't visited again. BUT multiple parents in current layer can point to same child.
            # So correct logic: remove 'layer' words from 'wordSet' before processing?
            # actually, standard is: remove all nodes in 'next_layer' from 'wordSet' *after* building next_layer.
            # Let's stick to the level-by-level BFS.
            
            # Proper logic:
            # 1. Identify all valid neighbors for all nodes in current layer.
            # 2. Build adjacency list.
            # 3. populate next_layer.
            # 4. Remove next_layer words from unvisited set.
            
            # To handle the removal correctly:
            # We remove words from wordSet *before* the loop? No. 
            # We remove used words from the global set *after* finishing the current level.
            
            words_in_this_level_visited = set()
            
            for word in layer:
                # Try changing each character to find neighbors
                for i in range(len(word)):
                    original_char = word[i]
                    for char_code in range(ord('a'), ord('z') + 1):
                        c = chr(char_code)
                        if c == original_char:
                            continue
                            
                        new_word = word[:i] + c + word[i+1:]
                        if new_word in wordSet:
                            if new_word not in words_in_this_level_visited:
                                next_layer.add(new_word)
                                words_in_this_level_visited.add(new_word)
                            
                            # Add edge parent -> child
                            adj[word].append(new_word)
                            
            # If we found endWord in this level, we are done building the graph
            if endWord in next_layer:
                break
                
            # Prepare for next iteration
            layer = next_layer
            # Remove visited words from global set so we don't go back to them
            wordSet -= next_layer
            
        # DFS Reconstruction
        res = []
        path = [beginWord]
        
        def backtrack(current_word):
            if current_word == endWord:
                res.append(list(path))
                return
            
            for neighbor in adj[current_word]:
                path.append(neighbor)
                backtrack(neighbor)
                path.pop()
                
        backtrack(beginWord)
        
        # NOTE: The problem asks for shortest paths.
        # If BFS finished without finding endWord, res will be empty, which is correct.
        # However, due to the break condition, we might have partial paths if endWord wasn't found.
        # But if endWord wasn't in next_layer, we continued.
        # If loop finished and we didn't hit 'break', res will be empty.
        
        return res

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log","cog"]
    print(f"Test 1 Output: {solver.findLadders(beginWord, endWord, wordList)}")
    # Expected: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
    
    # Test 2
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log"]
    print(f"Test 2 Output: {solver.findLadders(beginWord, endWord, wordList)}")
    # Expected: []
