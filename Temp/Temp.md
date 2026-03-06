---
title: Scratch book
nav_order: 5
layout: default
---

1. Core Java & Modern Language Features
   Since Java 17 and 21 are now the industry standards for enterprise apps, you’ll be expected to know more than just Streams and Lambdas.

Java 17–25 Features: Sealed classes, Records, Pattern Matching for switch, and Text Blocks.

Project Loom (Virtual Threads): This is the biggest topic in 2026. Be ready to explain how virtual threads differ from platform threads and why thread-per-request is back in style.

The Collections Framework: Deep dive into ConcurrentHashMap (segment locking), CopyOnWriteArrayList, and why Collections.synchronizedList is usually a bad idea for performance.

Generics & Type Erasure: Edge cases in PECS (Producer Extends, Consumer Super).

2. JVM Internals & Performance Tuning
   At a senior level, you aren't just writing code; you’re responsible for how it behaves in production.

Memory Management:

Heap vs. Stack vs. Metaspace: Where do Lambdas and method references live?

Garbage Collectors: In 2026, ZGC and Shenandoah are the stars for low-latency. Understand how they achieve sub-millisecond pauses.

Memory Leaks: How to find them using JProfiler, YourKit, or VisualVM (hint: look at static collections and unclosed resources).

JIT Compilation: How C1 and C2 compilers work and the concept of "Inlining" and "Escape Analysis."

GraalVM & Native Images: When to use AOT (Ahead-of-Time) compilation versus traditional JIT.

3. Advanced Concurrency
   Forget just using synchronized. Senior developers need to understand the "memory visibility" and "lock-free" world.

Java Memory Model (JMM): The happens-before relationship and how volatile actually works at the CPU cache level.

Lock-Free Programming: Using AtomicReference, LongAdder, and the Compare-And-Swap (CAS) algorithm.

Structured Concurrency: Managing multiple sub-tasks as a single unit of work (part of newer Java versions).

CompletableFuture: Chaining async tasks and handling exceptions in non-blocking pipelines.

4. Spring Framework & Ecosystem
   Most senior Java roles involve Spring Boot 3+.

Spring Boot 3 specifics: Native image support, Observation API (Micrometer), and the new RestClient.

Persistence & Transactions: * @Transactional pitfalls: (e.g., calling the method from the same class, checked vs. unchecked exceptions).

Hibernate/JPA Tuning: N+1 query problem, first/second-level caching, and lazy loading strategies.

Spring Security: OAuth2, JWT implementation, and Method-level security.

Reactive vs. Servlet: When to use Spring WebFlux vs. standard MVC in a Virtual Thread world.

5. System Design & Microservices
   This is usually where "Senior" candidates are separated from the rest.

Architecture Patterns:

Event-Driven Design: Using Kafka or RabbitMQ for decoupling.

Saga Pattern: Managing distributed transactions without XA.

CQRS & Event Sourcing: When is the complexity actually worth it?

Resiliency Patterns: Circuit Breakers (Resilience4j), Retries with exponential backoff, and Bulkheads.

API Design: Idempotency keys, versioning strategies, and GraphQL vs. REST.

6. The "Production" Mindset
   Observability: Distributed tracing with OpenTelemetry and using Prometheus/Grafana.

CI/CD & Containers: Building "distroless" Docker images for Java and managing them via Kubernetes.

Testing Strategy: The Testing Pyramid—Unit vs. Integration vs. Architecture tests (ArchUnit) vs. Contract tests (Pact).

The "Sneaky" Senior Question
"If Virtual Threads make blocking I/O cheap, do we still need Reactive Programming (WebFlux)?"


1. The "Java Bible" (Core Mastery)
   Effective Java (4th Edition) by Joshua Bloch: Released recently to cover Java 17 through 25, this is non-negotiable. It covers the correct way to use Records, Sealed Classes, and Pattern Matching. If you don’t know Item 1 (Static Factories) or the new items on Data-Oriented Programming, you aren't ready for a senior interview.

The Well-Grounded Java Developer (2nd Edition) by Evans, Verburg, and Martn: This is excellent for understanding the modern ecosystem, including the JVM's support for non-Java languages and modern build tools.

2. Concurrency & Performance
   Java Concurrency in Practice by Brian Goetz: Wait! This book is 20 years old. Why read it? Because the fundamental physics of threads, visibility, and safety haven't changed.

Supplement: "The State of Loom" (Online Articles/Blogs): Since no single book perfectly captures the 2026 state of Virtual Threads, follow Brian Goetz’s latest write-ups on OpenJDK. Focus on Structured Concurrency and Scoped Values.

Optimizing Java by Ben Evans: Essential for the JVM Internals section. It explains how Garbage Collectors (ZGC/Shenandoah) actually behave under load.

3. Architecture & System Design
   Designing Data-Intensive Applications (DDIA) by Martin Kleppmann: This remains the "S-Tier" resource for senior devs. It’s not Java-specific, but it explains the why behind Kafka, NoSQL, and Distributed Transactions.

System Design Interview (Vols 1 & 2) by Alex Xu: The gold standard for prepping for the "Whiteboard" portion of the interview. It provides clear blueprints for scaling from 0 to millions of users.

Building Microservices (2nd Edition) by Sam Newman: The definitive guide on how to avoid "Distributed Monoliths"—a common senior-level architectural failure.

4. Spring & Cloud-Native
   Spring Boot in Action (Latest Edition): Look for versions covering Spring Boot 3.x. Focus specifically on the chapters regarding Spring Native (GraalVM) and Observability.

Cloud Native Java by Josh Long: Even though it’s a few years old, the philosophy of "disposable" and "stateless" Java applications is vital for Kubernetes-heavy environments.


Conversation with Gemini
You said
Create a thorough and detailed study index for senior developer role specializing in Java

Gemini said
Becoming a senior Java developer in 2026 isn't just about mastering syntax; it’s about understanding the mechanics of the JVM, the orchestration of distributed systems, and the trade-offs of architectural decisions. Since Java 25 (the latest LTS) has recently landed, your study plan needs to bridge the gap between "modern Java" and "enterprise-scale engineering."

Here is your detailed study index, categorized by technical domain.

1. Modern Java Language Deep-Dive (Java 21–25)
   At the senior level, you are expected to write "idiomatic" modern Java. If you're still writing Java 8-style code, you're essentially using a Ferrari to drive to the grocery store.

Pattern Matching: Mastery of instanceof patterns, switch patterns, and Record patterns for destructuring.

Data Modeling: Proper use of Records (for DTOs/immutable data) and Sealed Classes to define restricted class hierarchies.

Java 25 Specifics: * Flexible Constructor Bodies: Performing logic before super().

Module Import Declarations: Simplifying imports at the module level.

Compact Source Files: Understanding the "instance main" method for smaller scripts.

API Evolution: Stream Gatherers (Java 24) for complex pipeline transformations and the Foreign Function & Memory API (Project Panama).

2. High-Performance Concurrency & Performance
   This is where senior devs are separated from juniors. You must understand how Java handles thousands of simultaneous tasks in 2026.

Virtual Threads (Project Loom): How they differ from platform threads, avoiding "thread pinning," and why you might not need reactive programming anymore.

Structured Concurrency: Managing subtasks as a single unit of work to prevent thread leaks.

Scoped Values: A modern, more efficient alternative to ThreadLocal for sharing data across threads.

JVM Internals & GC: * Garbage Collectors: Deep dive into G1GC (the default), ZGC (for sub-millisecond pauses), and Generational ZGC.

Runtime Tuning: Tuning Java for Kubernetes (memory limits vs. heap size).

JIT Compilation: Understanding C1/C2 compilers and GraalVM's Native Image for sub-second startup times.

3. The Spring Boot 3.x Ecosystem
   Spring remains the backbone of Java enterprise. In 2026, the focus has shifted toward cloud-native efficiency and observability.

Spring Boot 3 Fundamentals: Auto-configuration internals, custom starters, and the @Conditional annotation suite.

Security: OAuth2/OIDC flows, JWT implementation, and Method-level security.

Data Access: Hibernate/JPA optimization (N+1 problem, batching, and second-level caching), and Spring Data JDBC for simpler use cases.

Reactive vs. Imperative: When to use Project Reactor (WebFlux) vs. Virtual Threads.

Observability: Integrating Micrometer, Prometheus, and OpenTelemetry for distributed tracing.

4. System Design & Distributed Architecture
   As a senior, you spend more time drawing boxes than writing code. You must design for failure.

Pattern	Key Concepts to Master
Microservices	Service Discovery, API Gateways, Service Mesh (Istio/Linkerd).
Messaging	Kafka (partitions, consumer groups), RabbitMQ (exchanges).
Resilience	Circuit Breakers (Resilience4j), Retries, Rate Limiting, Bulkheads.
Data Consistency	Saga Pattern (Choreography vs. Orchestration), Outbox Pattern, Two-Phase Commit.
Database Scaling	CQRS, Sharding, Read Replicas, and CAP/PACELC theorems.
5. Infrastructure & Modern DevOps
   You don't need to be a SRE, but you must know where your code lives.

Containerization: Writing efficient Dockerfiles (multi-stage builds, distroless images).

Kubernetes (K8s): Pod lifecycles, Probes (Liveness/Readiness/Startup), ConfigMaps, and Secrets.

CI/CD: Designing pipelines in GitHub Actions or GitLab CI that include automated security scanning (SAST/DAST).

Infrastructure as Code: Basic reading/writing of Terraform or Pulumi.

6. Testing & Quality Assurance
   "It works on my machine" is a fireable offense at the senior level.

Testcontainers: The gold standard for integration testing with real databases/queues.

Property-Based Testing: Using tools like jqwik to find edge cases.

Architecture Testing: Using ArchUnit to enforce package structures and dependency rules.

Mocking: Advanced Mockito (mocking static methods, spying, argument captors).

A Note on Technical Leadership:
Beyond the code, a senior developer must master Code Reviews (focusing on architecture, not just style), Mentorship, and Communication. You are the bridge between product requirements and technical reality.

Would you like me to dive deeper into a specific area—for instance, a deep dive into Virtual Threads vs. Platform Threads, or a set of senior-level interview questions for Spring Boot 3?