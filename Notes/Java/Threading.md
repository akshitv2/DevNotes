# Threading in Java

1. Thread
    - Smallest unit of execution
2. Lifecycle:
    - New: Created but not started
    - Runnable: when `start()` is called and waits for CPU to run it
    - Running: Cpu executes `run()` method.
    - Blocked/Waiting: Waiting for resource
    - Terminated: Thread finishes execution
3. Synchronization:
    - Locks code to be only accessed by one thread at a time
    - Prevents Race Condition
    - Keyword: `synchronized`
4. `start()` vs. `run()`:
    - `start()` sets the code to be picked up by the CPU to be multithreaded
    - `run()` just runs the code in the same thread you call
5. `Runnable` vs `Thread`:
    - Difference between implementing an interface (Runnable) and extending a class (Thread)
    - Since only class can be extended in java, interface is preferred
    - ℹ️Note: In real world we don't actually create threads and instead create thread pools where we hand runnable to
      free threads in the pool
6. ThreadPool and Executor:
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
       - ℹCallable provides a Future object back
       - Shutdown executor (needed to exit JVM)
7. `Callable` and `Future`:
   - Runnable: Return type void, can't return a result
   - To get a response use callable or future

8. CompletableFuture