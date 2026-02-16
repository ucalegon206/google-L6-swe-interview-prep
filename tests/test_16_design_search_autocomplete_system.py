import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _16_design_search_autocomplete_system import AutocompleteSystem

class TestAutocompleteSystem:
    def test_example_1_standard(self):
        # sentences = ["i love you", "island", "ironman", "i love leetcode"]
        # times = [5, 3, 2, 2]
        sentences = ["i love you", "island", "ironman", "i love leetcode"]
        times = [5, 3, 2, 2]
        system = AutocompleteSystem(sentences, times)
        
        # input('i')
        # Expected: ["i love you", "island", "i love leetcode"]
        # "i love you" (5), "island" (3), "i love leetcode" (2), "ironman" (2)
        # "i love leetcode" vs "ironman": ' ' (32) < 'r' (114) -> "i love leetcode" first.
        assert system.input('i') == ["i love you", "island", "i love leetcode"]
        
        # input(' ') -> "i "
        # Candidates: "i love you", "i love leetcode"
        assert system.input(' ') == ["i love you", "i love leetcode"]
        
        # input('a') -> "i a"
        # Candidates: None
        assert system.input('a') == []
        
        # input('#') -> Finish "i a"
        assert system.input('#') == []
        
        # Now "i a" is in history with count 1.
        
        # input('i') again
        # Candidates:
        # "i love you" (5)
        # "island" (3)
        # "ironman" (2)
        # "i love leetcode" (2)
        # "i a" (1)
        # Top 3 still same.
        assert system.input('i') == ["i love you", "island", "i love leetcode"]
        
        # input(' ') -> "i "
        # Candidates: "i love you", "i love leetcode", "i a"
        assert system.input(' ') == ["i love you", "i love leetcode", "i a"]

    def test_hot_degree_sorting(self):
        sentences = ["a", "b", "c"]
        times = [1, 2, 3]
        system = AutocompleteSystem(sentences, times)
        
        # input('a') -> only matches "a" if prefix matches? No, inputs start fresh.
        # But wait, we initialized with "a", "b", "c".
        # If I type 'a', it matches "a".
        # If I type 'b', matches "b".
        assert system.input('a') == ["a"]
        system.input('#') # finish 'a', count 'a' becomes 2
        
        # Let's type 'd' to start new.
        # Wait, AutocompleteSystem maintains state. We must reset or use new instance or rely on '#' clearing.
        
    def test_ascii_sorting(self):
        # "a", "b", "c" all count 1.
        sentences = ["a", "b", "c"]
        times = [1, 1, 1]
        system = AutocompleteSystem(sentences, times)
        
        # This test is tricky because we need a common prefix to compare them.
        # Let's use "abc", "abd", "abe" with count 1
        sentences = ["abc", "abd", "abe"]
        times = [1, 1, 1]
        system = AutocompleteSystem(sentences, times)
        
        assert system.input('a') == ["abc", "abd", "abe"]
        system.input('#')

    def test_new_sentence_tracking(self):
        system = AutocompleteSystem([], [])
        
        # Type "abc"
        assert system.input('a') == []
        assert system.input('b') == []
        assert system.input('c') == []
        assert system.input('#') == [] # "abc" saved count 1
        
        # Type "a"
        assert system.input('a') == ["abc"]
        
        # Type "abc#" again -> count 2
        system.input('b') # cur "ab"
        system.input('c') # cur "abc"
        system.input('#')
        
        # Type "a"
        assert system.input('a') == ["abc"]

    def test_empty_input(self):
        # What if input is just '#'?
        system = AutocompleteSystem([], [])
        assert system.input('#') == [] # Saves empty string? Or invalid?
        # Problem says "at least one word". Assuming valid input.

    def test_special_characters(self):
        # "i love you" has spaces.
        pass
