---
parent: DBMS
nav_order: 1
layout: default
title: Basics
---

# Basics

### 1. Database vs Datastore

- Data Store: A broad, generic term for any repository where data is kept persistently. It is an umbrella category that
  includes files, folders, hard drives, and cloud storage, as well as databases.
- Database: A specific, highly structured type of data store that includes a Database Management System (DBMS). It
  provides advanced capabilities for querying, data integrity, security, and transaction management.

### 2. OLAP vs OLTP Database

OLTP (Online Transaction Processing) is optimized for executing operational tasks
OLAP (Online Analytical Processing) is optimized for complex data analysis and querying large volumes of historical data

| Feature        | OLTP (Transaction)                                          | OLAP (Analysis)                                                    |
|----------------|-------------------------------------------------------------|--------------------------------------------------------------------|
| Primary Focus  | Day-to-day operations, fast transaction processing.         | Data analysis, business intelligence, data mining.                 |
| Data Structure | Normalized (3NF) to reduce redundancy and ensure integrity. | Denormalized (Star/Snowflake schema) for fast querying.            |
| Query Type     | Short, simple inserts, updates, and deletes (CRUD).         | Complex queries involving heavy aggregations (SUM, AVG, GROUP BY). |
| Response Time  | Milliseconds.                                               | Seconds to hours (depending on data volume).                       |
| Data Volume    | Gigabytes to Terabytes (frequently archived).               | Terabytes to Petabytes (historical data).                          |
| Storage Style  | Typically row-oriented.                                     | Typically column-oriented.                                         |

### 3. Types of DataBases

- Broadly Two Types:
    - Relational Databases (RDBMS)
    - NoSQL Databases
- Note: OLTP includes more than just transactions, likes on an instagram post which go for eventual consistency and BASE
  are also OLTP
- Third Type: OLAP DBs (not included in the two since the first two are used for OLTP)

### 4. Relational Databases

* Data Model: Rows and columns in structured tables. Uses strict schemas.
* Properties: High ACID (Atomicity, Consistency, Isolation, Durability) compliance.
* Scaling: Primarily vertical (buying a bigger machine).
    * Horizontal scaling via sharding or replication is complex.
        * Why? Hard to commit to ACID
        * locking rows or tables to ensure a transaction succeeds completely or fails completely is straightforward on
          Single machine
        * For multiple machines need to use 2 Phase commit which adds significant latency
* For Financial systems, order management, or any application where data integrity and complex joins are non-negotiable.
* Historically RDB are the goto solution due to being a good default support
* Reasons for using NoSQL DBs:
    * Your application requires super-low latency.
    * Your data are unstructured, or you do not have any relational data.
    * You only need to serialize and deserialize data (JSON, XML, YAML,
      etc.).
    * You need to store a massive amount of data.

### 5. NoSQL Databases

Include all non RDB

- Key-Value Stores:
    - Concept: Highly performant hash tables.
    - Examples: Redis, Memcached.
    - Best Use Case: Caching, session management, leaderboards.
- Document Databases:
    - Concept: Stores data as JSON, BSON, or XML documents.
    - Examples: MongoDB, DynamoDB.
    - Best Use Case: Product catalogs, user profiles, content management.
- Wide-Column Stores:
    - Concept: Stores data in column families instead of rows
        - Essentially:
            - $$\text{Map}<\text{RowKey}, \text{Map}<\text{ColumnName}, \text{Value}>>$$
            - Where each row can have different columns unlike RDB
            - Rows can be infinitely wide and sparse, the database cannot store a row as a contiguous block of data on
              disk.
            - Instead, every single column value (or "cell") is treated as an independent key-value pair.
    - Highly optimized for massive write throughput and distributed setups.
    - Examples: Cassandra, ScyllaDB.
    - Best Use Case: IoT telemetry, time-series logging, high-volume analytics.
    - popularized by Google's Bigtable paper
    - Reason for high throughput?
        - Use of LSM Trees and lazy insertion using a WAL
        - In cases of conflicts, happen at read (since LSM Trees do not have single key consistency) last write wins
- Graph Databases:
    - Concept: Uses nodes (entities) and edges (relationships) to represent data.
    - Examples: Neo4j, Amazon Neptune.
    - Best Use Case: Social networks, fraud detection networks, recommendation engines.

### 6. DB Indexing Schemes

| Index Type                                | Underlying Structure             | Primary Use Case                       | Key Characteristic                                                                                       |
|-------------------------------------------|----------------------------------|----------------------------------------|----------------------------------------------------------------------------------------------------------|
| **B-Trees / B+ Trees**                    | Self-balancing search trees      | RDBMS read optimization                | Optimized for disk I/O and range queries; keeps data sorted.                                             |
| **LSM Trees** (Log-Structured Merge-tree) | MemTable (RAM) + SSTables (Disk) | Write-heavy NoSQL (Cassandra, RocksDB) | Appends writes to memory first, making writes extremely fast; background compaction resolves duplicates. |
| **Inverted Index**                        | Map of words to document IDs     | Search engines (Elasticsearch)         | Enables full-text search capability.                                                                     |

### 7. Decision Matrix for System Design Interviews

Use this mental checklist when selecting a database during an interview:

1. **What is the Read/Write ratio?**
    * Heavy Writes $\rightarrow$ LSM-Tree based NoSQL (Cassandra) or append-only logs.
    * Heavy Reads $\rightarrow$ RDBMS with Read Replicas, or Key-Value caches (Redis) in front.

2. **Does the data require complex relationships/joins?**

    * Yes $\rightarrow$ RDBMS or Graph DB.
    * No $\rightarrow$ Document or Key-Value store.

3. **What are the consistency requirements?**

    * Strict ACID required $\rightarrow$ RDBMS.
    * Eventual consistency acceptable $\rightarrow$ NoSQL / AP systems.

4. **Data Volume & Growth?**

    * Fits on a single terabyte-scale machine $\rightarrow$ Stick to RDBMS.
    * Petabyte scale requiring horizontal scaling $\rightarrow$ NoSQL or natively distributed SQL (e.g., CockroachDB,
      Google
      Spanner).

### 7. Other DB Paradigms

- ### Multi-Model Databases
    - Most modern databases no longer limit themselves to a single category.
    - Redis: Originated as a key-value cache; now natively handles JSON documents, time-series data, graph
      relationships,
      and
      vector search.
    - MongoDB: Primarily a document store; now includes graph lookups, time-series collections, and vector
      embeddings.Relational Databases
    - (PostgreSQL/MySQL): PostgreSQL handles relational tables, structured JSON documents (
      JSONB), and vector data (pgvector)

- ### OLAP DBs

    - OLAP (Online Analytical Processing) systems require databases optimized for complex, large-scale aggregation
      queries
    - Use columnar storage since large scale Analytics only need a few columns of data at a time
    - Note: OLAP is often the most used storage solution for Logs:
        - Columnar Storage
        - Append Only: OLAP databases are optimized for this append-only behavior
        - High Compression Ratios: data is stored column-by-column, identical or similar data types sit next to each
          other on disk (e.g., repeating strings like INFO or ERROR). OLAP databases leverage this to achieve massive
          compression ratios (often 5x to 10x better than standard RDBMS)
        - Exactly how Splunk and the ELK Stack (specifically Elasticsearch) work under the hood

- ### Othert Modern DBs in age of AI

| Database Category            | Core Focus                                                                                    | Prominent Examples                      |
|------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------|
| **Vector Databases**         | Optimizing high-dimensional embeddings for GenAI and LLM semantic search.                     | Pinecone, Milvus, Qdrant                |
| **Time-Series Databases**    | Ingesting and querying massive streams of time-stamped IoT, metrics, and log data.            | InfluxDB, TimescaleDB                   |
| **NewSQL / Distributed SQL** | Combining the horizontal scalability of NoSQL with strict ACID compliance of traditional SQL. | CockroachDB, Google Spanner, YugabyteDB |
|                              | Instead of traditional expensive 2 phase, issue copies to each and use consensus mechanism    |                                         |

### 8. Transactions

- Sequence of one or more operations (such as reading or writing data) executed as a single, logical unit of work.
- Every transaction must adhere to the four [ACID](#9-acid) properties to ensure data consistency and validity.

  ## Core Operations
    - Transactions rely primarily on two control statements:
        * `COMMIT`: Saves all modifications made during the transaction permanently.
        * `ROLLBACK`: Undoes all modifications made during the transaction, restoring the database to the last committed
          state.

### 9. ACID:

- **Atomicity**:
    - Smallest unit i.e. must occur fully or not at all (no partial running)
    - If some of the writes in a transaction fail even the successful ones are rolled back
    - With this retrying doesn't do the operation twice
- **Consistency**:
    - Actually a property of application
    - To verify that the operations don't violate the constraints of the system (i.e. balance should add up to credit -
      debit in accounting)
    - Doesn't actually belong in ACID
- **Isolation**:
    - Concurrent execution is isolated from each other
    - Ideally each transaction should occur as if they occur one by one
    - Gold standard is Serializable isolation where operations have to wait in line (but terrible for performance so
      hardly ever used)
- **Durability**:
    - Transactions data is not lost i.e. it is written to non-volatile storage
    - In some modern db it also means that it has been replicated
- Note: NoSQL Dbs don't have these guarantees in place, even operations like multi-put are often not atomic and may fail
  partially

### 10. CAP Theorem

A distributed data store can simultaneously provide at most two out of the following three guarantees:

1. **Consistency**
    - Once a write operation is successfully completed on any node in the system, all subsequent read
      operations—regardless of which node they land on—must return that new value, or an even newer one.
    - i.e. All nodes will return same value for the data
2. **Availability**
    - Each read or write request for a data item will either be processed successfully or will receive a message that
      the operation cannot be completed.
    - If a node is alive and healthy, it must accept reads and writes.
    - It is not allowed to say, "I am disconnected from the rest of the cluster, so I cannot answer you."
3. **Partition Tolerance**
    - A network partition is a communication failure between nodes. Messages are dropped, delayed, or split entirely,
      dividing one cluster into isolated groups that cannot talk to each other.
    - The system must continue to operate as a whole, despite arbitrary message loss or delays between nodes.
      Because networks are inherently imperfect, a distributed system must be designed to survive partitions. i.e.
      Partitioning is an inherent unavoidable issue

You cannot choose "CA" (Consistency + Availability) because Partition Tolerance (P) is not a configuration setting; it
is a law of physics.

## The Two Choices During a Partition

1. Choose Consistency (Cancel Availability)
    - You decide that serving old, incorrect data is worse than serving no data at all.
    - What happens: If a node is cut off from the rest of the cluster, it refuses to accept writes or answer reads. It
      returns an error or times out.
    - Result: Your data remains perfectly correct across the system, but your application appears "down" or broken to
      some users.

2. Choose Availability (Cancel Consistency)
    - You decide that keeping the application up and running is more important than perfect data accuracy.
    - What happens: The isolated node continues to accept writes and answer reads using whatever stale data it has.
    - Result: Your application stays online for everyone, but different users will see different versions of the
      data. The data diverges, and you will have to manually or automatically resolve the conflicts later once the
      network heals.
