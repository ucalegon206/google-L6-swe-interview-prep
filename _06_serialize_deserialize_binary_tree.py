"""
PROBLEM: Serialize and Deserialize Binary Tree
DIFFICULTY: Hard
TIME LIMIT: 40 Minutes

VISUAL EXPLANATIONS:
- NeetCode (DFS - Preorder): https://www.youtube.com/watch?v=u4JAi2JJhI8
- Tech Dose (Preorder Traversal): https://www.youtube.com/watch?v=jNw1CnHuGyA
- Tushar Roy (Level Order - BFS): https://www.youtube.com/watch?v=vQ059_Q5vU4

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, 
or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. 
You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Example 1:
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]

Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -1000 <= Node.val <= 1000

APPROACH: Preorder Traversal (DFS)
----------------------------------
We need a standard way to traverse the tree that covers every node.
Depth-First Search (DFS) using **Preorder Traversal** (Root -> Left -> Right) is efficient and intuitive for this.

Key Strategy:
1. **Serialization (Tree -> String)**:
   - Traverse the tree in Preorder.
   - For every non-null node, append its value to a list.
   - For every `None` (null) node, append a special marker (e.g., "N" or "#").
   - Join the list with a delimiter (e.g., comma) to form the string.
   - *Why Preorder?* It puts the root first. When we deserialize, we immediately know the first value is the root.

2. **Deserialization (String -> Tree)**:
   - Split the string by the delimiter to get a list of values (tokens).
   - Use an **iterator** (or a queue) to consume these tokens one by one from left to right.
   - Recursive Function `dfs()`:
     - Pop the next token.
     - If token is "N" (null marker), return `None`.
     - Otherwise, create a new `TreeNode(int(token))`.
     - Recursively call `dfs()` to build the `node.left`.
     - Recursively call `dfs()` to build the `node.right`.
     - Return the `node`.
   - The recursion naturally mirrors the Preorder traversal we used for serialization.

Time Complexity: O(N)
- We visit every node exactly once during both serialization and deserialization.

Space Complexity: O(N)
- Recursion stack: O(H) where H is tree height (worst case O(N) for skewed tree).
- Output string/list: O(N) to store values and null markers.
"""

from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        
    def __repr__(self):
        return f"Node({self.val})"

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        # Use a list to build the string efficiently (O(1) append typically).
        # In Python, string concatenation in a loop can be O(N^2), so list join is preferred.
        output = []
        
        def dfs(node):
            if not node:
                output.append("N") # 'N' represents a null/None node
                return
            
            # Preorder: Add root value, then traverse children
            output.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
            
        dfs(root)
        
        # Join all values with a delimiter (comma) for easy parsing later
        return ",".join(output)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree."""
        # Split the string back into a list of values (tokens)
        vals = data.split(",")
        
        # Use an iterator to consume tokens one by one.
        # An iterator is efficient because it yields the next item without removing from index 0 of a list (which is O(N)).
        # Alternatively, we could use a deque (double-ended queue) and popleft().
        # [PITFALL] Use an iterator!
        # popping from a list `vals.pop(0)` is O(N) operation in Python.
        # Doing this for N nodes makes the algorithm O(N^2).
        # `iter()` or `collections.deque.popleft()` ensures O(1) access, keeping total time O(N).
        self.iter_vals = iter(vals)
        
        def dfs():
            # Get the next token from the iterator
            # next() raises StopIteration if empty, but our logic guarantees valid structure based on serialization
            try:
                val = next(self.iter_vals)
            except StopIteration:
                return None
            
            # Base Case: simpler check
            if val == "N":
                return None
            
            # Create the node
            node = TreeNode(int(val))
            
            # Recursive Step:
            # Since we serialized in Preorder (Root -> Left -> Right),
            # the *next* values in the iterator naturally correspond to the Left subtree.
            node.left = dfs()
            
            # After the left subtree is fully built (hitting 'N's), the iterator
            # positions itself at the start of the Right subtree.
            node.right = dfs()
            
            return node
            
        return dfs()

# Test Cases
if __name__ == "__main__":
    # Helper to print tree (visualization) is hard, let's just verify serialize -> deserialize
    codec = Codec()
    
    # Test 1: [1, 2, 3, null, null, 4, 5]
    #      1
    #     / \
    #    2   3
    #       / \
    #      4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    serialized = codec.serialize(root)
    print(f"Serialized: {serialized}")
    # Expected: 1,2,N,N,3,4,N,N,5,N,N
    
    deserialized = codec.deserialize(serialized)
    # Check if structure is preserved by re-serializing
    reserialized = codec.serialize(deserialized)
    print(f"Reserialized: {reserialized}")
    
    assert serialized == reserialized
    print("Test Passed!")
