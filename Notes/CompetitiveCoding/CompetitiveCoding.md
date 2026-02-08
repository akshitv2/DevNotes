# Competitive Coding Tips & Tricks

1. Maps & Other Collections require Autoboxing
   - Autoboxing is slower and access time is between O(logN)-O(1)
   - Instead:
     - If your map is a static dict, use `switch` instead
     - If it's a character map just use an array `new int[128]`
2. Branchless programming is performant but slows down when using `%` and `/`
3. `for(int i:array)` is equally fast but `for(char ch:s.toCharArray())` requires conversion and is slower
4. Java doesn't cache (reliably) map.get(x) and s.charAt(i), better to store in variable than multiple calls