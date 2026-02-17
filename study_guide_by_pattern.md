# ⚡️ The L6 "Anti-Freeze" Coding Playbook

*Goal: Recognize the "Shape" of the problem in the first 3 minutes.*

## 1. The "Sliding Window" & "Two Pointers"
**Trigger:** "Longest/Shortest substring", "Subarray with sum K", "Continuous range".
**Visual Anchor:** A window pane sliding over a long tape.
**The L6 Twist:** The window size is dynamic, or the condition to shrink the window is complex (e.g., "contains all chars from T").

| Problem | Core Insight | Complexity |
|:---|:---|:---|
| **Trapping Rain Water** | **Two Pointers**: Walls limit water. Move the *shorter* wall inward to find a taller support. | O(N) / O(1) |
| **Min Window Substring** | **Expand-Contract**: Expand `right` until valid, then shrink `left` to minimize. | O(N) / O(1) |
| **Sliding Window Max** | **Monotonic Deque**: The "Big Fish" eats smaller/older fish. Front is always max. | O(N) / O(K) |

---

## 2. The "Binary Search" (on Answers)
**Trigger:** "Sorted array", "Find occurrences", "Minimize the Maximum", "K-th Smallest".
**Visual Anchor:** Cutting the search space in half repeatedly.
**The L6 Twist:** You aren't searching an array; you are searching a *solution space* (e.g., "Is it possible to do X in T time?").

| Problem | Core Insight | Complexity |
|:---|:---|:---|
| **Median 2 Sorted Arrays** | **Partitioning**: Find a cut in both arrays such that `left_part <= right_part`. | O(log(min(M,N))) |
| **Count Smaller After Self** | **Merge Sort**: During merge, if you pick from right, valid jumps from left increment count. | O(N log N) |

---

## 3. The "Heap" (Priority Queue)
**Trigger:** "Top K elements", "Merge K items", "Median of stream", "Schedule events".
**Visual Anchor:** A funnel that always lets the smallest/largest item out first.
**The L6 Twist:** The heap contains *objects* or *iterators*, not just integers (e.g., "Merge K sorted log files").

| Problem | Core Insight | Complexity |
|:---|:---|:---|
| **Merge K Sorted Lists** | **Min-Heap**: Keep the head of each list in heap. Pop min, push next from same list. | O(N log K) |
| **The Skyline Problem** | **Max-Heap + Line Sweep**: Process edges. Heap tracks "active buildings". Height changes = Contour. | O(N log N) |

---

## 4. Graph Search (BFS / DFS)
**Trigger:** "Shortest transformation", "Order of tasks", "Connected components", "Valid states".
**Visual Anchor:** Ripples in a pond (BFS) vs. Maze runner (DFS).
**The L6 Twist:** The graph is implicit (word ladder) or involves state compression.

| Problem | Core Insight | Complexity |
|:---|:---|:---|
| **Word Ladder II** | **BFS + DFS**: BFS for shortest distance (layers), DFS to backtrack paths. | O(V + E) |
| **Alien Dictionary** | **Topological Sort**: A comes before B is a directed edge `A -> B`. Detect cycles. | O(V + E) |
| **Remove Invalid Parens** | **BFS**: Each removal is an edge. First valid layer = Minimum removals. | O(2^N) |

---

## 5. Design & System (The Bridge)
**Trigger:** "Design a...", "Implement a class", "High frequency of updates".
**Visual Anchor:** A blueprint connecting multiple data structures.
**The L6 Twist:** Connects directly to System Design questions.

| Problem | Core Insight | System Design Bridge |
|:---|:---|:---|
| **LRU Cache** | **Dict + DLL**: O(1) lookup & O(1) move-to-front. | Redis / Memcached eviction policies. |
| **Search Autocomplete** | **Trie + Hot List**: Store top 3 hot queries *at each node* for O(1) lookup. | Google Search Typeahead / Solr. |
| **Serialize Binary Tree** | **BFS/DFS Traversal**: Convert structure to string and back. | JSON Serialization / ProtoBufs. |

---

## ⚡️ Quick Complexity Cheatsheet

- **N = 1,000,0000**: Need O(N) or O(N log N).
- **N = 10,000**: O(N^2) might pass (rarely).
- **Find "Shortest/Min" in Graph**: BFS.
- **Find "Any" Path**: DFS.
- **"Top K"**: Heap (N log K).
- **"Sorted"**: Binary Search (log N).
