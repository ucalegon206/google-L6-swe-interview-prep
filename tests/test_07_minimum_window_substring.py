import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _07_minimum_window_substring import Solution

class TestMinimumWindowSubstring:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: s = "ADOBECODEBANC", t = "ABC"
        # Output: "BANC"
        s = "ADOBECODEBANC"
        t = "ABC"
        # "BANC" contains A, B, C. Length 4.
        # "ADOBEC" contains A, B, C. Length 6.
        result = self.solver.minWindow(s, t)
        assert result == "BANC"

    def test_example_2_single_chars(self):
        # Input: s = "a", t = "a"
        # Output: "a"
        s = "a"
        t = "a"
        result = self.solver.minWindow(s, t)
        assert result == "a"

    def test_example_3_impossible(self):
        # Input: s = "a", t = "aa"
        # Output: ""
        s = "a"
        t = "aa"
        result = self.solver.minWindow(s, t)
        assert result == ""

    def test_substring_at_end(self):
        # s = "ab", t = "b" -> "b"
        s = "ab"
        t = "b"
        result = self.solver.minWindow(s, t)
        assert result == "b"

    def test_substring_at_start(self):
        # s = "abc", t = "a" -> "a"
        s = "abc"
        t = "a"
        result = self.solver.minWindow(s, t)
        assert result == "a"

    def test_exact_match(self):
        s = "abc"
        t = "abc"
        result = self.solver.minWindow(s, t)
        assert result == "abc"

    def test_duplicates_needed(self):
        # s = "aaflslflsldkalskaaa", t = "aaa"
        # first window "aaflslflsldkalska" (contains 3 a's, length long)
        # last window "aaa" is the best
        s = "bbaac"
        t = "aba" # need 2 a's, 1 b
        # "bbaa" -> 2 b's, 2 a's. Valid. Length 4.
        # "baac" -> 1 b, 2 a's. Valid. Length 4.
        # "aac"? No b.
        # result: "bbaa" or "baac"?
        # "bbaa" contains a:2, b:2. t needs a:2, b:1. Valid. Length 4.
        # "baac" contains a:2, b:1. Valid. Length 4.
        # Standard solution returns the first one found or specifically minimum. 
        # If lengths equal, problem statement "The testcases will be generated such that the answer is unique" only applies to LC.
        # Our code: `if r - l + 1 < ans[0]` -> strictly smaller. So first one found stays if equal length.
        
        result = self.solver.minWindow(s, t)
        # s[0:4] = "bbaa"
        # s[1:5] = "baac"
        # Both length 4.
        # First valid window found usually.
        # Let's verify manually:
        # r expands.
        # r=0, b. window={b:1}.
        # r=1, b. window={b:2}.
        # r=2, a. window={b:2, a:1}.
        # r=3, a. window={b:2, a:2}. Formed match? t={a:2, b:1}.
        #   b in window(2) >= t(1). a in window(2) >= t(2).
        #   Formed!
        #   Contract: l=0 ('b'). remove b. window={b:1, a:2}. Valid? yes.
        #   Update ans. ans="bbaa" (len 4). l=1.
        #   Contract: l=1 ('b'). remove b. window={b:0, a:2}. Valid? NO (need b>=1).
        #   l=2.
        # r expands.
        # r=4, c. window={b:0, a:2, c:1}.
        # ... never valid again? 
        # Wait, window was {b:0, a:2}. r adds 'c'.
        # window is {b:0, a:2, c:1}. t needs b.
        # never valid again.
        # So answer should be "baa"? No, index l=1 to r=3 ("baa") has b:1, a:2.
        # Wait.
        # l=0, r=3 ("bbaa"). Valid.
        # remove s[0]='b'. window now "baa" ({b:1, a:2}). Valid! t needs b:1, a:2.
        # update ans to "baa" (len 3). l=1.
        # remove s[1]='b'. window now "aa" ({b:0, a:2}). Invalid.
        
        # So "baa" is length 3.
        # My previous manual trace was slightly off.
        # Correct: "baa"
        
        assert result == "baa"

    def test_missing_char(self):
        s = "abc"
        t = "d"
        result = self.solver.minWindow(s, t)
        assert result == ""
