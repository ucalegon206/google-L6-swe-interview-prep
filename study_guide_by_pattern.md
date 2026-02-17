# ⚡️ The L6 "Anti-Freeze" Coding Playbook

*Goal: Recognize the "Shape" of the problem in the first 3 minutes.*

## 🧠 Global Mnemonic: "S.H.A.R.P."
If you panic, remember to stay **S.H.A.R.P.** to pick the right tool:
*   **S** - **S**liding Window (Two Pointers)
*   **H** - **H**eaps (Top K)
*   **A** - **A**rrays Sorted (Binary Search)
*   **R** - **R**outes & Recursion (Graphs/DP)
*   **P** - **P**lanning (System Design)

---

## 1. The "Sliding Window" & "Two Pointers"
**Trigger:** "Longest/Shortest substring", "Subarray with sum K", "Continuous range".
**Analogy:** 🪗 **The Accordion**.
*   You expand the bellows (window) to get the notes you want (valid state).
*   You shrink it to play the next part (minimize/optimize).
**Mnemonic:** "Expand to Valid, Shrink to Win."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Trapping Rain Water** | O(N) | Walls limit water. Shrink from the *short* side. |
| **Min Window Substring** | O(N) | Dynamic window size. Complex "validity" check (Hash Map). |
| **Sliding Window Max** | O(N) | **"Big Fish Eat Small Fish"** (Monotonic Queue). |

---

## 2. The "Binary Search" (on Answers)
**Trigger:** "Sorted array", "Minimize the Maximum", "K-th Smallest".
**Analogy:** 📖 **The Phonebook**.
*   You don't read every name. You open the middle, check the letter, and throw away half the book. Repeatedly.
**Mnemonic:** "Cut the Fat."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Median 2 Sorted Arrays** | O(log min(M,N)) | Partitioning two books to find the middle page. |
| **Count Smaller After Self** | O(N log N) | Merge Sort is just Binary Search with memory. |

---

## 3. The "Heap" (Priority Queue)
**Trigger:** "Top K elements", "Merge K items", "Median of stream".
**Analogy:** 🏰 **King of the Hill**.
*   Only the person at the very top (Max/Min) matters. Everyone else is just waiting in the pile.
**Mnemonic:** "VIP Only."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Merge K Sorted Lists** | O(N log K) | The "King" leaves, the next noble from his land takes his place. |
| **The Skyline Problem** | O(N log N) | **"Tetris with Gravity"**. Max height defines the roof. |

---

## 4. Routes & Recursion (Graphs / DP)
**Trigger:** "Shortest path", "Islands", "Valid parentheses", "Edit Distance".
**Analogy:** 🦠 **The Virus (BFS)** vs 🔦 **The Maze Runner (DFS)**.
*   **BFS (Virus):** Spreads to all neighbors equally. Finds the nearest exit (shortest path).
*   **DFS (Maze Runner):** Runs down one path until hitting a wall, then backtracks.
**Mnemonic:** "Layers (BFS) vs. Labyrinths (DFS)."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Word Ladder II** | O(V + E) | BFS for distance, DFS to write the path. |
| **Alien Dictionary** | O(V + E) | **"Task Scheduler"**. A must finish before B (Topological Sort). |
| **Remove Invalid Parens** | O(2^N) | BFS to find the "shallowest" valid solution. |

---

## 5. Planning (System Design Bridges)
**Trigger:** "Design a...", "Implement a class", "LRU", "Autocomplete".
**Analogy:** 📚 **The Librarian**.
*   Knows where every book is instantly (Index/Map) and keeps popular books on the front desk (Cache).
**Mnemonic:** "Dictionary & Desk."

| Problem | Complexity | System Design Bridge |
|:---|:---|:---|
| **LRU Cache** | O(1) | **Doubly Linked List + Map**. Essential for CDN/Redis. |
| **Search Autocomplete** | O(1) Lookup | **Trie + Hot List**. Essential for Typeahead/Search. |

---

## ⚡️ Quick Complexity Cheatsheet
- **N = 1,000,0000**: Need O(N) or O(N log N).
- **"Shortest"**: BFS.
- **"All Paths"**: DFS.
- **"Top K"**: Heap.
- **"Sorted"**: Binary Search.
