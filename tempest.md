## 3. Two Pointers & Sliding Window: Deep Dive Notes

---

### Core Structural Triggers

Recognizing when to use these techniques depends on identifying key constraints in the problem statement.

* **Linear Structures:** The problem explicitly involves arrays, strings, or linked lists.
* **Contiguity:** Look for keywords like **"subarray"**, **"substring"**, or **"contiguous"**.
* **Ordered State:** The input is sorted, or sorting it does not break the problem constraints (crucial for Two
  Pointers).
* **Subsegment Targets:** Finding pairs, triplets, or bounded subsegments meeting a specific sum or property constraint.

---

### Two Pointers: Classification & Mechanics

#### 1. Opposite Ends (Converging Inward)

* **Concept:** Used primarily on **sorted linear collections**. Two pointers (`left` at index `0`, `right` at index
  `n-1`) move toward each other based on a monotonic condition.
* **Mechanism:** If the current combined property (e.g., sum) is too small, move `left` inward to increase it. If it is
  too large, move `right` inward to decrease it.
* **Complexity:** $O(n)$ time (pointers cross at most once), $O(1)$ space.
* **Canonical Application (Two Sum on Sorted Array):**

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1  # Need a larger sum
        else:
            right -= 1  # Need a smaller sum
    return []

```

#### 2. Fast / Slow Pointers (Linked Lists & In-Place Mutation)

* **Concept:** Pointers move through the data structure at different speeds (e.g., `fast` moves 2 steps, `slow` moves 1
  step) or under different structural triggers.
* **Mechanisms:**
* **Cycle Detection (Floyd’s Tortoise & Hare):** If a cycle exists, `fast` will eventually enter the cycle and lap
  `slow`, meaning `fast == slow` at some point.
* **Midpoint Identification:** When `fast` reaches the end of a linked list, `slow` will be exactly at the middle
  element.
* **In-Place Array De-duplication:** `fast` scans every element, while `slow` marks the boundary of the valid, modified
  prefix array.

---

### Sliding Window: Classification & Mechanics

#### 1. Fixed-Size Window

* **Concept:** The window width $K$ is invariant. The window shifts right by one element per iteration.
* **Mechanism:** To slide the window efficiently without recomputing the entire contents, add the new element arriving
  at the right edge and subtract the old element leaving the left edge.
* **Complexity:** $O(n)$ time, $O(1)$ dynamic modification cost.
* **Template Pattern:**

```python
def max_sum_fixed_window(nums: list[int], k: int) -> int:
    # Compute first window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide window across remaining array
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # Add incoming, subtract outgoing
        max_sum = max(max_sum, window_sum)
    return max_sum

```

#### 2. Variable-Size Window

* **Concept:** The window expands and contracts dynamically based on constraints (e.g., "Max subarray sum $\le K$").
* **The Monotonicity Principle:** The window expands as long as the constraint is met. The moment the constraint is
  violated, the left boundary must shrink until validity is restored.
* **Amortized Complexity Analysis:** While a nested `while` loop controls the contraction, each pointer (`left` and
  `right`) increments at most $n$ times. Total operations are bounded by $2n$, yielding a strictly linear $O(n)$ runtime
  complexity.
* **State Maintenance:** Tracking validity usually requires a hash map, an array-based frequency counter (size 26 for
  English alphabet constraints), or a rolling unique tracker.

---

### Deep Dive: Canonical Solutions

#### 1. Longest Substring Without Repeating Characters

* **Strategy:** Variable window. Maintain the last seen index of characters in a hash map. When a duplicate character
  appears, instantly shift the `left` pointer to the right of the duplicate's previous position.

```
Example: "abcabcbb"
[a  b  c] a  b  c  b  b   -> Right=2, Left=0. Length = 3
 a [b  c  a] b  c  b  b   -> Right=3, Left=1 (a repeated, left moves past first 'a'). Length = 3

```

#### 2. Minimum Window Substring

* **Strategy:** Variable window. Expand `right` until the window contains all required target characters. Once valid,
  aggressively contract `left` while tracking the minimum valid window length until the criteria is no longer met.

#### 3. 3Sum

* **Strategy:** Convert to 2Sum. Sort the array. Iterate index $i$ from $0$ to $n-3$. For each fixed $i$, use **Opposite
  Ends Two Pointers** on the remaining subarray `[i+1...n-1]` targeting the value $-arr[i]$. De-duplicate by skipping
  identical adjacent values for $i$, `left`, and `right`.

#### 4. Trapping Rain Water

* **Strategy:** Two pointers at opposite ends. Maintain two tracking variables: `left_max` and `right_max`. The smaller
  of the two max boundaries dictates how much water can be trapped at the current pointer index, allowing you to compute
  water accumulation cell-by-cell in $O(n)$ time and $O(1)$ space.

---

### Interview Pitfalls Checklist

| Pitfall                              | Consequence                                           | Mitigation                                                                                                                                                                               |
|--------------------------------------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Invalid Window Eviction**          | Infinite loops or inaccurate tracking states.         | When shrinking `left` in variable windows, ensure the dynamic loop boundary strictly prevents `left` from passing `right` (`while left <= right:`).                                      |
| **Unsorted Input with Two Pointers** | Incorrect logic paths and missed target matches.      | Always verify whether the input array is explicitly sorted before running an opposite-ends strategy. If unsorted, evaluate if an $O(n \log n)$ sort step is acceptable.                  |
| **Out-of-Bound Map Erasure**         | Checking stale map variables inside the window state. | When using character maps to store frequency counters or indexes, verify whether stale historical records (indices outside the current `left` boundary) are being filtered out properly. |