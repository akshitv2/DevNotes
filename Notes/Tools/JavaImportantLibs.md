---
parent: Tools
nav_order: 2
layout: default
title: Java Libs
---

# Java Libraries — Interview Notes

## Core Collections & Data Structures (`java.util`)

- **ArrayList**: backed by resizable array. O(1) get/set, O(n) insert/remove in middle, amortized O(1) add at end. Not thread-safe.
- **LinkedList**: doubly-linked list. O(1) insert/remove at ends, O(n) get. Implements both `List` and `Deque`.
- **HashMap**: array of buckets + linked list/tree (treeified after 8 collisions per bucket, Java 8+). O(1) average get/put. Not thread-safe, allows one null key.
  - Know: initial capacity (16), load factor (0.75), resizing doubles capacity, hashCode/equals contract matters for correctness.
- **LinkedHashMap**: HashMap + insertion (or access) order. Useful for LRU cache implementations.
- **TreeMap**: Red-Black tree, sorted by key (natural order or Comparator). O(log n) operations. Implements `NavigableMap`.
- **HashSet / LinkedHashSet / TreeSet**: backed by corresponding Map implementations internally.
- **Arrays vs Collections utility classes**: `Arrays.asList()` returns fixed-size list backed by array; `Collections.unmodifiableList()` for immutability; `Collections.synchronizedList()` for basic thread safety.
- **Iterator vs ListIterator**: ListIterator supports bidirectional traversal and element replacement.
- **Fail-fast vs fail-safe iterators**: ArrayList/HashMap iterators throw `ConcurrentModificationException` if modified during iteration; `CopyOnWriteArrayList`/`ConcurrentHashMap` iterators are fail-safe (snapshot or weakly consistent).

**Common interview questions**: HashMap internal working, difference between HashMap/Hashtable/ConcurrentHashMap, how HashMap handles collisions, ArrayList vs LinkedList performance trade-offs, how to make a collection thread-safe.

---

## `java.util.concurrent`

- **ConcurrentHashMap**: segment/bucket-level locking (Java 8+ uses CAS + synchronized on bins). Better concurrent throughput than `Collections.synchronizedMap()`. Does not allow null keys/values.
- **CopyOnWriteArrayList**: copies underlying array on every write. Great for read-heavy, write-rare scenarios (e.g., listener lists). Iterators never throw `ConcurrentModificationException`.
- **BlockingQueue** (`ArrayBlockingQueue`, `LinkedBlockingQueue`): used in producer-consumer patterns; `put()`/`take()` block when full/empty.
- **CountDownLatch**: one-time gate — threads wait until counter hits zero. Cannot be reset.
- **CyclicBarrier**: reusable barrier where N threads wait for each other before proceeding.
- **Semaphore**: controls access to a resource pool via permits.
- **ExecutorService / ThreadPoolExecutor**: manage thread pools. Know the difference between `newFixedThreadPool`, `newCachedThreadPool`, `newSingleThreadExecutor`, `newScheduledThreadPool`.
- **Future / CompletableFuture**: async result handling; `CompletableFuture` supports chaining (`thenApply`, `thenCompose`, `thenCombine`) and exception handling (`exceptionally`, `handle`).
- **Locks (`ReentrantLock`, `ReadWriteLock`)**: more flexible than `synchronized` — supports tryLock, fairness policy, interruptible locking.
- **AtomicInteger / AtomicLong / AtomicReference**: lock-free thread-safe operations using CAS (compare-and-swap).

**Common interview questions**: How does ConcurrentHashMap achieve thread safety without locking the whole map? Explain CompletableFuture chaining. Difference between `synchronized` and `ReentrantLock`. When to use CopyOnWriteArrayList.

---

## Guava (Google Core Libraries)

- **Immutable collections**: `ImmutableList`, `ImmutableMap`, `ImmutableSet` — thread-safe by design, prevent accidental mutation.
- **Multimap / Multiset / BiMap**: collections not available in standard `java.util` (one key → multiple values, count occurrences, bidirectional lookup).
- **Caching**: `CacheBuilder`/`LoadingCache` — in-memory cache with eviction policies (size-based, time-based).
- **Preconditions**: `checkNotNull()`, `checkArgument()` for defensive programming/fail-fast validation.
- **Functional utilities**: `Functions`, `Predicates` (largely superseded by Java 8 Streams but still asked about in legacy codebases).

**Common interview questions**: Why use Guava's ImmutableList over Collections.unmodifiableList()? What problem does LoadingCache solve?

---

## HTTP & Networking

### `java.net`
- **HttpURLConnection**: low-level, verbose API for HTTP calls. Mostly replaced by `java.net.http.HttpClient` (Java 11+) which supports async and HTTP/2.

### OkHttp
- Connection pooling, transparent GZIP, response caching built in.
- **Interceptors**: application interceptors (business logic, retries, logging) vs network interceptors (see actual request/response over the wire, can handle redirects/caching).
- Supports synchronous (`execute()`) and asynchronous (`enqueue()`) calls.

### Apache HttpClient
- Older, very configurable (connection managers, retry handlers, connection pooling).
- Common in legacy enterprise Spring apps before `RestTemplate`/`WebClient` became standard.

### Retrofit
- Turns REST API into a Java interface using annotations (`@GET`, `@POST`, `@Path`, `@Body`).
- Built on top of OkHttp; supports converters (Gson, Jackson, Moshi) for automatic (de)serialization.
- Returns `Call<T>` (sync/async) or reactive types (`Observable`, `CompletableFuture`) with adapters.

**Common interview questions**: Difference between OkHttp interceptor types. Why prefer Retrofit over manual HttpClient calls? How does connection pooling improve performance?

---

## JSON & XML Processing

### Jackson (most asked about)
- **ObjectMapper** is the core class: `readValue()` (deserialize), `writeValueAsString()` (serialize).
- Annotations: `@JsonProperty`, `@JsonIgnore`, `@JsonInclude`, `@JsonCreator`, `@JsonFormat`.
- Handles polymorphic types via `@JsonTypeInfo`/`@JsonSubTypes`.
- Streaming API (`JsonParser`/`JsonGenerator`) for large payloads — memory efficient vs tree/data-binding APIs.
- Modules: `jackson-datatype-jsr310` for Java 8 date/time support.

### Gson
- Simpler API than Jackson, no annotations required for basic use.
- `Gson().toJson()` / `fromJson()`.
- Historically more lenient with malformed JSON; less performant than Jackson for large-scale use.

### JAXB
- Annotation-based XML binding (`@XmlRootElement`, `@XmlElement`).
- `Marshaller`/`Unmarshaller` convert between Java objects and XML.
- Removed from JDK in Java 11+ (now a separate dependency).

### DOM vs SAX parsers
- **DOM**: loads entire XML into memory tree — easy to navigate/modify, but memory-heavy.
- **SAX**: event-driven, streaming, low memory — but read-only, forward-only.

**Common interview questions**: Jackson vs Gson trade-offs. How does Jackson handle unknown JSON fields (`@JsonIgnoreProperties(ignoreUnknown = true)`)? DOM vs SAX use cases.

---

## Logging

### SLF4J
- **Facade/abstraction**, not an implementation — decouples application code from a specific logging framework.
- Use parameterized logging: `log.info("User {} logged in", userId)` — avoids string concatenation cost when log level is disabled.

### Logback
- Native SLF4J implementation; successor to Log4j 1.x. Supports XML-based configuration, appenders (console, file, rolling file), and filters.

### Log4j 2
- Asynchronous logging via LMAX Disruptor for high throughput.
- Note: Log4j 1.x and early Log4j 2.x had major CVEs (Log4Shell, CVE-2021-44228) — good to know for security-related discussions.

**Common interview questions**: Why use SLF4J instead of directly using Logback/Log4j? What's the performance benefit of parameterized logging? What was Log4Shell and why did it happen?

---

## Testing

### JUnit 4 / 5
- JUnit 5 = JUnit Platform + Jupiter (new API) + Vintage (backward compatibility).
- Key annotations: `@Test`, `@BeforeEach`/`@BeforeAll`, `@AfterEach`/`@AfterAll`, `@ParameterizedTest`, `@Disabled`.
- Assertions: `assertEquals`, `assertThrows`, `assertAll` (grouped assertions).

### Mockito
- `mock()` creates a fake object; `when(...).thenReturn(...)` stubs behavior; `verify()` checks interactions.
- `@Mock`, `@InjectMocks`, `@Spy` annotations (with `MockitoExtension` in JUnit 5).
- Difference between a **mock** (fully fake) and a **spy** (real object, selectively stubbed).
- `ArgumentCaptor` to capture and assert on arguments passed to mocked methods.

### TestNG
- Alternative to JUnit; supports more flexible test configuration (`@BeforeSuite`, dependency between tests, parallel execution natively).

### AssertJ
- Fluent, chainable assertions: `assertThat(list).hasSize(3).contains("a")`. More readable than plain JUnit assertions.

**Common interview questions**: Mock vs Stub vs Spy. How do you test a method with a private dependency? What's the difference between `@Mock` and `@InjectMocks`? Why use ArgumentCaptor?

---


## Database & ORM

### JDBC
- Core API: `DriverManager`, `Connection`, `Statement`/`PreparedStatement`, `ResultSet`.
- Always use `PreparedStatement` over `Statement` — prevents SQL injection, allows query plan caching.
- Connection pooling is not built in — handled by pools like HikariCP (fastest, default in Spring Boot), Apache DBCP.
- `try-with-resources` for auto-closing Connection/Statement/ResultSet.

### Hibernate
- ORM implementing JPA. Maps Java objects to DB tables via annotations (`@Entity`, `@Table`, `@Id`, `@Column`) or XML.
- **Session** = unit of work, first-level cache (per-session, always on).
- **Second-level cache**: optional, shared across sessions (e.g., Ehcache).
- **Lazy vs Eager loading**: lazy loads associations on-demand (can cause `LazyInitializationException` outside session); eager loads immediately (risk of N+1 or over-fetching).
- **N+1 select problem**: classic interview trap — fetching a list then triggering one extra query per item for an association. Fixed via `JOIN FETCH`, `@BatchSize`, or entity graphs.
- **Cascade types**: PERSIST, MERGE, REMOVE, etc. — control how operations propagate to related entities.

### JPA (Java Persistence API)
- Specification; Hibernate is the most common implementation.
- `EntityManager` is the JPA equivalent of Hibernate's `Session`.
- JPQL — object-oriented query language, DB-agnostic (vs native SQL).

### MyBatis
- SQL-mapping framework, not full ORM — you write your own SQL, MyBatis maps results to objects. Preferred when fine-grained SQL control matters more than abstraction.

### Spring Data (JPA)
- Repository abstraction: `JpaRepository`, `CrudRepository` — generates implementations at runtime.
- Derived query methods from method names, e.g., `findByLastNameAndAgeGreaterThan(...)`.
- `@Query` for custom JPQL/native SQL.

**Common interview questions**: Explain the N+1 problem and how to fix it. Difference between `save()` and `saveAndFlush()`. Lazy vs eager fetching trade-offs. First-level vs second-level cache. JDBC vs JPA vs Hibernate vs Spring Data — how do they relate?

---

## Dependency Injection & Configuration

### Spring Framework (Core / IoC)
- **IoC container** manages object lifecycle and wiring — you declare dependencies, Spring injects them.
- **Bean scopes**: singleton (default), prototype, request, session.
- **Injection types**: constructor injection (preferred — enables immutability & easier testing), setter injection, field injection (`@Autowired` directly on field — discouraged for testability).
- **`@Component`, `@Service`, `@Repository`, `@Controller`**: stereotype annotations — functionally similar, but semantically distinct and enable component-specific behavior (e.g., `@Repository` translates persistence exceptions).
- **`ApplicationContext` vs `BeanFactory`**: ApplicationContext is the more feature-rich container (event handling, AOP, i18n); BeanFactory is the basic, lazy-loading container.
- **`@Configuration` + `@Bean`**: Java-based configuration, alternative to XML.
- **AOP (Aspect-Oriented Programming)**: cross-cutting concerns like logging/transactions via `@Aspect`, `@Before`, `@After`, `@Around`.
- **Circular dependency handling**: Spring can resolve via setter injection but throws an error with pure constructor injection cycles.

### Guice
- Lightweight DI framework by Google. Uses `@Inject` annotation and `Module`/`Binder` for wiring — less "magic"/convention-based than Spring, more explicit.

**Common interview questions**: Constructor vs field injection — why is constructor preferred? What is a Spring bean lifecycle (instantiate → populate properties → `@PostConstruct` → ready → `@PreDestroy`)? Explain AOP with a real example (e.g., `@Transactional`).

---

## Web Frameworks

### Spring Boot
- Auto-configuration based on classpath contents (`@EnableAutoConfiguration`, `@SpringBootApplication`).
- Embedded servers (Tomcat/Jetty/Undertow) — no need for external app server deployment.
- `application.properties`/`application.yml` for externalized config; profiles (`@Profile`, `spring.profiles.active`) for environment-specific beans.
- Starters (`spring-boot-starter-web`, `-data-jpa`, etc.) bundle common dependencies.
- Actuator: production-ready endpoints (`/health`, `/metrics`, `/info`) for monitoring.

### Spring MVC
- `DispatcherServlet` is the front controller — routes requests to `@Controller`/`@RestController` methods.
- `@RequestMapping`/`@GetMapping`/`@PostMapping`, `@PathVariable`, `@RequestParam`, `@RequestBody`/`@ResponseBody`.
- Exception handling via `@ExceptionHandler`/`@ControllerAdvice` (global exception handling).
- `RestTemplate` (older, synchronous) vs `WebClient` (newer, reactive, non-blocking, part of Spring WebFlux) for making outbound HTTP calls.

### Jakarta EE (formerly Java EE) basics
- **Servlets**: `HttpServlet`, lifecycle (`init`, `service`, `destroy`), `doGet`/`doPost`.
- **JSP**: mostly legacy now, replaced by templating engines (Thymeleaf) or frontend frameworks + REST APIs.

**Common interview questions**: What happens when a request hits a Spring Boot app (DispatcherServlet flow)? RestTemplate vs WebClient. How does Spring Boot auto-configuration decide what beans to create? What does `@ControllerAdvice` do?

---

## Concurrency & Async (deeper dive)

- **CompletableFuture** chaining: `thenApply` (sync transform), `thenApplyAsync` (runs on `ForkJoinPool.commonPool()` or supplied executor), `thenCompose` (flattens nested futures — use when the transform itself returns a future), `thenCombine` (combine two independent futures), `exceptionally`/`handle` (error handling).
- **RxJava**: `Observable`/`Flowable`, operators (`map`, `flatMap`, `filter`, `debounce`), `Scheduler`s control which thread work runs on (`Schedulers.io()`, `Schedulers.computation()`). `Flowable` supports backpressure; `Observable` does not.
- **Project Reactor** (used by Spring WebFlux): `Mono` (0 or 1 result) and `Flux` (0 to N results) — the reactive types underlying Spring's non-blocking stack.
- **Backpressure**: mechanism for a slow consumer to signal a fast producer to slow down — key differentiator between reactive streams and plain async callbacks.

**Common interview questions**: Difference between `thenApply` and `thenApplyAsync`. What is backpressure and why does it matter? Mono vs Flux. When would you choose WebFlux (reactive) over traditional Spring MVC (blocking)?

---

## Functional Programming (Java 8+)

- **Functional interfaces** (`java.util.function`): `Function<T,R>`, `Consumer<T>`, `Supplier<T>`, `Predicate<T>`, `BiFunction<T,U,R>` — each has exactly one abstract method, enabling lambda assignment.
- **Streams API**: `stream()`, intermediate ops (`map`, `filter`, `sorted`, `distinct` — lazy, not executed until a terminal op is called), terminal ops (`collect`, `reduce`, `forEach`, `count`).
- **Collectors**: `toList()`, `toMap()`, `groupingBy()`, `partitioningBy()`, `joining()`.
- **Parallel streams**: `.parallelStream()` uses the common `ForkJoinPool` — good for CPU-bound, large, independent-element workloads; risky for I/O-bound or order-sensitive work.
- **Optional**: avoids null checks — `Optional.ofNullable()`, `.map()`, `.orElse()`, `.orElseThrow()`. Convention: use only as a method return type, not as a field type or method parameter.
- **Method references**: `ClassName::staticMethod`, `object::instanceMethod`, `ClassName::new` (constructor reference).

**Common interview questions**: How does `reduce()` work? Difference between `map` and `flatMap`. Why are streams lazy? When should you avoid parallel streams? Why shouldn't Optional be used as a field?

---

## Performance & Monitoring

- **Micrometer**: vendor-neutral metrics facade (same idea as SLF4J, but for metrics) — instrument code once, export to Prometheus, Datadog, New Relic, etc. Built into Spring Boot Actuator by default.
- **Prometheus**: pull-based time-series monitoring system; scrapes `/actuator/prometheus`; paired with Grafana for dashboards; queried with PromQL.
- **JMH (Java Microbenchmark Harness)**: the correct way to benchmark Java code — handles JIT warm-up, dead-code elimination, and other pitfalls that make naive `System.currentTimeMillis()` timing misleading.

**Common interview questions**: Why can't you just time code with `System.currentTimeMillis()` to benchmark it? Push-based vs pull-based metrics collection.

---

## Build & Dependency Management

### Maven
- **POM (`pom.xml`)**: declarative project config — dependencies, plugins, build lifecycle.
- **Lifecycle phases**: `validate` → `compile` → `test` → `package` → `verify` → `install` → `deploy`.
- **Scopes**: `compile` (default, everywhere), `provided` (compile-time only, e.g. servlet-api, not packaged), `runtime`, `test`.
- **Transitive dependencies**: resolved automatically; conflicts resolved by "nearest wins" (closest to root in the dependency tree) unless explicitly overridden with `<dependencyManagement>`.

### Gradle
- Groovy/Kotlin DSL instead of XML — more concise and programmable than Maven.
- **Incremental builds & build caching**: only rebuilds what changed — generally faster than Maven on large projects.
- Tasks are the fundamental unit of work (vs Maven's fixed lifecycle phases) — more flexible/customizable.

**Common interview questions**: Maven vs Gradle trade-offs. How does Maven resolve version conflicts in transitive dependencies? What are Maven scopes and when do you use `provided`?

---

## Utilities

### Apache Commons Lang
- `StringUtils` (null-safe string ops: `isBlank`, `isEmpty`, `trimToNull`), `ObjectUtils`, `ArrayUtils`, `RandomStringUtils`.
- Useful because core Java `String` methods often throw `NullPointerException` on null input; Commons Lang equivalents handle nulls gracefully.

### Apache Commons Collections
- Extra collection types/utilities not in `java.util` (e.g., `Bag`, `BidiMap`) — largely superseded by Guava and Java 8 Streams in modern codebases, but still seen in legacy systems.

### Lombok
- Compile-time annotation processor that generates boilerplate: `@Getter`, `@Setter`, `@ToString`, `@EqualsAndHashCode`, `@Builder`, `@NoArgsConstructor`/`@AllArgsConstructor`, `@Data` (bundles getter/setter/toString/equals/hashCode), `@Slf4j` (injects a logger field).
- Trade-off often discussed in interviews: faster to write, but can obscure what code is actually generated, and requires IDE plugin/annotation-processing support.

**Common interview questions**: What does `@Data` actually generate? Why might a team choose *not* to use Lombok? Apache Commons vs Guava — when would you reach for one over the other?

---

## Quick Reference: What to Prioritize by Role

- **Backend/Spring roles**: Spring Core, Spring Boot, Spring Data JPA, Hibernate (N+1, caching, fetch types), concurrency basics.
- **General Java roles**: Collections internals, Streams/functional interfaces, concurrency utilities, JUnit/Mockito.
- **Microservices/distributed roles**: HTTP clients, resilience patterns (consider also looking up Resilience4j — not covered above), reactive stacks (WebFlux/Reactor), monitoring (Micrometer/Prometheus).
- **Senior/staff roles**: be ready to discuss trade-offs and internals (HashMap resizing, JVM memory model basics, GC awareness) rather than just API usage.
