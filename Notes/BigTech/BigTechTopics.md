---
title: Topics
nav_order: 3
parent: Big Tech Topics
layout: default
---

# From Banking to Big Tech: The System Design Toolkit

## What you already have (don't discount this)

Banking gives you think Big Tech engineers often *lack*: rigorous ACID transaction reasoning, strong consistency
guarantees, reconciliation/audit thinking, regulatory-grade security, and often solid SQL/data-modeling instincts. Frame
your transition as "adding scale and eventual-consistency tools to an already-rigorous foundation," not starting over.

What's genuinely different: Big Tech systems are built around the assumption that **failure is constant and scale is
extreme** — a single service may handle more requests per second than your whole bank processes in a day. That reshapes
almost every design decision toward horizontal scaling, redundancy, and probabilistic tradeoffs instead of
single-source-of-truth consistency.

---

## 1. Probabilistic Data Structures (the "only makes sense at scale" category)

These trade a small, tunable error rate for huge savings in memory/time — irrelevant when you have millions of rows,
essential at billions.

- **Bloom Filter** — Tests "definitely not in set" vs "maybe in set" using a bit array + multiple hashes. No false
  negatives, tunable false positives. Used to avoid expensive lookups (e.g., "has this key ever been written to disk?"
  in Cassandra/HBase, or "has this URL been seen?" in web crawlers).
- **Counting Bloom Filter / Cuckoo Filter** — Like a Bloom filter but supports deletion.
- **Count-Min Sketch** — Approximates frequency counts of items in a stream (e.g., "top trending searches") in fixed
  memory regardless of stream size.
- **HyperLogLog** — Estimates the *cardinality* (count of distinct elements) of a massive set using barely any memory.
  This is how "37M unique visitors today" is computed without storing 37M IDs.
- **MinHash / SimHash** — Estimate similarity between large sets/documents cheaply (near-duplicate detection,
  plagiarism/spam detection).
- **Skip List** — Probabilistic alternative to balanced trees; used inside Redis sorted sets, LevelDB/RocksDB memtables.

---

## 2. Distributed Systems Fundamentals

- **CAP Theorem** — Under a network partition, you choose Consistency or Availability, not both. (PACELC extends this:
  even without a partition, you trade latency vs consistency.)
- **Consistency models** — Strong, eventual, causal, read-your-writes. Banking defaults to strong; Big Tech deliberately
  relaxes this per use case (e.g., "like" counts don't need strong consistency; account balances do).
- **Consensus algorithms** — **Paxos** and **Raft** (Raft is the one worth actually understanding deeply — leader
  election, log replication, term numbers). Powers etcd, Kafka's controller, CockroachDB, etc.
- **Vector clocks / Lamport timestamps** — Ways to reason about "happened-before" ordering without a global clock across
  machines.
- **Gossip protocols** — Nodes randomly exchange state with peers until info propagates cluster-wide (used in Cassandra,
  Dynamo, service discovery).
- **Quorum reads/writes (Dynamo-style)** — W + R > N guarantees overlap between write and read sets without requiring
  all nodes to agree.
- **Split-brain** — What happens when a cluster partitions and both halves think they're the leader; know why fencing
  tokens/quorums prevent it.

---

## 3. Scalability Patterns

- **Consistent Hashing** — Distributes keys across nodes so that adding/removing a node only reshuffles a small fraction
  of keys (vs. naive `hash % N` which reshuffles almost everything). Foundational to load balancers, distributed caches,
  and sharded databases.
- **Sharding/Partitioning strategies** — Range-based, hash-based, directory-based. Know the hot-shard problem and how to
  mitigate it (salting keys, dynamic re-sharding).
- **Load balancing algorithms** — Round robin, least connections, weighted, consistent-hash-based (for cache affinity).
- **Rate limiting algorithms** — Token bucket, leaky bucket, fixed window counter, sliding window log/counter. A very
  common interview question ("design a rate limiter").
- **Circuit breaker pattern** — Stop calling a failing downstream service temporarily instead of piling up timeouts (
  Hystrix/resilience4j pattern).
- **Bulkhead pattern** — Isolate resource pools so one failing dependency can't exhaust threads/connections for
  everything else.
- **Retries with exponential backoff + jitter** — Naive retries synchronize and create thundering herds; jitter
  desynchronizes them.
- **Backpressure** — Letting a slow consumer signal a fast producer to slow down, rather than buffering unboundedly.

---

## 4. Caching

- **Cache patterns** — Cache-aside (lazy load), write-through, write-back/write-behind, read-through.
- **Eviction policies** — LRU, LFU, ARC, TTL-based.
- **Cache stampede / thundering herd** — When a hot key expires and thousands of requests simultaneously hit the DB;
  mitigated with request coalescing, locking, or probabilistic early expiration.
- **CDN edge caching** — Caching static (and increasingly dynamic) content geographically close to users.
- **Distributed caches** — Redis and Memcached internals: why Redis is single-threaded per core (avoids lock
  contention), data structures Redis exposes (sorted sets, HyperLogLog built in, streams).

---

## 5. Storage & Databases at Scale

- **SQL vs NoSQL tradeoffs** — You know SQL/ACID cold; the gap is knowing *when* to give up joins/transactions for
  horizontal scale.
- **Wide-column stores** — Bigtable, Cassandra, HBase — optimized for huge sparse tables and write-heavy workloads.
- **Document stores** — MongoDB-style, schema-flexible.
- **Key-value stores** — DynamoDB, Redis — the simplest scaling model.
- **LSM Trees vs B-Trees** — B-trees (what most relational DBs use) are read-optimized; **Log-Structured Merge trees** (
  Cassandra, RocksDB, LevelDB) batch writes sequentially and are write-optimized — crucial for high-ingest systems.
- **Columnar storage / OLAP** — Parquet, BigQuery, Redshift, Snowflake. Contrast with the row-oriented OLTP systems
  banking lives in — columnar stores make "scan 2 columns across a billion rows" cheap.
- **Replication topologies** — Single-leader, multi-leader, leaderless (Dynamo-style with quorums). Know the tradeoffs
  of each for consistency and availability.
- **Change Data Capture (CDC)** — Streaming database changes out as events (Debezium + Kafka is the classic combo)
  instead of batch ETL.

---

## 6. Messaging & Streaming

- **Message queue vs pub/sub** — Point-to-point (SQS) vs fan-out to many subscribers (SNS, Kafka topics).
- **Kafka internals** — Partitions (unit of parallelism), consumer groups, offsets, replication factor, ISR (in-sync
  replicas). This is probably the single most-asked-about system in Big Tech infra interviews.
- **Delivery semantics** — At-most-once, at-least-once, exactly-once — and why "exactly-once" is really "
  effectively-once" via idempotency.
- **Idempotency keys** — Deduplicating retried requests/events — you likely already do this for payment processing, but
  it's used everywhere at scale.
- **Event sourcing / CQRS** — Store state as a sequence of immutable events, derive read models separately. Ledger-style
  banking systems already resemble this — lean on that intuition.
- **Saga pattern** — Coordinating a multi-step distributed transaction via a sequence of local transactions +
  compensating actions, replacing the two-phase commit you'd use in a monolith/single DB.

---

## 7. Big Data / Batch & Stream Processing

- **MapReduce** — The original "split work across thousands of machines" paradigm; conceptually still underlies Spark.
- **Lambda vs Kappa architecture** — Lambda runs parallel batch + streaming paths and merges results; Kappa treats
  everything as a stream, simplifying the architecture.
- **Spark / Flink** — Spark for batch + micro-batch, Flink for true low-latency streaming with stateful processing.
- **Data lake vs data warehouse** — Raw/unstructured storage (S3 + Parquet) vs structured, query-optimized storage (
  Snowflake/BigQuery).

---

## 8. Search & Indexing

- **Inverted index** — The core data structure behind all text search (term → list of documents containing it).
- **Elasticsearch/Lucene basics** — Sharding, tokenization/analyzers, relevance scoring (BM25/TF-IDF).
- **Trie** — Prefix tree, powers autocomplete/typeahead.
- **Geospatial indexes** — Geohashing, quad trees, R-trees — how "restaurants near me" queries work efficiently.

---

## 9. Microservices Architecture Patterns

- **API Gateway** — Single entry point handling auth, rate limiting, routing to backend services.
- **Service mesh (Istio/Envoy)** — Sidecar proxies handling retries, mTLS, and observability transparently, out of app
  code.
- **Service discovery** — How a service finds the current network location of another (Consul, Eureka, or
  DNS-based/Kubernetes-native).
- **Strangler fig pattern** — Incrementally replacing a legacy monolith by routing traffic to new services piece by
  piece — extremely relevant if your banking background involves legacy migration.
- **Backend for Frontend (BFF)** — Separate API layers tailored per client type (mobile vs web).

---

## 10. Reliability & Observability

- **SLI / SLO / SLA and error budgets** — The vocabulary Big Tech uses instead of (or alongside) uptime guarantees;
  error budgets formalize "how much can we break before it's a problem."
- **Chaos engineering** — Deliberately injecting failures in production (Netflix's Chaos Monkey) to verify resilience
  assumptions actually hold.
- **Distributed tracing** — OpenTelemetry/Jaeger — following one request across dozens of services to debug latency.
- **Metrics/logging at scale** — Why you aggregate (percentiles, not averages — p99 latency is the obsession, not mean
  latency).

---

## 11. Coordination & Identity at Scale

- **Snowflake IDs** — Time-sortable, distributed-unique-ID generation without a central counter (timestamp + machine
  ID + sequence).
- **Zookeeper / etcd** — Centralized coordination services for leader election, config, and distributed locks.

---

## 12. Networking & Protocols

- **REST vs gRPC vs GraphQL** — gRPC (Protocol Buffers + HTTP/2) is the internal service-to-service default at most Big
  Tech companies; REST/GraphQL more common at the edge/client-facing layer.
- **Protocol Buffers** — Compact binary serialization with schema evolution rules (why field numbers matter).
- **WebSockets / SSE / long polling** — Real-time communication tradeoffs.

---

## 13. Classic System Design Interview Problems (practice these)

- Design a URL shortener
- Design a rate limiter
- Design a distributed cache
- Design a news feed (the fan-out-on-write vs fan-out-on-read tradeoff — the "Twitter problem")
- Design a chat system (WhatsApp-style)
- Design a notification system
- Design a web crawler
- Design autocomplete/typeahead
- Design a distributed file store (S3/GFS-style)
- Design a ticket-booking/seat-reservation system (concurrency + inventory at scale — this one should feel comfortable
  coming from banking)

---

## 14. Infra Basics Worth Knowing

- **Docker & Kubernetes** — Pods, deployments, services, Horizontal Pod Autoscaler — the deployment model almost all Big
  Tech services run on.
- **Infrastructure as Code** — Terraform-style declarative infra, even at a conceptual level.

---

### How to use this list

You don't need deep expertise in all ~50 items — you need working fluency so you can reason about tradeoffs out loud.
For interviews specifically, prioritize: **consistent hashing, rate limiting, Kafka internals, caching strategies, the
CAP theorem, and 3-4 of the classic design problems** — those come up constantly. Bloom filters, HyperLogLog, and
count-min sketch are worth knowing conceptually even if you never implement one, because they signal "I understand how
to trade exactness for scale," which is the core Big Tech mindset shift.

Happy to go deep on any single topic here — for example, walk through a full "design a rate limiter" answer, or explain
Raft consensus step by step.
