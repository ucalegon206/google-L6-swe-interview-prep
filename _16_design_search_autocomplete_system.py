"""
PROBLEM: Design Search Autocomplete System
DIFFICULTY: Hard
TIME LIMIT: 50 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Trie + Heap): https://www.youtube.com/watch?v=D4T2N0yAr20
- Happy Girl ZT (Explanation): https://www.youtube.com/watch?v=PbZ51tE5Nls
- Knowledge Center (Design): https://www.youtube.com/watch?v=nx1qceR0WjE

Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character '#'). 
For each character they type except '#', you need to return the top 3 historical hot sentences that have prefix the same as the part of sentence already typed. 
Here are the specific rules:

1. The hot degree for a sentence is defined as the number of times a user typed this exact sentence before.
2. The returned top 3 hot sentences should be sorted by hot degree (The first is the hottest one). 
   If several sentences have the same degree of hotness, you need to use ASCII-code order (smaller one appears first).
3. If less than 3 hot sentences exist, return as many as you can.
4. When the input is a special character, it means the sentence ends, and in this case, you need to return an empty list.
5. Your job is to implement the following functions:

The constructor function:
`AutocompleteSystem(String[] sentences, int[] times)`: This is the constructor. The input is historical data. 
`sentences` is a string array consists of previously typed sentences. `times` is the corresponding times a sentence has been typed. 
Your system should record these historical data.

`List<String> input(char c)`: The input c is the next character typed by the user. 
The character will only be lower-case letters ('a' to 'z'), blank space (' '), or a special character ('#'). 
Also, the previously typed sentence should be recorded in your system. 
The output will be the top 3 historical hot sentences that have prefix the same as the part of sentence already typed.

Example:
Operation: AutocompleteSystem(["i love you", "island", "ironman", "i love leetcode"], [5, 3, 2, 2])
The system have these sentences with the following times:
"i love you" : 5 times
"island" : 3 times
"ironman" : 2 times
"i love leetcode" : 2 times

Now, the user begins another search:

Operation: input('i')
Output: ["i love you", "island", "i love leetcode"]
Explanation:
There are four sentences that have prefix "i". Among them, "ironman" and "i love leetcode" have same hot degree. 
Since ' ' has ASCII code 32 and 'r' has ASCII code 114, "i love leetcode" should be in front of "ironman". 
Also we only need to output top 3 hot sentences, so "ironman" will be ignored.

Operation: input(' ')
Output: ["i love you", "i love leetcode"]
Explanation:
There are only two sentences that have prefix "i ".

Operation: input('a')
Output: []
Explanation:
There are no sentences that have prefix "i a".

Operation: input('#')
Output: []
Explanation:
The user finished the input, the sentence "i a" should be saved as a historical sentence in system. 
And the following input will be counted as a new search.

Constraints:
- The string sentences[i] consists of lowercase English letters and spaces.
- 1 <= sentences.length <= 100
- 1 <= sentences[i].length <= 100
- 1 <= times[i] <= 50
- c is a lowercase English letter, a space ' ', or '#'.
- At most 5000 calls will be made to input.

APPROACH: Trie with Cached Hot List (or On-the-fly Search)
----------------------------------------------------------
Since we need prefix matches, a **Trie** is the standard choice.

Data Structures:
1. **TrieNode**: 
   - `children`: Dict[char, TrieNode]
   - `sentences`: Dictionary `{sentence: count}` for ALL sentences that pass through this node (i.e., this node is a prefix of them).

Algorithm:
1. **Initialization**: Build the Trie. For each sentence, traverse the Trie. At *every* node along the path, update the `sentences` dictionary with the sentence's count.
   (Why store at every node? So that when we are at that node during input, we have immediate access to all valid sentences and their counts to sort them).
   
2. **Input(c)**:
   - If `#`: This marks the end of a sentence.
     - Update the Trie with the new full sentence.
     - Increment its count in the `sentences` map of every node along its path.
     - Reset current tracking.
     - Return empty list.
   - If char:
     - Move to child node.
     - If no child exists, current prefix has no matches. Return [].
     - If child exists, retrieve all sentences from `child.sentences`.
     - **Sort** the sentences:
       - Primary Key: Frequency (Descending) -> Use `-freq`.
       - Secondary Key: ASCII string order (Ascending) -> Use `sentence`.
     - Return Top 3.

Optimization Note:
- Storing the full dictionary of sentences at every node consumes memory. 
- A more optimized "System Design" approach would be to store only the *Top 3* at each node.
- However, given the constraints (N=100 sentences, length=100), storing the full map is feasible and easier to implement correctly in an interview context.
"""

from typing import List
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = {}
        self.sentences = defaultdict(int) # Maps sentence -> freq for all sentences in this subtree

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = TrieNode()
        self.cur_node = self.root
        self.cur_sentence = []
        
        # Build initial Trie
        for s, t in zip(sentences, times):
            self._add_to_trie(s, t)

    def _add_to_trie(self, sentence, count):
        # Determine the delta to add? No, we need absolute count or additive?
        # The constructor provides initial counts.
        # But for new inputs, we increment count.
        # My approach: TrieNode stores {sentence: count}.
        
        node = self.root
        # We also need to update the counts in the nodes.
        # But wait, if I store *all* sentences in every node on the path, it consumes memory.
        # Given constraints (100 sentences), this is fine.
        
        for char in sentence:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.sentences[sentence] += count # Add count? 
            # Wait, constructor sets initial value. input('#') increments.
            # So _add_to_trie should likely take "count to add" or "absolute count"?
            # Simplest: The dictionary tracks the current count.
        
        # NOTE: logic error in simple accumulation.
        # If I call _add_to_trie("abc", 5), then later _add_to_trie("abc", 1), 
        # the node for 'a' will have "abc": 6. Correct.
        pass

    def input(self, c: str) -> List[str]:
        if c == '#':
            # End of sentence
            sentence = "".join(self.cur_sentence)
            # Add to Trie (increment count by 1)
            self._update_trie(sentence, 1)
            
            # Reset
            self.cur_sentence = []
            self.cur_node = self.root
            return []
        
        # Process character
        self.cur_sentence.append(c)
        if not self.cur_node:
            # We have deviated from known paths
            return []
            
        if c not in self.cur_node.children:
            self.cur_node = None # No path
            return []
            
        self.cur_node = self.cur_node.children[c]
        
        # Get statistics from current node
        # self.cur_node.sentences contains all sentences passing through here with their counts.
        # We need to sort them.
        # Criteria: -count (desc), then sentence (asc)
        
        candidates = []
        for s, freq in self.cur_node.sentences.items():
            # [PITFALL] Sorting Criteria.
            # 1. Hot degree (descending). Use -freq.
            # 2. ASCII order (ascending). Use s.
            # Tuple comparison (-freq, s) handles this naturally.
            candidates.append((-freq, s))
            
        candidates.sort()
        
        # Return top 3
        return [s for freq, s in candidates[:3]]

    def _update_trie(self, sentence, count):
        node = self.root
        for char in sentence:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.sentences[sentence] += count

# Test Cases
if __name__ == "__main__":
    sentences = ["i love you", "island", "ironman", "i love leetcode"]
    times = [5, 3, 2, 2]
    system = AutocompleteSystem(sentences, times)
    
    # Operation: input('i')
    # Expected: ["i love you", "island", "i love leetcode"]
    print(f"Input 'i': {system.input('i')}")
    
    # Operation: input(' ')
    # Expected: ["i love you", "i love leetcode"]
    print(f"Input ' ': {system.input(' ')}")
    
    # Operation: input('a')
    # Expected: []
    print(f"Input 'a': {system.input('a')}")
    
    # Operation: input('#')
    # Expected: [] (updates history)
    print(f"Input '#': {system.input('#')}")
    
    # Now "i a" has count 1.
