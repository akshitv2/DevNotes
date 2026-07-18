---
parent: DSA
---

# DSA Interview Notes

---

## Table of Contents

1. [How to Use These Notes](#how-to-use-these-notes)
2. [Complexity Analysis](#1-complexity-analysis)
3. [Arrays & Strings](#2-arrays--strings)
4. [Two Pointers & Sliding Window](#3-two-pointers--sliding-window)
5. [Hashing](#4-hashing)
6. [Linked Lists](#5-linked-lists)
7. [Stacks & Queues](#6-stacks--queues)
8. [Recursion & Backtracking](#7-recursion--backtracking)
9. [Sorting Algorithms](#8-sorting-algorithms)
10. [Binary Search](#9-binary-search)
11. [Trees](#10-trees)
12. [Heaps / Priority Queues](#11-heaps--priority-queues)
13. [Graphs](#12-graphs)
14. [Dynamic Programming](#13-dynamic-programming)
15. [Greedy Algorithms](#14-greedy-algorithms)
16. [Bit Manipulation](#15-bit-manipulation)
17. [Advanced Data Structures](#16-advanced-data-structures)
18. [String Algorithms](#17-string-algorithms)
19. [Math for DSA](#18-math-for-dsa)
20. [Problem-Solving Framework](#19-problem-solving-framework)
21. [Tech-Lead-Specific Angle](#20-tech-lead-specific-angle)
22. [Additional Topics (quick-reference list)](#21-additional-topics-quick-reference-list)

---

## How to Use These Notes

- Read a topic, then **implement it from scratch** without looking — muscle memory matters more than recognition.
- For each pattern, know: **when to use it** (trigger phrases in the problem), **time/space complexity**, and **1-2
  canonical problems**.
- As a tech lead, also prepare to explain **why** you chose an approach over alternatives — interviewers weight this
  heavily at senior levels.

---

## 1. Complexity Analysis

**Big-O** describes growth rate of time/space as input size `n → ∞`. Drop constants and lower-order terms.

| Notation   | Name         | Example                       |
|------------|--------------|-------------------------------|
| O(1)       | Constant     | array index access            |
| O(log n)   | Logarithmic  | binary search                 |
| O(n)       | Linear       | single pass scan              |
| O(n log n) | Linearithmic | merge sort, heap sort         |
| O(n²)      | Quadratic    | nested loops, bubble sort     |
| O(2ⁿ)      | Exponential  | naive recursive subsets       |
| O(n!)      | Factorial    | permutations, brute-force TSP |

**Key rules:**

- Sequential steps: add complexities → O(a) + O(b) = O(a+b) (keep both if not clearly dominant, e.g. graph algorithms
  are O(V+E)).
- Nested steps: multiply → O(a) × O(b) = O(a·b).
- **Amortized analysis**: e.g., dynamic array `push_back` is O(1) amortized meaning average is O(1) despite occasional
  O(n) resize, because resizes happen exponentially less often.
- **Master Theorem** for divide-and-conquer recurrences `T(n) = aT(n/b) + f(n)`:
    - If `f(n) = O(n^c)` where `c < log_b(a)` → `T(n) = Θ(n^log_b(a))`
    - If `c = log_b(a)` → `T(n) = Θ(n^c log n)`
    - If `c > log_b(a)` → `T(n) = Θ(f(n))`
- Space complexity includes **recursion call stack depth**, not just extra data structures — a common interview trap.

---

## 2. Arrays & Strings

The substrate for most problems. Know these cold:

- **In-place reversal**, rotation (via reversal trick: reverse whole array, then reverse each half — O(n) time, O(1)
  space).
- **Prefix sums**: precompute `prefix[i] = sum(arr[0..i])` for O(1) range-sum queries. Extend to 2D prefix sums for
  matrix range queries.
- **Kadane's Algorithm** (max subarray sum): track `currentMax = max(arr[i], currentMax + arr[i])`, update global max.
  O(n).
- **Dutch National Flag** (3-way partition, e.g. sort 0s/1s/2s in one pass using low/mid/high pointers). O(n), O(1)
  space.
- **Difference arrays** for range-update queries: `diff[l] += val; diff[r+1] -= val`, then prefix-sum to materialize.
- **In-place matrix operations**: transpose + reverse rows = rotate 90°.
- String immutability (Java/Python) — building strings in a loop is O(n²); use `StringBuilder`/list-join instead.

**Common pitfalls:** off-by-one on inclusive/exclusive ranges, integer overflow (less relevant in Python, critical in
Java/C++), mutating array while iterating.

---

## 3. Two Pointers & Sliding Window

**Trigger phrases:** "subarray", "substring", "contiguous", "pair with sum", "sorted array".

### Two Pointers

- **Opposite ends** (sorted array, converge inward): e.g., two-sum on sorted array, container with most water, valid
  palindrome.
- **Fast/slow pointers**: cycle detection (Floyd's Tortoise and Hare), finding middle of linked list, removing
  duplicates in-place.

### Sliding Window

- **Fixed-size window**: maintain running sum/count as window slides; O(n).
- **Variable-size window**: expand right pointer, shrink left pointer when a constraint is violated (e.g., "longest
  substring without repeating characters", "minimum window substring", "longest subarray with sum ≤ k").
- Maintain window state in a hash map/count array; complexity O(n) since each pointer moves ≤ n times total.

**Canonical problems:** Longest Substring Without Repeating Characters, Minimum Window Substring, 3Sum (sort + two
pointers), Trapping Rain Water, Longest Repeating Character Replacement.

---

## 4. Hashing

- **Hash map**: O(1) average insert/lookup/delete. Know collision handling conceptually (chaining vs open addressing) —
  occasionally asked to "design a hash map".
- **Hash set**: dedup, existence checks, O(1) membership test.
- Use hashing to convert O(n²) brute force → O(n): e.g., Two Sum (store complements), Group Anagrams (sorted string or
  char-count tuple as key), Longest Consecutive Sequence (hash set + only start counting from sequence heads → O(n)
  despite looking O(n²)).
- **Rolling hash** (see String Algorithms) for substring comparisons.
- Beware: hash map iteration order isn't guaranteed in most languages (Python 3.7+ dicts preserve insertion order — an
  implementation detail, not a language guarantee across all langs).

**Canonical problems:** Two Sum, Group Anagrams, Longest Consecutive Sequence, Subarray Sum Equals K (prefix sum + hash
map of counts), LRU Cache (hash map + doubly linked list).

---

## 5. Linked Lists

- **Singly vs doubly linked**, sentinel/dummy head nodes to simplify edge cases (empty list, single node, head removal).
- **Reversal**: iterative (prev/curr/next pointers, O(1) space) and recursive (O(n) call stack).
- **Cycle detection**: Floyd's algorithm (slow/fast pointers); to find cycle *start*, after detecting meeting point,
  reset one pointer to head and advance both by 1 until they meet.
- **Merge two sorted lists**: classic building block for merge sort on linked lists.
- **Reorder / partition / remove nth from end**: typically solved with two pointers offset by a gap, or a dummy node +
  fast pointer trick.
- Doubly linked list + hash map → **LRU Cache** design (O(1) get/put).

**Canonical problems:** Reverse Linked List, Detect Cycle, Merge K Sorted Lists (use a min-heap), LRU Cache, Add Two
Numbers, Copy List with Random Pointer (hash map or interleaving trick).

---

## 6. Stacks & Queues

- **Stack**: LIFO. Use for matching/nesting problems (parentheses validation), DFS iterative implementation, undo
  functionality, expression evaluation (infix→postfix, calculator problems).
- **Monotonic stack**: maintain increasing/decreasing order to solve "next greater element", "daily temperatures", "
  largest rectangle in histogram" in O(n) — each element pushed/popped once.
- **Queue**: FIFO. BFS traversal, task scheduling.
- **Deque (double-ended queue)**: sliding window maximum (monotonic deque keeps candidates in decreasing order, O(n)
  total).
- **Two stacks → implement a queue** (and vice versa) — a classic "design" question.

**Canonical problems:** Valid Parentheses, Min Stack (auxiliary stack tracking min), Daily Temperatures, Sliding Window
Maximum, Largest Rectangle in Histogram, Implement Queue using Stacks.

---

## 7. Recursion & Backtracking

- Every recursive solution needs: **base case(s)**, **recursive relation**, and confidence the state shrinks toward the
  base case.
- **Backtracking** = DFS + explicit choice/undo (`choose → recurse → un-choose`). Used for combinatorial search spaces:
  permutations, combinations, subsets, N-Queens, Sudoku solver, word search on grid.
- **Pruning** is what makes backtracking tractable: cut a branch early once it can't lead to a valid/optimal solution (
  e.g., partial sum already exceeds target).
- Complexity is often exponential (O(2ⁿ) for subsets, O(n!) for permutations) — the interview signal is recognizing this
  upfront and discussing pruning, not avoiding exponential complexity entirely (it's often unavoidable for exhaustive
  search).

**Canonical problems:** Subsets, Permutations, Combination Sum, N-Queens, Word Search, Generate Parentheses, Sudoku
Solver, Palindrome Partitioning.

---

## 8. Sorting Algorithms

| Algorithm                  | Time (avg) | Time (worst) | Space    | Stable?               | Notes                                                                                  |
|----------------------------|------------|--------------|----------|-----------------------|----------------------------------------------------------------------------------------|
| Bubble/Selection/Insertion | O(n²)      | O(n²)        | O(1)     | Bubble/Insertion: yes | Insertion sort is fast for nearly-sorted/small n                                       |
| Merge Sort                 | O(n log n) | O(n log n)   | O(n)     | Yes                   | Good for linked lists, external sorting, guarantees n log n                            |
| Quick Sort                 | O(n log n) | O(n²)        | O(log n) | No                    | Fast in practice; worst case with bad pivot (mitigate via median-of-3 or random pivot) |
| Heap Sort                  | O(n log n) | O(n log n)   | O(1)     | No                    | In-place, but poor cache locality                                                      |
| Counting Sort              | O(n + k)   | O(n + k)     | O(k)     | Yes                   | k = range of input values; not comparison-based                                        |
| Radix Sort                 | O(d·(n+k)) | same         | O(n+k)   | Yes                   | d = number of digits; good for integers/fixed-length strings                           |

- Know **Quickselect** (partition-based selection) for "Kth largest/smallest" in O(n) average — a very common follow-up
  to sorting questions.
- Understand **why comparison sorts have an Ω(n log n) lower bound** (decision tree argument) and how non-comparison
  sorts (counting/radix) beat it by exploiting input structure.
- Most languages' built-in sort: Timsort (Python, Java) — hybrid merge+insertion sort, O(n log n) worst case, stable,
  exploits existing runs.

---

## 9. Binary Search

**Trigger phrases:** "sorted array", "find minimum/maximum satisfying condition", "search space can be halved".

- Classic template (avoid infinite loops — use `lo <= hi` with `lo = mid+1`/`hi = mid-1`, or `lo < hi` with
  `mid = lo + (hi-lo)//2` depending on convention; be consistent and test boundary cases).
- **Binary search on the answer**: when the problem asks to minimize/maximize a value and you can write a monotonic
  `isFeasible(x)` predicate, binary search over the answer space (e.g., "minimum days to make m bouquets", "capacity to
  ship packages within d days", "split array largest sum minimized").
- Search in **rotated sorted array**: determine which half is properly sorted, then decide which half to recurse into.
- **Find first/last occurrence** (lower_bound/upper_bound) — careful boundary handling.
- Complexity: O(log n) per search; O(log n · f(n)) when combined with a feasibility check of cost f(n).

**Canonical problems:** Search in Rotated Sorted Array, Find Peak Element, Median of Two Sorted Arrays (O(log(min(m,n)))
via binary search on partition), Koko Eating Bananas, Capacity To Ship Packages.

---

## 10. Trees

### Basics

- **Traversals**: inorder (L-Root-R, gives sorted order for BST), preorder (Root-L-R, good for serialization),
  postorder (L-R-Root, good for deletion/bottom-up computation), level-order (BFS with a queue).
- Recursive traversal is O(n) time, O(h) space (h = height, due to call stack); iterative versions use an explicit
  stack.

### Binary Search Trees (BST)

- Invariant: left subtree < node < right subtree. Inorder traversal yields sorted sequence.
- Insert/search/delete: O(h) — O(log n) if balanced, O(n) worst case if degenerate (e.g., inserting sorted data into a
  naive BST).
- **Validate BST**: pass down (min, max) bounds, or do inorder traversal and check strictly increasing.
- **Deletion** has 3 cases: leaf (remove), one child (splice), two children (replace with inorder successor/predecessor,
  then delete that node).

### Balanced Trees (concept-level, rarely implemented from scratch in interviews)

- **AVL Tree**: strictly balanced via rotations, height difference ≤ 1 between subtrees; guarantees O(log n) operations.
- **Red-Black Tree**: looser balance than AVL, fewer rotations on insert/delete, used in `TreeMap`/`std::map`/Linux CFS
  scheduler.
- Know **why** balance matters (prevents O(n) degeneration) even if you don't implement rotations live.

### Tries (Prefix Trees)

- Node per character; used for autocomplete, prefix search, word dictionaries. O(L) insert/search where L = word length,
  independent of dictionary size.
- Space can be heavy; consider compressed tries (radix tries) for space-sensitive contexts.

### Other Tree Concepts

- **Lowest Common Ancestor (LCA)**: recursive approach for general binary tree (O(n)); binary lifting for repeated LCA
  queries at scale (O(log n) per query after O(n log n) preprocessing).
- **Diameter of a tree**, **serialize/deserialize a tree**, **tree from traversals** (preorder+inorder reconstructs a
  unique tree).
- **Segment tree / Fenwick tree** are specialized trees — see Advanced Data Structures.

**Canonical problems:** Validate BST, LCA, Serialize/Deserialize Binary Tree, Binary Tree Maximum Path Sum, Kth Smallest
in BST, Implement Trie, Word Search II (Trie + backtracking).

---

## 11. Heaps / Priority Queues

- **Binary heap**: array-backed complete binary tree. Insert O(log n), extract-min/max O(log n), peek O(1), build-heap
  from array O(n) (not O(n log n) — a common interview subtlety, via bottom-up heapify).
- **Min-heap vs max-heap**: choose based on whether you want smallest/largest element accessible quickly.
- **Top-K pattern**: maintain a heap of size K while scanning n elements → O(n log k), better than sorting (O(n log n))
  when k << n.
- **Two-heap technique**: median-of-stream — max-heap for lower half, min-heap for upper half, keep sizes balanced
  within 1.
- **K-way merge**: min-heap of size k holding one element from each list/stream — used for Merge K Sorted Lists, Kth
  smallest element in a sorted matrix.

**Canonical problems:** Kth Largest Element in a Stream, Top K Frequent Elements, Merge K Sorted Lists, Find Median from
Data Stream, Task Scheduler, Meeting Rooms II.

---

## 12. Graphs

### Representation

- **Adjacency list** (space O(V+E), preferred for sparse graphs) vs **adjacency matrix** (O(V²) space, O(1) edge lookup,
  good for dense graphs).

### Traversal

- **BFS**: queue-based, explores level by level — used for shortest path in **unweighted** graphs, level-order problems.
- **DFS**: stack/recursion-based — used for connectivity, cycle detection, topological sort, path existence,
  backtracking-style exploration.
- Both are O(V + E).

### Key Algorithms

- **Topological Sort**: only valid for DAGs. Two approaches: DFS with post-order stack push, or **Kahn's algorithm** (
  BFS using in-degree counting) — Kahn's also naturally detects cycles (if not all nodes are output, there's a cycle).
- **Union-Find / Disjoint Set Union (DSU)**: near-O(1) (`O(α(n))`, inverse Ackermann) union/find with **path compression
  ** + **union by rank/size**. Used for: cycle detection in undirected graphs, Kruskal's MST, connected components, "
  number of islands"-style grouping, dynamic connectivity.
- **Shortest Path**:
    - **Dijkstra's**: single-source shortest path, non-negative weights, min-heap based, O((V+E) log V).
    - **Bellman-Ford**: handles negative weights, detects negative cycles, O(V·E) — slower but more general.
    - **Floyd-Warshall**: all-pairs shortest path, O(V³), simple DP formulation, good for dense/small graphs.
    - **0-1 BFS**: deque-based, for graphs with only 0/1 edge weights, O(V+E).
- **Minimum Spanning Tree (MST)**:
    - **Kruskal's**: sort edges by weight, add if it doesn't create a cycle (via Union-Find). O(E log E).
    - **Prim's**: grow tree from a start node, always add cheapest edge to an unvisited node (min-heap). O(E log V).
- **Bipartite check**: 2-color via BFS/DFS; odd cycle ⇒ not bipartite.
- **Strongly Connected Components**: Kosaraju's (two DFS passes) or Tarjan's (single DFS with low-link values).
- **Bridges & Articulation Points**: Tarjan's low-link technique, used for network reliability analysis — good "tech
  lead" flavor question since it maps to real infra (single points of failure).

**Canonical problems:** Number of Islands, Course Schedule (topo sort), Clone Graph, Network Delay Time (Dijkstra),
Redundant Connection (Union-Find), Word Ladder (BFS), Cheapest Flights Within K Stops (Bellman-Ford variant), Alien
Dictionary (topo sort on custom order).

---

## 13. Dynamic Programming

The topic that separates "knows patterns" from "memorized problems." Focus on **recognizing the recurrence**, not
memorizing solutions.

### Core idea

Break a problem into overlapping subproblems with **optimal substructure** (optimal solution built from optimal
solutions to subproblems). Two implementation styles:

- **Top-down (memoization)**: recursion + cache. Easier to derive from brute force; add a memo dict/array keyed by
  state.
- **Bottom-up (tabulation)**: iterative, build table from base cases upward. Usually more space-efficient (can often
  compress to O(1) or O(n) rolling arrays instead of O(n²) tables).

### Common Patterns

1. **1D DP** (Fibonacci-style): `dp[i]` depends on `dp[i-1], dp[i-2], ...` — e.g., Climbing Stairs, House Robber.
2. **Knapsack family**:
    - 0/1 Knapsack: each item used at most once; `dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])`.
    - Unbounded Knapsack: items reusable — Coin Change, Rod Cutting.
    - Subset Sum / Partition Equal Subset Sum — knapsack in disguise (boolean feasibility version).
3. **Longest Increasing Subsequence (LIS)**: O(n²) DP or O(n log n) with binary search + patience sorting.
4. **Longest Common Subsequence (LCS) / Edit Distance**: 2D DP over two strings, `dp[i][j]` from `dp[i-1][j-1]`,
   `dp[i-1][j]`, `dp[i][j-1]`.
5. **Grid DP**: paths/min-cost in a grid, `dp[i][j]` from `dp[i-1][j]` and `dp[i][j-1]` — Unique Paths, Minimum Path
   Sum.
6. **Interval DP**: `dp[i][j]` represents best answer over subarray/substring `[i, j]`, built from smaller intervals —
   Matrix Chain Multiplication, Burst Balloons, Palindrome Partitioning min cuts.
7. **DP on Trees**: post-order traversal computing `dp[node]` from children's dp values — House Robber III, Diameter of
   Binary Tree.
8. **Bitmask DP**: state includes a bitmask of which elements are used — Traveling Salesman Problem (O(2ⁿ · n²)),
   assignment problems. Only tractable for small n (~20).
9. **State machine DP**: state includes an extra dimension representing "mode" — Best Time to Buy/Sell Stock with
   cooldown/fee/k-transactions (state = day × holding-or-not × transactions-used).

### How to derive a DP solution live in an interview

1. Define the state precisely in words: "`dp[i]` = ___".
2. Write the recurrence: what earlier states does `dp[i]` depend on?
3. Identify base case(s).
4. Decide iteration order (must compute dependencies before dependents).
5. Optimize space if only a few previous states are needed (rolling array).

**Canonical problems:** House Robber, Coin Change, LIS, Edit Distance, Longest Palindromic Substring, Unique Paths, Word
Break, Partition Equal Subset Sum, Best Time to Buy/Sell Stock (all variants), Regular Expression Matching.

---

## 14. Greedy Algorithms

- Make the locally optimal choice at each step, hoping it leads to a globally optimal solution — **only correct when the
  problem has the greedy-choice property** (a common interview trap is applying greedy where DP is actually required —
  be ready to justify *why* greedy works, e.g. via an exchange argument or matroid structure).
- **Interval scheduling**: sort by end time, greedily pick earliest-ending non-overlapping interval — classic proof of
  greedy correctness via exchange argument.
- **Interval merging**: sort by start time, merge overlapping.
- **Huffman coding**: build optimal prefix-free code via min-heap merging (greedy + heap).
- **Activity selection, Jump Game, Gas Station, Task Scheduler** all resolve to a greedy scan with a proof sketch you
  should be able to state.
- When unsure if greedy applies, try to find a counterexample first — that's the intellectually honest interview move,
  and one interviewers explicitly want to see from senior candidates.

**Canonical problems:** Merge Intervals, Non-overlapping Intervals, Jump Game I/II, Gas Station, Task Scheduler, Minimum
Number of Arrows to Burst Balloons.

---

## 15. Bit Manipulation

- Core ops: `&` AND, `|` OR, `^` XOR, `~` NOT, `<<`/`>>` shifts.
- **XOR properties**: `a ^ a = 0`, `a ^ 0 = a`, commutative/associative → find the single non-duplicate number in O(n)
  time O(1) space.
- **Check/set/clear/toggle a bit**: `n & (1<<i)`, `n | (1<<i)`, `n & ~(1<<i)`, `n ^ (1<<i)`.
- **n & (n-1)** clears the lowest set bit — used to count set bits (Brian Kernighan's algorithm, O(popcount)) and to
  check power of 2 (`n & (n-1) == 0`).
- **n & (-n)** isolates the lowest set bit.
- Bitmasks to represent subsets (pairs with bitmask DP).
- Practical relevance for a tech lead: bitmasks/flags in config systems, feature flag storage, permission systems (Unix
  file permissions as a real-world bitmask).

**Canonical problems:** Single Number, Counting Bits, Number of 1 Bits, Sum of Two Integers without +/-, Power of Two,
Subsets via bitmask.

---

## 16. Advanced Data Structures

These show up less often but signal strong depth, and matter in system-design-adjacent discussions:

- **Segment Tree**: supports range queries (sum/min/max) and point/range updates in O(log n). Built as a binary tree
  over array indices; each node aggregates its range. Extension: **lazy propagation** for efficient range updates.
- **Fenwick Tree / Binary Indexed Tree (BIT)**: simpler than a segment tree, supports prefix-sum queries and point
  updates in O(log n), O(n) space — favored for its compact implementation.
- **Disjoint Set Union (DSU)**: covered under Graphs; also useful in Kruskal's MST and dynamic connectivity problems
  outside of graph framing (e.g., "accounts merge", "redundant connection").
- **LRU / LFU Cache**: hash map + doubly linked list (LRU) or hash map + frequency buckets (LFU) — a very common "design
  a data structure" interview question, and directly relevant to real caching systems a tech lead would own.
- **Sparse Table**: O(1) range-min/max query after O(n log n) preprocessing, for **static** arrays (no updates) — useful
  for range-minimum-query-heavy problems (e.g., LCA via Euler tour + RMQ).
- **Skip List**: probabilistic alternative to balanced trees, O(log n) expected search/insert, used in Redis sorted
  sets.
- **Bloom Filter**: probabilistic set membership, O(k) per op, no false negatives but possible false positives,
  space-efficient — great "practical systems" tie-in for tech lead interviews (e.g., "how would you avoid a cache
  stampede/check membership at scale cheaply").

---

## 17. String Algorithms

- **KMP (Knuth-Morris-Pratt)**: pattern matching in O(n+m) using a precomputed "failure function" (longest proper
  prefix-suffix) to avoid re-scanning on mismatch.
- **Rabin-Karp**: rolling hash to compare substring hashes in O(n+m) average; watch for hash collisions (verify with
  direct comparison on hash match).
- **Z-function**: array where `z[i]` = length of longest substring starting at i that matches a prefix of the string —
  used for pattern matching and string periodicity.
- **Manacher's Algorithm**: finds the longest palindromic substring in O(n), beating the naive O(n²)
  expand-around-center approach.
- **Trie-based** multi-pattern matching (Aho-Corasick) for matching many patterns simultaneously in O(n + total pattern
  length) — relevant to real systems like content filtering.
- **Suffix Array / Suffix Tree** (concept-level): support substring queries, longest repeated substring, etc., in
  advanced string-heavy problems.

**Canonical problems:** Implement strStr() (KMP), Longest Palindromic Substring, Repeated DNA Sequences (rolling hash),
Shortest Palindrome.

---

## 18. Math for DSA

- **GCD/LCM**: Euclidean algorithm, O(log(min(a,b))).
- **Sieve of Eratosthenes**: find all primes up to n in O(n log log n) — precompute for prime-related queries.
- **Modular arithmetic**: `(a+b) % m`, `(a*b) % m`, modular exponentiation (fast power, O(log n)), modular inverse (via
  Fermat's little theorem when m is prime, or extended Euclidean algorithm generally) — relevant for problems asking to
  return an answer "mod 10^9+7" (a strong hint that intermediate values will overflow standard integer types and
  combinatorics/DP is expected).
- **Combinatorics**: permutations `n!/(n-k)!`, combinations `n!/(k!(n-k)!)`, Pascal's triangle for computing
  combinations with DP to avoid factorial overflow.
- **Fast exponentiation** (binary exponentiation): O(log n) for computing `x^n`.

---

## 19. Problem-Solving Framework

A repeatable process to narrate out loud in interviews (this itself is a signal at the tech lead level):

1. **Clarify**: restate the problem, ask about constraints (input size, value ranges, duplicates, sorted?), and edge
   cases (empty input, single element, negative numbers).
2. **Examples**: work through 1-2 examples by hand, including an edge case.
3. **Brute force first**: state the naive approach and its complexity — this anchors the conversation and often reveals
   the pattern needed to optimize.
4. **Identify the pattern**: does it smell like two pointers / sliding window / DP / graph traversal / binary search?
   Match against trigger phrases above.
5. **Discuss tradeoffs**: time vs space, and mention alternative approaches even if you don't implement them (this is a
   major differentiator at senior/lead level).
6. **Code cleanly**: meaningful variable names, small helper functions, handle edge cases explicitly.
7. **Test**: trace through your code with the examples from step 2, plus at least one edge case.
8. **State final complexity** and whether it can be improved further.

---

## 20. Tech-Lead-Specific Angle

Beyond raw DSA, tech lead interviews often layer in judgment signals on top of the same questions:

- **Explain tradeoffs unprompted**: e.g., "I'll use a hash map for O(1) lookup, trading O(n) space" — narrate this
  without being asked.
- **Code quality under pressure**: naming, modularity, and testability matter more than at junior levels — treat the
  whiteboard/editor code as if a teammate will read it.
- **Talk about scaling the naive solution**: "this works for n ≤ 10^4; if n were 10^9 we'd need a streaming/external
  approach" — shows systems thinking layered on algorithms.
- **Mentoring signal**: when given hints, integrate them gracefully and explain your updated reasoning — interviewers
  are also evaluating how you'd behave in a pairing/code-review session with a junior engineer.
- **Know when NOT to over-engineer**: a tech lead is also expected to recognize when O(n²) is genuinely fine (small,
  bounded n) rather than reflexively optimizing — pragmatism is a real signal.
- **Connect DSA to real systems**: LRU cache → real caching layers; Union-Find → distributed system
  membership/partitioning; trie → autocomplete/search services; consistent hashing (a common lead-level extension of
  hashing) → load balancing and sharding.
- **Consistent Hashing**: not classic DSA but frequently appears at senior/lead level bridging DSA and system design —
  hash nodes and keys onto a ring, use virtual nodes to smooth load distribution, minimizes re-distribution when nodes
  are added/removed compared to naive `hash(key) % n`.

---

## 21. Additional Topics (quick-reference list)

Topics worth at least a skim/refresher, listed briefly due to space — dig into any that feel unfamiliar:

- **Union-Find variants**: weighted union-find, union-find with rollback (for offline queries).
- **Euler Tour technique** for subtree queries / LCA via sparse table RMQ.
- **Heavy-Light Decomposition** and **Centroid Decomposition** (tree query techniques — advanced, mostly
  competitive-programming level, rarely required but good to name-drop for breadth).
- **Suffix Automaton** (advanced string structure).
- **Convex Hull** (Graham scan / Andrew's monotone chain, O(n log n)) and basic computational geometry (cross product
  for orientation, line intersection).
- **Reservoir Sampling** for sampling from a stream of unknown length.
- **Fisher-Yates shuffle** for unbiased array shuffling in O(n).
- **Monotonic queue/stack revisited** for "maximum in every window" and histogram-style problems.
- **Matrix exponentiation** for O(log n) linear recurrence computation (e.g., Fibonacci in O(log n)).
- **Bloom filter, Count-Min Sketch, HyperLogLog** — probabilistic data structures for streaming/large-scale approximate
  counting (great for tech-lead-level "how would you do this at scale" follow-ups).
- **A\* search** and **Dijkstra with heuristics** for pathfinding beyond plain BFS/Dijkstra.
- **Union of Intervals / Sweep Line algorithms** for scheduling and geometry problems.
- **Topological sort variants**: detecting *all* valid orderings, lexicographically smallest ordering (min-heap instead
  of plain queue in Kahn's algorithm).
- **Amortized data structures**: dynamic arrays, splay trees (self-adjusting BST with amortized O(log n)).
- **External sorting / merge sort for disk-based data** — relevant if asked about processing data larger than memory.
- **Randomized algorithms**: randomized quickselect/quicksort, skip lists, treaps (BST + heap hybrid using random
  priorities).
- **Concurrency-adjacent DSA**: thread-safe queues, producer-consumer patterns (often shows up as a "design" question
  bridging DSA and systems).

---

### Final tip

For tech lead interviews, breadth + articulate reasoning usually outweighs being able to solve the single hardest
problem. Prioritize being fluent in Sections 1–14 (the "core" patterns) before spending deep time on Sections 16–18 and
the quick-reference list.
