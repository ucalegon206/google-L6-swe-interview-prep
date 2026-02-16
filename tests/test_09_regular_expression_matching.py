import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _09_regular_expression_matching import Solution

class TestRegularExpressionMatching:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_mismatch(self):
        # s = "aa", p = "a" -> False
        assert not self.solver.isMatch("aa", "a")

    def test_example_2_star_repeat(self):
        # s = "aa", p = "a*" -> True
        assert self.solver.isMatch("aa", "a*")

    def test_example_3_dot_star(self):
        # s = "ab", p = ".*" -> True
        assert self.solver.isMatch("ab", ".*")

    def test_complex_match(self):
        # s = "aab", p = "c*a*b" -> True
        # c* -> empty
        # a* -> aa
        # b -> b
        assert self.solver.isMatch("aab", "c*a*b")

    def test_complex_mismatch(self):
        # s = "mississippi", p = "mis*is*p*." -> False
        assert not self.solver.isMatch("mississippi", "mis*is*p*.")
        
    def test_empty_string_and_pattern(self):
        assert self.solver.isMatch("", "")
        
    def test_empty_string_matches_skipped_pattern(self):
        # s = "", p = "a*" -> True
        assert self.solver.isMatch("", "a*")
        
    def test_empty_string_no_match(self):
        # s = "", p = "a" -> False
        assert not self.solver.isMatch("", "a")

    def test_multiple_stars(self):
        # s = "aaa", p = "a*a" -> True
        # a* eats 'aa', a matches 'a'
        assert self.solver.isMatch("aaa", "a*a")
        
    def test_multiple_stars_variants(self):
        # s = "aaa", p = "ab*a*c*a" -> True
        # ab* -> a
        # a* -> a
        # c* -> empty
        # a -> a
        # Total: a + a + a = aaa
        assert self.solver.isMatch("aaa", "ab*a*c*a")

    def test_dot_matches_any(self):
        assert self.solver.isMatch("abc", "a.c")
        assert not self.solver.isMatch("abc", "a.b")
