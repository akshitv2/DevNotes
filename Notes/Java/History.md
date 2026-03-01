---
parent: Java
nav_order: 2
layout: default
---

# History

## Phases

1. Sun Microsystems owned:
    - WORA ("Write Once, Run Anywhere")
    - Two types of Java:
        - Java SE: Consumer Applications libraries only
        - Java EE: Propreitary Libraries for uses like JPA, DB etc
2. Spring Introduction:
    - Spring decomposed giant EE servers into small libraries to use as need
    - Used Inversion of control
    - Blurred SE and EE
3. Oracle Acquisition of Sun (2010)
    - Legal battle against Google
    - Oracle gave up managing Java EE and donated to Eclipse Foundation
4. Jakarta EE: Modern Ecosystem
    - Oracle Refused to give up javax.* so Eclipse created jakarta.*
    - Java SE (The Language): Still managed by Oracle (via OpenJDK)
        - Comes with a price tag so companies created their own: Temurin by Eclipse, Corretto by Amazon, Azul by Azul
    - Jakarta EE (The Specs): Managed by the community
    - Spring Boot: The dominant framework that glues them both together
      Note: Eclipse was created then open sourced by IBM (to eclipse the sun 😂)

## Features Added in Versions:
1. Java 8 (2014) - Functional Update:
   - Lambda Expressions
   - Stream API
   - Optional Class
   - Default Methods
2. Java 11 (2018) - Consolidation and Clean up:
   - `var` for Lambda Parameters
   - new HTTP Client (Non blocking API client)
   - Removal of Java EE/CORBA
3. Java 17 (2021) - Data Oriented:
   - Records
   - Sealed Classes
   - Pattern Matching for `instanceof`
   - Text Blocks using `"""`
4. Java 21 (2023) - Performance & Concurrency:
   - Virtual Threads
   - Sequenced Collections
   - Record Patterns
   - Pattern Matching for `switch`
5. Java 25 (2025) :
   - Scoped Values: Alternative to ThreadLocal
   - Structured Concurrency
   - Flexible Constructor Bodies
   - Module Import Declarations
