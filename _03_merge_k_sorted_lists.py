"""
PROBLEM: Merge k Sorted Lists
DIFFICULTY: Hard
TIME LIMIT: 25 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Min Heap): https://www.youtube.com/watch?v=q5a5OiGbT6Q
- Take U Forward (Priority Queue): https://www.youtube.com/watch?v=kpCesr9VXDA
- Sweet Logic (Divide & Conquer vs Heap): https://www.youtube.com/watch?v=PTBxKk6xVXs

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []

Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order.
- The sum of lists[i].length will not exceed 10^4.

APPROACH: Min-Heap (Priority Queue)
---------------------------------
This problem is a classic application of a Min-Heap (or Priority Queue).
We want to repeatedly find the smallest element among the heads of the `k` lists to build our sorted result.

Algorithm:
1. Initialize a Min-Heap.
2. Push the head of each of the `k` linked lists onto the heap.
   - We store a tuple `(val, index, node)` in the heap.
   - `val`: The value of the node (primary sorting key).
   - `index`: A unique index (tie-breaker). This is crucial in Python because `ListNode` objects are not comparable by default. If two nodes have the same value, Python attempts to compare the next element in the tuple. If that were the `node` itself, it would crash. The `index` ensures we never compare nodes directly.
   - `node`: The reference to the node itself, so we can access `.next`.
3. While the heap is not empty:
   - Pop the smallest element `(val, i, node)` from the heap.
   - Append this `node` to our `result` linked list.
   - If `node.next` exists, push `(node.next.val, i, node.next)` onto the heap.
4. Return the head of the merged list (using a dummy head to simplify edge cases).

Time Complexity: O(N log k)
- N is the total number of nodes across all lists.
- k is the number of linked lists.
- We perform exactly N pop operations and up to N push operations.
- The heap size never exceeds k.
- Each heap operation (push/pop) allows O(log k).
- Total time: N * O(log k) = O(N log k).

Space Complexity: O(k)
- The heap stores at most k elements (one per list) at any given time.
- The result list is just a rearranging of existing nodes (or new nodes depending on implementation), but the auxiliary space for the algorithm is O(k) for the heap.
"""

from typing import List, Optional
import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
    def __repr__(self):
        return f"{self.val} -> {self.next}"

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Dummy head to simplify result list construction
        dummy = ListNode(0)
        curr = dummy
        
        # Min-heap to store (val, index, node)
        # Using 'index' as a tie-breaker because ListNode doesn't support comparison.
        # Although in Python 3, if first elements of tuple are equal, it compares the second.
        # If we just stored (node.val, node), it would try to compare nodes if vals are equal, causing TypeError.
        heap = []
        
        for i, node in enumerate(lists):
            if node:
                # [PITFALL] Why store 'i'?
                # Tuple comparison works element by element.
                # If values are equal (node.val), Python tries to compare the next element.
                # If we stored (node.val, node), it would compare `node1 < node2`, which raises TypeError (ListNode not comparable).
                # By adding unique 'i', we ensure the comparison breaks there and never reaches 'node'.
                heapq.heappush(heap, (node.val, i, node))
                
        while heap:
            val, i, node = heapq.heappop(heap)
            
            # Append node to result list
            curr.next = node
            curr = curr.next
            
            # If there is a next node in the source list, push it to heap
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
                
        return dummy.next

# Helper function to create linked list from list
def create_linked_list(arr):
    dummy = ListNode(0)
    curr = dummy
    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next
    return dummy.next

# Helper function to print linked list
def print_linked_list(node):
    vals = []
    while node:
        vals.append(str(node.val))
        node = node.next
    return "->".join(vals)

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    l1 = create_linked_list([1, 4, 5])
    l2 = create_linked_list([1, 3, 4])
    l3 = create_linked_list([2, 6])
    lists = [l1, l2, l3]
    
    result = solver.mergeKLists(lists)
    print(f"Test 1 Output: {print_linked_list(result)}")
    # Expected: 1->1->2->3->4->4->5->6
