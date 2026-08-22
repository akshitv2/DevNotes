---
nav_order: 1
parent: Problems
title: GFG Problems
layout: default
---

### Maths, Pattern & Recursion

#### Easy Maths

**1. Even or Odd**

* **Description:** Determine whether a given integer $N$ is even or odd.
* **Examples:** Input: $N = 4 \rightarrow$ Output: Even | Input: $N = 7 \rightarrow$ Output: Odd
* **Solution Steps:**
* *Approach 1 (Modulo):* Check if $N \pmod 2 == 0$. If true, return "Even", else "Odd".
* *Approach 2 (Bitwise):* Check if $(N \ \& \ 1) == 0$. If true, return "Even", else "Odd".

**2. Sum of Naturals**

* **Description:** Calculate the sum of the first $N$ natural numbers ($1 + 2 + \dots + N$).
* **Examples:** Input: $N = 5 \rightarrow$ Output: 15
* **Solution Steps:**
* *Naive:* Loop from $1$ to $N$ accumulating sum. Time: $O(N)$, Space: $O(1)$.
* *Efficient:* Apply formula $\frac{N \times (N + 1)}{2}$. Time: $O(1)$, Space: $O(1)$.



**3. Closest Number**

* **Description:** Given two integers $N$ and $M$, find the number closest to $N$ and divisible by $M$. If two exist, return the one with the maximum absolute value.
* **Examples:** Input: $N = 13, M = 4 \rightarrow$ Output: 12 | Input: $N = -15, M = 6 \rightarrow$ Output: -18
* **Solution Steps:**
1. Find quotient $q = N / M$.
2. Compute candidate product $p_1 = M \times q$.
3. If $N \times M > 0$, set $p_2 = M \times (q + 1)$, else $p_2 = M \times (q - 1)$.
4. Compare absolute differences $\vert{}N - p_1\vert{}$ and $\vert{}N - p_2\vert{}$, returning the closer or larger magnitude value.



**4. Sum of Consecutive**

* **Description:** Find the number of ways $N$ can be expressed as a sum of two or more consecutive positive integers.
* **Examples:** Input: $N = 15 \rightarrow$ Output: 3 (15 = 1+2+3+4+5 = 4+5+6 = 7+8)
* **Solution Steps:**
* *Naive:* Iterate starting integer $a$ and length $k$, checking all contiguous sums. Time: $O(N \sqrt{N})$.
* *Efficient:* Solve $N = k \cdot a + \frac{k(k-1)}{2}$. Loop length $k \ge 2$ while $\frac{k(k-1)}{2} < N$. Count where $(N - \frac{k(k-1)}{2}) \pmod k == 0$. Time: $O(\sqrt{N})$.



---

#### Easy Pattern

**5. Solid Rectangle**

* **Description:** Print a solid rectangle pattern of stars with $R$ rows and $C$ columns.
* **Examples:** Input: $R = 3, C = 4 \rightarrow$ Output: 3 lines containing `****`
* **Solution Steps:** Run outer loop $R$ times; inner loop $C$ times printing `*`.

**6. Floyd's Triangle**

* **Description:** Print a right-angled triangle filled with consecutive integers starting from 1 up to $N$ rows.
* **Examples:** Input: $N = 3 \rightarrow$ Row 1: `1`, Row 2: `2 3`, Row 3: `4 5 6`
* **Solution Steps:** Maintain counter `val = 1`. Outer loop $i$ from 1 to $N$, inner loop $j$ from 1 to $i$: print `val` and increment.

**7. Hollow Rectangle**

* **Description:** Print an $R \times C$ rectangle with `*` on borders and spaces inside.
* **Examples:** Input: $R=3, C=3 \rightarrow$ Row 1: `***`, Row 2: `* *`, Row 3: `***`
* **Solution Steps:** Outer loop $i \in [1..R]$, inner loop $j \in [1..C]$. Print `*` if $i=1, i=R, j=1,$ or $j=C$; else space.

---

#### Easy Recursion

**8. Print 1 to N**

* **Description:** Print numbers from 1 to $N$ recursively without loops.
* **Examples:** Input: $N = 5 \rightarrow$ Output: `1 2 3 4 5`
* **Solution Steps:**
1. Base case: If $N == 0$, return.
2. Recursive call: `print1ToN(N - 1)`.
3. Print $N$.



**9. Print N to 1**

* **Description:** Print numbers from $N$ down to 1 recursively.
* **Examples:** Input: $N = 5 \rightarrow$ Output: `5 4 3 2 1`
* **Solution Steps:**
1. Base case: If $N == 0$, return.
2. Print $N$.
3. Recursive call: `printNTo1(N - 1)`.



**10. Factorial**

* **Description:** Compute $N! = N \times (N-1) \times \dots \times 1$.
* **Examples:** Input: $N = 5 \rightarrow$ Output: 120
* **Solution Steps:** Base case $N \le 1$ returns 1; else return $N \times \text{factorial}(N - 1)$.

**11. Greatest Common Divisor (GCD)**

* **Description:** Find the greatest common divisor of integers $A$ and $B$.
* **Examples:** Input: $A = 12, B = 15 \rightarrow$ Output: 3
* **Solution Steps:** Euclidean algorithm: Base case $B == 0$ returns $A$; else return $\text{gcd}(B, A \pmod B)$. Time: $O(\log(\min(A, B)))$.

**12. Power ($A^B$)**

* **Description:** Compute $A$ raised to power $B$.
* **Examples:** Input: $A = 2, B = 5 \rightarrow$ Output: 32
* **Solution Steps:**
* *Naive Recursion:* Return $A \times \text{power}(A, B-1)$. Time: $O(B)$.
* *Binary Exponentiation:* Base $B == 0 \implies 1$. Calculate $half = \text{power}(A, \lfloor B/2 \rfloor)$. If $B$ is even return $half \times half$; else return $A \times half \times half$. Time: $O(\log B)$.



---

#### Medium Maths

**13. Count Digits**

* **Description:** Count the total digits in integer $N$.
* **Examples:** Input: $N = 12345 \rightarrow$ Output: 5
* **Solution Steps:**
* *Iterative:* Repeatedly divide $N$ by 10 until 0. Time: $O(\log_{10} N)$.
* *Math:* Return $\lfloor \log_{10}(N) \rfloor + 1$. Time: $O(1)$.



**14. Prime Testing**

* **Description:** Determine if integer $N$ is prime.
* **Examples:** Input: $N = 11 \rightarrow$ Output: True | Input: $N = 15 \rightarrow$ Output: False
* **Solution Steps:**
* *Naive:* Test factors from $2$ to $N-1$. Time: $O(N)$.
* *Efficient:* Handle divisibility by 2 and 3 explicitly. Loop $i$ from 5 to $\sqrt{N}$ with step 6, testing $i$ and $i+2$. Time: $O(\sqrt{N})$.



**15. Armstrong Number**

* **Description:** Check if a $k$-digit number equals the sum of its digits raised to $k$-th power.
* **Examples:** Input: $N = 153 \rightarrow$ Output: True ($1^3 + 5^3 + 3^3 = 153$)
* **Solution Steps:**
1. Determine digit count $k$.
2. Extract digits using modulo 10, raise each to power $k$, and sum.
3. Return whether sum equals original $N$.



**16. Trailing Zeros in Factorial**

* **Description:** Count trailing zeros in $N!$.
* **Examples:** Input: $N = 5 \rightarrow$ Output: 1 ($5! = 120$) | Input: $N = 100 \rightarrow$ Output: 24
* **Solution Steps:**
* *Naive:* Compute $N!$ and count trailing zeros. (Fails for large $N$ due to overflow).
* *Efficient:* Count prime factor 5 contributions: $\sum_{i=1}^{\infty} \lfloor \frac{N}{5^i} \rfloor$. Loop $i = 5, 25, 125 \dots \le N$. Time: $O(\log_5 N)$.



**17. Prime Factors**

* **Description:** Find all prime factors of $N$.
* **Examples:** Input: $N = 12 \rightarrow$ Output: `2, 2, 3`
* **Solution Steps:**
1. Divide $N$ by 2 repeatedly while $N \pmod 2 == 0$.
2. Loop $i$ from 3 to $\sqrt{N}$ (step 2), dividing $N$ while $N \pmod i == 0$.
3. If remaining $N > 2$, add $N$ to factor list. Time: $O(\sqrt{N})$.



**18. All Divisors**

* **Description:** Find all positive divisors of $N$.
* **Examples:** Input: $N = 10 \rightarrow$ Output: `1, 2, 5, 10`
* **Solution Steps:**
* *Naive:* Iterate $1 \dots N$. Time: $O(N)$.
* *Efficient:* Iterate $i$ from 1 to $\sqrt{N}$. If $N \pmod i == 0$, record $i$ and $N/i$. Time: $O(\sqrt{N})$.



---

### Arrays & Searching

#### Easy Array

**19. Is Sorted**

* **Description:** Check if an array is sorted in non-decreasing order.
* **Examples:** Input: `[1, 2, 3, 4]` $\rightarrow$ Output: True | Input: `[1, 3, 2]` $\rightarrow$ Output: False
* **Solution Steps:** Iterate $i$ from 1 to $N-1$. If `arr[i] < arr[i-1]`, return False. Return True if end reached. Time: $O(N)$.

**20. Reverse Array**

* **Description:** Reverse array elements in-place.
* **Examples:** Input: `[1, 2, 3, 4]` $\rightarrow$ Output: `[4, 3, 2, 1]`
* **Solution Steps:** Set `left = 0`, `right = N-1`. While `left < right`, swap elements, increment `left`, decrement `right`. Time: $O(N)$, Space: $O(1)$.

**21. Rotate Array**

* **Description:** Rotate array to the left by $K$ positions.
* **Examples:** Input: `[1, 2, 3, 4, 5]`, $K = 2 \rightarrow$ Output: `[3, 4, 5, 1, 2]`
* **Solution Steps:**
* *Naive:* Shift elements left by 1 position $K$ times. Time: $O(N \cdot K)$.
* *Reversal Algorithm:* Reverse sub-array `0..K-1`, reverse sub-array `K..N-1`, then reverse entire array `0..N-1`. Time: $O(N)$, Space: $O(1)$.



**22. Leaders in an Array**

* **Description:** Find all elements that are strictly greater than all elements to their right.
* **Examples:** Input: `[16, 17, 4, 3, 5, 2]` $\rightarrow$ Output: `[17, 5, 2]`
* **Solution Steps:** Traverse from right to left tracking `max_so_far`. If `arr[i] > max_so_far`, append `arr[i]` and update `max_so_far`. Reverse output array. Time: $O(N)$, Space: $O(1)$.

**23. Stock Buy and Sell (1 Transaction)**

* **Description:** Maximize profit buying and selling stock once.
* **Examples:** Input: `[7, 1, 5, 3, 6, 4]` $\rightarrow$ Output: 5 (Buy day 2 at 1, sell day 5 at 6)
* **Solution Steps:** Maintain `min_price` and `max_profit`. Iterate prices: update `min_price = min(min_price, price)`, and `max_profit = max(max_profit, price - min_price)`. Time: $O(N)$, Space: $O(1)$.

**24. Stock Buy and Sell (Multiple Transactions)**

* **Description:** Maximize profit with unlimited transactions (can hold at most 1 stock at a time).
* **Examples:** Input: `[1, 5, 3, 8, 12]` $\rightarrow$ Output: 13 ($(5-1) + (12-3)$)
* **Solution Steps:** Iterate $i$ from 1 to $N-1$. If `price[i] > price[i-1]`, accumulate `price[i] - price[i-1]` to profit. Time: $O(N)$, Space: $O(1)$.

---

#### Medium Array

**25. Majority Element**

* **Description:** Find element appearing strictly more than $\lfloor N/2 \rfloor$ times.
* **Examples:** Input: `[3, 3, 4, 2, 4, 4, 2, 4, 4]` $\rightarrow$ Output: 4
* **Solution Steps:**
* *Naive:* Hash map count frequencies. Time: $O(N)$, Space: $O(N)$.
* *Boyer-Moore Voting:* Track `candidate` and `count`. Iterate array: if `count == 0`, `candidate = arr[i]`. Increment `count` if `arr[i] == candidate`, else decrement. Validate candidate in second pass. Time: $O(N)$, Space: $O(1)$.



**26. Kadane's Algorithm (Max Subarray Sum)**

* **Description:** Find contiguous subarray with maximum sum.
* **Examples:** Input: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` $\rightarrow$ Output: 6 (`[4, -1, 2, 1]`)
* **Solution Steps:** Track `curr_max` and `global_max`. Iterate through array: `curr_max = max(arr[i], curr_max + arr[i])` and `global_max = max(global_max, curr_max)`. Time: $O(N)$, Space: $O(1)$.

**27. Next Permutation**

* **Description:** Rearrange numbers into lexicographically next greater permutation.
* **Examples:** Input: `[1, 2, 3]` $\rightarrow$ Output: `[1, 3, 2]` | Input: `[3, 2, 1]` $\rightarrow$ Output: `[1, 2, 3]`
* **Solution Steps:**
1. Find rightmost index $i$ where `arr[i] < arr[i+1]`.
2. If absent, reverse whole array.
3. Else, find rightmost index $j$ where `arr[j] > arr[i]` and swap `arr[i]`, `arr[j]`.
4. Reverse sub-array from $i+1$ to end. Time: $O(N)$, Space: $O(1)$.



**28. Maximum Product Subarray**

* **Description:** Find contiguous subarray with maximum product.
* **Examples:** Input: `[2, 3, -2, 4]` $\rightarrow$ Output: 6
* **Solution Steps:** Track `max_prod`, `min_prod`, and `res`. Loop elements: if negative, swap `max_prod` and `min_prod`. Update `max_prod = max(arr[i], max_prod * arr[i])` and `min_prod = min(arr[i], min_prod * arr[i])`. Update `res`. Time: $O(N)$, Space: $O(1)$.

---

#### Searching

**29. Binary Search**

* **Description:** Search key in sorted array using divide and conquer.
* **Examples:** Input: `[2, 5, 8, 12, 16]`, key = 12 $\rightarrow$ Output: Index 3
* **Solution Steps:** Maintain `low = 0`, `high = N-1`. Compute `mid = low + (high - low)/2`. If `arr[mid] == key`, return `mid`. If `arr[mid] < key`, `low = mid + 1`; else `high = mid - 1`. Time: $O(\log N)$.

**30. Search in Sorted & Rotated Array**

* **Description:** Search target in a sorted array that has been rotated.
* **Examples:** Input: `[4, 5, 6, 7, 0, 1, 2]`, target = 0 $\rightarrow$ Output: Index 4
* **Solution Steps:** Binary search: check if left half `[low..mid]` is sorted. If so, check if target falls in left half; adjust `high` or `low`. Else, right half is sorted; adjust pointers accordingly. Time: $O(\log N)$.

**31. Book Allocation Problem**

* **Description:** Allocate $N$ book pages among $M$ students minimizing maximum pages assigned to any student.
* **Examples:** Input: pages = `[12, 34, 67, 90]`, $M = 2 \rightarrow$ Output: 113
* **Solution Steps:**
* Binary search on answer range: `low = max(pages)`, `high = sum(pages)`.
* Validate if current `mid` pages capacity requires $\le M$ students.
* If valid, set `res = mid` and search lower range (`high = mid - 1`); else `low = mid + 1`. Time: $O(N \log(\text{sum} - \text{max}))$.



---

### Sorting & Pointer Patterns

#### Sorting

**32. Quick Sort**

* **Description:** Sort array via divide-and-conquer pivot partitioning.
* **Examples:** Input: `[4, 1, 3, 9, 7]` $\rightarrow$ Output: `[1, 3, 4, 7, 9]`
* **Solution Steps:** Choose pivot. Partition array placing smaller elements left of pivot and larger elements right. Recursively apply to left and right partitions. Time: Avg $O(N \log N)$, Worst $O(N^2)$.

**33. Merge Sort**

* **Description:** Divide-and-conquer stable sorting algorithm.
* **Examples:** Input: `[12, 11, 13, 5, 6, 7]` $\rightarrow$ Output: `[5, 6, 7, 11, 12, 13]`
* **Solution Steps:** Divide array into two halves at `mid`. Recursively call Merge Sort on left/right halves. Merge two sorted halves using temporary auxiliary storage. Time: $O(N \log N)$, Space: $O(N)$.

---

#### Two-Pointer & Sliding Window

**34. Two Sum in Sorted Array**

* **Description:** Find two indices in sorted array whose values sum to target.
* **Examples:** Input: `[2, 7, 11, 15]`, target = 9 $\rightarrow$ Output: `[0, 1]`
* **Solution Steps:** Set `left = 0`, `right = N-1`. Compute `sum = arr[left] + arr[right]`. If `sum == target`, return indices; if `sum < target`, `left++`; else `right--`. Time: $O(N)$, Space: $O(1)$.

**35. 3 Sum**

* **Description:** Find all unique triplets in array that sum to zero.
* **Examples:** Input: `[-1, 0, 1, 2, -1, -4]` $\rightarrow$ Output: `[[-1, -1, 2], [-1, 0, 1]]`
* **Solution Steps:** Sort array. Loop $i$ from 0 to $N-3$ (skip duplicate $i$). Use two-pointer approach (`left = i+1`, `right = N-1`) to find target `-arr[i]`. Skip duplicate `left`/`right` values upon match. Time: $O(N^2)$.

**36. Max Sum Subarray of Size K**

* **Description:** Find maximum sum of fixed-size subarray $K$.
* **Examples:** Input: `[100, 200, 300, 400]`, $K = 2 \rightarrow$ Output: 700
* **Solution Steps:** Compute initial window sum for first $K$ elements. Slide window across array: add `arr[i]`, subtract `arr[i-K]`, tracking global maximum. Time: $O(N)$, Space: $O(1)$.

**37. Longest Substring Without Repeating Characters**

* **Description:** Find length of longest substring without duplicate characters.
* **Examples:** Input: `"abcabcbb"` $\rightarrow$ Output: 3 (`"abc"`)
* **Solution Steps:** Sliding window with hash map storing character last seen positions. Advance `right` pointer; if `s[right]` was seen at index $\ge left$, update `left = last_seen + 1`. Track maximum length. Time: $O(N)$, Space: $O(\min(N, \text{alphabet}))$.

---

### Linear & Non-Linear Structures

#### Stack & Queue

**38. Balanced Parentheses**

* **Description:** Check if string brackets `()`, `{}`, `[]` are balanced.
* **Examples:** Input: `"{[()]}"` $\rightarrow$ Output: True | Input: `"{[(])}"` $\rightarrow$ Output: False
* **Solution Steps:** Push opening brackets onto stack. For closing brackets, return False if stack is empty or top element doesn't match opening counterpart. Return True if stack is empty at end. Time: $O(N)$, Space: $O(N)$.

**39. Next Greater Element**

* **Description:** Find first element strictly greater to the right for each array element.
* **Examples:** Input: `[4, 5, 2, 25]` $\rightarrow$ Output: `[5, 25, 25, -1]`
* **Solution Steps:** Monotonic stack: Traverse array from right to left. Pop elements from stack while `stack.top() <= arr[i]`. Result for `arr[i]` is top of stack (or -1 if empty). Push `arr[i]` onto stack. Time: $O(N)$, Space: $O(N)$.

**40. Trapping Rain Water**

* **Description:** Compute total water trapped after raining given elevation map array.
* **Examples:** Input: `[0,1,0,2,1,0,1,3,2,1,2,1]` $\rightarrow$ Output: 6
* **Solution Steps:** Two-pointer approach: track `left = 0`, `right = N-1`, `left_max = 0`, `right_max = 0`. While `left < right`, if `arr[left] < arr[right]`, update `left_max` and add `left_max - arr[left]` to answer, `left++`. Else update `right_max` and add `right_max - arr[right]`, `right--`. Time: $O(N)$, Space: $O(1)$.

---

#### Linked List & Trees

**41. Reverse Linked List**

* **Description:** Reverse a singly linked list in-place.
* **Examples:** Input: `1 -> 2 -> 3 -> NULL` $\rightarrow$ Output: `3 -> 2 -> 1 -> NULL`
* **Solution Steps:** Initialize `prev = NULL`, `curr = head`. Traverse list: store `next_node = curr->next`, set `curr->next = prev`, update `prev = curr` and `curr = next_node`. Return `prev`. Time: $O(N)$, Space: $O(1)$.

**42. Detect Cycle in Linked List**

* **Description:** Check if a linked list contains a cycle.
* **Examples:** Input: `1 -> 2 -> 3 -> 2 (cycle)` $\rightarrow$ Output: True
* **Solution Steps (Floyd’s Cycle Finding):** Maintain `slow` and `fast` pointers at `head`. Move `slow` by 1 step and `fast` by 2 steps. If `slow == fast`, a cycle exists. If `fast` or `fast->next` reaches `NULL`, no cycle exists. Time: $O(N)$, Space: $O(1)$.

**43. Lowest Common Ancestor (LCA) in Binary Tree**

* **Description:** Find lowest node in tree that has both nodes $P$ and $Q$ as descendants.
* **Examples:** Input: Tree with root 3, $P = 5, Q = 1 \rightarrow$ Output: Node 3
* **Solution Steps:** Recursively traverse tree: if root is `NULL`, $P$, or $Q$, return root. Search left and right subtrees. If both recursive calls return non-null, root is LCA. If only one returns non-null, pass that node upward. Time: $O(N)$, Space: $O(H)$.

**44. Validate Binary Search Tree**

* **Description:** Check if binary tree satisfies BST properties (all left subtree nodes < root < all right subtree nodes).
* **Examples:** Input: Tree `[2, 1, 3]` $\rightarrow$ Output: True
* **Solution Steps:** Recursive helper passing allowed bounds `validate(node, min_val, max_val)`. For current node, check if `min_val < node.val < max_val`. Recursively validate left subtree with updated max bound, and right subtree with updated min bound. Time: $O(N)$, Space: $O(H)$.

---

### Backtracking

**45. N-Queen Problem**

* **Description:** Place $N$ chess queens on an $N \times N$ chessboard such that no two queens attack each other (no two queens share the same row, column, or diagonal).
* **Examples:** Input: $N = 4 \rightarrow$ Output: `[[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]`
* **Solution Steps:**
1. Use backtracking row by row. Maintain state tracking set/arrays for used columns, positive diagonals ($\text{row} + \text{col}$), and negative diagonals ($\text{row} - \text{col}$).
2. For current row, iterate columns $0 \dots N-1$. If column and diagonals are unvisited, place queen and recurse to $\text{row} + 1$.
3. Backtrack by removing queen and restoring state if sub-tree returns no valid placement. Time: $O(N!)$, Space: $O(N^2)$.



**46. Sudoku Solver**

* **Description:** Fill a partially completed $9 \times 9$ Sudoku grid such that every row, column, and $3 \times 3$ subgrid contains numbers 1 to 9 without repetition.
* **Examples:** Input: $9 \times 9$ grid with empty cells marked as `'.'` $\rightarrow$ Output: Completely solved Sudoku grid.
* **Solution Steps:**
1. Find next empty cell `(r, c)`. If no empty cell remains, grid is solved.
2. Try placing digits $d \in [1..9]$. Check validity: digit $d$ must not already exist in row $r$, column $c$, or subgrid $(\lfloor r/3 \rfloor, \lfloor c/3 \rfloor)$.
3. If valid, set cell to $d$ and recurse. If recursion fails, reset cell to `'.'` and attempt next digit. Time: $O(9^{N})$, where $N$ is empty cell count.



**47. Word Search**

* **Description:** Given an $M \times N$ grid of characters and a string `word`, return `True` if `word` exists in the grid. Words are formed from sequentially adjacent cells (horizontally or vertically), without reusing cells.
* **Examples:** Input: grid = `[['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]`, word = `"ABCCED"` $\rightarrow$ Output: True
* **Solution Steps:**
1. Iterate every grid cell $(r, c)$. If $\text{grid}[r][c] == \text{word}[0]$, trigger DFS backtracking.
2. In DFS function at index $k$: base case $k == \text{len}(\text{word})$ returns True.
3. Mark current cell visited (e.g., set to `'#'`), recurse on 4 orthogonal directions for index $k+1$, then restore original character upon return. Time: $O(M \times N \times 3^L)$, Space: $O(L)$ where $L = \text{len}(\text{word})$.

---

### Greedy Algorithms

**48. Fractional Knapsack**

* **Description:** Given weights and values of $N$ items, put these items in a knapsack of capacity $W$ to maximize total value. Items can be broken into fractional parts.
* **Examples:** Input: values = `[60, 100, 120]`, weights = `[10, 20, 30]`, $W = 50 \rightarrow$ Output: 240.0
* **Solution Steps:**
1. Calculate value-to-weight ratio $\frac{\text{value}[i]}{\text{weight}[i]}$ for each item.
2. Sort items in descending order of this ratio.
3. Iterate sorted items: if item weight $\le W$, add full value and reduce $W$. Else, take fraction $(W / \text{weight}[i]) \times \text{value}[i]$ and set $W = 0$. Time: $O(N \log N)$, Space: $O(1)$.



**49. Activity Selection**

* **Description:** Select the maximum number of activities performed by a single person, assuming non-overlapping execution (start and finish times provided).
* **Examples:** Input: start = `[1, 3, 0, 5, 8, 5]`, finish = `[2, 4, 6, 7, 9, 9]` $\rightarrow$ Output: 4 activities
* **Solution Steps:**
1. Sort activities based on finish times in ascending order.
2. Select first activity and set `last_finish_time = finish[0]`.
3. Iterate remaining activities: if `start[i] >= last_finish_time`, select activity and update `last_finish_time = finish[i]`. Time: $O(N \log N)$, Space: $O(1)$.



**50. Jump Game**

* **Description:** Given an integer array where each element represents maximum jump length from that position, return `True` if you can reach the last index.
* **Examples:** Input: `[2, 3, 1, 1, 4]` $\rightarrow$ Output: True | Input: `[3, 2, 1, 0, 4]` $\rightarrow$ Output: False
* **Solution Steps:**
1. Maintain variable `max_reachable = 0`.
2. Iterate index $i$ from 0 to $N-1$: if $i > \text{max\_reachable}$, return False (stuck at 0-jump point).
3. Update $\text{max\_reachable} = \max(\text{max\_reachable}, i + \text{arr}[i])$. If $\text{max\_reachable} \ge N-1$, return True. Time: $O(N)$, Space: $O(1)$.



---

### Dynamic Programming

**51. 0/1 Knapsack Problem**

* **Description:** Select items with given weights and values to maximize value in capacity $W$. Each item can be picked at most once (no fractions).
* **Examples:** Input: values = `[1, 4, 5, 7]`, weights = `[1, 3, 4, 5]`, $W = 7 \rightarrow$ Output: 9
* **Solution Steps:**
* *Naive (Recursion):* Try picking/skipping each item. Time: $O(2^N)$.
* *Efficient (2D DP):* Create table `dp[i][w]` representing max value using first $i$ items with capacity $w$.
* Transition: If $\text{wt}[i-1] \le w$, $\text{dp}[i][w] = \max(\text{dp}[i-1][w], \text{val}[i-1] + \text{dp}[i-1][w - \text{wt}[i-1]])$; else $\text{dp}[i-1][w]$. Time: $O(N \times W)$, Space: $O(N \times W)$ (Space optimizable to $O(W)$ using 1D array).



**52. Longest Common Subsequence (LCS)**

* **Description:** Find length of longest subsequence common to two strings $S1$ and $S2$.
* **Examples:** Input: $S1 = \text{"abcde"}$, $S2 = \text{"ace"} \rightarrow$ Output: 3 (`"ace"`)
* **Solution Steps:**
* *Naive:* Generate all subsequences. Time: $O(2^{N+M})$.
* *Efficient:* `dp[i][j]` represents LCS length of $S1[0..i-1]$ and $S2[0..j-1]$.
* Loop $i \in [1..N]$ and $j \in [1..M]$:
* If $S1[i-1] == S2[j-1] \implies \text{dp}[i][j] = 1 + \text{dp}[i-1][j-1]$.
* Else $\implies \text{dp}[i][j] = \max(\text{dp}[i-1][j], \text{dp}[i][j-1])$.


* Return `dp[N][M]`. Time: $O(N \times M)$, Space: $O(N \times M)$.



**53. Longest Increasing Subsequence (LIS)**

* **Description:** Find length of longest strictly increasing subsequence in array.
* **Examples:** Input: `[10, 9, 2, 5, 3, 7, 101, 18]` $\rightarrow$ Output: 4 (`[2, 3, 7, 101]`)
* **Solution Steps:**
* *Standard DP:* `dp[i]` stores LIS ending at index $i$. For each $i$, check $j < i$: if $\text{arr}[j] < \text{arr}[i]$, $\text{dp}[i] = \max(\text{dp}[i], \text{dp}[j] + 1)$. Time: $O(N^2)$.
* *Binary Search (Patience Sorting):* Maintain dynamic array `tails`. For each element $x$, binary search position in `tails`. If $x$ larger than all elements, append $x$; else overwrite first element $\ge x$. Length of `tails` is LIS length. Time: $O(N \log N)$, Space: $O(N)$.



**54. Coin Change (Minimum Coins)**

* **Description:** Given coin denominations and target amount $A$, return minimum number of coins needed to make up that amount (infinite supply per denomination).
* **Examples:** Input: coins = `[1, 2, 5]`, $A = 11 \rightarrow$ Output: 3 ($5 + 5 + 1$)
* **Solution Steps:**
1. Initialize array `dp` of size $A+1$ filled with $\infty$, set `dp[0] = 0`.
2. Outer loop $i$ from 1 to $A$; inner loop through each coin $c$:
3. If $i - c \ge 0$, update $\text{dp}[i] = \min(\text{dp}[i], 1 + \text{dp}[i - c])$.
4. Return `dp[A]` if not $\infty$, else -1. Time: $O(N \times A)$, Space: $O(A)$.



---

### Graph Algorithms

**55. Graph Traversal: BFS & DFS**

* **Description:** Traverse all reachable nodes in a graph from a starting vertex $S$.
* **Examples:** Input: Adjacency list, $S = 0 \rightarrow$ Output: Traversal order sequence.
* **Solution Steps:**
* *Breadth-First Search (BFS):* Uses Queue. Push $S$, mark visited. While queue non-empty: pop node $u$, process $u$, iterate unvisited neighbors $v$, mark visited and enqueue $v$. Time: $O(V + E)$, Space: $O(V)$.
* *Depth-First Search (DFS):* Uses Recursion/Stack. Mark current node visited. Recursively process all unvisited neighbors. Time: $O(V + E)$, Space: $O(V)$.



**56. Dijkstra's Algorithm**

* **Description:** Find shortest distances from a single source node to all other nodes in a weighted graph with non-negative edge weights.
* **Examples:** Input: Graph with edges `(u, v, weight)`, source = $0 \rightarrow$ Output: Array of minimum distances from source.
* **Solution Steps:**
1. Initialize `dist` array of size $V$ with $\infty$, set `dist[src] = 0`. Min-priority queue stores `(distance, node)`. Push `(0, src)`.
2. While queue non-empty: pop `(d, u)`. If $d > \text{dist}[u]$, continue.
3. For each neighbor $(v, w)$ of $u$: if $\text{dist}[u] + w < \text{dist}[v]$, update $\text{dist}[v] = \text{dist}[u] + w$ and push `(dist[v], v)`. Time: $O((V + E) \log V)$, Space: $O(V)$.



**57. Topological Sort (Kahn's Algorithm)**

* **Description:** Provide a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge $u \to v$, node $u$ comes before $v$.
* **Examples:** Input: DAG with edges `[[5, 0], [5, 2], [4, 0], [4, 1], [2, 3], [3, 1]]` $\rightarrow$ Output: `[5, 4, 2, 3, 1, 0]`
* **Solution Steps:**
1. Calculate in-degree for every vertex.
2. Enqueue all vertices with in-degree 0.
3. While queue non-empty: pop node $u$, append to result list. Decrement in-degree of all neighbors of $u$. If neighbor in-degree reaches 0, enqueue it.
4. If result size equals $V$, return result; else cycle detected. Time: $O(V + E)$, Space: $O(V)$.



**58. Detect Cycle in Undirected Graph (Disjoint Set Union)**

* **Description:** Determine if an undirected graph contains at least one cycle using DSU.
* **Examples:** Input: Edges `[[0, 1], [1, 2], [2, 0]]` $\rightarrow$ Output: True
* **Solution Steps:**
1. Initialize DSU structure with `parent[i] = i` and `rank[i] = 0` for all $i \in [0..V-1]$.
2. Iterate through each edge $(u, v)$:
3. Find representative set roots: $r_u = \text{find}(u)$ and $r_v = \text{find}(v)$.
4. If $r_u == r_v$, edge $(u, v)$ connects nodes already in the same connected component, returning True (cycle exists). Else, perform $\text{union}(r_u, r_v)$. Time: $O(E \cdot \alpha(V))$, Space: $O(V)$.



---

### Trie & String Matching

**59. Implement Trie (Prefix Tree)**

* **Description:** Implement data structure supporting `insert(word)`, `search(word)`, and `startsWith(prefix)`.
* **Examples:** `insert("apple")`, `search("apple")` $\rightarrow$ True, `startsWith("app")` $\rightarrow$ True
* **Solution Steps:**
1. Define `TrieNode` containing array/hashmap of child nodes (size 26 for lowercase alphabets) and boolean flag `isEndOfWord`.
2. `insert`: Traverse/create nodes matching word characters. Mark `isEndOfWord = True` at final character node.
3. `search`/`startsWith`: Traverse tree matching query characters. Return False if missing link. `search` checks `isEndOfWord == True` at end; `startsWith` returns True if path completes. Time: $O(L)$ per operation where $L$ is word length.



**60. Maximum XOR of Two Numbers in an Array**

* **Description:** Given integer array, find maximum result of $A_i \oplus A_j$.
* **Examples:** Input: `[3, 10, 5, 25, 2, 8]` $\rightarrow$ Output: 28 ($5 \oplus 25$)
* **Solution Steps:**
1. Build a binary Trie storing 32-bit (or 31-bit) representations of numbers.
2. For each number $num$, insert bits from Most Significant Bit (MSB) to Least Significant Bit (LSB).
3. Iterate numbers again: for current $num$, query Trie by attempting to take opposite bit path ($1 - \text{bit}$) at each position to maximize XOR sum value. Track global maximum. Time: $O(N \cdot 32)$, Space: $O(N \cdot 32)$.



**61. KMP Algorithm (Pattern Searching)**

* **Description:** Search pattern $P$ in text $T$ in linear time by preventing redundant character re-evaluations.
* **Examples:** Input: $T = \text{"ababcabcababv"}$, $P = \text{"ababa"} \rightarrow$ Output: Found index / Not found
* **Solution Steps:**
1. Construct Longest Prefix Suffix (LPS) array for pattern $P$: `lps[i]` holds length of longest proper prefix of $P[0..i]$ that is also suffix. Time: $O(\vert{}P\vert{})$.
2. Traverse text using index $i$ and pattern index $j$.
3. If $T[i] == P[j]$, increment $i, j$. If $j == \vert{}P\vert{}$, pattern found; set $j = \text{lps}[j-1]$.
4. If mismatch $T[i] \neq P[j]$: if $j \neq 0$, set $j = \text{lps}[j-1]$; else increment $i$. Time: $O(\vert{}T\vert{} + \vert{}P\vert{})$, Space: $O(\vert{}P\vert{})$.



---

### Range Queries

**62. Segment Tree (Range Minimum Query & Updates)**

* **Description:** Structure to answer range queries (min/sum) and point updates on array in logarithmic time.
* **Examples:** Input: arr = `[1, 3, 5, 7, 9, 11]`, query Range Min `[1, 3]` $\rightarrow$ Output: 3
* **Solution Steps:**
1. **Build Tree:** Node $k$ covers interval $[L, R]$. Recursively divide array at mid point; node value stored is $\min(\text{left\_child}, \text{right\_child})$. Tree size array bounded by $4N$. Time: $O(N)$.
2. **Range Query $[qL, qR]$:**
* If node interval completely within $[qL, qR]$, return node value.
* If completely outside, return identity value ($\infty$).
* Else, recurse on both left and right children and combine results. Time: $O(\log N)$.


3. **Point Update:** Recurse to leaf corresponding to index $i$, update value, and re-evaluate path to root. Time: $O(\log N)$.



**63. Fenwick Tree / Binary Indexed Tree (BIT)**

* **Description:** Compact structure providing prefix sum calculations and point updates on an array.
* **Examples:** Update index 3 by $+5$, calculate sum of elements from index 1 to 5 $\rightarrow$ Output: Range sum
* **Solution Steps:**
1. Store array `tree` of size $N+1$ (1-indexed).
2. **Point Update `add(index, val)`:** Add `val` to `tree[index]`. Advance index using lowest set bit extraction: $\text{index} += (\text{index} \ \& \ -\text{index})$ repeatedly while $\text{index} \le N$.
3. **Prefix Sum `query(index)`:** Accumulate `tree[index]` sum. Retract index using lowest set bit subtraction: $\text{index} -= (\text{index} \ \& \ -\text{index})$ repeatedly while $\text{index} > 0$. Time: $O(\log N)$ per query/update, Space: $O(N)$.


---