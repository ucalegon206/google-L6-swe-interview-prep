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
**Analogy:** 🐛 **The Hungry Caterpillar**.
Imagine a caterpillar taking bites of a leaf.
1.  **Expand (Head)**: It stretches its head forward (Right Pointer) to grab more food until it's full (Valid Window).
2.  **Shrink (Tail)**: Once full, it pulls its tail forward (Left Pointer) to shorten its body (Minimize Window).
*It repeats this "inch-worm" movement across the entire array, never moving backward.*
**Mnemonic:** "Expand to Valid, Shrink to Win."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Trapping Rain Water** | O(N) | Walls limit water. Shrink from the *short* side. |
| **Min Window Substring** | O(N) | Dynamic window size. Complex "validity" check (Hash Map). |
| **Sliding Window Max** | O(N) | **"Big Fish Eat Small Fish"** (Monotonic Queue). |

---

## 2. The "Binary Search" (on Answers)
**Trigger:** "Sorted array", "Minimize the Maximum", "K-th Smallest".
**Analogy:** � **The Dictionary Rip-Out**.
You are looking for the word "Zebra".
1.  Open the book exactly in the middle. You see "Monkey".
2.  "Zebra" is after "Monkey".
3.  **The Violent Part**: You rip the entire first half of the book (A-M) and **throw it in the trash**. You never look at it again.
4.  Repeat with the remaining pages. *You eliminate massive chunks of the problem instantly.*
**Mnemonic:** "Cut the Fat."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Median 2 Sorted Arrays** | O(log min(M,N)) | Partitioning two books to find the middle page. |
| **Count Smaller After Self** | O(N log N) | Merge Sort is just Binary Search with memory. |

---

## 3. The "Heap" (Priority Queue)
**Trigger:** "Top K elements", "Merge K items", "Median of stream".
**Analogy:** � **The ER Triage Doctor**.
Patients (Numbers) arrive in the waiting room in random order.
1.  The Doctor doesn't care who arrived first.
2.  The Doctor *only* calls the patient with the **worst injury** (Max Value).
3.  As soon as that patient leaves, the next worst injury is called immediately.
*Standard queues are fair (Line at a deli). Heaps are strictly about **Urgency** (Priority).*
**Mnemonic:** "VIP Only."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Merge K Sorted Lists** | O(N log K) | The Doctor takes the worst patient from 5 different waiting rooms. |
| **The Skyline Problem** | O(N log N) | **"Tetris with Gravity"**. Max height defines the roof. |

---

## 4. Routes & Recursion (Graphs / DP)
**Trigger:** "Shortest path", "Islands", "Valid parentheses", "Edit Distance".
**Analogy:** 🌊 **The Tsunami (BFS)** vs � **The Lab Mouse (DFS)**.
*   **BFS (The Tsunami)**: A giant wave expanding in all directions at once. It hits *everything* at distance 1 meter, then *everything* at 2 meters. It guarantees finding the **closest** dry land, but implies a massive wall of water (Memory).
*   **DFS (The Lab Mouse)**: A mouse running fast down a maze corridor. It ignores side paths and runs until it hits a wall (Dead End). Only then does it backtrack. It uses very little memory, but might take a long path to find the cheese.
**Mnemonic:** "Layers (BFS) vs. Labyrinths (DFS)."

| Problem | Complexity | L6 Twist |
|:---|:---|:---|
| **Word Ladder II** | O(V + E) | BFS for distance, DFS to write the path. |
| **Alien Dictionary** | O(V + E) | **"Task Scheduler"**. A must finish before B (Topological Sort). |
| **Remove Invalid Parens** | O(2^N) | BFS to find the "shallowest" valid solution. |

---

## 5. Planning (System Design Bridges)
**Trigger:** "Design a...", "Implement a class", "LRU", "Autocomplete".
**Analogy:** � **The Supermarket Manager**.
*   **Map/Index**: The **Aisle Signs**. You don't walk every aisle to find Milk; you look up at the sign "Dairy" and go straight there (O(1) Lookup).
*   **Cache**: The **Checkout Candy**. The store knows everyone buys Snickers, so they put them right next to your hand (Fastest Access) instead of hiding them in the back of the store.
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
