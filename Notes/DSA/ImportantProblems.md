---
nav_order: 4
parent: DSA
title: DSA Problems Quick
layout: default
---

| x  | Problem                                                    | Solution                                                                                                                                          |
|----|------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| 🟢 | Check Substring of Other                                   | Loop String B over A, check if B in A at every position                                                                                           |
| 🟠 | Check Substring of Other                                   | KMP Algo                                                                                                                                          |
|    |                                                            | The Rule: When a mismatch occurs, use precomputed table to find the longest matching prefix that is also a suffix of the pattern analyzed so far. |
|    |                                                            | The Action: Shift the pattern rightward to align that prefix with the suffix in the text, allowing the text pointer to never move backward.       |
| 🟢 | Stock with 1 transaction [7, 10, 1, 3, 6, 9, 2]            | Go right to left, see highest in future compared to current price = 9-1                                                                           |
| 🟢 | Stock with Multiple transaction                            | You're essentially buying and selling at every price change except when it goes down                                                              |
|    | [100, 180, 260, 310, 40, 535, 695]                         | Since this is theoretical you can you terminate at high point, rather than holding loss                                                           |
| 🟢 | First non repeating char in string                         | Map of all chars with -2 default state, loop over array and add indexes to each, -1 if repeat. Return lowest non negative index char              |
| 🟢 | Majority element i.e. appears more than n/2 times in array | Maintain count map and check for each                                                                                                             |
| 🟠 | Majority element i.e. appears more than n/2 times in array | Moore voting algo, maintain a cursor and counter, +1 on same as cursor -1 on different. Check finally if cursor appears more than n/2             |
| 🟠 | Majority element i.e. appears more than n/2 times in array | Moore voting algo, maintain a cursor and counter, +1 on same as cursor -1 on different. Check finally if cursor appears more than n/2             |
| 🟢 | Sorted subsequence of size 3                               | Make a smallest and greatest array. Smallest go left -> right putting smallest till this element, Greatest right -> left greatest till this       |
|    | if an array find all a[i] < a[j] < a[k] where i < j < k    | Finally go through all 3 and print where smallest[i]<a[i]<greatest[i]                                                                             |
| 🟢 | Count Strictly Increasing Subarrays (only continous)       | Count how many numbers in array increasing, number of subarrays of n(n+1)/2                                                                       |
|    | arr = [1, 4, 5, 3, 7, 9], output: 6                        | since subarrays = n-1 + n-2+ n-3 ... +1                                                                                                           |
| 🟠 | Next Permutation [2, 4, 1, 7, 5, 0] -> [2, 4, 5, 0, 1, 7]  | Find first number from right which is arr[i]<arr[i+1], this needs to be replaced with the next biggest element                                    |
|    |                                                            | Rest of the array becomes sorted automatically, just reverse the rest                                                                             |
| 🟢 | Maximum Subarray Sum [2, 3, -8, **7, -1, 2, 3**] -> 11     | Max can only be formed by positive sequence, if a negative is too negative to bridge the gap start over                                           |
|    |                                                            | Maintain a runningsum which resets on going -ve                                                                                                   |
| 🟠 | Sum Of All Subarrays                                       | Counting Technique                                                                                                                                |
|    |                                                            | For each containing index i arrays can start from (i+1) places and end at (n-i) places so solution at each index = (i+1)*(n-i)                    |
| 🟠 | Maximum Product of Subarray sequence                       | Maintain largest and smallest number possible till i (since i can flip it if i is negative)                                                       |
|    | [-2, **6, -3, -10**, 0, 2] -> 180                          | Finally return largest overall                                                                                                                    |
| 🟢 | Sum of Diagonals of 2D array                               | Just know diagonals rule are i == j  and i+j == n-1                                                                                               |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |
|    |                                                            |                                                                                                                                                   |