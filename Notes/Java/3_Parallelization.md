# Threading in Java

## 1. Fundamentals

### Thread Basics

* **Thread:** The smallest unit of execution.
* **`start()` vs `run()`:**
    * `start()`: Schedules the code for asynchronous execution on a new multithreaded CPU stack.
    * `run()`: Synchronously executes the code on the current thread.
* **`Runnable` vs `Thread`:**
    * `Thread` requires class inheritance.
    * `Runnable` implements an interface, leaving room for single inheritance.
    * *Note:* Avoid manually creating threads in production; use managed Thread Pools instead.

### Lifecycle

* **New:** Instantiated, but `start()` has not been called.
* **Runnable:** `start()` called; waiting for CPU allocation.
* **Running:** CPU is actively executing the `run()` method.
* **Blocked / Waiting:** Suspended, waiting for a lock or resource.
* **Terminated:** Execution completed.

### Synchronization

* Uses the `synchronized` keyword to lock execution to a single thread at a time, preventing race conditions.

---

## 2. Thread Pools & Executors

### Key Concepts

* **ThreadPool:** A managed collection of reusable worker threads that prevents memory exhaustion and overhead from
  frequent thread creation/destruction.
    * **Core Components:** Worker Threads, Work Queue, Rejection Policy (handles full queues).
* **Executor Framework:** Part of `java.util.concurrent`.
    * `Executor`: Base interface defining `execute(Runnable)`.
    * `ExecutorService`: Extends `Executor` to manage task submissions and pool lifecycles.

### Task Types

* **`Runnable`:** Defines a task with a `void` return type that cannot throw checked exceptions.
* **`Callable` & `Future`:**
    * `Callable`: Returns a value and can throw exceptions.
    * `Future`: Holds the pending result of an asynchronous computation, accessed via `.get()`.

---

## 3. Advanced Concurrency Models

### CompletableFuture

Eliminates blocking `.get()` calls by allowing task chaining and non-blocking asynchronous processing.

```java
CompletableFuture.supplyAsync(() ->"Data Ready")
        .

thenApply(data ->data +" - Processed")
        .

thenAccept(finalResult ->System.out.

println(finalResult))
        .

exceptionally(ex ->{
        System.out.

println("Error: "+ex.getMessage());
        return null;
        });

        System.out.

println("Main thread is free to do other things!");
```

---

### Virtual Threads (Project Loom)

Lightweight JVM-managed threads designed to replace 1:1 OS platform threads during I/O operations.

* **Mechanism:** When a virtual thread blocks on I/O, the JVM unmounts it from the underlying platform thread to execute
  other work.
* **Configuration Flag:** `-Djdk.virtualThreadScheduler.parallelism=N` sets available platform threads.
* Note: A traditional ThreadPool manages a limited number of expensive OS threads. Virtual threads allow you to create millions of cheap threads and let the JVM efficiently schedule them onto a smaller number of OS threads.

```java
// Traditional (Platform Threads)
ExecutorService fixedPool = Executors.newFixedThreadPool(100);

// Loom (Virtual Threads)
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

---

### Structured Concurrency

Uses `StructuredTaskScope` to bind the life cycle of concurrent child tasks to a single parent scope, handling automatic
cancellation on failures.

```java
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

    static void main(String[] args) throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var userTask = scope.fork(() -> fetchUser());
            var ordersTask = scope.fork(() -> fetchOrders());

            scope.join();            // Wait for all tasks
            scope.throwIfFailed();   // Propagate errors

            System.out.println("User: " + userTask.get());
            System.out.println("Orders: " + ordersTask.get());
        }
    }
}
```

---

### Fork-Join Pool

An `ExecutorService` optimized for CPU-bound "divide-and-conquer" computations using a **Work-Stealing Algorithm**.

* **Work-Stealing:** Idle threads steal tasks from the back of busy threads' queues.
* **Key Methods:** `fork()` (dispatches sub-task asynchronously) and `join()` (waits and retrieves result while
  continuing work).
* **Constraint:** Avoid using for blocking I/O bound tasks to prevent thread pool starvation.

```java
class SumTask extends RecursiveTask<Long> {
    private static final int THRESHOLD = 1000;
    private final int[] array;
    private final int start, end;

    public SumTask(int[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end = end;
    }

    @Override
    protected Long compute() {
        int length = end - start;
        if (length <= THRESHOLD) {
            long sum = 0;
            for (int i = start; i < end; i++) sum += array[i];
            return sum;
        }
        int midpoint = start + (length / 2);
        SumTask leftTask = new SumTask(array, start, midpoint);
        SumTask rightTask = new SumTask(array, midpoint, end);

        leftTask.fork();
        long rightResult = rightTask.compute();
        long leftResult = leftTask.join();

        return leftResult + rightResult;
    }
}
```

---

## 4. Selection Guide

| Framework                        | Target Use Case                                   | Primary Advantage                                     | When to Avoid                                          |
|:---------------------------------|:--------------------------------------------------|:------------------------------------------------------|:-------------------------------------------------------|
| **Parallel Streams / Fork-Join** | CPU-bound data processing on large collections.   | Automatic recursive task splitting across CPU cores.  | Tasks involving blocking I/O.                          |
| **Virtual Threads**              | High-volume I/O operations (REST APIs, DB calls). | Scalable "thread-per-request" model without blocking. | Purely CPU-bound mathematical operations.              |
| **Structured Concurrency**       | Parent-child multi-task orchestration.            | Automatic cancellation and scope-bound execution.     | Legacy systems or single-task background jobs.         |
| **CompletableFuture**            | Non-blocking, event-driven task pipelines.        | Flexible fluent API for chaining operations.          | Scenarios where simple sequential syntax is preferred. |
| **Platform Threads**             | Long-running background workers or native code.   | Direct 1:1 binding to OS thread scheduling.           | High-concurrency operations (thousands of tasks).      |
