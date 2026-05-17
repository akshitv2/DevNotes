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
9. ### Virtual Threads (Project Loom)
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
10. ### Structured Concurrency
    - Treats groups of related tasks running in different threads as a single unit of work.
    - Structured concurrency is primarily a programming model / design principle with a single java library to cordinate it: `StructuredTaskScope`
    - Aim: Concurrent tasks should follow the same lifetime structure as method calls.
      - Why? Traditional thread pools lacked ownership and cancellation of task on parents failure
    - Usage:
      - `try (var scope = new StructuredTaskScope.ShutdownOnFailure())` creates a lifetime boundary
    - Example:
      - ```java
        import java.util.concurrent.StructuredTaskScope;
        
        public class StructuredConcurrencyExample {
        
            static String fetchUser() throws InterruptedException {
                Thread.sleep(1000);
                return "Alice";
            }
        
            static int fetchOrders() throws InterruptedException {
                Thread.sleep(1500);
                return 5;
            }
        
            public static void main(String[] args) throws Exception {
        
                try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        
                    var userTask = scope.fork(() -> fetchUser());
                    var ordersTask = scope.fork(() -> fetchOrders());
        
                    // Wait for all tasks
                    scope.join();
        
                    // Propagate exceptions if any task failed
                    scope.throwIfFailed();
        
                    String user = userTask.get();
                    int orders = ordersTask.get();
        
                    System.out.println("User: " + user);
                    System.out.println("Orders: " + orders);
                }
            }
        }        
        ```
11. ### Fork Join Pool:
    - specialized implementation of the ExecutorService introduced in Java 7.
    - designed for "divide-and-conquer" algorithms
    - Work-Stealing Algorithm: Unlike a standard ThreadPoolExecutor, if a worker thread runs out of things to do, it
      can "steal" tasks from the back of the queues of other threads that are still busy. This maximizes CPU
      utilization.
    - fork(): Starts the sub-task asynchronously.
    - join(): Waits for the sub-task to finish and returns the result.
    - Code Example:
        - ```java
          class SumTask extends RecursiveTask<Long> {
          private static final int THRESHOLD = 1000;
          private final int[] array;
          private final int start;
          private final int end;
          
              public SumTask(int[] array, int start, int end) {
                  this.array = array;
                  this.start = start;
                  this.end = end;
              }
          
              @Override
              protected Long compute() {
                  int length = end - start;
                  // Recursive case: split task
                  int midpoint = start + (length / 2);
                  SumTask leftTask = new SumTask(array, start, midpoint);
                  SumTask rightTask = new SumTask(array, midpoint, end);
                  // Fork the first task and compute the second
                  leftTask.fork();
                  long rightResult = rightTask.compute();
                  // Join the forked task result
                  long leftResult = leftTask.join();
                  return leftResult + rightResult;
              }
          }
          
          public class ForkJoinExample {
          public static void main(String[] args) {
          int[] numbers = new int[10000];
          for (int i = 0; i < numbers.length; i++) numbers[i] = i;
          
                  // Use the common pool or create a custom one
                  ForkJoinPool pool = new ForkJoinPool();
                  long result = pool.invoke(new SumTask(numbers, 0, numbers.length));
          
                  System.out.println("Total Sum: " + result);
              }
          }
          ```
        - Similarity to `Future.submit()` and `get()`
            - The fork() and join() methods are conceptually similar to Future.submit() and Future.get(), but they
              differ significantly in how they manage resources and execution.
            - In a standard ExecutorService, if you call Future.get() and the task isn't done, the thread blocks and
              stays idle.
            - In a ForkJoinPool, when a thread calls join(), it doesn't just sit idle; it looks for other
              pending sub-tasks to execute while waiting. This is the Work-Stealing algorithm.
        - Note: Fork Join doesn't have to be recurisve
            - ```java
          public void runMultipleTasks() {
          ForkJoinPool pool = ForkJoinPool.commonPool();

                RecursiveAction taskA = new SimpleAction("Task A");
                RecursiveAction taskB = new SimpleAction("Task B");
            
                taskA.fork(); // Dispatched to pool
                taskB.fork(); // Dispatched to pool
            
                taskA.join();
                taskB.join();
          }
            ```
        - ForkJoinPool is designed for **CPU-bound work** (calculations, sorting, searching). It assumes threads will be
          busy computing.
        - **Not for I/O**: If a thread in a ForkJoinPool blocks on a network call or a database query, it cannot steal other work
          efficiently. If many threads block, the pool starves.
12. ### Choosing Concurrency FW:
    - ### Decision Flowchart
        - Is it CPU-bound? (Complex math, image processing, heavy data transformation)
            - Large data set? Use Parallel Streams / Fork-Join.
            - Single long task? Use Platform Threads or a fixed ThreadPool.
            - Is it I/O-bound? (API calls, DB queries, serving web requests)
                - Massive scaling needed? Use Virtual Threads.
                - Need to manage task lifecycles? Use Structured Concurrency.
                - Need to chain dependent results? Use CompletableFuture.
        -  ### Usage
            1. Parallel Streams (Fork-Join)
                - **Use case:** Processing large collections where each element is independent.
                - **Why:** It uses the `ForkJoinPool` under the hood to recursively split your data into smaller chunks
                  across all available CPU cores. It is optimized for data throughput.
                - **Avoid if:** Your tasks involve blocking I/O (e.g., calling an API inside the stream), as this will
                  starve the shared pool and stall the entire application.

            2. Virtual Threads
                - **Use case:** High-volume request/response applications (like a REST API).
                - **Why:** They allow you to write "blocking" code that scales like "asynchronous" code. Since they are
                  nearly free to create, you can assign one thread per request. When the thread waits for a database, it
                  is "unmounted," allowing the CPU to handle other requests.
                - **Avoid if:** The task is purely mathematical. Virtual threads don't make the CPU faster; they just
                  make "waiting" more efficient.

            3. Structured Concurrency (StructuredTaskScope)
                - **Use case:** When one "parent" task needs to trigger multiple "child" tasks and wait for them.
                - **Why:** It provides a clean "entry and exit" point. If one child task fails, the others are
                  automatically canceled. It turns the "spaghetti" of asynchronous programming into a readable,
                  tree-like structure.
                - **Avoid if:** You are on an older Java version (pre-Java 21) or doing simple, single-thread background
                  work.

            4. CompletableFuture
                - **Use case:** Chaining complex, non-blocking pipelines (e.g., "Get User" → "Get Orders" → "Calculate
                  Discount").
                - **Why:** It is excellent for "event-driven" logic where you want to define a path of execution (
                  `thenApply`, `thenCompose`) without blocking the main thread.
                - **Avoid if:** You find the syntax too "callback-heavy." Virtual threads often provide a simpler
                  alternative to `CompletableFuture` for basic I/O.

            5. Platform Threads
                - **Use case:** Background "heartbeat" tasks, long-running listeners, or CPU-intensive singleton tasks.
                - **Why:** Some tasks need a 1:1 relationship with the OS for priority or because they use native code (
                  JNI) that might pin a thread.
                - **Avoid if:** You need to scale to thousands of concurrent tasks.
