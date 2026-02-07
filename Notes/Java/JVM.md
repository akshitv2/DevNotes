# JVM (Java Virtual Machine)

1. Basics
    - bytecode: platform independent
    - JVM: platform dependent

2. Related concepts:
    - JVM (java virtual machine): Engine that runs the code
    - JRE (java runtime env): JVM + Libs, You only need JRE to be running precompiled java app
    - JDK (java development kit): Contains above 2 as well as javac and support files. Can compile java code

3. Components of JVM:
    1. Classloader:
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
    2. Runtime Data Area:
    3. Execution Engine
    4. Garbage Collector:
       - Collects and removes unreferenced objects
       - Types:
         1. G1 (Garbage First)
            - Default in modern java (since java 9)
            - Breaks memory into small pieces, clears most garbage filled piece first
            - Balances throughput vs latency i.e. amount of code executed vs pause to clean garbage
         2. ZGC (Z Garbage Collector)
            - Scalable, low latency
            - Best for massive datasets
            - clears concurrently, thus taxes CPU
            - ⚠️Only when latency is critical and you have massive RAM
         3. Shenandoah
            - RedHat's version of ZGC
            - Even effective at smaller RAM sizes
            - Best for docker envs where memory is released back to virtual computing