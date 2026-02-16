"""
PROBLEM: The Skyline Problem
DIFFICULTY: Hard
TIME LIMIT: 60 Minutes

VISUAL EXPLANATIONS:
- NeetCode (Sweep Line + Max Heap): https://www.youtube.com/watch?v=FgfBkPyPfrY
- Tushar Roy (Detailed Logic): https://www.youtube.com/watch?v=GSBLe8cKu0s
- Happy Coding (Explanation): https://www.youtube.com/watch?v=8Kd-tzkQ9tU

A city's skyline is the outer contour of the silhouette formed by all the buildings in that city when viewed from a distance. 
Given the locations and heights of all the buildings, return the skyline formed by these buildings collectively.

The geometric information of each building is given by a triplet `[left, right, height]`.
The output is a list of "key points" `[x, y]` in the format of `[[x1,y1], [x2,y2], ...]`.
A key point is the left endpoint of a horizontal line segment.

Example 1:
Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]

Constraints:
- 1 <= buildings.length <= 10^4
- 0 <= left < right <= 2^31 - 1
- 1 <= height <= 2^31 - 1
- buildings is sorted by left edge.

APPROACH: Sweep Line Algorithm + Max Heap
-----------------------------------------
We need to process the "critical points" where the height of the skyline *might* change.
These critical points are the left and right edges of the buildings.

Events:
1. **Start of Building**: The max height might increase.
2. **End of Building**: The max height might decrease.

We can collect all these events and sort them by x-coordinate.
If `x` coordinates are the same, we need careful tie-breaking:
- If two buildings START, we process the taller one first (to record the max height immediately).
- If two buildings END, we process the shorter one first? (Actually, it doesn't matter much for removal, but consistency helps).
- If one STARTS and one ENDS: we must process START first. Why? If a building starts at `x` with height 10 and another ends at `x` with height 10, the skyline continues at 10. If we process End first, height drops to 0, then Start raises to 10 -> we get redundant (x,0), (x,10) points.
  
Standard Tie-Breaking Trick:
- Represent Start as `(x, -height)` (Negative height makes taller start come first in sort).
- Represent End as `(x, height)` (Positive height makes End come *after* Start).
- Sort events.

Data Structure:
We need a container to store "active" building heights and efficiently return the maximum.
A **Max Heap** is perfect.
However, Python's `heapq` is a Min Heap (so we store negative heights), and it **Does Not Support Efficient Removal** of arbitrary elements (O(N) to remove).
Since we need to remove a height when a building ends, we use a **Lazy Removal** strategy.
- We maintain a `live_heap` of all started buildings.
- We maintain a `past_heap` of all ended buildings.
- When querying `max()`, we check if `live_heap.top() == past_heap.top()`. If so, it means the max building has actually ended. We pop both and repeat until `live_heap.top()` is truly alive.

Algorithm:
1. Create events list.
2. Sort events.
3. Iterate events.
   - If Start: Push height to `live_heap`.
   - If End: Push height to `past_heap` (mark for lazy removal).
   - Clean heaps (lazy removal).
   - Check current max height. If it differs from the last recorded skyline height, add a new key point `[x, current_max]`.

Time Complexity: O(N log N) - Sorting events. Heap operations are log N.
Space Complexity: O(N) - Storing events and heap.

Industry Nomenclature:
- **Sweep Line**: A conceptual vertical line moving across the plane, processing events at specific coordinates.
- **Lazy Removal / Lazy Deletion**: Marking an item as deleted rather than physically removing it immediately, cleaning up later when accessing the item.
"""

from typing import List
import heapq

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # 1. Create Events
        # Start: (x, -height). End: (x, height).
        events = []
        for l, r, h in buildings:
            events.append((l, -h)) 
            events.append((r, h))
            
        # 2. Sort Events
        # Sort by x. Tie break: -h before h.
        # This handles:
        # - Start before End at same x (-h < h)
        # - Taller start before Shorter start (-10 < -5)
        # - Shorter end before Taller end (5 < 10) -> Removal order less critical, but consistent.
        # [PITFALL] Sorting Order is Critical.
        # 1. Sort by x-coordinate.
        # 2. Tie-break:
        #    - Start (-h) comes before End (h) since negative < positive.
        #      This prevents gaps: if one building starts where another ends, we process start first to maintain max height.
        #    - Taller Start (-10) comes before Shorter Start (-5).
        #    - Shorter End (5) comes before Taller End (10).
        events.sort()
        
        # 3. Setup Heaps
        # We need a dummy 0 height building that represents "ground" and never ends.
        # This simplifies logic so heap is never empty.
        live_heap = [0] # Stores -height (Max Heap behavior)
        past_heap = []  # Stores -height of removed buildings
        
        result = [[0, 0]] # Dummy start
        
        for x, h in events:
            if h < 0:
                # START event: h is negative. Push it to live_heap.
                # (Remember heap stores -height to simulate max heap, so we push h directly)
                heapq.heappush(live_heap, h)
            else:
                # END event: h is positive.
                # We need to remove the corresponding building (height h).
                # In our heap, heights are stored as negative. So we push -h to past_heap.
                heapq.heappush(past_heap, -h)
                
            # Lazy Removal
            # Remove heights from top of live_heap if they are in past_heap
            while past_heap and live_heap[0] == past_heap[0]:
                heapq.heappop(live_heap)
                heapq.heappop(past_heap)
            
            # Current max height is -live_heap[0]
            current_max = -live_heap[0]
            
            # If max height changes, record a key point
            if result[-1][1] != current_max:
                result.append([x, current_max])
                
        # Remove dummy start result [0,0] if it's redundant (e.g. first building starts at 2)
        return result[1:]

# Test Cases
if __name__ == "__main__":
    solver = Solution()
    
    # Test 1
    buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
    # Expected: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
    print(f"Test 1: {solver.getSkyline(buildings)}")
    
    # Test 2: Touching buildings
    buildings2 = [[0,2,3],[2,5,3]]
    # Expected: [[0,3],[5,0]] (Merge into one flat line)
    print(f"Test 2: {solver.getSkyline(buildings2)}")
