# Spring Boot Interview Notes

Companion to the Spring Framework notes — this file focuses specifically on what Spring Boot adds on top of core Spring:
autoconfiguration internals, starters, configuration, packaging, and Boot-specific tooling.

---

## 1. What Spring Boot Actually Is

Spring Boot is **not a replacement** for the Spring Framework — it's an opinionated layer on top of it that removes
boilerplate:

* No XML configuration required
* Sensible defaults for almost everything (auto-configuration)
* Embedded server — no need to deploy a WAR to an external Tomcat
* Production-ready features out of the box (Actuator: health checks, metrics)
* Curated dependency versions via **starters** so you don't manually resolve version conflicts

**Spring vs. Spring Boot:**

* **Infrastructure:** Spring Framework provides raw, low-level infrastructure. Spring Boot adds autoconfiguration,
  embedded servers, and prewritten boilerplate on top of it.
* **Convention over Configuration:** Spring Boot prioritizes sensible default choices (conventions) based on declared
  dependencies and application structure, eliminating explicit manual configuration.
* **Packaging:** Spring applications typically generate WAR files requiring external container deployment (e.g.,
  Tomcat). Spring Boot generates self-contained **FAT / uber JARs** (containing application compiled `.class` files, all
  bundled dependency JARs, and configs) runnable directly on a JRE.

**Interview one-liner:** "Spring Boot is to Spring what a scaffolding tool is to a raw framework — it doesn't add new
core capabilities, it removes the setup cost of using the ones that already exist."

---

## 2. `@SpringBootApplication` & Core Annotations Breakdown

```java

@SpringBootApplication
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}

```

`@SpringBootApplication` is a meta-annotation combining three core annotations:

| Annotation                 | Role                                                                                                           |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| `@SpringBootConfiguration` | Specialization of `@Configuration` — marks this class as a source of bean definitions                          |
| `@EnableAutoConfiguration` | Tells Spring Boot to automatically configure your application based on dependencies available on the classpath |
| `@ComponentScan`           | Scans the current package and sub-packages for `@Component`/`@Service`/`@Repository`/`@Controller` beans       |

**Interview gotcha:** because `@ComponentScan` only scans the package of the annotated class **and below**, your main
application class should sit in the root package of your project — components in sibling or parent packages won't be
picked up automatically unless you widen `@ComponentScan(basePackages = ...)`.

`SpringApplication.run()` does the heavy lifting: creates the appropriate `ApplicationContext` (servlet, reactive, or
plain, auto-detected from the classpath), refreshes it, starts the embedded server if present, and fires lifecycle
events (`ApplicationStartingEvent` → ... → `ApplicationReadyEvent`).

### Essential Spring Boot & Spring Annotations

* **`@Bean`:** Used on methods within configuration classes to return an object that Spring should register as a bean in
  the context.
* **Stereotype Annotations:**
* `@Component`: Generic stereotype for any Spring-managed component.
* `@Service`: Specialized `@Component` for the business logic layer; semantically indicates domain logic, typically
  paired with `@Transactional` and security constraints.
* `@Repository`: Specialized `@Component` for data access/persistence layers; provides automatic exception translation
  for JDBC, JPA, and Hibernate exceptions into Spring's `DataAccessException` hierarchy.
* `@Controller`: Marks a class as a web controller to handle HTTP requests, typically serving web pages via view
  technologies like JSP or Thymeleaf.
* `@RestController`: Specialization combining `@Controller` and `@ResponseBody`; returns domain objects directly
  serialized into JSON/XML REST responses.

### `@Configuration` Processing Modes

* **Full Mode:** Applied when `@Configuration` decorates a class. Uses CGLIB (Code Generation Library) proxying to
  intercept method calls to `@Bean` methods, ensuring shared inter-bean dependencies return the existing singleton
  instance rather than recreating objects. Uses more CPU and memory at startup.
* **Lite Mode:** Active when `@Bean` methods are declared inside plain `@Component` classes or without `@Configuration`.
  No CGLIB proxies are generated; invoking a `@Bean` method directly from code executes plain Java invocation, which can
  inadvertently create multiple instances of a singleton candidate.

---

## 3. Starters & Dependency Management

A **starter** is a curated POM/Gradle dependency descriptor that pulls in everything typically needed for a given
capability, with compatible versions.

| Starter                            | Pulls in                                                                                                                                                                |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `spring-boot-starter`              | Core starter providing basic context, logging (SLF4J/Logback), and YAML support                                                                                         |
| `spring-boot-starter-web`          | Spring MVC, embedded Tomcat, Jackson (JSON)                                                                                                                             |
| `spring-boot-starter-data-jpa`     | Spring Data JPA, Hibernate, HikariCP, JDBC                                                                                                                              |
| `spring-boot-starter-data-mongodb` | Spring Data MongoDB support                                                                                                                                             |
| `spring-boot-starter-data-redis`   | Spring Data Redis support via Lettuce/Jedis                                                                                                                             |
| `spring-boot-starter-security`     | Spring Security (secures endpoints, basic auth, CSRF protection)                                                                                                        |
| `spring-boot-starter-test`         | JUnit Jupiter (JUnit 5), Mockito, AssertJ, Hamcrest, Spring Test                                                                                                        |
| `spring-boot-starter-validation`   | Bean Validation (Hibernate Validator)                                                                                                                                   |
| `spring-boot-starter-actuator`     | Production-readiness features, health checks, and metrics endpoints                                                                                                     |
| `spring-boot-starter-webflux`      | Reactive stack (Netty, Project Reactor) — **cannot be combined with `-web**` in the same app in most setups, since they wire different embedded servers/dispatch models |

**Naming Convention:** Official Spring Boot starters follow `spring-boot-starter-*`. Third-party/community starters
follow the pattern `*-spring-boot-starter` (e.g., `mybatis-spring-boot-starter`).

**Dependency management (BOM):** the `spring-boot-dependencies` BOM (inherited via `spring-boot-starter-parent` or
imported directly) pins compatible versions of hundreds of third-party libraries — so you typically declare a starter
*without* a version, and Boot resolves a version known to work with the rest of the stack. Overriding one dependency's
version manually can break compatibility guarantees.

---

## 4. Auto-Configuration — How It Actually Works

This is one of the most commonly probed "explain the internals" topics.

1. Classpath Inspection: Spring Boot scans dependencies declared in `pom.xml` / `build.gradle`.
2. `@EnableAutoConfiguration` triggers Boot to look up candidate configuration classes listed in:
   `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
   (in older Boot 2.x: `META-INF/spring.factories` under the `EnableAutoConfiguration` key).
3. Each candidate is a `@Configuration` class guarded by `@Conditional`-family annotations, so it only activates if
   certain conditions hold.
4. Conditions are evaluated in order and cheaply short-circuit — most auto-configuration classes do nothing at runtime
   if their trigger isn't present.

### Key conditional annotations

| Annotation                                                         | Activates when...                                                                                                                                        |
|--------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `@ConditionalOnClass`                                              | A given class is present on the classpath                                                                                                                |
| `@ConditionalOnMissingClass`                                       | A given class is **absent**                                                                                                                              |
| `@ConditionalOnBean`                                               | A bean of a given type already exists in the context                                                                                                     |
| `@ConditionalOnMissingBean`                                        | No bean of a given type exists yet — **this is how you override auto-configuration**: define your own bean of the same type and Boot's default backs off |
| `@ConditionalOnProperty`                                           | A property has a specific value (or is simply present)                                                                                                   |
| `@ConditionalOnWebApplication` / `@ConditionalOnNotWebApplication` | App is/isn't a web app                                                                                                                                   |
| `@ConditionalOnResource`                                           | A specific classpath resource exists                                                                                                                     |

### Worked example

`DataSourceAutoConfiguration` only activates if a JDBC driver + `DataSource` class are on the classpath (
`@ConditionalOnClass`) and you haven't already defined your own `DataSource` bean (`@ConditionalOnMissingBean`). Define
your own `@Bean DataSource dataSource()` and Boot's auto-configured one silently steps aside.

**Debugging auto-configuration:** run with `--debug` (or `debug=true` in properties) to print the **auto-configuration
report** — shows every candidate config class and whether it was applied ("positive matches") or skipped and why ("
negative matches"). This is a very practical, commonly-asked "how would you debug this" answer.

### Excluding auto-configuration explicitly

```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})

```

or via property: `spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration`.

---

## 5. Configuration: Properties, YAML, Profiles

### `application.properties` vs `application.yml`

Functionally equivalent; YAML supports hierarchical structure more readably and native lists, at the cost of being
whitespace-sensitive.

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: admin
server:
  port: 8081

```

### Profiles

Environment-specific configuration and beans.

```yaml
# application-dev.yml, application-prod.yml

```

Activate via `spring.profiles.active=dev` (property, env var, or `--spring.profiles.active=dev` CLI arg). Beans can be
restricted to a profile with `@Profile("dev")`. Multiple profiles can be active simultaneously (comma-separated) — later
ones override earlier ones for conflicting properties.

**Profile groups** (Boot 2.4+): bundle several profiles under one name via
`spring.profiles.group.production=db-prod,cache-prod`.

### Relaxed binding

Boot is lenient about property naming: `my.example-property`, `my.exampleProperty`, `my.EXAMPLE_PROPERTY`, and
`MY_EXAMPLE_PROPERTY` (env var style) can all bind to the same field — critical for environment variables, since shells
don't allow dots/case-sensitivity the way `.properties` files do.

### Precedence order (abbreviated — see full order in Spring Framework notes §17)

Command-line args > env vars > `application-{profile}.yml` > `application.yml` > `@PropertySource` > defaults. *
*Command-line args win over everything else** by default — this is the standard way to override config per-deployment
without rebuilding.

---

## 6. Embedded Servers

Boot ships with an embedded servlet container so the app is a **self-contained runnable JAR** — no external Tomcat
install needed.

| Server                                              | Notes                                                                                          |
|-----------------------------------------------------|------------------------------------------------------------------------------------------------|
| **Tomcat** (default with `spring-boot-starter-web`) | Most widely used, well-documented, thread-per-request                                          |
| **Jetty**                                           | Lighter-weight alternative, swap in by excluding Tomcat and adding `spring-boot-starter-jetty` |
| **Undertow**                                        | Non-blocking I/O, often used for high-throughput scenarios, lower memory footprint             |
| **Netty**                                           | Used by WebFlux (reactive stack), not a servlet container                                      |

Switching servers:

```xml

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-undertow</artifactId>
</dependency>

```

**Customizing the embedded server:** via properties (`server.port`, `server.tomcat.max-threads`,
`server.compression.enabled`) or a `WebServerFactoryCustomizer<ConfigurableServletWebServerFactory>` bean for
programmatic control.

---

## 7. DevTools

`spring-boot-devtools` (dev-only dependency, auto-excluded from production packaging) provides:

* **Automatic restart** — watches the classpath and restarts the app (fast, since it uses two classloaders — a "base"
  one for unchanged libraries and a "restart" one for your code, so only your code gets reloaded).
* **LiveReload** — auto-refreshes the browser on static resource changes.
* **Property defaults tuned for development** — e.g., disables template caching so view changes show immediately.

**Interview note:** DevTools restart is *not* true hot-swapping of bytecode (like JRebel) — it's a fast full context
restart, so instance state doesn't survive a restart.

---

## 8. Logging

Boot uses **Commons Logging** as the facade, with **Logback** as the default underlying implementation (bundled via
`spring-boot-starter-logging`, itself pulled in transitively by most starters).

### Levels

`TRACE < DEBUG < INFO < WARN < ERROR` — setting a level enables that level and everything above it.

```properties
logging.level.root=INFO
logging.level.com.myapp=DEBUG
logging.level.org.hibernate.SQL=DEBUG

```

### Switching implementations

Swap Logback for **Log4j2** by excluding `spring-boot-starter-logging` and adding `spring-boot-starter-log4j2` — Boot
auto-detects whichever is on the classpath.

### Structured / JSON logging

Boot 3.4+ added built-in structured logging support (`logging.structured.format.console=ecs` or `logstash`/`gelf`)
without needing a custom Logback encoder — useful for log aggregation pipelines (ELK, Datadog).

### File output

`logging.file.name=app.log` or `logging.file.path=/var/logs` — Boot applies sensible rolling-file defaults via Logback
under the hood.

**Interview note:** logging Hibernate SQL is a very commonly cited debugging trick:
`logging.level.org.hibernate.SQL=DEBUG` plus `org.hibernate.orm.jdbc.bind=TRACE` (Hibernate 6/Boot 3) to also see bound
parameter values.

---

## 9. Packaging & Running

### Executable ("fat") JAR

`mvn package` / `gradle bootJar` produces a single runnable JAR containing your compiled classes **plus all dependencies
** plus an embedded server — run with `java -jar app.jar`. Under the hood, Boot uses a custom `JarLauncher` and
nested-JAR class loading (`BOOT-INF/classes`, `BOOT-INF/lib`) since the JVM doesn't natively support JARs-within-JARs.

### Layered JARs (for efficient Docker images)

`bootBuildImage` / layered jar support splits the fat JAR into layers (dependencies, resources, application classes) so
Docker can cache the rarely-changing dependency layer separately from your frequently-changing application code —
meaningfully speeds up image rebuilds and reduces registry push size.

```dockerfile
# Multi-stage, layered approach (typical interview-expected answer)
FROM eclipse-temurin:21-jre AS builder
COPY app.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

FROM eclipse-temurin:21-jre
COPY --from=builder dependencies/ ./
COPY --from=builder spring-boot-loader/ ./
COPY --from=builder snapshot-dependencies/ ./
COPY --from=builder application/ ./
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]

```

### Buildpacks

`spring-boot:build-image` (Maven) / `bootBuildImage` (Gradle) builds an OCI-compliant Docker image directly from source
using Cloud Native Buildpacks — no handwritten Dockerfile needed, and it automatically applies the layering optimization
above.

### WAR deployment (legacy/optional)

Boot apps can still be packaged as a deployable WAR for an external servlet container by extending
`SpringBootServletInitializer` — mostly relevant only in enterprises still requiring external app servers.

---

## 10. Actuator — Deeper Dive

Building on the basics (health/info endpoints), a few things commonly probed further:

### Common endpoints

| Endpoint                                     | Purpose                                                                                                                       |
|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `/actuator/health`                           | Liveness/readiness-style status, with optional **groups** (`management.endpoint.health.group.readiness.include=db,diskSpace`) |
| `/actuator/metrics`                          | Micrometer-backed metrics (JVM memory, HTTP request timings, custom counters/gauges)                                          |
| `/actuator/info`                             | Arbitrary static/build info (git commit, build version) — populate via `info.*` properties or `git.properties`                |
| `/actuator/env`                              | All resolved property sources — **sensitive**, should never be public                                                         |
| `/actuator/loggers`                          | View/change log levels **at runtime** without restarting the app                                                              |
| `/actuator/threaddump`, `/actuator/heapdump` | Diagnostics — also sensitive                                                                                                  |
| `/actuator/beans`, `/actuator/mappings`      | Introspect the loaded bean graph / request mappings                                                                           |

### Kubernetes-friendly health groups

Boot's health groups map directly onto k8s liveness/readiness probes: `/actuator/health/liveness` and
`/actuator/health/readiness` are exposed automatically when running in a container (auto-detected), letting you wire
`livenessProbe`/`readinessProbe` in a k8s manifest straight to these endpoints.

### Micrometer & custom metrics

```java

@Component
public class OrderMetrics {
    private final Counter orderCounter;

    public OrderMetrics(MeterRegistry registry) {
        this.orderCounter = Counter.builder("orders.placed").register(registry);
    }

    public void recordOrder() {
        orderCounter.increment();
    }
}

```

Micrometer is a vendor-neutral metrics facade (like SLF4J, but for metrics) — the same instrumentation code exports to
Prometheus, Datadog, New Relic, etc. by swapping the registry dependency.

### Custom endpoints

```java

@Component
@Endpoint(id = "features")
public class FeaturesEndpoint {
    @ReadOperation
    public Map<String, Boolean> features() {
        return featureFlags;
    }
}

```

Exposes `/actuator/features`.

**Security reminder (repeat because it's a favorite trick question):** only `health` and `info` are exposed over HTTP by
default; everything else requires explicit opt-in via `management.endpoints.web.exposure.include`, and sensitive
endpoints should sit behind authentication/a separate management port (`management.server.port`) in production.

---

## 11. Testing — Slice Tests in Depth

Boot's "test slice" annotations load **only the relevant part** of the application context, which is faster and more
focused than a full `@SpringBootTest`.

| Annotation                               | Loads                                                                                                                     | Typical use                                                           |
|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| `@WebMvcTest(UserController.class)`      | Just the web layer (controllers, `@ControllerAdvice`, filters, JSON serialization) — services/repositories must be mocked | Testing controller request/response mapping, validation, status codes |
| `@DataJpaTest`                           | JPA repositories + an in-memory DB (H2 by default), wraps each test in a transaction that's rolled back afterward         | Testing repository queries                                            |
| `@JsonTest`                              | Just Jackson serialization/deserialization config                                                                         | Verifying custom `@JsonSerialize`/`@JsonDeserialize` logic            |
| `@RestClientTest`                        | `RestTemplate`/`WebClient` beans with a `MockRestServiceServer`                                                           | Testing outbound HTTP client code without real network calls          |
| `@DataMongoTest`, `@DataRedisTest`, etc. | Equivalent slices for other data stores                                                                                   |                                                                       |

```java

@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired
    MockMvc mockMvc;
    @MockBean
    UserService userService;

    @Test
    void returnsUser() throws Exception {
        when(userService.findById("1")).thenReturn(new User("1", "Ada"));
        mockMvc.perform(get("/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Ada"));
    }
}

```

### Testcontainers (very commonly asked about in modern Boot interviews)

Instead of H2 (which behaves subtly differently from production databases), **Testcontainers** spins up a real
Dockerized Postgres/MySQL/Kafka/etc. for integration tests, giving much higher fidelity.

```java

@SpringBootTest
@Testcontainers
class OrderRepositoryIT {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
    }
}

```

Boot 3.1+ added first-class support via `@ServiceConnection`, which auto-wires the datasource/connection properties from
the container without manually registering `@DynamicPropertySource`.

---

## 12. Spring Boot 3 & Native Images

### Boot 3 headline changes (frequently asked "what's new")

* **Baseline Java 17+** (Boot 2.x supported Java 8+).
* **Jakarta EE 9+ namespace migration:** all `javax.*` packages (`javax.persistence`, `javax.servlet`,
  `javax.validation`) became `jakarta.*` — a major, breaking migration point for anyone upgrading from Boot 2.
* **Built-in GraalVM native image support** via the `spring-boot-maven-plugin`'s `native` goal (backed by the
  separately-developed Spring Native project, now merged into core Boot).
* Observability overhaul: Spring Cloud Sleuth folded into **Micrometer Tracing**.

### GraalVM Native Images

Compiles your app **ahead-of-time** into a standalone native executable (no JVM needed at runtime).

**Trade-offs (commonly asked):**

| Feature                    | JVM (traditional)                          | Native image                                                                                                                                                      |
|----------------------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Startup time               | Seconds                                    | Milliseconds — huge win for serverless/scale-to-zero                                                                                                              |
| Memory footprint           | Higher                                     | Significantly lower                                                                                                                                               |
| Peak throughput            | Higher (JIT optimizes hot paths over time) | Slightly lower (no JIT warm-up optimization)                                                                                                                      |
| Build time                 | Fast                                       | Much slower (AOT compilation is expensive)                                                                                                                        |
| Reflection/dynamic proxies | Fully supported                            | Requires explicit "reachability metadata" hints — Boot auto-generates most of this via its AOT processing, but custom reflection-heavy code may need manual hints |

**When to reach for it:** serverless functions, CLI tools, or any environment where fast cold-start and low memory
matter more than raw sustained throughput or build-time simplicity.

---

## 13. Rapid-Fire Boot-Specific Q&A

* **What happens if two starters try to auto-configure the same type of bean (e.g., two different `DataSource`
  candidates)?** Whichever auto-configuration class is ordered first via `@AutoConfigureOrder`/`@AutoConfigureAfter`/
  `@AutoConfigureBefore` wins, unless you define your own bean, which takes precedence over all of them via
  `@ConditionalOnMissingBean`.
* **Can you have both `spring-boot-starter-web` and `spring-boot-starter-webflux` in one app?** Technically yes with
  careful configuration, but by default Boot will configure a servlet-based app if `-web` is present, and mixing them is
  almost always an anti-pattern — pick one reactive/imperative model per app.
* **What's the difference between `CommandLineRunner` and `ApplicationRunner`?** Both run once at startup after the
  context is fully loaded; `CommandLineRunner.run(String... args)` gets raw args,
  `ApplicationRunner.run(ApplicationArguments args)` gets a parsed representation (easy access to named `--option=value`
  args vs. positional ones).
* **How do you change the default embedded server port?** `server.port=8081`, or `0` for a random free port (common in
  integration tests running multiple instances in parallel).
* **How would you run scheduled/cron-style jobs in Boot?** `@EnableScheduling` + `@Scheduled(cron = "0 0 * * * *")` or
  `fixedRate`/`fixedDelay` on a method — note this uses a single-threaded scheduler by default unless you configure a
  `TaskScheduler` bean with a larger pool, so long-running scheduled tasks can starve others.
* **What's `spring.jpa.hibernate.ddl-auto` and why should you be careful with it in production?** Controls schema
  generation (`none`, `validate`, `update`, `create`, `create-drop`). `update`/`create-drop` are convenient in dev but
  dangerous in production (can silently alter or drop production schema) — production should use `validate` (or `none`)
  paired with a migration tool.
* **How do you manage DB schema changes properly in a Boot app?** Flyway or Liquibase — versioned, auditable migration
  scripts that run automatically on startup (`spring-boot-starter-...` isn't needed; just add `flyway-core`/
  `liquibase-core` as a dependency and Boot auto-configures the migration runner).

---

## Topics not yet covered (say the word to go deeper on any)

* Spring Boot CLI (groovy-based rapid prototyping — increasingly rarely used/asked about)
* Custom `@ConditionalOn...` annotations for building your own auto-configuration starter
* Full Micrometer Tracing + Zipkin/Jaeger setup walkthrough
* Boot's AOT (ahead-of-time) processing pipeline in more depth (how it generates the native-image hints)
* Detailed Flyway vs Liquibase comparison and versioning strategy
* Multi-module Gradle/Maven Boot project structure best practices