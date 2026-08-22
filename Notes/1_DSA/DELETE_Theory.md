---
nav_order: 99
parent: DSA
layout: default
title: DELETE
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
- ## Algos:
    - **Insertion sort** picks an element and carries it through to its place on the sorted side inserting it there
        - Best case: O(n)
            - Would terminate instantly in sorted arrays because each element before would be smaller
    - **Bubble sort** freely replaces which element it is carrying if it finds bigger and bubbles them up
        - Best Case: O(n)
            - We have early termination flag if no swaps were made
    - **Selection sort** goes through the entire thing and selects the smallest one
        - Best Case: O(n<sup>2</sup>)
            - Still looks every single time if something smaller exists in sorted array
- Quick sort
- Merge sort
- 