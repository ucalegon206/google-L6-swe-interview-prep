import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _04_word_ladder_ii import Solution

class TestWordLadderII:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
        # Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
        beginWord = "hit"
        endWord = "cog"
        wordList = ["hot","dot","dog","lot","log","cog"]
        result = self.solver.findLadders(beginWord, endWord, wordList)
        
        expected = [
            ["hit","hot","dot","dog","cog"],
            ["hit","hot","lot","log","cog"]
        ]
        
        # Sort inner lists and outer list for comparison since order doesn't matter
        # Actually, path order matters, but order of paths in list doesn't.
        # Paths themselves are ordered sequences.
        
        assert len(result) == len(expected)
        # Convert to tuple for set comparison to ignore order of paths
        result_set = set(tuple(path) for path in result)
        expected_set = set(tuple(path) for path in expected)
        assert result_set == expected_set

    def test_example_2_no_path(self):
        # Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
        # Output: [] (endWord not in wordList)
        beginWord = "hit"
        endWord = "cog"
        wordList = ["hot","dot","dog","lot","log"]
        result = self.solver.findLadders(beginWord, endWord, wordList)
        assert result == []

    def test_end_word_not_reachable(self):
        # Input: beginWord = "hit", endWord = "pog", wordList = ["hot","dot","dog","lot","log","cog"]
        # "pog" not in list
        beginWord = "hit"
        endWord = "pog"
        wordList = ["hot","dot","dog","lot","log","cog"]
        result = self.solver.findLadders(beginWord, endWord, wordList)
        assert result == []

    def test_single_transformation(self):
        # hit -> hot
        beginWord = "hit"
        endWord = "hot"
        wordList = ["hot", "dot", "dog"]
        result = self.solver.findLadders(beginWord, endWord, wordList)
        expected = [["hit", "hot"]]
        assert result == expected

    def test_disconnected_graph(self):
        # a -> b (no path) -> c
        beginWord = "a"
        endWord = "c"
        wordList = ["b", "c"] # b is dist 1 from a (no), a->b needs ascii adjacent? No, problem says "differs by single letter"
        # a -> b is OK if words are same length.
        # 'a' to 'b' is 1 diff.
        # 'b' to 'c' is 1 diff.
        # So a->b->c is valid path.
        
        # Let's try truly disconnected: "aaa" -> "bbb" with empty list
        beginWord = "aaa"
        endWord = "bbb"
        wordList = ["ccc", "ddd", "bbb"]
        # aaa -> ccc (3 diffs) - impossible
        result = self.solver.findLadders(beginWord, endWord, wordList)
        assert result == []

    def test_multiple_paths_same_length(self):
        # start: "red", end: "tax", paths: red->rex->tex->tax, red->ted->tex->tax, red->ted->tad->tax
        # red -> ted (1 change)
        # red -> rex (1 change)
        # ted -> tex (1 change)
        # ted -> tad (1 change)
        # rex -> tex (1 change)
        # tex -> tax (1 change)
        # tad -> tax (1 change)
        
        beginWord = "red"
        endWord = "tax"
        wordList = ["ted","tex","red","tax","tad","den","rex","pee"]
        
        # Paths length 4:
        # red -> ted -> tex -> tax
        # red -> ted -> tad -> tax
        # red -> rex -> tex -> tax
        
        result = self.solver.findLadders(beginWord, endWord, wordList)
        
        expected = [
            ["red","ted","tex","tax"],
            ["red","ted","tad","tax"],
            ["red","rex","tex","tax"]
        ]
        
        result_set = set(tuple(path) for path in result)
        expected_set = set(tuple(path) for path in expected)
        assert result_set == expected_set

    def test_complex_loop_prevention(self):
        # Ensure we don't go in circles or reuse words in same path
        beginWord = "hot"
        endWord = "dog"
        wordList = ["hot", "dog", "dot"]
        # hot -> dot -> dog
        result = self.solver.findLadders(beginWord, endWord, wordList)
        expected = [["hot", "dot", "dog"]]
        assert result == expected
