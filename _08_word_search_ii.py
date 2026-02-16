"""
PROBLEM: Word Search II
DIFFICULTY: Hard
TIME LIMIT: 45 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Trie + DFS): https://www.youtube.com/watch?v=asbcE9mZz_U
- Tech Dose (Backtracking + Trie): https://www.youtube.com/watch?v=hTrrrp03yMY
- CodeLucky (Explained): https://www.youtube.com/watch?v=3iBbL-Vj61M

Given an m x n board of characters and a list of strings `words`, return all words on the board.

Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. 
The same letter cell may not be used more than once in a word.

Example 1:
Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]

Example 2:
Input: board = [["a","b"],["c","d"]], words = ["abcb"]
Output: []

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 12
- 1 <= words.length <= 3 * 10^4
- 1 <= words[i].length <= 10

APPROACH: Trie (Prefix Tree) + DFS (Backtracking)
-------------------------------------------------
A naive approach would be to run DFS for *every word* on *every cell* of the board. 
If there are K words, M*N cells, and average word length L, complexity is O(K * M * N * 3^L).
Given K can be 30,000, checking every word independently is too slow.

Optimization:
Instead of searching for words one by one, we search for ALL words simultaneously.
How? We store all candidate `words` in a **Trie (Prefix Tree)**.
Then, we start a DFS from every cell on the board. As we traverse the board, we traverse the Trie in parallel.
If the current path exists in the Trie, we keep going. If it doesn't, we prune the search immediately.

Key Operations:
1. **Build Trie**: Insert all `words` into a Trie. Mark the end of a word nodes.
2. **DFS**: 
   - Check if current board char matches a child of current Trie node.
   - If yes, move to that child.
   - If that child marks the end of a word, add it to results.
   - Mark board cell as visited (temporary mutation).
   - Recurse neighbors.
   - Backtrack (restore board cell).
   
Optimization Tip (Trie Pruning):
- Once a word is found, we can remove it from the Trie (or mark it as found) to avoid duplicate entries and speed up finding remaining words.

Industry Nomenclature:
- **Trie / Prefix Tree**: Specialized tree for searching strings.
- **Pruning**: Cutting off search branches that cannot possibly lead to a solution.
- **Backtracking**: Algorithmic-technique for solving problems recursively by trying to build a solution incrementally.
"""

from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store the actual word at the end node for easy retrieval

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        if not board or not board[0]:
            return []

        # Step 1: Build the Trie
        root = TrieNode()
        for w in words:
            node = root
            for char in w:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = w  # Mark end of word
        
        ROWS, COLS = len(board), len(board[0])
        res = set() # Use set to avoid duplicates easily
        
        def dfs(r, c, node):
            # Base logic implicitly handled: we only recurse if char is in node.children
            
            char = board[r][c]
            curr_node = node.children[char]
            
            # Check if we found a word
            if curr_node.word:
                res.add(curr_node.word)
                # Optimization: Mark word as None so we don't add it again (deduplication)
                # Ideally, we should prune the Trie here (remove leaf nodes), but that is complex to implement in interview.
                # Just setting word to None helps avoid duplicate adds for same word found via differnet paths.
                # [PITFALL] Deduplication.
                # Since multiple paths on the board can form the same word, 
                # we must ensure we don't add duplicates. 
                # Marking word=None is a simple way to "consume" it. 
                curr_node.word = None
                
            # Mark as visited
            board[r][c] = '#'
            
            # Explore neighbors
            row_offsets = [0, 0, 1, -1]
            col_offsets = [1, -1, 0, 0]
            
            for i in range(4):
                new_r, new_c = r + row_offsets[i], c + col_offsets[i]
                if (0 <= new_r < ROWS and 0 <= new_c < COLS and 
                    board[new_r][new_c] in curr_node.children): # ONLY recurse if next char is in Trie
                    dfs(new_r, new_c, curr_node)
            
            # Backtrack
            board[r][c] = char
        
        # Step 2: Run DFS from every cell
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] in root.children:
                    dfs(r, c, root)
                    
        return list(res)

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    board = [
        ["o","a","a","n"],
        ["e","t","a","e"],
        ["i","h","k","r"],
        ["i","f","l","v"]
    ]
    words = ["oath","pea","eat","rain"]
    print(f"Test 1: {solver.findWords(board, words)} (Expected: ['eat', 'oath'] order may vary)")
    
    # Test 2
    board = [["a","b"],["c","d"]]
    words = ["abcb"]
    print(f"Test 2: {solver.findWords(board, words)} (Expected: [])")
