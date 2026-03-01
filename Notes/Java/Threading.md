---
parent: Java
nav_order: 3
layout: default
---

# Threading in Java

1. ### Thread
    - Smallest unit of execution
2. ### Lifecycle:
    - New: Created but not started
    - Runnable: when `start()` is called and waits for CPU to run it
    - Running: Cpu executes `run()` method.
    - Blocked/Waiting: Waiting for resource
    - Terminated: Thread finishes execution
3. ### Synchronization:
    - Locks code to be only accessed by one thread at a time
    - Prevents Race Condition
    - Keyword: `synchronized`
4. ### `start()` vs. `run()`:
    - `start()` sets the code to be picked up by the CPU to be multithreaded
    - `run()` just runs the code in the same thread you call
5. ### `Runnable` vs `Thread`:
    - Difference between implementing an interface (Runnable) and extending a class (Thread)
    - Since only class can be extended in java, interface is preferred
    - ℹ️Note: In real world we don't actually create threads and instead create thread pools where we hand runnable to
      free threads in the pool
6. ### ThreadPool and Executor:
    1. ThreadPool:
        - Managed collection of worker threads
            - 🟢Reuses existing threads skipping creation and termination
            - 🟢Prevents spawning too many threads and Out of memory issue
            - 🟢Easier to manage
        - Components:
            - Threads
            - Work Queue
            - Rejection Policy: i.e. what happens if queue is full
    2. Executor:
        - part of `java.util.concurrent`
        - Functional Heirarchy:
            - `Executor`: simple interface with execute(Runnable) method
            - `ExecutorService` manages pool, you just submit tasks
    3. How to Use these?
        - Create a pool i.e. ExecutorService
        - Pass Runnable or Callable
        - ℹ️Callable provides a Future object back
        - Shutdown executor (needed to exit JVM)
7. ### `Callable` and `Future`:
    - Runnable: Return type void, can't return a result
    - To get a response use callable and future

8. ### `CompletableFuture`
    - Using Future one can get result using `.get()`
    - Next task must be designated by main thread and blocks it
    - Solution:CompletableFuture
        - Chains tasks together
        - Non Blocking
        - Allows manual completion
    - Example:
        - ```java
          CompletableFuture.supplyAsync(() -> "Data Ready")
          .thenApply(data -> data + " - Processed")
          .thenAccept(finalResult -> System.out.println(finalResult))
          .exceptionally(ex -> {
          System.out.println("Error: " + ex.getMessage());
          return null;
          });
            System.out.println("Main thread is free to do other things!");
          ```
9. ### Virtual Threads (Project Loon)
    - java.lang.Thread are platform threads, essentially 1:1 mapped to hardware threads
    - During IOs and waits, thread sits idle in blocked state
    - Solution: Virtual Threads
    - Lightweight, managed by JVM, mounted unmounted as needed
    - On periods of wait, JVM unmounts real thread and mounts other process onto thread
    - Works by minor change in the code:
        - ```java
       // Traditional way (Platform Threads)
       ExecutorService fixedPool = Executors.newFixedThreadPool(100);

       // The Loom way (Virtual Threads)
       ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
       ```
    - `-Djdk.virtualThreadScheduler.parallelism=N`: Sets the number of platform threads available to carry virtual
      threads.