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


1. ## Basics
    1. Input Output:
        - use Scanner with System.in and out in java
            - ```java
          Scanner sc = new Scanner(System.in);
          int age = sc.nextInt();

          System.out.println(age);
          ```
        - input() and print() in python

2. ## Complexity Analysis
    1. Order of Growth
        - Simply the rate at which the algorithm completes a task
        - for 4n2 + 3n + 100
        - After ignoring lower order terms, we get 4n2
        - After ignoring constants, we get n2
        - Hence, order of growth is n2
    2. Asymptotic Analysis
        - Evaluate the performance and efficiency of an algorithm as the input size ($n$) grows arbitrarily large
        - It allows you to state that the algorithm's worst-case running time by declaring bounds
        - Notations:
            - ## Big O ($O$)
              The most important notation is Big O notation.Why it is the most important:
                - Focuses on the Worst Case: Software engineering prioritizes predictability and reliability. Big O
                  defines the upper bound (maximum limit) of execution time.
                - Knowing the absolute longest an algorithm will take ensures systems do not
                  fail or timeout under heavy loads.

              ## Other notations:
                - Big Omega ($\Omega$): Represents the lower bound (Best Case). The algorithm will take at least this
                  much time.
                - Big Theta ($\Theta$): Represents the tight bound. Used only when the best case and worst case grow at
                  the same rate.

3. ## Programming
   1. Recursion
      - function calls itself directly or indirectly
      - Needs a termination condition to not go on infinitely
      - Uses the system call stack to keep track of active function calls.

## Sorting

- In-place Sorting: An in-place sorting algorithm uses constant space for producing the output (modifies the given array
  only. Examples: Selection Sort, Bubble Sort, Insertion Sort and Heap Sort.

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