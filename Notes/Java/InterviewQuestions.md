# Java Interview Questions & Ideal Answers

*A running set of notes — new sections added as we go.*

---

## Section 1: OOP Fundamentals

### 1. What are the four pillars of OOP, and how does Java implement each?

**Ideal answer:**

- **Encapsulation** — Bundling data (fields) and methods that operate on it into a single unit (class), and restricting
  direct access using access modifiers (`private`, `protected`, `public`). Achieved via private fields + public
  getters/setters.
- **Abstraction** — Hiding implementation details and exposing only essential features. Achieved via abstract classes
  and interfaces.
- **Inheritance** — A class (subclass) can acquire fields/methods of another class (superclass) using `extends`.
  Promotes code reuse.
- **Polymorphism** — The ability of an object to take many forms. Two types:
    - *Compile-time (static)*: method overloading.
    - *Runtime (dynamic)*: method overriding, resolved via dynamic dispatch (vtable lookup).

---

### 2. What is the difference between method overloading and method overriding?

**Ideal answer:**

| Aspect                             | Overloading                                            | Overriding                                           |
|------------------------------------|--------------------------------------------------------|------------------------------------------------------|
| Definition                         | Same method name, different parameter list, same class | Same signature, subclass redefines superclass method |
| Binding                            | Compile-time (static binding)                          | Runtime (dynamic binding)                            |
| Return type                        | Can differ                                             | Must be same or covariant                            |
| Access modifier                    | Can differ freely                                      | Cannot reduce visibility                             |
| `static`/`final`/`private` methods | Can be overloaded                                      | Cannot be overridden (they're not polymorphic)       |

---

### 3. Why is Java called "platform independent"? What role does the JVM play?

**Ideal answer:**
Java source code (`.java`) is compiled by `javac` into **bytecode** (`.class`), not native machine code. This bytecode
runs on any device with a **Java Virtual Machine (JVM)**, which interprets or JIT-compiles it into the underlying
platform's native instructions. So the same `.class` file runs unmodified on Windows, Linux, or macOS — "write once, run
anywhere." The JVM is platform-specific, but the bytecode is not.

---

### 4. Can you explain the difference between an abstract class and an interface?

**Ideal answer:**

| Aspect               | Abstract Class                                 | Interface                                                           |
|----------------------|------------------------------------------------|---------------------------------------------------------------------|
| Methods              | Can have abstract + concrete methods           | Can have abstract, default, static, and private methods (Java 8+)   |
| Fields               | Any type of field (instance state allowed)     | Only `public static final` constants                                |
| Constructor          | Yes                                            | No                                                                  |
| Multiple inheritance | A class can extend only one abstract class     | A class can implement multiple interfaces                           |
| When to use          | "is-a" relationship with shared state/behavior | Defining a contract/capability, especially across unrelated classes |

Since Java 8, interfaces can have `default` and `static` methods, narrowing the gap — but interfaces still can't hold
instance state, which remains the key distinction.

---

### 5. What is constructor chaining, and how do `this()` and `super()` work?

**Ideal answer:**
Constructor chaining is calling one constructor from another.

- `this(...)` calls another constructor **in the same class** — must be the first statement.
- `super(...)` calls the **parent class's constructor** — must also be the first statement.
- If neither is explicitly called, the compiler inserts an implicit `super()` call to the no-arg parent constructor.
- You cannot call both `this()` and `super()` in the same constructor (only one "first statement" is allowed).
- This is used to avoid duplicating initialization logic across overloaded constructors.

---

### 6. Why are `String` objects immutable in Java? What are the benefits?

**Ideal answer:**
`String` is immutable because:

1. **Security** — Strings are used for things like class loading, file paths, network connections; immutability prevents
   tampering after validation.
2. **String pool caching** — Immutability lets the JVM safely reuse String literals in the **string constant pool**,
   saving memory.
3. **Thread safety** — Immutable objects are inherently thread-safe; no synchronization needed when sharing across
   threads.
4. **Hashcode caching** — Since the value never changes, `String` caches its hashcode after first computation, making it
   efficient as a `HashMap` key.

Internally, `String` stores its data in a `final` array (`byte[]` since Java 9 for compact strings), and any "
modification" (like `concat()`) creates a new `String` object.

---

## Section 2: Collections Framework

### 1. What is the difference between `ArrayList` and `LinkedList`?

**Ideal answer:**

| Aspect                     | ArrayList                                                  | LinkedList                                              |
|----------------------------|------------------------------------------------------------|---------------------------------------------------------|
| Backing structure          | Dynamic array                                              | Doubly linked list                                      |
| Random access (`get(i)`)   | O(1)                                                       | O(n)                                                    |
| Insertion/deletion at ends | O(1) amortized (end), O(n) (start/middle, due to shifting) | O(1) at ends, O(n) to reach a middle position           |
| Memory overhead            | Lower (contiguous array)                                   | Higher (each node stores prev/next pointers)            |
| Implements                 | `List`, `RandomAccess`                                     | `List`, `Deque`                                         |
| Best use case              | Frequent reads/iteration                                   | Frequent insertions/deletions at ends (queue/deque use) |

---

### 2. How does `HashMap` work internally?

**Ideal answer:**

- Backed by an array of "buckets" (`Node<K,V>[] table`).
- `put(key, value)`: computes `hashCode()` of the key, applies a **hash spreading function** (XOR-shift to reduce
  collisions), then maps it to a bucket index via `(n - 1) & hash` where `n` is table length (always a power of 2).
- Collisions within a bucket are handled via a **linked list**; if a bucket's list grows beyond a threshold (8 entries)
  **and** the table has ≥64 buckets, it's converted to a **red-black tree** (Java 8+) for O(log n) worst-case lookups
  instead of O(n).
- **Resizing**: when `size > capacity * loadFactor` (default load factor 0.75), the table doubles in size and all
  entries are rehashed.
- `equals()` and `hashCode()` contract matters: two equal keys must have the same hash code, or lookups break.
- Not thread-safe — use `ConcurrentHashMap` for concurrent access.

---

### 3. What is the difference between `HashMap`, `LinkedHashMap`, and `TreeMap`?

**Ideal answer:**

- **`HashMap`** — No ordering guarantee; O(1) average-case operations.
- **`LinkedHashMap`** — Maintains **insertion order** (or optionally access order, useful for LRU caches) by threading a
  doubly linked list through entries; slightly more memory overhead than `HashMap`.
- **`TreeMap`** — Maintains keys in **sorted order** (natural ordering or via a `Comparator`), backed by a Red-Black
  tree; O(log n) operations.

---

### 4. What is the difference between `Comparable` and `Comparator`?

**Ideal answer:**

- **`Comparable`** (`compareTo()`) — Defines the **natural ordering** of a class; implemented *inside* the class itself.
  A class can only have one natural ordering.
- **`Comparator`** (`compare()`) — Defines **external, custom ordering logic**, separate from the class. You can create
  multiple comparators for different sort criteria (e.g., sort `Employee` by name, salary, or age) without modifying the
  `Employee` class.
- Use `Comparable` when there's one obvious default order; use `Comparator` for flexible/multiple sort strategies, or
  when you can't modify the source class.

---

### 5. What is `ConcurrentModificationException`, and how do you avoid it?

**Ideal answer:**
Thrown when a collection is structurally modified (add/remove) while being iterated with a standard iterator (e.g.,
inside a for-each loop), other than through the iterator's own `remove()` method. Java's fail-fast iterators track a
`modCount`; if it changes unexpectedly during iteration, the exception fires.

**Avoidance strategies:**

1. Use `Iterator.remove()` instead of modifying the collection directly during iteration.
2. Use `CopyOnWriteArrayList` or `ConcurrentHashMap` for concurrent-safe iteration (fail-safe, operates on a snapshot).
3. Collect items to remove/add in a separate list, then apply changes after iteration completes.
4. Use `removeIf()` (Java 8+) for safe conditional removal.

---

### 6. Why is it important to override both `equals()` and `hashCode()` together?

**Ideal answer:**
The **general contract** states: if two objects are equal according to `equals()`, they **must** have the same
`hashCode()`. Hash-based collections (`HashMap`, `HashSet`) rely on `hashCode()` to locate the bucket, then `equals()`
to confirm identity within that bucket.

If you override `equals()` without `hashCode()`:

- Two "equal" objects could land in different buckets, so a `HashSet` might allow duplicates, or a `HashMap.get()` might
  fail to find a value even though an "equal" key was inserted.

Rule of thumb: **override both, or neither.** Also, `hashCode()` must remain consistent across calls as long as the
object's relevant fields don't change.

---

## Section 3: Exception Handling

### 1. What is the difference between checked and unchecked exceptions?

**Ideal answer:**

| Aspect               | Checked Exception                                                            | Unchecked Exception                                                                  |
|----------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Hierarchy            | Subclass of `Exception` (excluding `RuntimeException`)                       | Subclass of `RuntimeException` or `Error`                                            |
| Compiler enforcement | Must be caught or declared with `throws`                                     | No compiler enforcement                                                              |
| Examples             | `IOException`, `SQLException`, `ClassNotFoundException`                      | `NullPointerException`, `ArrayIndexOutOfBoundsException`, `IllegalArgumentException` |
| When used            | Recoverable conditions the caller *should* anticipate (e.g., file not found) | Programming errors or conditions usually not recoverable at runtime                  |

`Error` (e.g., `OutOfMemoryError`, `StackOverflowError`) represents serious problems the application typically shouldn't
try to catch/recover from.

---

### 2. Explain the `try-catch-finally` flow, including edge cases with `return`.

**Ideal answer:**

- `try` — code that might throw.
- `catch` — handles a specific exception type; multiple catch blocks are checked top-to-bottom, so subclasses must come
  **before** superclasses.
- `finally` — always executes, whether or not an exception occurred, **except** if the JVM exits (`System.exit()`) or
  the thread is killed.

**Edge case:** If both the `try` (or `catch`) block and the `finally` block contain a `return` statement, the `finally`
block's return **wins** — it overrides the earlier return value. This is considered bad practice because it silently
discards results/exceptions. Similarly, if `finally` throws an exception, it suppresses any exception from `try`/
`catch`.

---

### 3. What is try-with-resources, and why is it preferred over manual `finally` cleanup?

**Ideal answer:**
Introduced in Java 7, it automatically closes resources that implement `AutoCloseable`/`Closeable` at the end of the
block, regardless of whether an exception occurred:

```java
try(BufferedReader br = new BufferedReader(new FileReader("file.txt"))){
        return br.

readLine();
}
```

Benefits over manual `finally`:

1. Less boilerplate — no need to null-check and close manually.
2. Handles **suppressed exceptions** correctly: if both the try block and the `close()` call throw, the original
   exception is preserved as primary and the close exception is attached via `getSuppressed()`, instead of silently
   overwriting it (a common bug with manual `finally` blocks).
3. Multiple resources can be declared, closed in reverse order of declaration.

---

### 4. What's the difference between `throw` and `throws`?

**Ideal answer:**

- `throw` — a statement used to **actually throw** an exception instance:
  `throw new IllegalArgumentException("bad input");`
- `throws` — a clause in a method **signature** declaring that the method *might* throw certain checked exceptions,
  shifting responsibility to the caller: `void readFile() throws IOException { ... }`

---

### 5. Can you create a custom exception? What are best practices?

**Ideal answer:**
Yes — extend `Exception` (checked) or `RuntimeException` (unchecked) depending on whether callers should be forced to
handle it.

```java
public class InsufficientFundsException extends Exception {
    public InsufficientFundsException(String message) {
        super(message);
    }

    public InsufficientFundsException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

**Best practices:**

- Always provide constructors that accept a message and a cause (for **exception chaining** — preserves the original
  stack trace).
- Name it with an `Exception` suffix.
- Use checked exceptions for recoverable, expected business conditions (e.g., insufficient funds); use unchecked for
  programming errors.
- Don't overuse custom exceptions where a standard one (`IllegalArgumentException`, `IllegalStateException`) already
  fits.
- Avoid catching generic `Exception` or `Throwable` unless at a top-level boundary (e.g., a request handler) — it hides
  real bugs.

---

### 6. What is exception chaining, and why does it matter?

**Ideal answer:**
Exception chaining wraps a lower-level exception inside a higher-level, more meaningful one while preserving the
original as the **cause**:

```java
try{
connectToDatabase();
}catch(
SQLException e){
        throw new

ServiceException("Failed to load user data",e);
}
```

This matters because:

1. It preserves the **root cause** stack trace (`getCause()`) for debugging, instead of losing it.
2. It lets each layer of an application throw exceptions meaningful to its own abstraction level (e.g., a service layer
   shouldn't leak `SQLException` to a UI layer) while still keeping the full diagnostic trail.

---

## Section 4: Multithreading & Concurrency

### 1. What is the difference between a process and a thread?

**Ideal answer:**

- A **process** is an independent execution unit with its own memory space (heap, code, data segments); processes don't
  share memory directly and communicate via IPC.
- A **thread** is a lightweight unit of execution *within* a process; threads of the same process share the heap and
  static/class data but have their own stack, program counter, and local variables.
- Threads are cheaper to create and context-switch than processes, but shared memory introduces synchronization
  concerns (race conditions) that processes don't have.

---

### 2. What are the ways to create a thread in Java, and which is preferred?

**Ideal answer:**

1. **Extend `Thread`** and override `run()`.
2. **Implement `Runnable`** and pass it to a `Thread` constructor.
3. **Implement `Callable`** (can return a value / throw checked exceptions) and submit it to an `ExecutorService`.

**Preferred approach:** Implement `Runnable`/`Callable` and submit to an **`ExecutorService`** (thread pool), rather
than extending `Thread` or manually creating threads. Reasons:

- Java only supports single inheritance — extending `Thread` wastes that slot.
- Thread pools reuse threads, avoiding the overhead of constant creation/destruction.
- Executors provide lifecycle management, task queuing, and easier testing.

---

### 3. What is the difference between `synchronized` methods and `synchronized` blocks?

**Ideal answer:**

- **Synchronized method** — locks on `this` (instance methods) or the `Class` object (static methods) for the **entire
  method body**.
- **Synchronized block** — locks on a specified object, for only the critical section needed:

```java
public void update() {
    // non-critical code runs without lock
    synchronized (lockObject) {
        // only this section is protected
    }
}
```

Synchronized blocks are generally preferred because they **minimize the lock's scope**, improving concurrency by not
blocking unrelated code, and allow locking on a dedicated private lock object rather than `this` (avoiding accidental
external locking interference).

---

### 4. What is a race condition, and how do you prevent it?

**Ideal answer:**
A race condition is a bug that happens when two or more operations access or modify the same shared data at about the
same time, and the final result depends on which operation happens first thus resulting in unpredictable
timing/interleaving of operations — e.g., two threads incrementing a shared counter (`count++`) can lose
updates because the operation isn't atomic (read-modify-write).

**Prevention strategies:**

1. **Synchronization** (`synchronized` keyword) to enforce mutual exclusion.
2. **`java.util.concurrent.atomic`** classes (`AtomicInteger`, `AtomicLong`) for lock-free atomic operations.
3. **`Lock` implementations** (`ReentrantLock`) for more flexible locking (tryLock, timed lock, interruptible lock).
4. **Immutable objects** — no mutable shared state means no race condition possible.
5. **Thread-confinement** — keep data local to one thread (e.g., `ThreadLocal`).
6. **Concurrent collections** (`ConcurrentHashMap`, `CopyOnWriteArrayList`) designed for safe concurrent access.

---

### 5. What is the difference between `wait()`/`notify()` and `Condition`?

**Ideal answer:**

- **`wait()`/`notify()`/`notifyAll()`** — Object-level methods (from `Object` class) used inside `synchronized` blocks
  for thread coordination. A thread calling `wait()` releases the monitor lock and pauses until another thread calls
  `notify()`/`notifyAll()` on the same object.
- **`Condition`** (from `java.util.concurrent.locks`) — Works with `Lock` (e.g., `ReentrantLock`) instead of intrinsic
  locks, offering more flexibility: multiple `Condition` objects per lock (e.g., "not full" and "not empty" conditions
  for a bounded buffer), timed waits, and interruptible waits.

Both suffer from the same core rule: always call `wait()` in a loop (checking the condition), not an `if`, because of *
*spurious wakeups** and to handle multiple waiting threads correctly.

---

### 6. What is a deadlock, and how can you avoid it?

**Ideal answer:**
A deadlock occurs when two or more threads are blocked forever, each waiting for a resource the other holds. Classic
scenario: Thread A locks Resource 1 and waits for Resource 2; Thread B locks Resource 2 and waits for Resource 1.

**Four necessary conditions** (Coffman conditions): mutual exclusion (held by only one thread), hold-and-wait, no preemption (cannot take away forcibly), circular wait.

**Avoidance strategies:**

1. **Lock ordering** — always acquire locks in a consistent global order across all threads.
2. **Lock timeout** — use `tryLock(timeout)` instead of blocking indefinitely, and back off/retry on failure.
3. **Avoid nested locks** where possible; minimize the number of locks held simultaneously.
4. Use higher-level concurrency utilities (`ExecutorService`, concurrent collections) instead of manual lock management.

---

### 7. What is the difference between `Runnable` and `Callable`?

**Ideal answer:**

| Aspect             | Runnable                              | Callable                                          |
|--------------------|---------------------------------------|---------------------------------------------------|
| Return value       | `void` (`run()`)                      | Returns a value (`call()` returns `V`)            |
| Checked exceptions | Cannot throw checked exceptions       | Can throw checked exceptions                      |
| Used with          | `Thread`, `ExecutorService.execute()` | `ExecutorService.submit()`, returns a `Future<V>` |

`Future<V>` from `submit(Callable)` lets you retrieve the result (`future.get()`, blocking) or check completion (
`isDone()`), and cancel the task.

---

## Section 5: Java 8 Features

### 1. What are lambda expressions, and what problem do they solve?

**Ideal answer:**
A lambda expression is a concise way to represent an anonymous function — an implementation of a **functional interface
** (an interface with exactly one abstract method):

```java
Comparator<String> byLength = (a, b) -> a.length() - b.length();
```

**Problem solved:** Before Java 8, passing behavior as a parameter required verbose anonymous inner classes:

```java
Comparator<String> byLength = new Comparator<String>() {
    public int compare(String a, String b) {
        return a.length() - b.length();
    }
};
```

Lambdas reduce this boilerplate significantly and enable a more functional programming style, especially with the
Streams API. Internally, lambdas are implemented via `invokedynamic` and method handles, not by generating anonymous
classes at compile time — making them more efficient.

---

### 2. What is a functional interface? Name a few built-in ones.

**Ideal answer:**
An interface with **exactly one abstract method** (it can have any number of `default`/`static` methods). Marked (
optionally) with `@FunctionalInterface` for compile-time checking.

Common built-in ones (`java.util.function`):

- **`Function<T,R>`** — takes T, returns R (`apply()`).
- **`Predicate<T>`** — takes T, returns boolean (`test()`) — used for filtering.
- **`Consumer<T>`** — takes T, returns nothing (`accept()`) — used for side effects (e.g., printing).
- **`Supplier<T>`** — takes nothing, returns T (`get()`) — used for lazy generation.
- **`BiFunction<T,U,R>`** — takes two args, returns R.

---

### 3. Explain the Streams API. How is it different from Collections?

**Ideal answer:**
A **Stream** represents a sequence of elements supporting functional-style operations (`filter`, `map`, `reduce`,
`collect`) that can be chained in a pipeline.

Key differences from Collections:
| Aspect | Collection | Stream |
|---|---|---|
| Storage | Stores elements in memory | Doesn't store elements — computes on demand |
| Traversal | Can be iterated multiple times | Can be **consumed only once** |
| Mutation | Elements can be added/removed | Doesn't modify the source; produces new results |
| Evaluation | Eager | **Lazy** — intermediate operations (`filter`, `map`) aren't executed until a terminal operation (
`collect`, `forEach`, `reduce`) is invoked |

Example:

```java
List<String> names = employees.stream()
        .filter(e -> e.getSalary() > 50000)
        .map(Employee::getName)
        .sorted()
        .collect(Collectors.toList());
```

Streams also support **parallel execution** via `parallelStream()`, splitting work across threads using the common
`ForkJoinPool` — useful for CPU-bound bulk operations on large datasets, though not always faster for small collections
due to overhead.

---

### 4. What is the difference between `map()` and `flatMap()`?

**Ideal answer:**

- **`map()`** — Transforms each element into exactly one output element (1-to-1). If the mapping function returns a
  `Stream`, you'd end up with a `Stream<Stream<T>>` (nested).
- **`flatMap()`** — Transforms each element into a stream of elements, then **flattens** all resulting streams into a
  single stream (1-to-many, flattened).

```java
List<List<Integer>> nested = List.of(List.of(1, 2), List.of(3, 4));

// map: Stream<Stream<Integer>>
nested.

stream().

map(List::stream);

// flatMap: Stream<Integer> -> [1, 2, 3, 4]
nested.

stream().

flatMap(List::stream).

collect(Collectors.toList());
```

---

### 5. What are default and static methods in interfaces? Why were they introduced?

**Ideal answer:**

- **`default` methods** — provide a method body directly in an interface; implementing classes inherit the default
  behavior unless they override it.
- **`static` methods** — utility methods belonging to the interface itself, called as `InterfaceName.method()`, not
  inherited by implementing classes.

**Why introduced:** Primarily to support **interface evolution without breaking existing implementations** — e.g.,
adding `forEach()` to the `Iterable` interface in Java 8 would have broken every existing class implementing it, had
`default` methods not allowed a backward-compatible default implementation.

**Diamond problem:** If a class implements two interfaces with conflicting default methods, it must explicitly override
the method and can call a specific one via `InterfaceName.super.method()`.

---

### 6. What is `Optional`, and how should it be used properly?

**Ideal answer:**
`Optional<T>` is a container object that may or may not hold a non-null value, designed to reduce `NullPointerException`
s and make "value may be absent" explicit in method signatures.

```java
Optional<String> name = Optional.ofNullable(getName());
String result = name.orElse("default");
name.

ifPresent(System.out::println);
```

**Best practices:**

- Use as a **return type** for methods that might not have a result — don't use it for fields, method parameters, or
  collection elements (adds unnecessary wrapping overhead).
- Avoid `optional.get()` without checking `isPresent()` first — prefer `orElse()`, `orElseGet()`, `orElseThrow()`, or
  `map()`/`ifPresent()` for a more functional style.
- Don't use `Optional` just to avoid a simple null check — it's meant to communicate intent in APIs, not as a blanket
  null-avoidance tool everywhere.

---

### 7. What is the difference between `Collectors.toList()` and `Collectors.toUnmodifiableList()`?

**Ideal answer:**

- **`Collectors.toList()`** — Returns a mutable list (implementation not guaranteed, typically `ArrayList`); no
  guarantee it's unmodifiable, though you shouldn't rely on mutability either since the JDK doesn't promise it.
- **`Collectors.toUnmodifiableList()`** (Java 10+) — Explicitly returns an **immutable** list; any attempt to modify
  it (`add`, `remove`, `set`) throws `UnsupportedOperationException`.

Using the unmodifiable variant is preferred when the resulting collection should be treated as read-only, making that
intent explicit and safe.

---

## Section 6: JVM Internals & Memory Management

### 1. What are the main memory areas of the JVM?

**Ideal answer:**

- **Heap** — Stores all objects and their instance variables; shared across all threads. Divided into **Young Generation
  ** (Eden + two Survivor spaces) and **Old (Tenured) Generation**.
- **Stack** — One per thread; stores method call frames, local variables, and partial results. Each frame is popped when
  its method returns. Throws `StackOverflowError` on excessive recursion.
- **Method Area / Metaspace** — Stores class metadata (structure, method bytecode, runtime constant pool, static
  variables). Since Java 8, this replaced **PermGen** and lives in **native memory** rather than the heap, so it can
  grow dynamically (subject to available OS memory).
- **PC (Program Counter) Register** — Per-thread, holds the address of the current executing JVM instruction.
- **Native Method Stack** — Supports native (non-Java, e.g., JNI) method calls.

---

### 2. Explain the generational garbage collection model. Why is the heap divided this way?

**Ideal answer:**
Based on the **weak generational hypothesis**: most objects die young. So the heap is split to optimize collection:

- **Young Generation** — New objects are allocated in **Eden**. A **Minor GC** runs frequently here; surviving objects
  move to a **Survivor space** (S0/S1, alternating), and objects surviving several GC cycles (tracked via an "age"
  counter) are **promoted** to the Old Generation.
- **Old Generation** — Holds long-lived objects. Collected less frequently via **Major/Full GC**, which is more
  expensive since it scans a much larger region.

This design means Minor GCs (on the small, frequently-collected Young Gen) are fast and cheap, while the costlier Full
GC on Old Gen happens rarely — overall much more efficient than treating the whole heap uniformly.

---

### 3. What is the difference between Minor GC, Major GC, and Full GC?

**Ideal answer:**

- **Minor GC** — Collects only the Young Generation; typically fast, uses a stop-the-world pause but a brief one.
- **Major GC** — Collects the Old Generation.
- **Full GC** — Collects the entire heap (Young + Old) and often Metaspace; usually the most expensive, causing longer
  application pauses. Frequent Full GCs are usually a sign of memory pressure or a poorly tuned/undersized heap.

---

### 4. What garbage collectors does the JVM offer, and how do you choose one?

**Ideal answer:**

- **Serial GC** — Single-threaded, stop-the-world; suited for small applications/single-core environments.
- **Parallel GC** (throughput collector) — Multiple threads for GC work; maximizes throughput, but pauses can be longer.
  Good for batch-processing workloads where pause time is less critical.
- **CMS (Concurrent Mark Sweep)** — Deprecated/removed in newer JDKs; did most work concurrently with the application to
  reduce pause times, at the cost of CPU overhead and heap fragmentation.
- **G1 (Garbage First)** — Default since Java 9. Divides the heap into many equally-sized regions and prioritizes
  collecting regions with the most garbage first; aims for predictable, low pause times while handling large heaps well.
- **ZGC / Shenandoah** — Low-latency collectors designed for very large heaps with sub-millisecond pause targets, doing
  almost all work concurrently.

**Choice depends on:** heap size, latency requirements (pause-time sensitive vs throughput-focused), and available CPU
cores.

---

### 5. What causes a memory leak in Java, given it has automatic garbage collection?

**Ideal answer:**
GC only reclaims objects that are **unreachable**. A "leak" in Java means objects remain **reachable but are no longer
needed**, so they're never collected. Common causes:

1. **Static collections** that keep growing (e.g., a `static List` used as a cache with no eviction).
2. **Unclosed resources** (streams, connections) holding references indirectly.
3. **Listener/callback registrations** that are never deregistered, keeping the registering object alive.
4. **Inner classes** (non-static) holding an implicit reference to their outer class instance, kept alive by something
   else.
5. **`ThreadLocal`** variables not removed (`.remove()`) — especially dangerous in thread-pooled environments where
   threads are long-lived.
6. Long-lived caches without proper eviction (should use `WeakHashMap`, soft references, or bounded caches like
   Caffeine).

Diagnosed via heap dumps (`jmap`, `VisualVM`, `Eclipse MAT`) analyzing retained object graphs and GC roots.

---

### 6. What's the difference between strong, weak, soft, and phantom references?

**Ideal answer:**
| Reference type | Behavior |
|---|---|
| **Strong** | Default — object is never GC'd while a strong reference exists. |
| **Soft (`SoftReference`)** | GC'd only when the JVM is running low on memory (before throwing `OutOfMemoryError`).
Good for memory-sensitive caches. |
| **Weak (`WeakReference`)** | GC'd on the **next** GC cycle regardless of memory pressure, as soon as no strong
references exist. Used in `WeakHashMap`, and to avoid memory leaks (e.g., listener maps keyed by objects that should be
collectible). |
| **Phantom (`PhantomReference`)** | Enqueued *after* the object is finalized but before memory is reclaimed; `get()`
always returns `null`. Used for cleanup actions/tracking exact reclaim timing, replacing the deprecated `finalize()`. |

---

### 7. Class loading: explain the class loader hierarchy and lazy loading.

**Ideal answer:**
Java uses a **delegation model** with three built-in loaders:

1. **Bootstrap Class Loader** — Loads core JDK classes (`java.lang.*`, etc.) from the JDK's core library, written in
   native code.
2. **Platform/Extension Class Loader** — Loads classes from the Java platform's extension libraries.
3. **Application/System Class Loader** — Loads classes from the application's classpath.

**Delegation model:** Before a class loader loads a class itself, it delegates the request to its parent first. Only if
the parent can't find the class does the child attempt to load it — this prevents core classes from being
overridden/spoofed by application code (e.g., you can't redefine `java.lang.String`).

**Lazy loading:** Classes are loaded **on first active use** (e.g., instantiation, static field access, static method
call) — not all at once at startup. This improves startup time and memory footprint. The loading process itself has
phases: **Loading** (reading bytecode) → **Linking** (verification, preparation, resolution) → **Initialization** (
running static initializers).

---

## Section 7: Design Patterns

### 1. Explain the Singleton pattern and the thread-safe ways to implement it in Java.

**Ideal answer:**
Singleton ensures a class has exactly **one instance** and provides a global access point to it.

**Common implementations:**

1. **Eager initialization** — instance created at class-load time:

```java
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();

    private Singleton() {
    }

    public static Singleton getInstance() {
        return INSTANCE;
    }
}
```

Thread-safe by nature (class loading is thread-safe), but instantiates even if unused.

2. **Double-checked locking (lazy + thread-safe):**

```java
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {
    }

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

`volatile` is essential — without it, another thread could see a partially constructed object due to instruction
reordering.

3. **Initialization-on-demand holder idiom** — relies on JVM's lazy class initialization guarantee, no synchronization
   overhead:

```java
public class Singleton {
    private Singleton() {
    }

    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }

    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}
```

4. **Enum singleton** — simplest and safest; JVM guarantees single instantiation and it's serialization-safe by default:

```java
public enum Singleton {
    INSTANCE;

    public void doSomething() { ...}
}
```

---

### 2. What is the difference between Factory Method and Abstract Factory patterns?

**Ideal answer:**

- **Factory Method** — Defines a method (often overridden by subclasses) for creating **one type** of object, letting
  subclasses decide which concrete class to instantiate.

```java
abstract class DocumentCreator {
    abstract Document createDocument();
}

class PdfCreator extends DocumentCreator {
    Document createDocument() {
        return new PdfDocument();
    }
}
```

- **Abstract Factory** — Provides an interface for creating **families of related objects** without specifying concrete
  classes, typically composing multiple factory methods.

```java
interface UIFactory {
    Button createButton();

    Checkbox createCheckbox();
}

class DarkThemeFactory implements UIFactory {
    public Button createButton() {
        return new DarkButton();
    }

    public Checkbox createCheckbox() {
        return new DarkCheckbox();
    }
}
```

**Key distinction:** Factory Method creates one product via inheritance/overriding; Abstract Factory creates a *family*
of related products via composition.

---

### 3. Explain the Builder pattern. Why use it over a large constructor?

**Ideal answer:**
Builder separates the construction of a complex object from its representation, especially useful when a class has many
optional fields (avoiding "telescoping constructors"):

```java
Pizza pizza = new Pizza.Builder()
        .size(12)
        .cheese(true)
        .pepperoni(true)
        .build();
```

**Advantages over a large constructor:**

1. Avoids constructors with many parameters (error-prone if parameters share a type and order is easy to mix up).
2. Enables **immutability** — the final object can have all `final` fields, set only via the builder.
3. Readable, self-documenting client code (named methods instead of positional args).
4. Can enforce validation logic in `build()` before returning a valid object.

Java's `StringBuilder`, `Stream.Builder`, and Lombok's `@Builder` are common real-world examples.

---

### 4. Explain the Observer pattern, and how it relates to Java's event-listener model.

**Ideal answer:**
Observer defines a one-to-many dependency: when a **subject's** state changes, all registered **observers** are notified
automatically.

```java
interface Observer {
    void update(String event);
}

class EventPublisher {
    private List<Observer> observers = new ArrayList<>();

    void subscribe(Observer o) {
        observers.add(o);
    }

    void publish(String event) {
        observers.forEach(o -> o.update(event));
    }
}
```

This is the foundation of Java's **event-listener model** (e.g., GUI `ActionListener`s, or Spring's `ApplicationEvent`/
`ApplicationListener`). It promotes loose coupling — the subject doesn't need to know concrete observer types, only the
`Observer` interface.

---

### 5. What is the Strategy pattern, and how do lambdas make it more concise in modern Java?

**Ideal answer:**
Strategy defines a family of interchangeable algorithms, encapsulated behind a common interface, selected at runtime:

```java
interface DiscountStrategy {
    double apply(double price);
}

class Checkout {
    private DiscountStrategy strategy;

    Checkout(DiscountStrategy strategy) {
        this.strategy = strategy;
    }

    double checkout(double price) {
        return strategy.apply(price);
    }
}
```

Traditionally each strategy required a separate concrete class implementing the interface. Since Java 8, if the strategy
interface is functional (one abstract method), you can pass a **lambda** directly instead of creating verbose classes:

```java
Checkout checkout = new Checkout(price -> price * 0.9); // 10% off strategy
```

This dramatically reduces boilerplate for simple strategies while keeping the pattern's flexibility for more complex
ones.

---

### 6. What is Dependency Injection, and what problem does it solve?

**Ideal answer:**
Dependency Injection (DI) is a form of **Inversion of Control** where an object's dependencies are provided ("injected")
from the outside rather than the object creating them itself.

```java
// Without DI - tightly coupled, hard to test
class OrderService {
    private PaymentGateway gateway = new StripeGateway();
}

// With DI - loosely coupled
class OrderService {
    private final PaymentGateway gateway;

    OrderService(PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```

**Problems it solves:**

1. **Testability** — dependencies can be swapped for mocks/stubs in unit tests.
2. **Loose coupling** — `OrderService` depends on the `PaymentGateway` abstraction, not a concrete implementation;
   swapping providers doesn't require changing `OrderService`.
3. **Single Responsibility** — object creation/wiring logic is centralized (e.g., in a DI container like Spring), not
   scattered across business logic.

Three common injection types: **constructor injection** (preferred — enables immutability and makes required
dependencies explicit), **setter injection**, and **field injection** (convenient but harder to test/mock, and hides
required dependencies).

---

*(More sections coming — just say "next" or name a topic like Generics, Spring basics, Java Records/Sealed Classes, or
SOLID Principles.)*
