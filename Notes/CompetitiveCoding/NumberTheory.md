---
nav_order: 2
parent: Competitive Coding
layout: default
---

# Number Theory

- Binary Exponentiation:
    - $$x^n = \begin{cases}
      x \cdot (x^2)^{\frac{n-1}{2}} & \text{, if } n \text{ is odd} \\
      (x^2)^{\frac{n}{2}} & \text{, if } n \text{ is even}
      \end{cases}$$
- Modular Arithematic
    - N = Q*D + R
    - N mod D = R
    - (A + B) mod m = ((A mod m) + (B mod m) ) mod m
- Modular Multiplicative Inverse
- GCD (Greatest Common Divisor):
    - Largest Number that divides two numbers
    - Fastest way:
        - Recursion using mod
        - code:
          ```java
            public static int gcd(int a, int b) {
                if (b == 0)
                    return a;
                else
                    return gcd(b, a % b);
                }
          ```
- LCM (Lowest Common Multiple)
  - A * B = LCM(A,B)*GCD(A,B)
  - LCM(A,B) = (A*B)/GCD(A,B)
- Sieve of Eratosthenes
  - Method to eliminate composite numbers thus sieving primes
  - Efficient Method:
    - From 2 to sqrt(N) mark all multiples as non primes
    - Use array
    - What's left behind is primes
- 