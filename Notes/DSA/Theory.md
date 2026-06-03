---
nav_order: 3
parent: DSA
layout: default
---

# Theory

1. ## Array
    1. Questions:
        1. IsSorted:
            - Iterate 1 to n making sure i+1 >= i element
        2. Reverse:
            - Start from both ends, use temp to swap
        3. Reverse An Array in groups:
            - Solved in LeetCode practice
        4. Rotate an array  (clockwise or counter)
            - Store overflow in a separate array and rotate others, add overflow separately
        5. Generating all subarrays
            - Recursively combine while moving ahead in terms of index
1. ## String
1. ## Matrix


1. Complexity Analysis
   ## The Most Important Notation: Big O ($O$)
   The most important notation is Big O notation.Why it is the most important:
    - Focuses on the Worst Case: Software engineering prioritizes predictability and reliability. Big O defines the
      upper
      bound (maximum limit) of execution time.
    - Knowing the absolute longest an algorithm will take ensures systems do not
      fail or timeout under heavy loads.

   ## Other notations:
    - Big Omega ($\Omega$): Represents the lower bound (Best Case). The algorithm will take at least this much time.
    - Big Theta ($\Theta$): Represents the tight bound. Used only when the best case and worst case grow at the same
      rate.

## Sorting

- In-place Sorting: An in-place sorting algorithm uses constant space for producing the output (modifies the given array
only. Examples: Selection Sort, Bubble Sort, Insertion Sort and Heap Sort.
