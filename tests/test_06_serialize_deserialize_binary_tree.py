import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _06_serialize_deserialize_binary_tree import Codec, TreeNode

class TestSerializeDeserialize:
    def setup_method(self):
        self.codec = Codec()

    def assert_trees_equal(self, t1, t2):
        """Helper to recursively verify two trees are identical in structure and value."""
        if not t1 and not t2:
            return
        
        if not t1 or not t2:
            assert False, f"Structural mismatch: {t1} vs {t2}"
            
        assert t1.val == t2.val, f"Value mismatch: {t1.val} != {t2.val}"
        
        self.assert_trees_equal(t1.left, t2.left)
        self.assert_trees_equal(t1.right, t2.right)

    def test_example_1_standard(self):
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
        
        serialized = self.codec.serialize(root)
        deserialized = self.codec.deserialize(serialized)
        
        self.assert_trees_equal(root, deserialized)

    def test_empty_tree(self):
        root = None
        serialized = self.codec.serialize(root)
        # Expect "N"
        assert serialized == "N"
        deserialized = self.codec.deserialize(serialized)
        assert deserialized is None

    def test_single_node(self):
        root = TreeNode(100)
        serialized = self.codec.serialize(root)
        # 100,N,N
        deserialized = self.codec.deserialize(serialized)
        self.assert_trees_equal(root, deserialized)

    def test_left_skewed_tree(self):
        # 1 -> 2 -> 3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        
        serialized = self.codec.serialize(root)
        deserialized = self.codec.deserialize(serialized)
        self.assert_trees_equal(root, deserialized)

    def test_right_skewed_tree(self):
        # 1 -> 2 -> 3
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)
        
        serialized = self.codec.serialize(root)
        deserialized = self.codec.deserialize(serialized)
        self.assert_trees_equal(root, deserialized)

    def test_negative_values(self):
        root = TreeNode(-50)
        root.left = TreeNode(-10)
        
        serialized = self.codec.serialize(root)
        deserialized = self.codec.deserialize(serialized)
        self.assert_trees_equal(root, deserialized)

    def test_full_tree(self):
        # Complete tree depth 2
        #     1
        #   2   3
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        
        serialized = self.codec.serialize(root)
        deserialized = self.codec.deserialize(serialized)
        self.assert_trees_equal(root, deserialized)
