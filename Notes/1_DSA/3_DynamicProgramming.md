---
parent: DSA
nav_order: 2
---

# Dynamic Programming

## 1. What Problem Is DP Actually Solving?

Before touching syntax or code, understand the *shape* of problems DP exists for.

Most problems that need DP are, at heart, **search problems**: you're choosing among many possible decisions (
include/exclude an item, go left/right, cut here/there) and each choice branches into more choices. If you drew every
possible sequence of decisions as a tree, you'd get an exponential number of paths.

DP is not a new way of solving problems — it's an optimization applied to **brute-force recursive search**, exploiting
the fact that the recursion tree often has massive redundancy: the same sub-question gets asked over and over in
different branches.

So the mental model is:

> Brute force recursion (exponential) → notice repeated subproblems → cache results → polynomial time.

This is why you should never start by memorizing "DP patterns." Start by writing the brute-force recursive solution. DP
falls out of that naturally.

---

## 2. The Two Pillars: Optimal Substructure & Overlapping Subproblems

A problem is solvable with DP only if it has **both** of these properties. Miss either one and DP either doesn't apply
or gives you no speedup.

### 2.1 Optimal Substructure

The optimal solution to a problem can be constructed from optimal solutions to its subproblems.

Example: shortest path from A to C through B. If A→B→C is the shortest path from A to C, then A→B must be the shortest
path from A to B, and B→C must be the shortest path from B to C. You can't have a globally optimal path built from a
locally suboptimal segment (in a graph with non-negative edges, at least).

Counter-example where this breaks: **longest simple path** in a graph does *not* have optimal substructure in the usable
sense, because the "optimal" sub-path might reuse a vertex, making it invalid for the bigger path. That's part of why
longest-simple-path is NP-hard while shortest-path is easy — the substructure property fails.

**Test you can apply:** Ask "if I knew the best answers to the smaller versions of this problem, could I *combine*
them (with a simple formula/decision) to get the best answer to the bigger problem?" If yes → optimal substructure
holds.

### 2.2 Overlapping Subproblems

When you break the problem down recursively, the *same* subproblem (same parameters) reappears many times across
different branches of the recursion tree.

Example: computing Fibonacci(5) via naive recursion calls Fibonacci(3) twice, Fibonacci(2) three times, etc. The
subproblems overlap.

Contrast with **merge sort**, which also breaks a problem into subproblems and combines them — but the subproblems (sort
left half, sort right half) never overlap; they're disjoint. That's why merge sort is "divide and conquer," not DP. DP
is best understood as **divide and conquer + memoization**, applicable specifically when the divisions aren't disjoint.

**Rule of thumb:**

- Optimal substructure + non-overlapping subproblems → Divide and Conquer
- Optimal substructure + overlapping subproblems → Dynamic Programming

---

## 3. The Recursion Tree: Seeing the Redundancy

Take Fibonacci as the simplest possible illustration.

```
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2)
│   │   │   ├── fib(1)
│   │   │   └── fib(0)
│   │   └── fib(1)
│   └── fib(2)          <-- recomputed
│       ├── fib(1)
│       └── fib(0)
└── fib(3)               <-- recomputed
    ├── fib(2)           <-- recomputed again
    │   ├── fib(1)
    │   └── fib(0)
    └── fib(1)
```

fib(2) is computed 3 times. fib(1) is computed 5 times. As n grows, the number of redundant calls grows exponentially (
the naive recursion is O(2^n)), even though there are only n+1 *distinct* subproblems (fib(0) through fib(n)).

This gap — "exponentially many calls, but only polynomially many *distinct* subproblems" — is exactly what DP exploits.
If you cache each distinct subproblem's answer the first time you compute it, every subsequent call becomes O(1) lookup.

This is the single most important diagram to internalize before doing any DP problem: **draw the recursion tree, and
look for repeated nodes.**

---

## 4. Memoization (Top-Down) vs Tabulation (Bottom-Up)

Both are DP. They're the same underlying idea implemented in opposite directions.

### 4.1 Memoization (Top-Down)

You keep the natural recursive structure, but before computing a subproblem, check a cache (usually a hash map or
array). If it's there, return it. If not, compute it, store it, then return it.

```python
memo = {}
def fib(n):
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

Characteristics:

- Feels like "brute force + a cache." Easiest to derive from the naive solution.
- Only computes subproblems that are actually needed (lazy) — useful when the full state space is large but only a
  fraction of it is reachable.
- Uses the call stack → risk of stack overflow for deep recursion.
- Slightly more overhead per call (function calls, hashing).

### 4.2 Tabulation (Bottom-Up)

You identify the smallest subproblems, solve them first, and iteratively build up to the answer for the full problem,
storing every result in a table (usually an array).

```python
def fib(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

Characteristics:

- No recursion → no stack overflow, generally faster in practice (no function call overhead).
- Computes *all* subproblems up to the target, even ones you might not need — can be wasteful if the reachable state
  space is much smaller than the full table.
- Requires you to figure out a valid **order** of evaluation ahead of time — every subproblem must be solved before
  something that depends on it. This ordering question is often the conceptually hardest part of tabulation.
- Naturally lets you optimize space afterward (see §7), since you can see explicitly which past rows/values you actually
  need.

### 4.3 Which to use?

Start with memoization if you're deriving the solution from scratch — it's a mechanical transformation of the
brute-force recursion (add a cache check + cache write). Once it works, convert to tabulation if you need the
performance/space benefits or want to avoid recursion depth issues. Many people design in memo form and "ship" in
tabulation form.

---

## 5. Defining "State" — The Real Skill of DP

The hard part of DP is almost never the loop or the recurrence arithmetic. It's figuring out **what a subproblem even is
** — i.e., what minimal set of parameters uniquely identifies a subproblem, so that:

1. The answer to the full problem can be expressed in terms of subproblems' answers (recurrence).
2. Two calls with the same parameters really do have the same answer (this is what makes caching valid).

Ask this sequence of questions when facing a new DP problem:

- **What am I choosing at each step?** (include item or not, which index to move to, how much to spend, etc.)
- **What information from the past decisions could possibly affect future decisions/answers?** That information is your
  state.
- **What's varying between subproblems?** Usually an index into an array/string, and some resource constraint (remaining
  capacity, remaining budget, number of moves used, etc.)

Example — 0/1 Knapsack: state is `(i, remaining_capacity)` — "considering items from index i onward, with this much
capacity left, what's the best value achievable?" You need *both* pieces: the index alone doesn't tell you how much room
you have left, and capacity alone doesn't tell you which items are still available to consider.

If your recurrence doesn't correctly disambiguate subproblems (e.g., you drop a needed dimension), you'll either get
wrong answers or accidentally reintroduce exponential blowup because "different" subproblems collide into the same cache
key incorrectly, or genuinely different problems don't get merged when they should.

**Common state dimensions you'll see repeatedly:**

- Position/index in an array or string (often more than one, e.g. two-pointer DP over two strings)
- Remaining capacity/budget/weight
- Whether some binary condition is true (e.g., "have I already used my one skip," "am I currently holding a stock")
- Count of something used so far (k transactions, k changes allowed)
- A bitmask representing a subset of used elements (common in "visit all cities" style problems)

---

## 6. The Recurrence — Connecting Subproblems

Once state is defined, the recurrence is the rule that expresses `answer(state)` in terms of
`answer(smaller/related states)`.

General derivation method:

1. Pick an arbitrary valid state.
2. Ask: "What are all the *choices* available at this state?"
3. For each choice, express what state you transition to, and what happens to your answer/cost as a result of that
   choice.
4. Combine: the answer for the current state is the best (min/max/sum/count, depending on the problem) over all choices.

Example — 0/1 Knapsack recurrence:

```
dp(i, cap) =
    if i == n: 0
    else:
        skip = dp(i+1, cap)
        take = value[i] + dp(i+1, cap - weight[i])   [only valid if weight[i] <= cap]
        dp(i, cap) = max(skip, take)
```

Notice the recurrence is really just "the brute force decision tree," written as a formula instead of code. That's the
point — you're not inventing something new, you're formalizing the recursion you'd already write.

**Base cases** matter as much as the recurrence — they're the "smallest subproblems" that don't need further breakdown,
and if defined wrong, everything built on top is wrong. Always check them explicitly: what happens at i == n, cap == 0,
empty string, etc.

---

## 7. Space Optimization

Once tabulation works, look at the recurrence: does `dp[i]` only depend on a constant number of previous rows/entries (
e.g., `dp[i-1]`, `dp[i-2]`)? If so, you don't need the whole table — keep only what's needed.

Fibonacci needs only the last two values → O(1) space instead of O(n).
Many 2D DPs (e.g., edit distance, knapsack) only need the *previous row* → O(n) instead of O(n·m) space, sometimes
further reducible to O(min(n,m)) by iterating over the smaller dimension.

This optimization is usually done *after* getting a correct tabulated solution — don't try to prematurely compress state
while still debugging correctness.

---

## 8. When DP Does NOT Apply / Common Misconceptions

- **Overlapping subproblems without optimal substructure**: DP doesn't help; you may need other techniques.
- **Optimal substructure without overlapping subproblems**: plain divide and conquer or greedy may suffice; DP just adds
  unnecessary memoization overhead.
- **Greedy vs DP confusion**: Greedy also builds a solution from local decisions, but commits to the locally best choice
  *without* considering all alternatives, and never revisits it. DP considers *all* valid choices at each state and only
  commits once it has compared them (implicitly, through the recurrence). If a problem admits a greedy solution, it's
  usually more efficient than DP — but proving greedy correctness is often harder than just writing the DP. A useful
  habit: try to find a counter-example to the greedy approach; if you can't easily find one, greedy might work, but if
  you find one instantly, you likely need DP.
- **Thinking DP = 2D table**: state can be 1D, 2D, 3D, a bitmask, a tree node, a graph node — table shape follows from
  state definition, not the other way around.

---

*(End of Part 1 — reply length limit reached. Continuing in Part 2 with: worked derivation walkthroughs for classic
problems using this framework — Fibonacci, Climbing Stairs, 0/1 Knapsack, Longest Common Subsequence, Coin Change; DP on
strings/sequences patterns; interval DP; DP on trees; DP on graphs (Bellman-Ford, DAG shortest/longest path); bitmask
DP; how to recognize DP from problem phrasing; and a practice framework/checklist for approaching new problems
methodically.)*

## 9. Worked Derivations

The point of these isn't "here's the answer" — it's watching the *framework from Part 1* produce the solution
mechanically. Every example follows the same steps:

1. What am I choosing?
2. What state fully describes a subproblem?
3. What's the recurrence (in terms of smaller states)?
4. What are the base cases?
5. Memoize, then tabulate, then optimize space.

### 9.1 Climbing Stairs

*You can climb 1 or 2 steps at a time. How many distinct ways to reach step n?*

- **Choice:** at each step, take a 1-step or 2-step move.
- **State:** just the current step `i` — nothing else affects how many ways remain.
- **Recurrence:** to reach step `i`, your last move was either from `i-1` (a 1-step) or `i-2` (a 2-step). So:
  `ways(i) = ways(i-1) + ways(i-2)`
- **Base cases:** `ways(0) = 1` (one way: do nothing), `ways(1) = 1`.

This is *literally* Fibonacci with different base cases. Recognizing "this is secretly Fibonacci" is a common and useful
move — many DP problems reduce to recurrences you've already seen, just with a different base case or a different
combination rule (sum vs max vs count).

Tabulated, O(n) time, and since `ways(i)` only needs the last two values, O(1) space.

### 9.2 0/1 Knapsack

*n items, each with weight[i] and value[i]. Capacity W. Maximize value without exceeding W. Each item used at most
once.*

- **Choice:** for each item, take it or skip it.
- **State:** `(i, cap)` — which item we're considering, and capacity remaining. Both are necessary (see §5 in Part 1):
  the index alone doesn't tell you what room is left, and capacity alone doesn't tell you which items remain to choose
  from.
- **Recurrence:**
  ```
  dp(i, cap) = 0                                    if i == n
  dp(i, cap) = dp(i+1, cap)                         if weight[i] > cap   (can't take it)
  dp(i, cap) = max( dp(i+1, cap),                   (skip)
                     value[i] + dp(i+1, cap-weight[i]) )  (take)   otherwise
  ```
- **Base case:** `dp(n, cap) = 0` for any cap (no items left → no value).

Tabulated as a 2D table (rows = items, columns = capacity 0..W), filled from `i = n` down to `0` (or reindexed to go 0
to n — direction depends on how you set it up, just make sure `dp(i+1, ...)` is always computed before `dp(i, ...)`).

**Space optimization:** each row only depends on the row below it (`i+1`), so you can collapse to a single 1D array of
size `W+1`, iterating capacity in the right direction (right-to-left, specifically, to avoid reusing an item within the
same row — this subtlety is a classic bug source; think about *why* left-to-right would be wrong here: it would let one
item's value be added twice into the same row of computation).

### 9.3 Longest Common Subsequence (LCS)

*Given strings A (length n) and B (length m), find the length of the longest subsequence common to both.*

- **Choice:** compare characters `A[i]` and `B[j]` from the end (or start) — either they match (use both), or they
  don't (skip one from either string).
- **State:** `(i, j)` — how much of A and how much of B remain to be considered. Two indices are needed because progress
  through A and progress through B are independent quantities.
- **Recurrence:**
  ```
  lcs(i, j) = 0                                          if i == n or j == m
  lcs(i, j) = 1 + lcs(i+1, j+1)                          if A[i] == B[j]
  lcs(i, j) = max(lcs(i+1, j), lcs(i, j+1))              if A[i] != B[j]
  ```
- **Base case:** either string exhausted → 0.

This is the prototype for a huge family: **2D DP over a pair of sequences**. Edit distance, longest common substring,
longest palindromic subsequence, and shortest common supersequence all use a close variant of this exact `(i, j)` state
and a similar match/mismatch branching structure. Once you've internalized this one, the others are minor variations —
learn *this* deeply rather than memorizing all of them separately.

Space: each `(i, j)` depends only on row `i+1`, so 2D → O(min(n, m)) with rolling array.

### 9.4 Coin Change (fewest coins to make amount)

*Given coin denominations and a target amount, find the minimum number of coins to make that amount (or determine
impossible).*

- **Choice:** which coin to use next.
- **State:** just the remaining `amount` — which coins you've already used doesn't matter, only how much is left to
  make.
- **Recurrence:**
  `minCoins(amt) = 1 + min( minCoins(amt - c) )` for every coin `c <= amt`, taking the best over all valid coins.
- **Base case:** `minCoins(0) = 0`. `minCoins(amt) = infinity` if no coin ≤ amt (unreachable), which propagates up as "
  impossible."

Notice this state is **1D**, unlike knapsack's 2D — because you're allowed to reuse coins (unbounded), there's no "index
into item list" needed; you're not tracking which coins remain available, since all remain available always. Comparing
this to 0/1 Knapsack directly is a good exercise: **why does removing the "used once" restriction collapse a dimension
of the state?** Because "which item" stops mattering — only "how much is left" does.

---

## 10. DP Pattern Families

Rather than treating every LeetCode-style problem as unique, most DP problems belong to a small number of *shape*
families. Recognize the shape, and you mostly know the state definition already.

### 10.1 Linear/Sequence DP (1D)

State = position in a single array/string, sometimes plus a small extra flag or count.
Examples: Climbing Stairs, House Robber, Maximum Subarray, Longest Increasing Subsequence.
Recurrence typically looks at a fixed small window back (`i-1`, `i-2`) or scans all `j < i`.

### 10.2 Two-Sequence DP (2D grid over indices)

State = `(i, j)`, one index per sequence.
Examples: LCS, Edit Distance, String Interleaving.
Visualize as filling a 2D grid, usually row by row.

### 10.3 Interval DP

State = `(i, j)` representing a *contiguous subrange* of a single array/string (not two arrays — the range boundaries of
the same array).
Examples: Matrix Chain Multiplication, Burst Balloons, Palindrome Partitioning, optimal BST.
Key structural difference from §10.2: the recurrence usually involves picking a "split point" `k` between `i` and `j`
and combining `solve(i,k)` and `solve(k,j)`:

```
dp(i,j) = min over k in (i,j) of  [ dp(i,k) + dp(k,j) + cost(i,j,k) ]
```

Fill order matters a lot here: you must process **shorter intervals before longer ones**, since `dp(i,j)` depends on
strictly smaller sub-intervals. This is usually implemented by iterating over interval *length* as the outer loop, not
the start index.

### 10.4 DP on Subsets / Bitmask DP

State includes a bitmask representing which elements of a set have been used/visited so far.
Examples: Traveling Salesman (exact DP solution), assigning tasks to workers, "visit all X" problems.
State: `(mask, i)` — "having already visited exactly the set of nodes in `mask`, currently at node `i`." Size of state
space is O(2^n · n) — exponential in n, but far better than trying all n! permutations directly (which is what brute
force does). This is a case where DP turns "factorial" into "exponential" rather than into "polynomial" — still an
enormous win, but recognize DP doesn't always get you all the way to polynomial time; sometimes the honest ceiling for
the problem is exponential, and DP just gets you to the *best possible* exponential.

### 10.5 DP on Trees

State is defined per node, usually representing "the best answer for the subtree rooted here," sometimes with an extra
dimension for a constraint (e.g., "best answer in this subtree if the parent is/isn't selected").
Examples: House Robber III (binary tree version), maximum independent set in a tree, tree diameter.
Computed via post-order DFS: you can't know a node's answer until you know both children's answers, so children must be
resolved first (this *is* the topological order for tree DP — no need to think about it separately, DFS naturally goes
leaves-first).

### 10.6 DP on DAGs / Graphs

Many DP problems are literally shortest/longest path in a DAG in disguise, even when not phrased as a graph problem.
Longest Increasing Subsequence, for instance, can be modeled as: nodes = array elements, edges `i → j` when `i < j` and
`A[i] < A[j]`, and you want the longest path.

General graph DP recurrence: `dp(node) = combine( dp(neighbor) for neighbor in transitions(node) )`. This only works
directly (without extra machinery) when the graph is a **DAG** — cycles break the "smaller subproblems first" ordering,
which is why graphs with cycles and negative structure need Bellman-Ford-style relaxation (iterating until convergence)
instead of a single clean topological pass.

**Recognizing this pattern is valuable**: if you can phrase a problem as "nodes are states, edges are valid transitions
with a cost, find best path," you can often import all your graph algorithm intuition directly.

---

## 11. Recognizing "This Needs DP" From Problem Phrasing

Signal words/phrases and what they suggest:

| Phrasing                                                                             | Suggests                                             |
|--------------------------------------------------------------------------------------|------------------------------------------------------|
| "minimum/maximum number of ways"                                                     | counting DP                                          |
| "is it possible to..."                                                               | boolean/reachability DP                              |
| "longest/shortest subsequence/substring/path satisfying..."                          | sequence DP, often 1D or 2D                          |
| "partition into..."                                                                  | interval DP or subset DP                             |
| Constraints mention small n (≤ 20) with "subsets," "visit all," "each used once"     | bitmask DP                                           |
| "at most k operations/changes/transactions allowed"                                  | extra state dimension for remaining budget k         |
| Choices with a **cost or reward per decision**, made repeatedly over a sequence      | classic 1D/2D sequence DP                            |
| Problem *looks* like brute-force recursion/backtracking would work but is "too slow" | strong DP candidate — go write the brute force first |

**A genuinely reliable test:** write the brute-force recursive/backtracking solution regardless of complexity concerns.
Then check: does it re-solve identical `(parameters)` calls repeatedly? If yes, it's DP — add memoization. If every call
is a genuinely distinct subproblem (never repeats), it's just divide-and-conquer or plain backtracking, and memoization
won't help (it'll just add overhead with a 100% cache-miss rate).

This is more reliable than pattern-matching from a table, because it's actually testing for the defining property (§2.2)
rather than guessing from surface phrasing.

---

## 12. A Practice Framework / Checklist

When you hit a new problem you suspect is DP, work through these in order — don't skip to coding:

1. **Write the brute force.** Recursive, exponential, doesn't matter. What are you choosing at each step? What's the
   base case where you stop?
2. **Identify the parameters that change between recursive calls.** These are your candidate state variables.
3. **Check overlap.** Do identical `(state)` tuples get hit more than once across different call paths? Sketch a small
   recursion tree by hand if unsure.
4. **Check optimal substructure.** Can you build the best answer for a state purely from the best answers of the states
   it transitions to (no need to know *how* those sub-answers were achieved, just their value)?
5. **Write the recurrence formally**, including all base cases explicitly.
6. **Memoize** the brute force (minimal-diff change: add a cache dict, check/set it).
7. **Verify correctness** against brute force on small inputs.
8. **Convert to tabulation** if needed: figure out a valid fill order (usually "smaller state values before larger,"
   e.g., smaller index before larger, shorter interval before longer).
9. **Optimize space** if the recurrence only touches a small, fixed window of previous states.

Steps 1–5 are "the thinking." Steps 6–9 are "the mechanical part." Most people's difficulty with DP comes from rushing
steps 1–5 and trying to pattern-match a table shape immediately — resist that; the derivation is always available if you
actually do steps 1–5 honestly.

---

## 13. Summary — The One-Paragraph Version

DP is memoized brute-force recursive search, applicable exactly when a problem has optimal substructure (bigger answers
built cleanly from smaller ones) and overlapping subproblems (the same smaller question gets asked repeatedly). The
entire discipline of "doing DP" is: define state precisely enough to make the recurrence valid and small enough to make
caching worthwhile, derive the recurrence by listing every choice available at a state, nail the base cases, then choose
top-down memoization (simple, lazy) or bottom-up tabulation (faster, needs an explicit fill order) as an implementation
detail — not a conceptual one. Everything else (knapsack, LCS, interval DP, bitmask DP, tree DP) is the same idea
wearing different state shapes.
