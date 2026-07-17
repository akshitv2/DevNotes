---
parent: Java
nav_order: 2
layout: default
---

# Java Interview Preparation Notes

---

## 1. Java Basics & Fundamentals

### 1.1 Java Platform Overview

- **JDK (Java Development Kit)**: Contains JRE + development tools (javac, javadoc, debugger). Can compile java code
- **JRE (Java Runtime Environment)**: Contains JVM + core libraries needed to run Java apps. (All System, Object Classes
  are in these libs which are hardcoded and required by java to run)
- **JVM (Java Virtual Machine)**: Executes bytecode; provides platform independence ("Write Once, Run Anywhere").
- **JIT (Just-In-Time Compiler)**: Part of JVM; compiles hot bytecode paths to native machine code at runtime for
  performance.

### Components of JVM:

1. **Classloader**:  
   Loads classes at runtime whenever they're needed (not all at once on init)  
   Components:
    1. **Bootstrap Classloader**:  
       Required to load all java code, this loads native code (not java code)
    2. **Extensions Classloader**:  
       Loads all classes from jre/libs i.e. system libs
    3. **Application Classloader**:    
       Loads the application classes

    - **Linking**:  
      Performs 3 steps:
        1. Verification (ensures bytecode is valid)
        2. Preparation (allocates memory for static variables)
        3. Resolution (replaces symbolic references with direct memory references).

    - Note: Loading and linking happens lazily as needed and is thus not just a startup task, this is why when a class
      is required and not found it throws NoClassDefFoundError
2. **Runtime Data Area**:  
   The JVM organizes memory into several distinct areas during execution:
    1. **Method Area**:  Stores class-level data, including static variables and bytecode for methods.
    2. **Heap**: The primary area for dynamic memory allocation; When one instantiates an object of a class it's put
       in heap
    3. **Stack**: Each thread has its own stack, storing "frames" that contain local variables and partial results
       for method execution.
    4. **PC Registers**: Contains the address of the JVM instruction currently being executed for each thread.
    5. **Native Method Stack**: Stores instructions for native methods (written in languages like C or C++) since JVM
       relies on native code to interface with the CPU, GPU, or physical memory and OS

    - Note: Memory usually refers to Heap and Stack only since that's where most JVM issues occur

3. **Execution Engine**:  
   Central component of the JVM that communicates with the underlying OS and hardware to execute the bytecode.  
   Composed of:
    - Interpreter: Reads and executes bytecode instructions one by one. Slow for repeated code.
    - JIT (Just-In-Time) Compiler: Compiles frequently used bytecode (hotspots) into native machine code to improve
      performance.
    - Garbage Collector (GC): Automatically identifies and deletes unreferenced objects from the Heap to free up
      memory.

4. **Garbage Collector**:  
   Collects and removes unreferenced objects  
   Mark and Sweep: It "marks" objects that are still in use and "sweeps" (deletes) those that aren't.  
   Types:
    1. **G1 (Garbage First)**: Default since java 9; Breaks memory into small pieces, clears most garbage filled
       piece
       first balancing throughput and latency
    2. **ZGC (Z Garbage Collector)**: Scalable, low latency, cpu taxing (since it clears concurrently), for low
       latency
       when RAM is massive
    3. **Shenandoah**: RedHat's version of ZGC which is Even effective at smaller RAM sizes

5. **Java Flight Recorder (JFR)**:
    - Profiling and event-collection framework built into the Java Virtual Machine (JVM)
    - Captures discrete events such as thread stalls, GC (Garbage Collection) pauses, CPU usage, and I/O activity

### 1.2 Compilation & Execution Flow

```
.java file --(javac)--> .class file (bytecode) --(JVM Class Loader)--> Execution
```

- Class Loader Subsystem: Loading → Linking (Verify, Prepare, Resolve) → Initialization.
- Types of class loaders: Bootstrap → Extension/Platform → Application/System (delegation hierarchy — parent-first).

### 1.3 Data Types

- **Primitives (8)**: byte, short, int, long, float, double, char, boolean.
- **Wrapper classes**: Integer, Long, Double, Character, Boolean, etc. — enable autoboxing/unboxing and use in
  Collections (which need Objects).
- Default values differ for fields (0, null, false) vs local variables (must be explicitly initialized — no default).

> 🎯 Often Asked: Difference between primitive and wrapper types; autoboxing pitfalls (e.g., `==` comparison on Integer
> objects failing outside -128 to 127 cache range); why local variables need explicit initialization.

### 1.4 Variables & Literals

- Instance variables, static (class) variables, local variables.
- `final` variable = constant, must be assigned once.
- Note: `final` keyword has multiple uses:
    - Variables:
        - Local Variables: Must be assigned a value exactly once.
        - Instance Variables: Can be initialized at the time of declaration, inside an instance initializer block, or
          within the constructor
        - Static Variables (Constants): Can be initialized at declaration or inside a static block. They are typically
          named in UPPERCASE_SNAKE_CASE.
    - Methods:
        - A method declared as `final` cannot be overridden by subclasses.
    - Class:
        - A class declared as `final` cannot be extended (inherited). Used for security

### 1.5 Operators & Control Flow

- Standard arithmetic, relational, logical, bitwise, ternary operators.
- `switch` supports int, char, String (since Java 7), enums; Java 14+ introduced switch expressions and pattern
  matching (Java 21 finalized pattern matching for switch).

---

## 2. Object-Oriented Programming (OOP)

### 2.1 Four Pillars

1. **Encapsulation** – bundling data + methods as a single unit; achieved via private fields + public getters/setters.
2. **Inheritance** – code reuse via `extends`/`implements`; Java supports single inheritance for classes, multiple for
   interfaces.
3. **Polymorphism**
    - *Compile-time (static)*: Method overloading.
    - *Runtime (dynamic)*: Method overriding, achieved via dynamic method dispatch.
4. **Abstraction** – hiding implementation details via abstract classes/interfaces.

> 🎯 Often Asked: Difference between overloading and overriding; can we override static/private/final methods (No —
> static is hidden not overridden, private/final can't be overridden); real-world examples of each pillar.

### 2.2 Abstract Class vs Interface

| Aspect               | Abstract Class               | Interface                                                                   |
|----------------------|------------------------------|-----------------------------------------------------------------------------|
| Methods              | Can have abstract + concrete | Since Java 8: default, static, private methods allowed; abstract by default |
| Fields               | Instance variables allowed   | Only `public static final` constants                                        |
| Constructor          | Yes                          | No                                                                          |
| Multiple inheritance | Not supported                | Supported (a class can implement many)                                      |
| Access modifiers     | Any                          | Public (implicitly)                                                         |

> 🎯 Often Asked: When to use abstract class vs interface; functional interfaces; diamond problem with default methods
> and how Java resolves it (explicit override required).

### 2.2.1 Inheritance
- Constructors are not inherited, subclass constructor needs to call `super()` as first statement to init
- Subclass can override existing method
- In java one class can only extend one parent class
- No Multiple inheritance: Only one parent, avoids ambiguity when two parent classes have same method

### 2.3 Constructors

- Default, parameterized, copy constructor (not built-in like C++, done manually).
- Constructor chaining: `this()` and `super()` — must be the first statement.
- Constructors are not inherited.

### 2.4 `this` vs `super`

- `this` refers to current instance; `super` refers to parent class instance/methods/constructor.

### 2.5 Access Modifiers

- Determine where a particular class, method or variable can be used within code
- `private` (class only) < default/package-private < `protected` (package + subclasses) < `public` (everywhere).  
  Crucial for encapsulation
- ℹ️Note: Access modifiers in Java control visibility based on both geographic location (packages) and the chain of
  inheritance (subclasses).

| Modifier             | Class | Package | Subclass | World |
|----------------------|-------|---------|----------|-------|
| public               | Yes   | Yes     | Yes      | Yes   |
| protected            | Yes   | Yes     | Yes      | No    |
| Default (no keyword) | Yes   | Yes     | No       | No    |
| private              | Yes   | No      | No       | No    |

### 2.6 `static` Keyword

- Static variables: shared across all instances (class-level).
- Static methods: can't access instance members directly, no `this`/`super`.
- Static blocks: run once at class loading, used for static initialization.
- Static nested classes vs inner classes.

### 2.7 `final` Keyword

- Final variable → constant.
- Final method → cannot be overridden.
- Final class → cannot be extended (e.g., `String`, `Integer`).

### 2.8 Object Class Methods

- `equals()`, `hashCode()`, `toString()`, `clone()`, `getClass()`, `wait()/notify()/notifyAll()`.

> 🎯 Often Asked: The `equals()`/`hashCode()` contract — if two objects are equal, hashCodes must be equal (not vice
> versa); why overriding one without the other breaks HashMap/HashSet behavior.

### 2.9 Object Cloning

- Shallow copy (default `Object.clone()`) vs deep copy (manual or via serialization/copy constructors).
- Marker interface `Cloneable` needed, else `CloneNotSupportedException`.

---

## 3. Strings in Java

### 3.1 String Immutability

- `String` objects are immutable — any modification creates a new object.
- Reasons: security (used in class loading, network connections), thread-safety, hashcode caching (safe as HashMap
  keys), String pool reuse.

### 3.2 String Pool (String Intern Pool)

- `String s1 = "abc";` → stored in String Constant Pool (part of heap since Java 7+).
- `new String("abc")` → creates new object in heap, bypassing the pool.
- `.intern()` forces pooling.

> 🎯 Often Asked: `String s1 = "abc"; String s2 = new String("abc"); s1 == s2` → false (different memory);
`s1.equals(s2)` → true. Also asked: why String is immutable, and String vs StringBuilder vs StringBuffer.

### 3.3 String vs StringBuilder vs StringBuffer

|               | Mutable? | Thread-safe?       | Performance                     |
|---------------|----------|--------------------|---------------------------------|
| String        | No       | N/A (immutable)    | Slow for concatenation in loops |
| StringBuilder | Yes      | No                 | Fast                            |
| StringBuffer  | Yes      | Yes (synchronized) | Slower than StringBuilder       |

### 3.4 Common String Methods

- `substring()`, `split()`, `replace()`, `trim()/strip()`, `equalsIgnoreCase()`, `compareTo()`, `format()`.
- Text blocks (`"""`) introduced in Java 15 for multi-line strings.

---

## 4. Exception Handling

### 4.1 Exception Hierarchy

```
Throwable
 ├── Error (unchecked, unrecoverable: OutOfMemoryError, StackOverflowError)
 └── Exception
      ├── Checked Exceptions (IOException, SQLException) — must be handled/declared
      └── RuntimeException (unchecked: NullPointerException, ArrayIndexOutOfBoundsException, ArithmeticException)
```

### 4.2 Checked vs Unchecked

- Checked: checked at compile-time, must be caught or declared via `throws`.
- Unchecked: subclass of `RuntimeException`, not enforced at compile-time.

> 🎯 Often Asked: Why does Java have both checked and unchecked exceptions; custom exception creation; difference between
`throw` and `throws`.

### 4.3 try-catch-finally

- `finally` always executes (except `System.exit()` or JVM crash), used for resource cleanup.
- Multi-catch: `catch (IOException | SQLException e)`.
- Try-with-resources (Java 7+): auto-closes resources implementing `AutoCloseable`.

### 4.4 Custom Exceptions

- Extend `Exception` (checked) or `RuntimeException` (unchecked) based on need.

### 4.5 Exception Handling Best Practices

- Don't swallow exceptions silently.
- Catch specific exceptions before generic ones.
- Avoid using exceptions for normal control flow.

---

## 5. Collections Framework

### 5.1 Hierarchy Overview

```
Collection
 ├── List (ordered, duplicates allowed): ArrayList, LinkedList, Vector
 ├── Set (no duplicates): HashSet, LinkedHashSet, TreeSet
 └── Queue/Deque: PriorityQueue, ArrayDeque, LinkedList

Map (key-value, not a Collection): HashMap, LinkedHashMap, TreeMap, Hashtable, ConcurrentHashMap
```

### 5.2 List Implementations

- **ArrayList**: backed by resizable array; O(1) get, O(n) insert/delete (except at end); not synchronized.
- **LinkedList**: doubly linked list; O(1) insert/delete at ends, O(n) get; implements both List and Deque.
- **Vector**: legacy, synchronized version of ArrayList (slower, rarely used now).

> 🎯 Often Asked: ArrayList vs LinkedList performance trade-offs; how ArrayList grows internally (default capacity 10,
> grows by 1.5x); fail-fast vs fail-safe iterators.

### 5.3 Set Implementations

- **HashSet**: backed by HashMap internally, no order guarantee, O(1) average operations.
- **LinkedHashSet**: maintains insertion order.
- **TreeSet**: sorted order (Red-Black tree / `NavigableSet`), O(log n) operations, requires `Comparable`/`Comparator`.

### 5.4 Map Implementations

- **HashMap**: array of buckets + linked list/red-black tree (treeified after 8 collisions in a bucket, Java 8+); allows
  one null key, multiple null values; not thread-safe.
- **LinkedHashMap**: maintains insertion (or access) order; useful for LRU cache implementations.
- **TreeMap**: sorted by keys, implements `NavigableMap`, O(log n).
- **Hashtable**: legacy, synchronized, no null keys/values.
- **ConcurrentHashMap**: thread-safe, segment/bucket-level locking (Java 8+ uses CAS + synchronized blocks per bin, not
  the old segment-lock model).

> 🎯 Often Asked: How HashMap works internally (hashing, bucket index calculation, collision handling via chaining then
> tree-ification); HashMap vs Hashtable vs ConcurrentHashMap; what happens on hashCode collision; load factor &
> resizing (
> default 0.75, doubles capacity).

### 5.5 Iterators

- `Iterator` (forward-only, remove supported), `ListIterator` (bidirectional, for Lists only).
- **Fail-fast**: throws `ConcurrentModificationException` if collection structurally modified during iteration (
  ArrayList, HashMap).
- **Fail-safe**: works on a clone/snapshot, no exception (CopyOnWriteArrayList, ConcurrentHashMap).

### 5.6 Comparable vs Comparator

- `Comparable`: `compareTo()`, defines natural ordering, implemented by the class itself.
- `Comparator`: `compare()`, external, allows multiple sort orders, often used with lambdas:
  `list.sort((a,b) -> a.getAge() - b.getAge())`.

### 5.7 Queue/Deque

- `PriorityQueue`: heap-based, orders elements by natural ordering/comparator, not FIFO.
- `ArrayDeque`: resizable array, can be used as stack or queue, faster than `Stack`/`LinkedList` for that purpose.

### 5.8 Collections Utility Class

- `Collections.sort()`, `Collections.unmodifiableList()`, `Collections.synchronizedList()`, `Collections.emptyList()`.

---

## 6. Generics

- Enables type-safety at compile time, eliminates need for explicit casting.
- **Bounded types**: `<T extends Number>`.
- **Wildcards**: `<?>` (unknown), `<? extends T>` (upper bound, read-only/producer), `<? super T>` (lower bound,
  write/consumer) — PECS principle ("Producer Extends, Consumer Super").
- **Type erasure**: generic type info removed at runtime by compiler, replaced with bounds or Object — this is why you
  can't do `new T()` or `instanceof T`.

> 🎯 Often Asked: What is type erasure and its implications; PECS principle; why generic arrays can't be created
> directly (`new T[]` not allowed).

---

## 7. Multithreading & Concurrency

### 7.1 Creating Threads

- Extend `Thread` class (override `run()`) or implement `Runnable` (preferred — allows extending other classes, better
  separation of task from execution mechanism).
- `Callable` (returns value + can throw checked exception) vs `Runnable` (no return, no checked exceptions).

### 7.2 Thread Lifecycle

```
NEW → RUNNABLE → RUNNING → (BLOCKED/WAITING/TIMED_WAITING) → TERMINATED
```

### 7.3 Synchronization

- `synchronized` keyword: method-level or block-level; uses intrinsic lock (monitor) per object.
- `static synchronized` locks on the Class object, not instance.
- Deadlock: two+ threads waiting on each other's locks forever. Avoid via consistent lock ordering, timeouts.

> 🎯 Often Asked: Difference between synchronized method and block; how to avoid deadlock; difference between `wait()`/
`sleep()` (wait releases lock, is called on object monitor; sleep doesn't release lock, called on Thread).

### 7.4 volatile Keyword

- Ensures visibility of changes across threads (reads/writes go directly to main memory, not thread-local cache).
- Does NOT guarantee atomicity (e.g., `count++` on volatile int is still not thread-safe).

### 7.5 java.util.concurrent Package

- **Executors/ExecutorService**: thread pool management (`newFixedThreadPool`, `newCachedThreadPool`,
  `newSingleThreadExecutor`).
- **Future/CompletableFuture**: async computation results; `CompletableFuture` supports chaining (`thenApply`,
  `thenCompose`, `thenCombine`).
- **Locks**: `ReentrantLock` (more flexible than synchronized — tryLock, fairness, interruptible), `ReadWriteLock`.
- **Atomic classes**: `AtomicInteger`, `AtomicLong` — lock-free thread-safe operations via CAS (Compare-And-Swap).
- **Concurrent collections**: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue` (producer-consumer pattern).
- **CountDownLatch, CyclicBarrier, Semaphore**: thread coordination utilities.

> 🎯 Often Asked: ExecutorService vs creating raw threads; CountDownLatch vs CyclicBarrier; how CAS works and why it's
> lock-free; producer-consumer implementation using BlockingQueue.

### 7.6 Thread Safety Approaches

1. Immutability (immutable objects are inherently thread-safe).
2. Synchronization (locks).
3. Atomic variables.
4. Thread confinement (`ThreadLocal`).
5. Concurrent collections.

---

## 8. Java Memory Management & JVM Internals

### 8.1 JVM Memory Areas

- **Heap**: objects live here; divided into Young Generation (Eden + Survivor S0/S1) and Old Generation (Tenured).
- **Stack**: per-thread, stores method frames, local variables, partial results — `StackOverflowError` if exceeded.
- **Method Area/Metaspace** (Java 8+, replaced PermGen): stores class metadata, static variables, constant pool.
- **PC Register**: per-thread, holds address of current executing instruction.
- **Native Method Stack**: for native (non-Java) method calls.

### 8.2 Garbage Collection (GC)

- Automatic memory management — reclaims objects with no reachable references.
- **Generational hypothesis**: most objects die young → Young Gen collected frequently (Minor GC), Old Gen less often (
  Major/Full GC).
- **GC Algorithms**: Serial, Parallel, CMS (deprecated), **G1 (Garbage First)** — default since Java 9, **ZGC** and *
  *Shenandoah** — low-latency collectors for large heaps.
- Objects become eligible for GC when unreachable (no strong references) — `System.gc()` only *suggests* GC, doesn't
  guarantee it.

> 🎯 Often Asked: Explain the generational GC model; difference between minor and major GC; strong vs weak vs soft vs
> phantom references; how memory leaks happen despite GC (e.g., static collections holding references, unclosed
> resources,
> listener leaks).

### 8.3 Reference Types

- **Strong**: normal reference, prevents GC.
- **Soft**: cleared only when JVM needs memory (used in caches).
- **Weak**: cleared on next GC cycle regardless of memory pressure (`WeakHashMap`).
- **Phantom**: enqueued after finalization, used for cleanup actions before memory reclaim.

---

## 9. Java 8+ Features (Very Commonly Asked)

### 9.1 Lambda Expressions

- Syntax: `(parameters) -> expression/block`.
- Enables treating functionality as a method argument (functional programming style).

### 9.2 Functional Interfaces

- Interface with exactly one abstract method (SAM), annotated `@FunctionalInterface` (optional but recommended).
- Built-in ones: `Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`, `BiFunction<T,U,R>`, `UnaryOperator<T>`.

> 🎯 Often Asked: Write/explain a custom functional interface; difference between `Function`, `Predicate`, `Consumer`,
`Supplier`; can a functional interface have default/static methods (yes, only one abstract method restriction applies).

### 9.3 Streams API

- Declarative way to process collections: `list.stream().filter(...).map(...).collect(...)`.
- **Intermediate operations** (lazy): `filter`, `map`, `sorted`, `distinct`, `limit`, `flatMap`.
- **Terminal operations** (trigger execution): `collect`, `forEach`, `reduce`, `count`, `anyMatch`, `findFirst`.
- Streams are single-use (consumed after a terminal operation).
- `Collectors`: `toList()`, `toMap()`, `groupingBy()`, `partitioningBy()`, `joining()`.
- Parallel streams: `parallelStream()` — uses ForkJoinPool, useful for CPU-bound bulk operations on large data; not
  always faster (overhead for small datasets).

> 🎯 Often Asked: Difference between intermediate and terminal operations; how `flatMap` differs from `map`; when NOT to
> use parallel streams; write a stream pipeline to group/sort/aggregate data (very common coding round question).

### 9.4 Optional

- Wrapper to avoid `NullPointerException`; `Optional.of()`, `Optional.ofNullable()`, `Optional.empty()`.
- Methods: `isPresent()`, `orElse()`, `orElseGet()`, `orElseThrow()`, `map()`, `filter()`.

### 9.5 Default & Static Methods in Interfaces

- Allows adding new methods to interfaces without breaking existing implementations (backward compatibility).

### 9.6 Method References

- `ClassName::methodName`, `object::instanceMethod`, `ClassName::new` (constructor reference).

### 9.7 Date/Time API (java.time)

- Replaced old `Date`/`Calendar` (mutable, not thread-safe).
- `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `Duration`, `Period` — all immutable and thread-safe.

### 9.8 Later Java Version Highlights (Often Asked in "What's New" Rounds)

- **Java 9**: Module system (Project Jigsaw), `var` not yet (that's 10).
- **Java 10**: Local variable type inference (`var`).
- **Java 11**: New String methods (`isBlank`, `strip`, `repeat`), HTTP Client API.
- **Java 14/15**: Records (preview), Text blocks, Pattern matching for `instanceof`.
- **Java 16/17**: Records finalized, sealed classes.
- **Java 21 (LTS)**: Virtual threads (Project Loom), pattern matching for switch, record patterns.

> 🎯 Often Asked: What are Records and how they differ from normal classes (implicit constructor, getters,
> equals/hashCode/toString, immutable); what are sealed classes; what are virtual threads and why they matter for
> scalability.

---

## 10. Design Patterns (Commonly Asked in Java Interviews)

### 10.1 Creational

- **Singleton**: one instance only. Approaches: eager initialization, lazy initialization, double-checked locking with
  `volatile`, enum-based singleton (safest against reflection/serialization attacks).
- **Factory / Abstract Factory**: delegate object creation to a factory method/class.
- **Builder**: step-by-step object construction, useful for objects with many optional parameters (e.g.,
  `Lombok @Builder`, `StringBuilder`).

### 10.2 Structural

- **Adapter**: converts one interface into another expected by client.
- **Decorator**: adds behavior dynamically without altering original class (e.g., `BufferedReader` wrapping
  `FileReader`).
- **Proxy**: placeholder/surrogate controlling access to another object (used heavily in Spring AOP).

### 10.3 Behavioral

- **Observer**: one-to-many dependency, subject notifies observers on state change (used in event listeners).
- **Strategy**: encapsulate interchangeable algorithms, select at runtime (e.g., `Comparator` passed to `sort()`).
- **Template Method**: define algorithm skeleton in base class, let subclasses override specific steps.

> 🎯 Often Asked: Implement thread-safe Singleton; why enum singleton is considered best; real examples of these patterns
> from Java standard library or Spring framework.

---

## 11. I/O & Serialization

### 11.1 I/O Streams

- **Byte streams**: `InputStream`/`OutputStream` (for binary data).
- **Character streams**: `Reader`/`Writer` (for text, handles encoding).
- **Buffered streams**: `BufferedReader`, `BufferedInputStream` — reduce I/O calls via internal buffer.
- **NIO (New I/O)**: `Channels`, `Buffers`, `Selectors` — non-blocking I/O, better for high-throughput apps.

### 11.2 Serialization

- Converting object to byte stream (`Serializable` marker interface) for storage/transfer.
- `transient` keyword: excludes a field from serialization.
- `serialVersionUID`: version control for serialized classes — mismatch causes `InvalidClassException` on
  deserialization.

> 🎯 Often Asked: Why is `serialVersionUID` important; how to serialize an object graph with transient fields;
> Serializable vs Externalizable.

---

## 12. Miscellaneous but Frequently Asked Topics

- **equals() and == difference**: `==` compares references (or values for primitives); `equals()` compares
  logical/content equality (when overridden).
- **Autoboxing/Unboxing pitfalls**: NPE risk when unboxing a null wrapper in arithmetic/conditional contexts.
- **Varargs**: `method(String... args)` — internally treated as an array.
- **Enum**: type-safe constants, can have fields/methods/constructors, singleton-safe.
- **Reflection**: inspect/modify classes, methods, fields at runtime (`Class<?>`, `Method`, `Field`) — used by
  frameworks like Spring, Hibernate.
- **Annotations**: metadata (`@Override`, `@Deprecated`, `@FunctionalInterface`); custom annotations via `@interface`.
- **Inner classes**: member inner class, static nested class, local inner class, anonymous inner class — each with
  different access to outer class state.
- **Immutability**: how to create an immutable class (final class, final fields, no setters, deep copy in
  constructor/getters for mutable fields).

> 🎯 Often Asked: How to design an immutable class (classic follow-up: what if a field is a mutable object like `List` or
`Date` — need defensive copying); difference between `Enum` and constants (`static final int`); reflection
> performance/security concerns.

---

## Suggested Study Order

1. OOP fundamentals + Strings (foundation, always asked first)
2. Collections Framework (heavily tested, especially HashMap internals)
3. Exception Handling
4. Multithreading & Concurrency (mid-to-senior roles focus heavily here)
5. Java 8 Streams/Lambdas (near-universal in modern interviews)
6. JVM/Memory Management (for deeper/senior-level rounds)
7. Design Patterns + Misc (rounds out system design discussions)

---

*Let me know which topic you'd like to go deeper on, or when you're ready, I can add interview questions (conceptual +
coding) for any of these sections.*
