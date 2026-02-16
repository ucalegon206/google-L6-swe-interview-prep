import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _08_word_search_ii import Solution

class TestWordSearchII:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
        # Output: ["eat","oath"]
        board = [
            ["o","a","a","n"],
            ["e","t","a","e"],
            ["i","h","k","r"],
            ["i","f","l","v"]
        ]
        words = ["oath","pea","eat","rain"]
        result = self.solver.findWords(board, words)
        expected = {"eat", "oath"}
        assert set(result) == expected

    def test_example_2_no_match(self):
        # Input: board = [["a","b"],["c","d"]], words = ["abcb"]
        # Output: []
        board = [["a","b"],["c","d"]]
        words = ["abcb"]
        result = self.solver.findWords(board, words)
        assert result == []

    def test_empty_board(self):
        board = []
        words = ["oath"]
        result = self.solver.findWords(board, words)
        assert result == []

    def test_word_contains_same_letter_twice_reuse_forbidden(self):
        # board: ["a", "a"]
        # words: ["aaa"] -> reuse forbidden, can only make "aa"
        board = [["a", "a"]]
        words = ["aaa"]
        result = self.solver.findWords(board, words)
        assert result == []
        
        # words: ["aa"] -> possible
        words = ["aa"]
        result = self.solver.findWords(board, words)
        assert set(result) == {"aa"}

    def test_multiple_occurrences(self):
        # board can form "oath" starting at two places, should result unique "oath" once
        # o a
        # t h
        # o a
        board = [
            ["o", "a"],
            ["t", "h"],
            ["o", "a"]
        ]
        words = ["oath"]
        # "oath" can be: (0,0)->(0,1)->(1,0)->(1,1). Yes.
        # also (2,0)->(2,1)... wait t is at (1,0). h at (1,1).
        # (2,0)='o', (2,1)='a'. neighbors of 'a' at (2,1) are (1,1)='h', (2,0)='o'.
        # oath needs o->a->t->h.
        
        # Path 1: (0,0)o -> (0,1)a -> (1,0)t -> (1,1)h. Valid.
        # Path 2: (2,0)o -> (2,1)a -> ... needs 't'. (1,1) is 'h'. (2,0) is 'o'. 
        # neighbors of (2,1) are (2,0), (1,1). 't' is at (1,0). (2,1) is not adj to (1,0).
        # So only 1 path. 
        
        # Let's simple duplicate:
        board = [["a", "a"]]
        words = ["a"]
        result = self.solver.findWords(board, words)
        assert result == ["a"]

    def test_prefix_is_also_a_word(self):
        # words = ["oath", "oat"]
        board = [
            ["o","a","t","h"]
        ]
        words = ["oath", "oat"]
        result = self.solver.findWords(board, words)
        assert set(result) == {"oath", "oat"}

    def test_all_matches(self):
        # board 2x2: a b
        #            c d
        # words: [ab, ac, bd, cd]
        board = [["a", "b"], ["c", "d"]]
        words = ["ab", "ac", "bd", "cd", "db", "ca"]
        result = self.solver.findWords(board, words)
        expected = {"ab", "ac", "bd", "cd", "db", "ca"}
        assert set(result) == expected
