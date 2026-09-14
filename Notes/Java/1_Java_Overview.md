# Java Interview Preparation Notes

## Table of Contents

- [1. Java Basics & Fundamentals](#1-java-basics--fundamentals)
    - [1.1 Java Platform Overview](#11-java-platform-overview)
    - [1.2 Compilation & Execution Flow](#12-compilation--execution-flow)
    - [1.3 Data Types](#13-data-types)
    - [1.4 Variables & Literals](#14-variables--literals)
    - [1.5 Operators & Control Flow](#15-operators--control-flow)
- [2. Object-Oriented Programming (OOP)](#2-object-oriented-programming-oop)
    - [2.1 Four Pillars](#21-four-pillars)
    - [2.2 Abstract Class vs Interface](#22-abstract-class-vs-interface)
    - [2.3 Inheritance](#23-inheritance)
    - [2.4 Constructors](#24-constructors)
    - [2.5 `this` vs `super`](#25-this-vs-super)
    - [2.6 Access Modifiers](#26-access-modifiers)
    - [2.7 `static` Keyword](#27-static-keyword)
    - [2.8 `final` Keyword](#28-final-keyword)
    - [2.9 Object Class Methods](#29-object-class-methods)
    - [2.10 Object Cloning](#210-object-cloning)
- [3. Strings in Java](#3-strings-in-java)
    - [3.1 String Immutability](#31-string-immutability)
    - [3.2 String Pool (String Intern Pool)](#32-string-pool-string-intern-pool)
    - [3.3 String vs StringBuilder vs StringBuffer](#33-string-vs-stringbuilder-vs-stringbuffer)
    - [3.4 Common String Methods](#34-common-string-methods)
- [4. Exception Handling](#4-exception-handling)
    - [4.1 Exception Hierarchy](#41-exception-hierarchy)
    - [4.2 Checked vs Unchecked](#42-checked-vs-unchecked)
    - [4.3 try-catch-finally](#43-try-catch-finally)
    - [4.4 Custom Exceptions](#44-custom-exceptions)
    - [4.5 Exception Handling Best Practices](#45-exception-handling-best-practices)
- [5. Collections Framework](#5-collections-framework)
    - [5.1 Hierarchy Overview](#51-hierarchy-overview)
    - [5.2 List Implementations](#52-list-implementations)
    - [5.3 Set Implementations](#53-set-implementations)
    - [5.4 Map Implementations](#54-map-implementations)
    - [5.5 Iterators](#55-iterators)
    - [5.6 Comparable vs Comparator](#56-comparable-vs-comparator)
    - [5.7 Queue/Deque/Stack](#57-queuedeuestack)
    - [5.8 Collections Utility Class](#58-collections-utility-class)
- [6. Generics](#6-generics)
- [7. Multithreading & Concurrency](#7-multithreading--concurrency)
    - [7.1 Concurrency Basics & Thread Creation](#71-concurrency-basics--thread-creation)
    - [7.2 Thread Lifecycle](#72-thread-lifecycle)
    - [7.3 Synchronization](#73-synchronization)
    - [7.4 volatile Keyword](#74-volatile-keyword)
    - [7.5 java.util.concurrent Package](#75-javautilconcurrent-package)
    - [7.6 Thread Safety Approaches](#76-thread-safety-approaches)
- [8. Java Memory Management & JVM Internals](#8-java-memory-management--jvm-internals)
    - [8.1 JVM Memory Areas](#81-jvm-memory-areas)
    - [8.2 Garbage Collection (GC)](#82-garbage-collection-gc)
    - [8.3 Reference Types](#83-reference-types)
- [9. Java 8+ Features (Very Commonly Asked)](#9-java-8-features-very-commonly-asked)
    - [9.1 Lambda Expressions](#91-lambda-expressions)
    - [9.2 Functional Interfaces](#92-functional-interfaces)
    - [9.3 Streams API](#93-streams-api)
    - [9.4 Optional](#94-optional)
    - [9.5 Default & Static Methods in Interfaces](#95-default--static-methods-in-interfaces)
    - [9.6 Method References](#96-method-references)
    - [9.7 Date/Time API (java.time)](#97-datetime-api-javatime)
    - [9.8 Later Java Version Highlights (Often Asked in "What's New" Rounds)](#98-later-java-version-highlights-often-asked-in-whats-new-rounds)
- [10. Design Patterns (Commonly Asked in Java Interviews)](#10-design-patterns-commonly-asked-in-java-interviews)
    - [10.1 Creational](#101-creational)
    - [10.2 Structural](#102-structural)
    - [10.3 Behavioral](#103-behavioral)
- [11. I/O & Serialization](#11-io--serialization)
    - [11.1 I/O Streams](#111-io-streams)
    - [11.2 Serialization](#112-serialization)
- [12. Miscellaneous but Frequently Asked Topics](#12-miscellaneous-but-frequently-asked-topics)
- [13. Suggested Study Order](#13-suggested-study-order)
- [14. History](#14-history)
    - [14.1 Phases](#141-phases)
    - [14.2 Features Added in Versions](#142-features-added-in-versions)

---

## 1. Java Basics & Fundamentals

### 1.1 Java Platform Overview

**JDK (Java Development Kit)** Contains JRE + development tools (javac, javadoc, debugger). Can compile java code  
**JRE (Java Runtime Environment)**: Contains JVM + core libraries needed to run Java apps. (All System, Object Classes
are in these libs which are hardcoded and required by java to run)  
**JVM (Java Virtual Machine)**: Executes bytecode; provides platform independence ("Write Once, Run Anywhere").  
**JIT (Just-In-Time Compiler)**: Part of JVM; compiles hot bytecode paths to native machine code at runtime for
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

    - Loading means bringing the `.class` file into JVM memory.
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
    - **Interpreter:** Reads and executes bytecode instructions one by one. Slow for repeated code.
    - **JIT (Just-In-Time) Compiler:** Compiles frequently used bytecode (hotspots) into native machine code to improve
      performance.
    - **Garbage Collector (GC):** Automatically identifies and deletes unreferenced objects from the Heap to free up
      memory.

4. **Garbage Collector**:  
   Collects and removes unreferenced objects  
   Mark and Sweep: It "marks" objects that are still in use and "sweeps" (deletes) those that aren't.  
   Types:
    1. **G1 (Garbage First)**: Default since java 9; Breaks memory into small pieces, clears most garbage filled
       piece first balancing throughput and latency. Causes sizable pauses (compared to others)
    2. **ZGC (Z Garbage Collector)**: Scalable, low latency, cpu taxing (since it clears concurrently), for low
       latency
       when RAM is massive
    3. **Shenandoah**: RedHat's version of ZGC which is Even effective at smaller RAM sizes

5. **Java Flight Recorder (JFR)**:
    - Profiling and event-collection framework built into the Java Virtual Machine (JVM)
    - Captures discrete events such as thread stalls, GC (Garbage Collection) pauses, CPU usage, and I/O activity

6. Key JVMs:
    - GraalVM: High-performance Java Virtual Machine (JVM) and software development ecosystem created by Oracle.
        - **Ahead-of-Time (AOT) Compilation:** Compiles Java applications into standalone native executables (using
          GraalVM Native Image), resulting in faster startup times and lower memory footprints.
        - **Polyglot Capabilities:** Allows code written in Java, JavaScript, Python, Ruby, and WebAssembly to run
          seamlessly together and interoperate within the same application.
        - **Advanced Just-in-Time (JIT) Compiler:** Utilizes the Graal compiler to optimize application performance
          dynamically at runtime.

### 1.2 Compilation & Execution Flow


```

.java file --(javac)--> .class file (bytecode) --(JVM Class Loader)--> Execution

```

- Class Loader Subsystem: Loading → Linking (Verify, Prepare, Resolve) → Initialization.

### 1.3 Data Types

- **Primitives (8)**: byte, short, int, long, float, double, char, boolean.
- **Wrapper classes**: Integer, Long, Double, Character, Boolean, etc. — enable autoboxing/unboxing and use in
  Collections (which need Objects).
- Default values differ for fields (0, null, false) vs local variables (must be explicitly initialized — no default).

- 🎯 Often Asked: Difference between primitive and wrapper types;
    - Data Storage: Primitives stored straight in stack memory faster to use, wrapper in heap with a pointer
    - Primitives cannot be null unlike wrappers
    - Wrappers required for collections
- autoboxing pitfalls (e.g., `==` comparison on Integer
    - it compares object references, not their values. This often leads to unexpected bugs.
- why local variables need explicit initialization.
    - Don't get init to 0 or false like class variables, init prevents reading uncleaned memory value

### 1.4 Variables & Literals

- Instance variables, static (class) variables, local variables.
- `final` variable = constant, must be assigned once.
- Note: `final` keyword has multiple uses:
    - Variables: Can be assigned only once (depending on local at creation, instance at init, static in class)
    - Methods: A method declared as `final` cannot be overridden by subclasses.
    - Class:  A class declared as `final` cannot be extended (inherited). Used for security

### 1.5 Operators & Control Flow

- Standard arithmetic, relational, logical, bitwise, ternary operators.
- `switch` supports int, char, String (since Java 7), enums; Java 14+ introduced switch expressions and pattern
  matching (Java 21 finalized pattern matching for switch).

---

## 2. Object-Oriented Programming (OOP)

### 2.1 Four Pillars

1. **Encapsulation** –
    - bundling data + methods as a single unit and restricting access to certain components achieved via private
      fields + public getters/setters.
    - 🟢 Prevents unauthorized external modification and corrupt state bugs by controlling access strictly through
      getter/setter methods.
2. **Inheritance**
    - code reuse via `extends`/`implements`; Java supports single inheritance for classes, multiple for
      interfaces.
3. **Polymorphism**: Allows different implementation for same method call
    - *Compile-time (static)*: Method overloading.
    - *Runtime (dynamic)*: Method overriding, achieved via dynamic method dispatch.
    - 🟢 Flexibility: Enables writing modular code that can process different data types or object behaviors through a
      uniform API without modifying existing logic.
4. **Abstraction**
    - hiding implementation details via abstract classes/interfaces.
    - 🟢Reduces complexity: Allows developers to interact with system components without needing to understand or manage
      internal logic.

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

> 🎯 Often Asked:

- When to use abstract class vs interface;
    - Abstract class **Is A** relationship, when you need instance variables
    - Interface **Can Do** relationship
    - Single or multiple inheritance
- functional interfaces
    - interface that contains exactly one abstract method, useful for lambda expressions
    - e.g. `Runnable newWay = () -> System.out.println("Running");`  implies execute this inside the only method in this
      functional interface
- diamond problem with default methods and how Java resolves it
    - When two interfaces are implemented with same default
        - Either explicitly override both
        - Or Refer one my name `InterfaceName.super.methodName()`

### 2.3 Inheritance

- Constructors are not inherited, subclass constructor needs to call `super()` as first statement to init
- Subclass can override existing method
- In java one class can only extend one parent class
- No Multiple inheritance: Only one parent, avoids ambiguity when two parent classes have same method

### 2.4 Constructors

- Default, parameterized, copy constructor (not built-in like C++, done manually).
- Constructor chaining: `this()` and `super()` — must be the first statement.
- Constructors are not inherited.

### 2.5 `this` vs `super`

- `this` refers to current instance; `super` refers to parent class instance/methods/constructor.

### 2.6 Access Modifiers

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

### 2.7 `static` Keyword

- Static variables: shared across all instances (class-level).
- Static methods: can't access instance members directly, no `this`/`super`.
- Static blocks: run once at class loading, used for static initialization.
- Static nested classes vs inner classes.

### 2.8 `final` Keyword

- Final variable → constant.
- Final method → cannot be overridden.
- Final class → cannot be extended (e.g., `String`, `Integer`).

### 2.9 Object Class Methods

- `equals()`, `hashCode()`, `toString()`, `clone()`, `getClass()`, `wait()/notify()/notifyAll()`.

> 🎯 Often Asked: The `equals()`/`hashCode()` contract — if two objects are equal, hashCodes must be equal (not vice
> versa); why overriding one without the other breaks HashMap/HashSet behavior.

### 2.10 Object Cloning

- Shallow copy (default `Object.clone()`) vs deep copy (manual or via serialization/copy constructors).
- Marker interface `Cloneable` needed, else `CloneNotSupportedException`.

---

## 3. Strings in Java

### 3.1 String Immutability

- `String` objects are immutable — any modification creates a new object.
- Reasons: security (used in class loading, network connections), thread-safety, hashcode caching (safe as HashMap
  keys), String pool keeps static strings which promotes reuse since multiple can refer the same safely.
- Since java is pass by value important params cannot be modified between methods

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
- **LinkedHashMap**: maintains insertion (or access) order; useful for LRU cache implementations. done by a hashtable +
  a doubly linked list.
- **TreeMap**: sorted by keys, implements `NavigableMap`, O(log n).
- **Hashtable**: legacy, synchronized, no null keys/values.
- **ConcurrentHashMap**: thread-safe, segment/bucket-level locking (Java 8+ uses CAS + synchronized blocks per bin, not
  the old segment-lock model).

> 🎯 Often Asked: How HashMap works internally (hashing, bucket index calculation, collision handling via chaining then
> tree-ification); HashMap vs Hashtable vs ConcurrentHashMap; what happens on hashCode collision; load factor &
> resizing (default 0.75, doubles capacity).

### 5.5 Iterators

- `Iterator` (forward-only, remove supported), `ListIterator` (bidirectional, for Lists only).
- **Fail-fast**: throws `ConcurrentModificationException` if collection structurally modified during iteration (
  ArrayList, HashMap).
- **Fail-safe**: works on a clone/snapshot, no exception (CopyOnWriteArrayList, ConcurrentHashMap).
- No real benifit but allows more precise control over traversal
    - Used in for each loop for(String x:y) (for each can't do remove while looping through)

### 5.6 Comparable vs Comparator

- `Comparable`: `compareTo()`, interface, defines natural ordering, implemented by the class itself.
- `Comparator`: `compare()`, external, allows multiple sort orders, often used with lambdas:
  `list.sort((a,b) -> a.getAge() - b.getAge())`.

### 5.7 Queue/Deque/Stack

| Data structure | Principle | Add        | Remove     |
|----------------|-----------|------------|------------|
| **Stack**      | LIFO      | Top        | Top        |
| **Queue**      | FIFO      | Rear       | Front      |
| **Deque**      | Both ends | Front/Rear | Front/Rear |

- `PriorityQueue`: heap-based, orders elements by natural ordering/comparator, not FIFO.
- `ArrayDeque`: resizable array, can be used as stack or queue, faster than `Stack`/`LinkedList` for that purpose.

### 5.8 Collections Utility Class

- `Collections.sort()`, `Collections.unmodifiableList()`, `Collections.synchronizedList()`, `Collections.emptyList()`.

---

## 6. Generics

Enables type-safety at compile time, eliminates need for explicit casting.

* **Bounded types**: `<T extends Number>`.
* **Wildcards**: `<?>` (unknown), `<? extends T>` (upper bound, read-only/producer), `<? super T>` (lower bound,
  write/consumer) — PECS principle ("Producer Extends, Consumer Super").
* **Type erasure**: generic type info removed at runtime by compiler, replaced with bounds or Object — this is why you
  can't do `new T()` or `instanceof T`.

Example:

```java
static <T Number extends> double square(T x) {
    return x.doubleValue() * x.doubleValue();
}
//Declaration for T comes before return type

```

```java
double retZero(List<? extends Number> x) {
    return 0;
}

<T Number extends> double retZero(List<T> x) {
    return 0;
}
// these are functionally the same since type erasure removes List<...> -> List

```

> 🎯 Often Asked:
> What is type erasure and its implications? Java actually converts `List<String> names = new ArrayList<>();` to
> `List names = new ArrayList();` in runtime
>
>
>
> `String` is applied on the get `String name = (String) names.get(0);`
>
>
>
>
> Implication: `if (obj instanceof List<String>)` ❌ Incorrect
>
>
>
>
> PECS = Producer Extends(read), Consumer Super (write)(Mnemonic), If a collection produces values for you to read, use
> extends.

Note: Java's generic types are invariant by default. This means List is not a subtype of List, even
though Integer is a subtype of Number.

---

## 7. Multithreading & Concurrency

### 7.1 Concurrency Basics & Thread Creation

* Creation via extending `Thread` or implementing `Runnable` / `Callable<V>`.

### 7.2 Thread Lifecycle

* States: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.

### 7.3 Synchronization

`synchronized` means only one thread at a time can execute a particular piece of code or access a particular
object’s protected state. Can be method-level or block-level; uses intrinsic lock (monitor) per object.

`static synchronized` locks on the Class object, not instance.

* Deadlock: two+ threads waiting on each other's locks forever. Avoid via consistent lock ordering, timeouts.

> 🎯 Often Asked:

1. Difference between synchronized method and block: Same thing but block gives more granular control
2. how to avoid deadlock;
3. difference between `wait()` and `sleep()` (wait releases lock, is called on object monitor; sleep doesn't release
   lock, called on Thread).

### 7.4 volatile Keyword

Ensures visibility of changes across threads (reads/writes go directly to main memory, not thread-local cache).

Does NOT guarantee atomicity (e.g., `count++` on volatile int is still not thread-safe).

### 7.5 java.util.concurrent Package

* **Executors/ExecutorService**: thread pool management (`newFixedThreadPool`, `newCachedThreadPool`,
  `newSingleThreadExecutor`).
* **Future/CompletableFuture**: async computation results; `CompletableFuture` supports chaining (`thenApply`,
  `thenCompose`, `thenCombine`).
* **Locks**: `ReentrantLock` (more flexible than synchronized — tryLock, fairness, interruptible), `ReadWriteLock`.
* **Atomic classes**: `AtomicInteger`, `AtomicLong` — lock-free thread-safe operations via CAS (Compare-And-Swap).
* **Concurrent collections**: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue` (producer-consumer pattern).
* **CountDownLatch, CyclicBarrier, Semaphore**: thread coordination utilities.

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

* Method Area, Heap, Stack, PC Registers, Native Method Stack.

### 8.2 Garbage Collection (GC)

* Mark and Sweep algorithms, Generational Garbage Collection (Young Gen, Old Gen, Permanent Gen/Metaspace).

### 8.3 Reference Types

* Strong, Soft, Weak, and Phantom references.

---

## 9. Java 8+ Features (Very Commonly Asked)

### 9.1 Lambda Expressions

Syntax: `(parameters) -> expression/block`.

Essentially a quick way to implement a functional interface that lets you **pass behavior as a value**

### 9.2 Functional Interfaces

Interface with exactly one abstract method (SAM), annotated `@FunctionalInterface` (optional but recommended).

Built-in ones: `Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`, `BiFunction<T,U,R>`, `UnaryOperator<T>`.

> 🎯 Often Asked: Write/explain a custom functional interface;

| Interface | Takes | Returns | Typical use |  |
| --- | --- | --- | --- | --- |
| `Function<T, R>` | 1 input | 1 output | Transform something | `Function<String, String> toUpperCase = name -> name.toUpperCase();` |
| `Predicate<T>` | 1 input | `boolean` | Test something | `Predicate<Integer> isEven = n -> n % 2 == 0;` |
| `Consumer<T>` | 1 input | Nothing (`void`) | Do something with it | `Consumer<String> printName = name -> System.out.println(name);` |
| `Supplier<T>` | Nothing | 1 output | Provide/create something | `Supplier<Integer> randomNumber = () -> (int) (Math.random() * 100);` |

We need to call the function.apply for example to execute

**Can a functional interface have default/static methods?** Yes as many as it wants, but only one abstract method

### 9.3 Streams API

* Declarative way to process collections: `list.stream().filter(...).map(...).collect(...)`.
* **Intermediate operations** (lazy): `filter`, `map`, `sorted`, `distinct`, `limit`, `flatMap`.
* **Terminal operations** (trigger execution): `collect`, `forEach`, `reduce`, `count`, `anyMatch`, `findFirst`.
* Streams are single-use (consumed after a terminal operation).
* `Collectors`: `toList()`, `toMap()`, `groupingBy()`, `partitioningBy()`, `joining()`.
* Parallel streams: `parallelStream()` — uses ForkJoinPool, useful for CPU-bound bulk operations on large data; not
  always faster (overhead for small datasets).
* Follows Fluid Api

> 🎯 Often Asked: Difference between intermediate and terminal operations; how `flatMap` differs from `map`; when NOT to
> use parallel streams; write a stream pipeline to group/sort/aggregate data (very common coding round question).

### 9.4 Optional

* Wrapper to avoid `NullPointerException`
* Optional t
* Methods: `isPresent()`, `get`

### 9.5 Default & Static Methods in Interfaces

* Allows adding new methods to interfaces without breaking existing implementations (backward compatibility).

### 9.6 Method References

* `ClassName::methodName`, `object::instanceMethod`, `ClassName::new` (constructor reference).

### 9.7 Date/Time API (java.time)

* Replaced old `Date`/`Calendar` (mutable, not thread-safe).
* `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `Duration`, `Period` — all immutable and thread-safe.

### 9.8 Later Java Version Highlights (Often Asked in "What's New" Rounds)

* **Java 9**: Module system (Project Jigsaw), `var` not yet (that's 10).
* **Java 10**: Local variable type inference (`var`).
* **Java 11**: New String methods (`isBlank`, `strip`, `repeat`), HTTP Client API.
* **Java 14/15**: Records (preview), Text blocks, Pattern matching for `instanceof`.
* **Java 16/17**: Records finalized, sealed classes.
* **Java 21 (LTS)**: Virtual threads (Project Loom), pattern matching for switch, record patterns.

> 🎯 Often Asked: What are Records and how they differ from normal classes (implicit constructor, getters,
> equals/hashCode/toString, immutable); what are sealed classes; what are virtual threads and why they matter for
> scalability.

---

## 10. Design Patterns (Commonly Asked in Java Interviews)

### 10.1 Creational

* Singleton, Factory, Abstract Factory, Builder, Prototype.

### 10.2 Structural

* Adapter, Decorator, Proxy, Facade, Composite.

### 10.3 Behavioral

* Strategy, Observer, Command, Template Method, State.

---

## 11. I/O & Serialization

### 11.1 I/O Streams

* **Byte streams**: `InputStream`/`OutputStream` (for binary data).
* **Character streams**: `Reader`/`Writer` (for text, handles encoding).
* **Buffered streams**: `BufferedReader`, `BufferedInputStream` — reduce I/O calls via internal buffer.
* **NIO (New I/O)**: `Channels`, `Buffers`, `Selectors` — non-blocking I/O, better for high-throughput apps.

### 11.2 Serialization

* Converting object to byte stream (`Serializable` marker interface) for storage/transfer.
* `transient` keyword: excludes a field from serialization.
* `serialVersionUID`: version control for serialized classes — mismatch causes `InvalidClassException` on
  deserialization.

> 🎯 Often Asked: Why is `serialVersionUID` important; how to serialize an object graph with transient fields;
> Serializable vs Externalizable.

---

## 12. Miscellaneous but Frequently Asked Topics

* **equals() and == difference**: `==` compares references (or values for primitives); `equals()` compares
  logical/content equality (when overridden).
* **Autoboxing/Unboxing pitfalls**: NPE risk when unboxing a null wrapper in arithmetic/conditional contexts.
* **Varargs**: `method(String... args)` — internally treated as an array.
* **Enum**: type-safe constants, can have fields/methods/constructors, singleton-safe.
* **Reflection**: inspect/modify classes, methods, fields at runtime (`Class<?>`, `Method`, `Field`) — used by
  frameworks like Spring, Hibernate.
* **Annotations**: metadata (`@Override`, `@Deprecated`, `@FunctionalInterface`); custom annotations via `@interface`.
* **Inner classes**: member inner class, static nested class, local inner class, anonymous inner class — each with
  different access to outer class state.
* **Immutability**: how to create an immutable class (final class, final fields, no setters, deep copy in
  constructor/getters for mutable fields).

> 🎯 Often Asked: How to design an immutable class (classic follow-up: what if a field is a mutable object like `List` or
> `Date` — need defensive copying); difference between `Enum` and constants (`static final int`); reflection
> performance/security concerns.

---

## 13. Suggested Study Order

1. OOP fundamentals + Strings (foundation, always asked first)
2. Collections Framework (heavily tested, especially HashMap internals)
3. Exception Handling
4. Multithreading & Concurrency (mid-to-senior roles focus heavily here)
5. Java 8 Streams/Lambdas (near-universal in modern interviews)
6. JVM/Memory Management (for deeper/senior-level rounds)
7. Design Patterns + Misc (rounds out system design discussions)

---

## 14. History

### 14.1 Phases

1. Sun Microsystems owned:
* WORA ("Write Once, Run Anywhere")
* Two types of Java:
* Java SE: Consumer Applications libraries only
* Java EE: Proprietary Libraries for uses like JPA, DB etc




2. Spring Introduction:
* Spring decomposed giant EE servers into small libraries to use as need
* Used Inversion of control
* Blurred SE and EE


3. Oracle Acquisition of Sun (2010)
* Legal battle against Google
* Oracle gave up managing Java EE and donated to Eclipse Foundation


4. Jakarta EE: Modern Ecosystem
* Oracle Refused to give up javax.* so Eclipse created jakarta.*
* Java SE (The Language): Still managed by Oracle (via OpenJDK)
* Comes with a price tag so companies created their own: Temurin by Eclipse, Corretto by Amazon, Azul by Azul


* Jakarta EE (The Specs): Managed by the community
* Spring Boot: The dominant framework that glues them both together
  Note: Eclipse was created then open sourced by IBM (to eclipse the sun 😂)



### 14.2 Features Added in Versions

# Java Features

## 1. Streams (Java 8)

Functional framework for processing collections without modifying the underlying source.

* **Execution Overhead:** Slower than or equal to manual `for` loops due to abstraction layers, object allocations,
  boxing/unboxing, and JIT loop optimization limitations.
* **Parallel Streams:** Provides multi-core execution out of the box, often outperforming manual iteration for heavy
  workloads.

| Operation Type | Description | Key Methods |
| --- | --- | --- |
| **Intermediate** | Lazy evaluation; returns a new stream for chaining. | `map()`, `flatMap()`, `filter()`, `distinct()`, `sorted()`, `peek()` |
| **Terminal** | Triggers execution; produces a result or side-effect. | `collect()`, `reduce()`, `forEach()`, `count()`, `findFirst()` |

---

## 2. Records (Java 16)

Classes designed to model immutable data carriers without boilerplate. Autogenerates `private final` fields, canonical
constructor, getters (e.g., `id()`), `equals()`, `hashCode()`, and `toString()`.

```java
// Compact Canonical Constructor with Validation
public record Employee(int id, String name) {
    public Employee {
        if (id < 0) throw new IllegalArgumentException("Invalid ID");
    }
}

```

---

## 3. Sealed Classes (Java 17)

Restricts which classes or interfaces can extend or implement them.

* **Rules:** Permitted subclasses must directly extend the parent, reside in the same package (or module), and declare a
  modifier: `final` (prevents further inheritance), `sealed` (further restricts subclasses), or `non-sealed` (opens
  inheritance).
* **Syntax:**

```java
public sealed class Shape permits Circle, Triangle {
}

public final class Circle extends Shape {
}

public non-sealed class Triangle extends Shape {
}

```

---

## 4. Java Modules / Project Jigsaw (Java 9)

Replaces the flat classpath with a structured module path.

* **Key Benefits:**
* **Strong Encapsulation:** Explicitly exposes packages via `exports`; hides internal APIs.
* **Reliable Configuration:** Fails at startup if dependencies are missing or duplicated, preventing lazy runtime
  exceptions.
* **Descriptor Example (`module-info.java`):**

```java
module com.mycompany.service {
    requires java.sql;
    exports com.mycompany.service.api;
}

```

* **Compilation Command:**

```bash
javac -d mods/com.mycompany.service --module-source-path src $(find src -name "*.java")

```

---

## 5. Virtual Threads / Project Loom (Java 21)

Lightweight threads managed by the JVM rather than the OS. Allows applications to spawn millions of concurrent threads
with low memory footprint, scaling high-throughput I/O blocking operations efficiently without async callback code.

---

## 6. Scoped Values (Java 21 / Preview)

Enables safe, immutable data sharing both within a thread and across child threads (such as Virtual Threads) without the
memory leak risks, overhead, and mutability issues associated with `ThreadLocal`.

---

## 7. Pattern Matching for `switch` (Java 21)

Enhances `switch` statements and expressions to evaluate types directly, support pattern guards (`when`), and handle
`null` safely.

```java
String result = switch (obj) {
    case null -> "Null input";
    case Integer i -> "Integer: " + i;
    case String s when s.length() > 5 -> "Long string: " + s;
    case String s -> "Short string: " + s;
    default -> "Unknown type";
};

```

---

## 8. Sequenced Collections (Java 21)

Introduces uniform interfaces (`SequencedCollection`, `SequencedSet`, `SequencedMap`) for collections with a defined
encounter order, fixing inconsistent access methods across legacy collections.

* **Unified API:** `addFirst()`, `addLast()`, `getFirst()`, `getLast()`, `removeFirst()`, `removeLast()`, and
  `reversed()`.

---

## 9. Java Memory Barriers & Instruction Reordering

Compilers and CPUs reorder instructions to maximize execution speed for single-threaded contexts. In multi-threaded
contexts, unconstrained reordering leads to race conditions and stale reads.

* **Compiler Barriers:** Prevent the Java compiler/JIT from reordering code across specific instruction boundaries.
* **CPU Memory Barriers:** Instructions emitted to force hardware caches to flush/invalidate and preserve ordering.
* **LoadLoad / StoreStore:** Prevent reordering of reads/writes relative to each other.
* **LoadStore / StoreLoad:** Enforce strict execution boundaries (e.g., after volatile writes).
* **Java Enforcement:** Handled via memory barriers inserted when using `volatile` fields, synchronized blocks, explicit
  locks, or `java.lang.invoke.VarHandle` acquire/release fences.

```

```