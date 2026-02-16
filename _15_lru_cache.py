"""
PROBLEM: LRU Cache
DIFFICULTY: Medium (But Expected to be implemented cleanly in Hard Interviews)
TIME LIMIT: 30 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Hash Map + Double Linked List): https://www.youtube.com/watch?v=7V856LH8fqE
- Tech Dose (Explained): https://www.youtube.com/watch?v=xDEuM5qa0zg
- Google Engineer Explains: https://www.youtube.com/watch?v=NDpwj0VWz1U

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the `LRUCache` class:
- `LRUCache(int capacity)` Initialize the LRU cache with positive size capacity.
- `int get(int key)` Return the value of the key if the key exists, otherwise return -1.
- `void put(int key, int value)` Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. 
  If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions `get` and `put` must each run in O(1) average time complexity.

Example 1:
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Constraints:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls will be made to get and put.

APPROACH: Hash Map + Doubly Linked List
---------------------------------------
To achieve O(1) for both `get` and `put`, we need two data structures working together:
1. **Hash Map (Dictionary)**: 
   - Maps `key` -> `Node`.
   - Allows O(1) access to a node given its key.
2. **Doubly Linked List**:
   - Maintains the order of elements based on usage (Most Recently Used at one end, Least Recently Used at the other).
   - Allows O(1) removal and insertion of nodes (unlike an array which is O(N)).

Logic:
- When we access a node (`get` or `put` existing), we move it to the "Most Recently Used" (MRU) position (usually the head/right end).
- When we insert a new node (`put` new), we add it to the MRU position.
- If we exceed capacity, we remove the node at the "Least Recently Used" (LRU) position (usually the tail/left end) and delete it from the Hash Map.

Why Doubly Linked List?
- We need to remove a node from the middle of the list (when `get` is called) and move it to the front. 
- With a singly linked list, we can't delete a node in O(1) without having a reference to its *previous* node.
- With a doubly linked list, each node has `prev` and `next`, so we can delete it directly.

Industry Nomenclature:
- **Eviction Policy**: The algorithm used to decide which item to discard (LRU, LFU, FIFO).
- **Sentinel Nodes / Dummy Nodes**: Nodes at the head and tail that act as guards to simplify edge cases (empty list, single element list).
"""

class DNode:
    """Doubly Linked List Node"""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # Map key -> DNode
        
        # Initialize dummy head and tail nodes
        # Head -> LRU (Least Recently Used)
        # Tail -> MRU (Most Recently Used)
        # Or vice versa. Let's strictly define:
        # Head.next is the FIRST node (LRU).
        # Tail.prev is the LAST node (MRU).
        self.head = DNode()
        self.tail = DNode()
        
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DNode):
        """Removes a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: DNode):
        """Adds a node right before the tail (MRU position)."""
        prev_node = self.tail.prev
        
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # Move accessed node to MRU (remove then add to end)
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update value and move to MRU
            # [PITFALL] Update Existing Key.
            # Two steps: 
            # 1. Update the value.
            # 2. Move to MRU (remove and re-add).
            # Common mistake: forgetting to move to MRU on update, or forgetting to update value.
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add(node)
        else:
            # Create new node
            new_node = DNode(key, value)
            self.cache[key] = new_node
            self._add(new_node)
            
            # Check capacity
            if len(self.cache) > self.capacity:
                # Evict LRU (node after head)
                lru_node = self.head.next
                self._remove(lru_node)
                del self.cache[lru_node.key]

# Test Cases
if __name__ == "__main__":
    # Test 1
    lru = LRUCache(2)
    lru.put(1, 1) # Cache: {1=1}
    lru.put(2, 2) # Cache: {1=1, 2=2}
    print(f"Get 1: {lru.get(1)} (Expected 1)") # Cache: {2=2, 1=1} (1 is MRU)
    
    lru.put(3, 3) # Evicts key 2. Cache: {1=1, 3=3}
    print(f"Get 2: {lru.get(2)} (Expected -1)") 
    
    lru.put(4, 4) # Evicts key 1. Cache: {3=3, 4=4}
    print(f"Get 1: {lru.get(1)} (Expected -1)")
    print(f"Get 3: {lru.get(3)} (Expected 3)")
    print(f"Get 4: {lru.get(4)} (Expected 4)")
