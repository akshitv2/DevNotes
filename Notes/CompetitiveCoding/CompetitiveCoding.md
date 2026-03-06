---
nav_order: 1
parent: Competitive Coding
layout: default
---

# Competitive Coding Tips & Tricks

1. Maps & Other Collections require Autoboxing
    - Autoboxing is slower and access time is between O(logN)-O(1)
    - Instead:
        - If your map is a static dict, use `switch` instead
        - If it's a character map just use an array `new int[128]`
2. Branchless programming is performant but slows down when using `%` and `/`
3. `for(int i:array)` is equally fast but `for(char ch:s.toCharArray())` requires conversion and is slower
4. Java doesn't cache (reliably) map.get(x) and s.charAt(i), better to store in variable than multiple calls
5. CPUs predict next few steps instead of just current instruction. Everytime cpu hits fork in the road i.e. if or while
   or loop it has a chance to guess wrong path and incur Wrong Branch Penalty  
   How to avoid?
    - Use math instead of branching
    - ```java
      int a = 5;
      int b = 10;
      int result = 0;
      if (a < b) {
          result += a;
      } else {
          result += b;
      }
      result += Math.min(a, b); 
      // Internally, many compilers optimize this to a CMOV (Conditional Move) instruction
      ```
    - Loop unrolling:
        - If you have a loop that runs a very small, fixed number of times, you can "unroll" it to remove the overhead
          of the loop counter and the exit condition.
        - ```java
            for (int i = 0; i < 3; i++) { sum += arr[i]; }
            sum = arr[0] + arr[1] + arr[2];
        ```
      