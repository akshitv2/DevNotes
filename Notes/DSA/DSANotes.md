---
nav_order: 3
parent: DSA
title: DSA
layout: default
---

# DSA

1. ## Recursion
   - A recursive algorithm takes one step toward solution and then recursively call itself to further move. The algorithm
   stops once we reach the solution.
   - Recursive thinking helps in solving complex problems by breaking them into smaller subproblems.
   - Works as a basis for Dynamic Programming and Divide and Conquer algorithms.
   - ℹ️Note: Be sure that there is a termination condition to prevent stack overflow errors
   - The internal systems use a stack because function calling follows LIFO structure, the last called function finishes
     first.
   - 🟢 Recursion provides a clean and simple way to write code.
   - 🔴 Recursion can make the code more difficult to understand and debug
   - 🔴 Recursive programs typically have more space requirements and also more time to maintain the recursion call stack.
   -
   - Example:
       - The Problem: The Staircase Variations
           - You are standing at the bottom of a staircase with $n$ steps. You can climb either 1 step, 2 steps, or 3 steps
             at a time. Write a recursive function to calculate the total number of distinct ways you can reach the top.
           - Constraints
               - $n \ge 0$
               - If $n = 0$, there is 1 way (staying put).
               - If $n < 0$, there are 0 ways.
       - Solution:
       ```java
       static int staircase(int n){
             if(n == 0){
                 return 1;
             }else if(n <0 ){
                 return 0;
             }else{
                 return staircase(n-3) + staircase(n-2) + staircase(n-1);
             }
         }
       ```
   - Applications:
     - Tree and Graph Traversal: Used for systematically exploring nodes/vertices in data structures like trees and graphs.
     - Sorting Algorithms: Algorithms like quicksort and merge sort divide data into subarrays, sort them recursively, and merge them.
     - Divide and Conquer Algorithms
2. ## Easy Math
    - Even or Odd: Mod 2 == 1 or 0
    - Sum of first n natural numbers: n(n+1)/2