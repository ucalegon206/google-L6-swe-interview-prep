import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _12_remove_invalid_parentheses import Solution

class TestRemoveInvalidParentheses:
    def setup_method(self):
        self.solver = Solution()

    def test_example_1_standard(self):
        # Input: s = "()())()"
        # Output: ["(())()","()()()"]
        s = "()())()"
        result = self.solver.removeInvalidParentheses(s)
        expected = {"(())()", "()()()"}
        assert set(result) == expected

    def test_example_2_letters(self):
        # Input: s = "(a)())()"
        # Output: ["(a())()","(a)()()"]
        s = "(a)())()"
        result = self.solver.removeInvalidParentheses(s)
        expected = {"(a())()", "(a)()()"}
        assert set(result) == expected

    def test_example_3_empty_result(self):
        # Input: s = ")("
        # Output: [""]
        s = ")("
        result = self.solver.removeInvalidParentheses(s)
        assert result == [""]

    def test_already_valid(self):
        s = "()"
        result = self.solver.removeInvalidParentheses(s)
        assert result == ["()"]

    def test_remove_all(self):
        # ((( -> ""
        # ))) -> ""
        s = "((("
        assert self.solver.removeInvalidParentheses(s) == [""]
        s = ")))"
        assert self.solver.removeInvalidParentheses(s) == [""]

    def test_remove_all_mixed(self):
        # )(( -> ""
        s = ")(( "
        # wait " " is space? prompt says "lowercase English letters and parentheses".
        # Assuming only parentheses for this test case logic if I can't guarantee spaces.
        s = ")((a" 
        # remove first ), then ((. result "a".
        result = self.solver.removeInvalidParentheses(s)
        assert result == ["a"]

    def test_multiple_solutions(self):
        # s = "()())()"
        # covered in example 1.
        # s = "(())())" -> "(())()", "(()())"
        s = "(())())"
        result = self.solver.removeInvalidParentheses(s)
        expected = {"(())()", "(()())"}
        assert set(result) == expected

    def test_complex_nesting(self):
        # s = "n"
        s = "n"
        assert self.solver.removeInvalidParentheses(s) == ["n"]
