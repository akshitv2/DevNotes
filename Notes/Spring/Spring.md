# Spring Framework Interview Notes

A complete reference covering Core Spring, Spring Boot, Spring MVC, Spring Data, AOP, Security, Transactions, Testing,
Microservices, and WebFlux — organized for interview prep.

---

## 1. Core Concepts: IoC & DI

* **Inversion of Control (IoC):** Instead of application code dictating the execution flow and instantiating
  dependencies directly, control is inverted and managed by the Spring IoC container.


* **Dependency Injection (DI):** The mechanism IoC uses to inject required objects into a class, adhering to the
  Dependency Inversion principle.


* **Why it matters:** Provides loose coupling, enables easy unit testing with mock objects, centralizes application
  configuration, and simplifies implementation swapping.

**Enterprise Java Before IoC:**

* **Tight Coupling:** User code was heavily polluted with framework-specific factory and lookup logic.


* **Lookup Problem:** Objects manually located dependencies using pattern lookups like Service Locators.


* **Testing Friction:** Tight dependencies made isolating components for unit testing difficult.


* **Modern IoC Impact:** Injects dependencies seamlessly, removes server-creation boilerplate, and enables isolated bean
  testing.

**Types of Dependency Injection**

| Type                  | How                                 | Notes                                                                                                           |
|-----------------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Constructor injection | Dependencies passed via constructor | **Recommended.** Enables field immutability (`final`), explicit dependencies, and fail-fast container startups. |
| Setter injection      | Dependencies set via setter methods | Preferred for optional dependencies or post-instantiation configuration.                                        |
| Field injection       | `@Autowired` directly on fields     | Simple for prototyping, but hides dependencies, complicates testing, and is discouraged for production.         |

**The Spring IoC Container**

* **BeanFactory:** Bare-metal IoC container providing basic dependency injection, bean lifecycle management, and XML
  `BeanDefinition` parsing (`ClassPathResource`, `XmlBeanFactory`).


* **ApplicationContext:** Advanced superset of `BeanFactory` adding eager singleton instantiation, event publication,
  i18n, property loading, and direct AOP integration.


* **Implementations:** `ClassPathXmlApplicationContext`, `AnnotationConfigApplicationContext`, and
  `WebApplicationContext`.

---

## 2. Beans & Bean Lifecycle

A **bean** is an object instantiated, assembled, and managed by the Spring IoC container.

**Ways to declare a bean:**

* Stereotype annotations: `@Component` (generic), `@Service` (business logic), `@Repository` (persistence with exception
  translation), `@Controller` / `@RestController` (web).


* Java configuration: Explicit `@Bean` methods within `@Configuration` classes.

**Bean Scopes**

| Scope                 | Description                                                                                                            |
|-----------------------|------------------------------------------------------------------------------------------------------------------------|
| `singleton` (default) | Single instance per Spring IoC container. Ideal for stateless components like Controllers, Services, and Repositories. |
| `prototype`           | New instance created on every container request. Ideal for stateful objects needing independent instances.             |
| `request`             | One instance per HTTP request lifecycle (web-aware context).                                                           |
| `session`             | One instance per HTTP session lifecycle (web-aware context).                                                           |
| `application`         | One instance per ServletContext lifecycle (web-aware context).                                                         |

* **Web-Aware Context Requirement:** Request, Session, and Application scopes require a web-aware `ApplicationContext`
  integrated with a Servlet Container handling `HttpServletRequest` objects. Standard desktop/CLI containers do not
  support them.


* **Prototype-in-Singleton Injection:** Injecting a prototype bean into a singleton bean resolves the prototype
  dependency only once during singleton initialization. Fix using `ObjectProvider`, scoped proxies (
  `proxyMode = ScopedProxyMode.TARGET_CLASS`), or `@Lookup` method injection.

**Bean Lifecycle Sequence**

1. **Container Init & Instantiation:** Container initializes and instantiates the bean via constructor.


2. **Dependency Injection (Population):** Injects properties and dependencies via setters or field autowiring.


3. **Aware Interfaces Execution:**

* `BeanNameAware`: Supplies the bean's explicit ID/name (useful for dynamic runtime references where `@Qualifier` is
  insufficient).


* `BeanFactoryAware`: Provides access to the owning `BeanFactory`.


* `ApplicationContextAware`: Provides access to the `ApplicationContext`.


* `EnvironmentAware`: Passes environment properties prior to standard `@Autowired`/`@Value` post-processing.


* `ResourceLoaderAware`: Supplies the Spring `ResourceLoader`.


4. **Initialization Phase:**

* `BeanPostProcessor.postProcessBeforeInitialization()` executes across registered processors.


* Custom init methods run: `@PostConstruct`, `InitializingBean.afterPropertiesSet()`, or `@Bean(initMethod)`.


* `BeanPostProcessor.postProcessAfterInitialization()` executes (where Spring wraps target beans in proxies for features
  like `@Transactional` and `@Async`).


5. **Bean Ready:** Bean is fully configured and ready for application use.


6. **Destruction Phase:** On container shutdown, `@PreDestroy`, `DisposableBean.destroy()`, or custom `destroyMethod`
   hooks execute.

**Container Post-Processors:**

* **`BeanFactoryPostProcessor`:** Modifies bean definitions and metadata before any beans are instantiated (e.g.,
  `PropertySourcesPlaceholderConfigurer`).


* **`BeanPostProcessor`:** Intercepts instantiated bean instances before/after initialization (e.g.,
  `AutowiredAnnotationBeanPostProcessor` handling `@Autowired` and `@Value`).

**Circular Dependencies:**

* Resolved automatically for singleton beans using setter or field injection through Spring's three-level cache. (With
  setter/field injection, Spring can create the object first, expose a reference to it, and complete dependency
  injection later. So two singleton beans can temporarily hold references to each other before their initialization is
  fully complete.)
* Fails for constructor injection (`BeanCurrentlyInCreationException`). Fix via `@Lazy`, component redesign, or setter
  injection.

---

## 3. Key Annotations Cheat Sheet

| Annotation                       | Purpose                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------|
| `@Autowired`                     | Injects a dependency by type (falls back to bean name if multiple candidates exist). |
| `@Qualifier("beanName")`         | Disambiguates between multiple candidate beans of the same type.                     |
| `@Primary`                       | Designates a bean as the primary candidate when multiple beans match.                |
| `@Value("${property}")`          | Injects values from external properties, environment variables, or SpEL expressions. |
| `@Configuration`                 | Marks a class as a source of Spring bean definitions.                                |
| `@ComponentScan`                 | Configures package scanning paths for stereotype components.                         |
| `@Bean`                          | Declares an explicit bean returned by a method inside a `@Configuration` class.      |
| `@Scope`                         | Defines the scope of a bean (`singleton`, `prototype`, etc.).                        |
| `@Lazy`                          | Delays bean initialization until its first explicit invocation.                      |
| `@Profile("dev")`                | Conditionally registers beans based on active environment profiles.                  |
| `@PostConstruct` / `@PreDestroy` | Lifecycle hooks for post-initialization and pre-destruction callbacks.               |
| `@Conditional`                   | Conditionally registers beans based on programmatic matching logic.                  |

---

## 4. Spring vs Spring Boot

| Feature           | Spring Framework                                                      | Spring Boot                                                                  |
|-------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Primary Goal**  | Comprehensive model for Java enterprise applications (DI, AOP, Data). | Minimizes configuration overhead to fast-track production-ready Spring apps. |
| **Configuration** | Manual configuration required (XML or Java `@Configuration`).         | Opinionated auto-configuration based on classpath dependencies.              |
| **Server**        | Requires external web/app servers (Tomcat, GlassFish, WildFly).       | Embedded web servers (Tomcat, Jetty, Undertow) packaged in runnable JARs.    |
| **Boilerplate**   | High setup overhead for project creation and dependency management.   | Minimal setup via `spring-boot-starter-*` curated dependency BOMs.           |
| **Approach**      | Un-opinionated (developer configures every component manually).       | Opinionated (provides sensible pre-configured defaults).                     |

**Auto-Configuration:** Defined via `@SpringBootApplication` (combines `@Configuration`, `@EnableAutoConfiguration`, and
`@ComponentScan`). Auto-configuration classes evaluate `@Conditional` annotations (`@ConditionalOnClass`,
`@ConditionalOnMissingBean`, `@ConditionalOnProperty`) to auto-configure components based on classpath presence.

**Monolith to Spring Boot Migration Challenges:**

* **Servlet Container Coupling:** Refactoring `web.xml` filters, listeners, and `DispatcherServlet` setups into Java
  Boot configurations.


* **XML Dependency Trees:** Refactoring complex XML dependency injections and hidden circular dependencies.


* **Dependency Baselines:** Upgrading legacy dependencies to modern Java (Java 17+) and Jakarta EE baselines.


* **Session Management:** Shifting from JVM in-memory sticky web sessions to stateless architectures or external
  stores (e.g., Redis).


* **Application Server Services:** Replacing server-managed JNDI, JTA, and managed datasources with standalone
  configurations.

---

## 5. Spring MVC & HTTP Clients

**Request Flow:**

1. Client HTTP request hits **`DispatcherServlet`** (Front Controller).


2. `DispatcherServlet` queries **`HandlerMapping`** to locate the target controller method.


3. Controller method executes business logic and returns a model + view name or direct response payload.


4. **`ViewResolver`** resolves view names to template views (e.g., Thymeleaf).


5. Rendered view or serialized body payload is returned to the client.

**Key Web Annotations:** `@Controller`, `@RestController`, `@RequestMapping`, `@GetMapping`, `@PostMapping`,
`@PutMapping`, `@DeleteMapping`, `@PatchMapping`, `@PathVariable`, `@RequestParam`, `@RequestBody`, `@ResponseBody`,
`@ExceptionHandler`, `@RestControllerAdvice`.

**Filters vs Interceptors vs WebFilters**

| Feature       | Filter                                                    | HandlerInterceptor                                          | WebFilter                                   |
|---------------|-----------------------------------------------------------|-------------------------------------------------------------|---------------------------------------------|
| **Layer**     | Web Container / Servlet level.                            | Spring MVC / DispatcherServlet.                             | Spring WebFlux / Reactive stack.            |
| **Execution** | Processes request before reaching Spring's servlet.       | Intercepts execution before/after Controllers.              | Asynchronous, non-blocking pipeline.        |
| **Awareness** | Agnostic of Spring Controller mappings.                   | Aware of target Controller and handler method.              | Built on Project Reactor (`Mono<Void>`).    |
| **Use Cases** | IP blocking, CORS, raw request logging, data compression. | App business logic, `ModelAndView` edits, endpoint metrics. | Asynchronous request/response interception. |

* **HandlerInterceptor Hooks:** `preHandle()` (can halt execution), `postHandle()` (modifies `ModelAndView`), and
  `afterCompletion()` (resource cleanup/monitoring).


* **Outbound HTTP Interceptors:** `ClientHttpRequestInterceptor` (blocking `RestTemplate`) and
  `ExchangeFilterFunction` (reactive `WebClient`). Note: Serialized JSON request bodies cannot be mutated in place; a
  replacement request or data buffer must be constructed.

**HTTP Client Comparison**

* **RestTemplate:** Legacy, blocking, synchronous HTTP client (in maintenance mode).


* **RestClient (Spring 6+):** Modern, synchronous client offering a fluent, method-chaining API (`.get()`, `.uri()`,
  `.retrieve()`) while reusing HTTP message converters from `RestTemplate`.


* **WebClient:** Non-blocking, reactive client supporting synchronous and asynchronous streaming (`Mono`/`Flux`).

---

## 6. AOP (Aspect-Oriented Programming)

**Purpose:** Modularizes cross-cutting concerns (logging, security, transactions, caching) out of core business logic
into central aspects. **Note:** Avoid placing core business logic in aspects, as implicit hooks complicate code
execution tracking.

**Key Terminology:**

* **Aspect:** Class encapsulating a cross-cutting concern.


* **Join Point:** Execution point (e.g., method execution) where an aspect can intervene.


* **Advice:** Action taken at a join point (`@Before`, `@After`, `@Around`, `@AfterReturning`, `@AfterThrowing`).


* **Pointcut:** Expression matching targeted join points (e.g., `execution(* com.app.service.*.*(..))`).


* **Weaving:** Process linking aspects with target objects to generate proxy instances.

**Proxy Mechanisms:**

* **JDK Dynamic Proxies:** Used when the target object implements an interface.


* **CGLIB Proxies:** Used via subclassing when no interfaces exist.


* **Self-Invocation Limitation:** Direct internal method calls (`this.method()`) bypass proxy objects, preventing AOP
  advice, `@Transactional`, and `@Cacheable` execution.

---

## 7. Transactions

`@Transactional` provides declarative transaction management using proxy-based interceptors.

**Propagation Types:** `REQUIRED` (default), `REQUIRES_NEW`, `SUPPORTS`, `NOT_SUPPORTED`, `MANDATORY`, `NEVER`,
`NESTED`.

**Isolation Levels:** `READ_UNCOMMITTED`, `READ_COMMITTED`, `REPEATABLE_READ`, `SERIALIZABLE`.

**Common Transaction Gotchas:**

* Rollbacks trigger **only on unchecked exceptions** (`RuntimeException`, `Error`) by default unless explicit via
  `rollbackFor = Exception.class`.


* `@Transactional` on private methods is ignored by Spring proxy interceptors.


* Internal self-invocation within the same class bypasses proxy wrappers.

---

## 8. Spring Data JPA

* **Repository Hierarchy:** `JpaRepository<T, ID>` extends `PagingAndSortingRepository` extends `CrudRepository`.


* **Queries:** Supports derived query method names (`findByLastNameAndAgeGreaterThan`), JPQL (`@Query`), and native SQL.
  `@Modifying` is required for UPDATE/DELETE operations.


* **Fetch Defaults:** `@OneToMany` and `@ManyToMany` default to `FetchType.LAZY`; `@OneToOne` and `@ManyToOne` default
  to `FetchType.EAGER`.


* **N+1 Query Problem:** Triggering separate queries for each child collection across N parent records. Fixed using
  `JOIN FETCH` JPQL, `@EntityGraph`, or `@BatchSize`.

---

## 9. Spring Security (fundamentals)

* **SecurityFilterChain:** Chain of servlet filters handling authentication, authorization, CSRF, and CORS prior to
  `DispatcherServlet`.


* **Authentication vs Authorization:** Authentication verifies user identity; Authorization verifies access permissions.


* **Components:** `UserDetailsService` fetches user data; `PasswordEncoder` (e.g., `BCryptPasswordEncoder`) handles
  password hashing.


* **Method Security:** Enabled using `@PreAuthorize`, `@PostAuthorize`, and `@Secured`.


* **Stateless JWT:** Custom security filters validate incoming tokens per request and populate the `SecurityContext`
  without server-side sessions.

---

## 10. Testing in Spring

| Annotation               | Purpose                                                               |
|--------------------------|-----------------------------------------------------------------------|
| `@SpringBootTest`        | Integration test annotation; loads full `ApplicationContext`.         |
| `@WebMvcTest`            | Web layer unit testing; loads controllers while mocking dependencies. |
| `@DataJpaTest`           | Persistence layer testing; configures JPA and in-memory databases.    |
| `@MockBean`              | Replaces an existing Spring context bean with a Mockito mock.         |
| `@Mock` / `@InjectMocks` | Plain Mockito testing without booting a Spring context.               |

---

## 11. Microservices / Spring Cloud

* **Discovery & Gateway:** Service registration via Eureka/Consul; entry routing and rate limiting via Spring Cloud
  Gateway.


* **Config & Resilience:** Centralized properties via Spring Cloud Config; circuit breakers via Resilience4j.


* **Communication & Tracing:** Inter-service calls via `WebClient` or `OpenFeign`; distributed tracing via Micrometer
  Tracing + Zipkin/Jaeger.

---

## 12. Spring Boot Actuator

Provides production-ready monitoring endpoints (`/actuator/health`, `/actuator/metrics`, `/actuator/info`) integrating
with Micrometer for Prometheus/Grafana. Explicitly expose required endpoints using
`management.endpoints.web.exposure.include`.

---

## 13. Frequently Asked Conceptual Questions (rapid-fire prep)

* **Stereotype Distinctions:** `@Component` is a general component; `@Service` designates service layer beans;
  `@Repository` converts DB exceptions into Spring's `DataAccessException` hierarchy; `@Controller` handles web routes.


* **Proxy Beans:** Dynamic wrappers generated by Spring to inject cross-cutting logic (AOP, security, transactions)
  around target beans.


* **Why Constructor Injection?:** Ensures immutability, prevents `NullPointerException` at construction, supports
  container-free unit tests, and avoids circular dependency masking.


* **`@RequestParam` vs `@PathVariable`:** `@RequestParam` extracts URL query parameters (`?id=1`); `@PathVariable`
  extracts values from URI path templates (`/users/{id}`).


* **`@Mock` vs `@MockBean`:** `@Mock` creates standard Mockito mocks; `@MockBean` replaces a bean inside the active
  Spring `ApplicationContext`.

---

## 14. Spring WebFlux / Reactive Programming

**Why Reactive?:** Traditional Spring MVC uses blocking, thread-per-request I/O. WebFlux uses a non-blocking, event-loop
model (Project Reactor + Netty) allowing a few threads to process thousands of concurrent connections.

**Core Reactive Types:**

* `Mono<T>`: Emits 0 or 1 asynchronous result.


* `Flux<T>`: Emits 0 to N asynchronous stream elements.


* **Lazy Execution:** Reactive operators do not execute until `.subscribe()` is invoked.

**Key Concepts & Trade-offs:**

* **Backpressure:** Subscribers signal demand (`request(n)`) to prevent producer flooding.


* **Stream Error Scenarios:** If an initial response header returns HTTP 200, the status code cannot be modified
  mid-stream on error; an error payload must be emitted.


* **WebFlux vs MVC:** Choose WebFlux for high-concurrency non-blocking I/O microservices and API gateways; choose MVC
  for standard relational CRUD applications. WebFlux increases architectural complexity in exchange for thread
  scalability.

---

## 15. Spring Batch

Framework for batch ETL processing of bulk data.

* **Job & Step:** A `Job` consists of sequential or parallel `Step` execution phases.


* **Chunk Architecture:** Steps execute using `ItemReader`, `ItemProcessor`, and `ItemWriter` on configurable chunk
  sizes.


* **JobRepository:** Persists execution metadata, enabling failed jobs to restart from the last successful chunk commit.

---

## 16. Caching Abstraction

Enable using `@EnableCaching`.

* `@Cacheable`: Checks cache first; skips method execution on cache hit.


* `@CachePut`: Always executes method and updates cache with result.


* `@CacheEvict`: Removes cached entries (`allEntries = true` clears namespace).


* **Gotchas:** Self-invocation bypasses caching proxies. Explicitly define SpEL keys (`key = "#id"`) to prevent key
  generation collisions.

---

## 17. Externalized Configuration & Precedence

**Precedence Order (Highest to Lowest):**

1. Command-line arguments (`--server.port=8081`).


2. `SPRING_APPLICATION_JSON` environment variables.


3. System properties (`-Dserver.port=8081`).


4. OS environment variables.


5. External profile properties (`application-{profile}.yml` outside JAR).


6. Internal profile properties packaged inside JAR.


7. Application properties packaged inside JAR (`application.yml`).

**`@ConfigurationProperties` vs `@Value`:** `@ConfigurationProperties` supports type-safe POJO binding, relaxed property
name binding (`my-prop`, `MY_PROP`), and nested validation, whereas `@Value` is best suited for simple standalone
property injection.

---

## 18. CORS Configuration

* **Configuration Options:** `@CrossOrigin` on individual endpoints or global `WebMvcConfigurer.addCorsMappings()`.


* **Security Integration:** Spring Security requires `.cors()` and a `CorsConfigurationSource` bean because Security
  filter chains run prior to MVC processing.


* **Browser Security:** CORS is enforced by browsers and does not restrict non-browser HTTP clients (cURL, Postman).

---

## 19. Messaging: Kafka & RabbitMQ with Spring

| Feature       | Spring Kafka                                               | Spring AMQP (RabbitMQ)                                |
|---------------|------------------------------------------------------------|-------------------------------------------------------|
| **Model**     | Distributed log stream with partition consumer offsets.    | AMQP broker routing messages via exchanges to queues. |
| **Ordering**  | Guaranteed per topic partition.                            | Guaranteed per single queue.                          |
| **Retention** | Retained post-consumption based on log retention policies. | Removed immediately after consumer acknowledgment.    |
| **Use Case**  | Event streaming, log aggregation, event sourcing.          | Complex message routing (fanout, topic), task queues. |

---

## 20. Actuator: Custom Health Indicators

Implement `HealthIndicator` and override `health()` returning `Health.up()` or `Health.down()`. If any indicator returns
`DOWN`, the overall aggregate status on `/actuator/health` evaluates to `DOWN`.

---

## 21. Hibernate Caching Deep Dive

* **First-Level Cache (L1):** `Session` / `EntityManager` scoped, mandatory, and active per transaction.


* **Second-Level Cache (L2):** Shared application-wide `SessionFactory` cache (e.g., Ehcache, Redis) requiring
  `@Cacheable` and `@Cache(usage = ...)` annotations.


* **Query Cache:** Caches query result entity IDs; invalidated when target tables mutate.

---

## 22. Spring's Event Publishing Model

* **Publish & Listen:** Inject `ApplicationEventPublisher.publishEvent()` and annotate target handler methods with
  `@EventListener`.


* **Execution:** Synchronous by default. Add `@Async` to make listener execution non-blocking.


* **Transactional Listeners:** `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)` defers execution
  until transaction completion, preventing listener execution if database transactions roll back.