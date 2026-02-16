import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _05_alien_dictionary import Solution

class TestAlienDictionary:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: words = ["wrt","wrf","er","ett","rftt"]
        # Output: "wertf"
        words = ["wrt","wrf","er","ett","rftt"]
        result = self.solver.alienOrder(words)
        assert result == "wertf"

    def test_example_2_simple(self):
        # Input: words = ["z","x"]
        # Output: "zx"
        words = ["z","x"]
        result = self.solver.alienOrder(words)
        assert result == "zx"

    def test_example_3_invalid_cycle(self):
        # Input: words = ["z","x","z"]
        # Output: "" (z < x < z impossible)
        words = ["z","x","z"]
        result = self.solver.alienOrder(words)
        assert result == ""
        
    def test_invalid_prefix(self):
        # "abc", "ab" -> invalid because "ab" is prefix of "abc" but comes later
        words = ["abc", "ab"]
        result = self.solver.alienOrder(words)
        assert result == ""

    def test_valid_prefix(self):
        # "ab", "abc" -> valid, but provides NO info about 'c' related to anything else
        words = ["ab", "abc"]
        # order could be "abc" or "cab" or "cba" depending on impl, but 'a' must be before 'b'. 
        # Actually strictly speaking, ab vs abc gives no edge. 
        # But 'a' and 'b' and 'c' exist.
        # Since no edges, usually output is just arbitrary topo sort (often alphabetical if queue sorted, or insertion order).
        result = self.solver.alienOrder(words)
        # Any string containing a, b, c is valid as long as no contradictions.
        assert len(result) == 3
        assert set(result) == set("abc")

    def test_disconnected_components(self):
        # ["a", "b", "ca", "cc"]
        # a < b
        # a < c (from ca vs cc? No, distinct words)
        # Pairs:
        # (a, b) -> a < b
        # (b, ca) -> b < c
        # (ca, cc) -> a < c
        # So a < b < c.
        words = ["a", "b", "ca", "cc"]
        result = self.solver.alienOrder(words)
        assert result == "abc"

    def test_single_word(self):
        # "z" -> "z"
        words = ["z"]
        result = self.solver.alienOrder(words)
        assert result == "z"

    def test_no_edges_just_chars(self):
        # ["z", "z"] -> valid, unique chars is "z"
        words = ["z", "z"]
        result = self.solver.alienOrder(words)
        assert result == "z"

    def test_complex_cycle(self):
        # a < b, b < c, c < a
        words = ["a", "b", "c", "a"]
        result = self.solver.alienOrder(words)
        assert result == ""
