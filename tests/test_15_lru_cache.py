import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _15_lru_cache import LRUCache

class TestLRUCache:
    def setup_method(self):
        self.cache = LRUCache(2)

    def test_example_1_standard(self):
        # ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
        # [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
        # Output: [null, null, null, 1, null, -1, null, -1, 3, 4]
        
        self.cache.put(1, 1) # {1:1}
        self.cache.put(2, 2) # {1:1, 2:2}
        
        assert self.cache.get(1) == 1 # {2:2, 1:1} (1 MRU)
        
        self.cache.put(3, 3) # Evicts 2. {1:1, 3:3}
        assert self.cache.get(2) == -1
        
        self.cache.put(4, 4) # Evicts 1. {3:3, 4:4}
        assert self.cache.get(1) == -1
        assert self.cache.get(3) == 3
        assert self.cache.get(4) == 4

    def test_overwrite_value(self):
        self.cache.put(1, 1)
        self.cache.put(1, 100) # Update 1. {1:100}
        assert self.cache.get(1) == 100
        
        self.cache.put(2, 2) # {1:100, 2:2}
        self.cache.put(3, 3) # Evicts 1? No, 1 was updated recently (if implemented correctly).
        # Wait, updating SHOULD make it MRU.
        # Sequence: put(1,1), put(1,100) [1 is MRU], put(2,2) [2 is MRU], put(3,3) [3 is MRU, 1 is LRU, evict 1].
        # Let's trace my logic carefully.
        # If put(1,100) updates, it should move 1 to MRU.
        # Current state: {1:100}
        # put(2,2) -> {1:100, 2:2} (1 is LRU, 2 is MRU)
        # put(3,3) -> Evicts 1. {2:2, 3:3}
        
        # Checking implementation detail: does put update move to MRU? YES.
        
        self.cache = LRUCache(2)
        self.cache.put(1, 1)
        self.cache.put(2, 2) # {1:1, 2:2}
        self.cache.put(1, 100) # {2:2, 1:100} (1 MRU)
        self.cache.put(3, 3) # Evicts 2. {1:100, 3:3}
        
        assert self.cache.get(2) == -1
        assert self.cache.get(1) == 100

    def test_capacity_zero(self):
        # Is capacity 0 allowed? Constraints say 1 <= capacity.
        # But let's test 1.
        self.cache = LRUCache(1)
        self.cache.put(1, 1)
        self.cache.put(2, 2) # Evicts 1.
        assert self.cache.get(1) == -1
        assert self.cache.get(2) == 2

    def test_access_updates_order(self):
        self.cache.put(1, 1)
        self.cache.put(2, 2) # {1, 2}
        self.cache.get(1) # {2, 1}
        self.cache.put(3, 3) # Evicts 2
        assert self.cache.get(2) == -1
        assert self.cache.get(1) == 1
        assert self.cache.get(3) == 3

    def test_large_capacity(self):
        self.cache = LRUCache(100)
        for i in range(100):
            self.cache.put(i, i)
        assert self.cache.get(0) == 0
        self.cache.put(100, 100) # Evicts nothing, capacity logic full? No, 100+1=101 items. Evicts 0 (LRU).
        # Wait, I just accessed 0. So 0 is MRU.
        # {1..99, 0}
        # put(100) -> evicts 1 (LRU).
        assert self.cache.get(1) == -1
        assert self.cache.get(0) == 0

    def test_missing_key(self):
        assert self.cache.get(999) == -1
