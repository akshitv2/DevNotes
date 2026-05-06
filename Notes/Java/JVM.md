---
parent: Java
nav_order: 1
layout: default
---

# JVM (Java Virtual Machine)

1. ## Basics
    - bytecode: platform independent
    - JVM: platform dependent

2. ## Related concepts:
    - JVM (java virtual machine): Engine that runs the code
    - JRE (java runtime env): JVM + Libs, You only need JRE to be running precompiled java app
    - JDK (java development kit): Contains above 2 as well as javac and support files. Can compile java code

3. ## Components of JVM:
    1. ### Classloader:
        - Loads classes at runtime whenever they're needed (not all at once on init)
        - Only if class is required and not found does it throw NoClassDefFoundError
        - Components:
            1. Bootstrap Classloader:
                - Required to load all other code
                - This is not java code but instead native code
                - Bootstrapping is the process which loads all other processes
            2. Extensions Classloader:
                - Loads all classes from jre/libs i.e. system libs
            3. Application Classloader:
                - Loads the application classes
        - Linking:
            - Performs verification (ensures bytecode is valid)
              - Does integrity check of the .class file and data flow (return types) analysis (within class)
              - Doesn't check target classes yet
            - Preparation (allocates memory for static variables)
            - Resolution (replaces symbolic references with direct references).
    2. ### Runtime Data Area:
        - When memory is discussed most of the time it's about Heap and Stack since that's where most JVM issues occur
        - The JVM organizes memory into several distinct areas during execution:
            1. ### Method Area: 
               - Stores class-level data, including static variables and bytecode for methods.
            2. ### Heap:
               - The primary area for dynamic memory allocation; all objects and their corresponding instance
                    variables are stored here.
               - When one instantiates an object of a class it's put in heap
            3. ### Stack:
               - Each thread has its own stack, storing "frames" that contain local variables and partial results
                    for method execution.
               - Same as method call stack we see in IntelliJ debugger
            4. ### PC Registers:
               - Contains the address of the JVM instruction currently being executed for each thread.
               - Most frequently updated components within the JVM.
            5. ### Native Method Stack:
               - Stores instructions for native methods (written in languages like C or C++).
               - JVM relies on native code to interface with the CPU, GPU, or physical memory and OS
    3. ### Execution Engine:
       - Central component of the JVM that communicates with the underlying OS and hardware to execute the bytecode.
       - Composed of:
         - Interpreter:
           - Reads and executes bytecode instructions one by one. While fast to start, it is slow for repeated code.
         - JIT (Just-In-Time) Compiler:
           - Compiles frequently used bytecode (hotspots) into native machine code to improve performance.
           - The compiled native code is stored in a special area of memory called the Code Cache.
         - Garbage Collector (GC): 
           - Automatically identifies and deletes unreferenced objects from the Heap to free up memory.
    4. ### Garbage Collector:
        - Collects and removes unreferenced objects
        - Mark and Sweep: It "marks" objects that are still in use and "sweeps" (deletes) those that aren't.
        - Types:
            1. ### G1 (Garbage First)
                - Default in modern java (since java 9)
                - Breaks memory into small pieces, clears most garbage filled piece first
                - Balances throughput vs latency i.e. amount of code executed vs pause to clean garbage
            2. ### ZGC (Z Garbage Collector)
                - Scalable, low latency
                - Best for massive datasets
                - clears concurrently, thus taxes CPU
                - ⚠️Only when latency is critical and you have massive RAM
            3. ### Shenandoah
                - RedHat's version of ZGC
                - Even effective at smaller RAM sizes
                - Best for docker envs where memory is released back to virtual computing
    5. ### Java Flight Recorder (JFR)
       - Profiling and event-collection framework built into the Java Virtual Machine (JVM)
       - Designed to gather detailed performance data about a running Java application with minimal overhead (typically less than 1%)
       - Captures discrete events such as thread stalls, GC (Garbage Collection) pauses, CPU usage, and I/O activity.
       - Output:
         - JFR uses a tiered buffering system to handle data before it is written to a file. It does not output human-readable logs; it produces a binary file format (.jfr).
       - Useful for execution telemetry and not application state and business auditing