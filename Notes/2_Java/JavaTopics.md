---
title: Todo
nav_order: 99
parent: Java
layout: default
---

## **Future Topics**

**1. Core Java & Modern Language Features**

* **Language Features:** Flexible Constructor Bodies, Module Import Declarations, Compact Source Files, Stream Gatherers, and Foreign Function & Memory API (Project Panama).

**2. JVM Internals & Performance Tuning**

* **Memory Management:** Memory Leaks (detecting via JProfiler, YourKit, or VisualVM).
* **Garbage Collectors:** Sub-millisecond pause strategies in ZGC, Generational ZGC, and Shenandoah.
* **JIT & Native Compilation:** C1/C2 compilers, Inlining, Escape Analysis, Runtime Tuning for Kubernetes (memory limits vs. heap size), and GraalVM Native Images.

**3. Advanced Concurrency**

* **Java Memory Model (JMM):** Memory visibility, happens-before relationships, and memory barriers at the CPU cache level.


* **Lock-Free Programming:** `AtomicReference`, `LongAdder`, and lock-free execution structures.
* **Thread Safety & Storage:** Scoped Values as a modern alternative to `ThreadLocal`, and performance trade-offs in concurrent collections (`ConcurrentHashMap` segment/bin locking vs `CopyOnWriteArrayList` vs `Collections.synchronizedList`).



**4. Spring Framework & Enterprise Ecosystem**

* **Spring Boot 3.x:** Auto-configuration internals, custom starters, `@Conditional` annotations, Native Image support, Observation API (Micrometer), and `RestClient`.
* **Persistence & Transactions:** `@Transactional` pitfalls (same-class calls, exception propagation) and Hibernate/JPA tuning (N+1 query problem, first/second-level caching, lazy loading strategies).
* **Spring Security:** OAuth2/OIDC, JWT implementations, and method-level security.
* **Reactive vs. Servlet:** Spring WebFlux vs. Standard MVC in a Virtual Thread world.

**5. System Design & Microservices Architecture**

* **Architecture & Messaging:** Microservices patterns (Service Discovery, API Gateways, Mesh like Istio/Linkerd), Kafka (partitions, consumer groups), and RabbitMQ.
* **Resiliency & Consistency:** Circuit Breakers (Resilience4j), Retries with exponential backoff, Bulkheads, Saga Pattern (Choreography vs. Orchestration), Outbox Pattern, and Two-Phase Commit.
* **Database Scaling & APIs:** CQRS, Sharding, Read Replicas, CAP/PACELC theorems, Idempotency keys, Versioning, and GraphQL vs. REST.

**6. Production Mindset, Testing & Tooling**

* **Observability & Infrastructure:** OpenTelemetry, Prometheus/Grafana, distroless Docker multi-stage builds, and Kubernetes (Pod lifecycles, Probes, ConfigMaps).
* **Testing Strategy:** Testcontainers for integration tests, ArchUnit for architecture rules, Property-Based Testing (jqwik), Pact for contract tests, and advanced Mockito (spying, argument captors).
* **Recommended Reading:** *Effective Java (4th Edition)*, *The Well-Grounded Java Developer (2nd Edition)*, *Optimizing Java*, *Designing Data-Intensive Applications (DDIA)*, *System Design Interview*, *Building Microservices (2nd Edition)*, and *Cloud Native Java*.