---
parent: Competitive Coding
layout: default
---

# Dynamic Programming

Mainly an optimization over plain recursion.  
Can be used whenever there is a recursive solution that has repeated calls for the same inputs.

1. Top-Down Dynamic Programming (Memoization)
    - Top-down is a strategy where you solve a large problem by breaking it down into smaller sub-problems.
    - Optimize the recursive solution by storing the results of already solved subproblems in a memoization table.
    - Reuse the stored result instead of recomputing it
    - **Top-down always implies using recursion.**
    - "memoization" (like we are writing in a memo pad)

2. Bottom-Up Dynamic Programming (Tabulation)
    - Bottom-up Dynamic Programming is a method where you solve a problem by first solving its smallest possible
      sub-problems, and then using those answers to build up to the main problem.
    - **Bottom-up dynamic programming is explicitly designed to avoid recursion entirely.**

- In interviews, bottom-up dynamic programming is generally preferred, due to efficiency, optimization, and this
  approach demonstrating advanced mastery.
    - Predictable Performance: Bottom-up guarantees that every sub-problem is visited in a strict, predictable linear
      order.
    - Space Optimization: In many bottom-up solutions, you only need the results from the previous row or the last few
      variables to compute the current state.
    - Avoids Stack Overflow (Call Stack Overhead)

## Examples:

1. Fibbonaci
    - Bottom Up:
    - ```java
      class GFG {
        static int nthFibonacci(int n) {
      // base cases
        if (n <= 1) return n;
      
              int[] dp = new int[n + 1];
      
              dp[0] = 0;
              dp[1] = 1;
      
              // solving the smaller problems first
              // and finally solving the complete problem
              for (int i = 2; i <= n; ++i) {
                  dp[i] = dp[i - 1] + dp[i - 2];
              }
      
              return dp[n];
          }
      
          public static void main(String[] args) {
              int n = 5;
              int result = nthFibonacci(n);
              System.out.println(result);
          }
      }
      ```

## Problems:

## 1. 0-1 Knapsack

Given **N** items with weights $w_i$ and values $v_i$, and a maximum weight **W**, determine the maximum
value $\sum_{i=1}^{k} v_i$ for each subset of items of size $k$ $(1 \le k \le N)$ while
ensuring $\sum_{i=1}^{k} w_i \le W$.

## Solution:

```java
static int getDP(int[][] dp, int i, int j) {
    if (i < 0 || j < 0) {
        return 0;
    } else {
        return dp[i][j];
    }
}

static int knapsack(int[] weights, int[] values, int capacity) {
    int[][] dp = new int[values.length][capacity + 1];

    for (int i = 0; i < weights.length; i++) {
        for (int curCap = 1; curCap <= capacity; curCap++) {
            if (curCap - weights[i] >= 0) {
                dp[i][curCap] = Math.max(getDP(dp, i - 1, curCap), getDP(dp, i - 1, curCap - weights[i]) + values[i]);
            } else {
                dp[i][curCap] = getDP(dp, i - 1, curCap);
            }
        }
    }

    ezprint(dp, new int[]{1, 2, 3, 4}, new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8});
    return dp[values.length - 1][capacity];
}
```

## 2.

## 