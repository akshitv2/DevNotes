---
title: Designing Data Intensive Applications
nav_order: 1
parent: Books
layout: default
---

# Designing Data Intensive Applications

1. ## Chapter 1: Reliable, Scalable, and Maintainable Applications
    1. Reliability:
        - Continuing to work correctly even when things go wrong
        - Also called resiliency and fault tolerance i.e. doesn't turn fault to failures
        - Good way to test faults is to introduce them yourselves
            - ChaosMonkey by Netflix does this

        1. Fault vs Failure:
            - Fault: One component deviating from its spec
            - Failure: Whole system stops providing service
            - Aim: Stop Fault → Failure
            - Good way to test:
                - Introduce fault and see if it causes failure
                - example: chaos monkey
            - Faults and How to fix?
                - Hardware Faults:
                    - Disk crashes, Memory corruption
                    - RAID, Dual power supply
                - Software:
                    - Bugs, Systematic Errors
                    - Harder to isolate, require thorough testing, rethinking assumptions
                - Human Errors:
                    - Configuration error leading cause
                    - Create simple abstracted admin interfaces
                    - Sandbox to test all scenarios on lower env
                    - Provide easy rollback options
        2. Ways To Prevent Error Escalation:
            - Provide easy to use dashboards to Monitor (telemetry)
            - Roll out new code gradually to limit impact
            - Provide tools to roll back fast in failure
    2. Scalability
        - Ability to cope with increased load
        - Loads is expressed in:
            - Requests/sec for servers
            - Read/Writes /sec for DB
            - No. of simultaneous active users
            - In twitters case, Fan out i.e. poster to follower fan out 1:Million
        - Describing Performance:
            - Throughput: i.e. rate at which data processed
            - For server response times
            - For most response times we use percentiles over average, p95, p99, p999 being common describing % users
              time taken avg
            - Often defined clearly in SLAs (Service Level Agreements) and must be met by companies providing products
        - Measuring:
            - Important to measure response times on client-side than time taken by server to process
                - Why?
                    - Request might sit waiting in queue (head of line blocking)
                        - When testing load on server keep sending requests async (rather than waiting for response from
                          server)
                    - When multiple downstream services are called to serve a request a single slow call can slow down
                      client
                      experience
        - Approaches to cope with load:
            - Scale up: Vertical Scaling: Upgrade to a more powerful machine
            - Scale Out: Horizontal Scaling: Add more machines to distribute
        - Elasticity:
            - Automatically add computational resource when load increases
        - ℹ️Note: Latency vs Response Time:
            - Latency = delay inherent in system, the waiting time it took to travel from source to destination (and
              back in transit)
                - Metric for infrastructure
            - Response Time = Total time it took, includes Latency + processing time
                - Metric for user experience
    3. Maintainability
        - Make systems easier for people to work upon in future
        - Three Principles:
            1. Operability:
                - Make it easy for operations to keep system running
                - Monitoring, documentation, automation
                    - Operations are what make good software work long term. Key Principles:
                        - Monitoring and telemetry
                        - Updating and security patching on time
                        - Capacity planning based on current metrics
                        - Defining Processes for each operation
            2. Simplicity:
                - Keep it simple for new engineers to continue work upon
                - Through abstractions:
                    - Complexity:
                        - Aim should be avoid adding additional Complexity, KISS
                        - Find and use useful abstractions instead

            3. Evolvability:
                - Make it easy to add new features in the future
                - Also called extensibility

    4. Conclusion:
        - No size fits all solution
        - Each solution is a trade-off

2. ## Chapter 2: Data Models and Query Languages
    1. Relational vs Document Model
        1. Definitions:
            1. Relational (SQL):
                - Structure: Tables (relations), each table is unordered collection of rows
                - Best for: Many-to-one and many-to-many relationships
                - Strict schema and normalization to reduce redundancy
                - Schema on write
            2. Document Model (NoSQL)
                - Structure: Data stored in self-contained documents (JSON/XML)
                - Best for: One-to-many relationships where data usually accessed together
                - Flexible schema
                - For schema on read (dynamic type checking)
                - Require data locality for queries to be performant, update usually requires rewriting full document
        2. Convergence (i.e. supporting each other)
            - RelationalDB added Json/XML support
            - Document DBs added better querying capabilities, joins and schema options
            - Hybrid options quite common
        3. Impedance Mismatch
            - The difference between OOP representation and the way we store it
            - Relational Approach: Dividing classes into multiple tables (normalization)
            - Document Approach: Storing data as it exists on OOP, in one class
        4. Use in Many-to-One and Many-to-Many Relationships
            - Relational: Handle these very well via joins and foreign keys
            - Document: Struggle with this, require often joining data in application data, slow and complex
    2. Declarative vs Imperative Query Languages
        - SQL (Declarative):
            - Tell the DB what you want, let it decide the best path to find it
            - Usually more concise
            - Easier to parallelize as query handler can pick and choose how to run different parts in parallel
            - Also used in CSS to automatically add to classes' style
        - IMS/CODASYL (Imperative):
            - Provide the path as well
            - Brittle as paths break on db structure changes
    3. Graph Like Data Models:
        - Useful when many-to-many relationships dominate
        - Components: Vertices (nodes) and Edges (relationships)
        - Use cases: Social graphs, semantic web
        - Querying: Language like Cypher (Neo4j)
        - Example:
            - Creating relationships:
                - ```
                  CREATE (alice:Person {name: 'Alice', age: 30})
                  CREATE (bob:Person {name: 'Bob', age: 32})
                  CREATE (alice)-[:FRIEND]->(bob)
                  ```
            - Pattern Matching:
                - ```
                  MATCH (p:Person {name: 'Alice'})-[:FRIEND]->(friend)
                  RETURN friend.name
                 ```
    4. Map Reduce:
        - Programming model for processing bulk data
        - Described in Chapter 10

3. ### Storage And Retrieval
    1. Log Structured Storage (LSM Trees)
        - Treat Databases as append only log, new data simply added at end of file
        - SSTables (Sorted String Tables):
            - Instead of random appending, append to each key
        - LSM-Trees (Log Structured Merge Trees):
            - ![img.png](Media/img.png)
            - Not an actual tree, more like large array where parts are sorted by compaction in tree like manner
            - High throughput in memory structure, dump to SSTables
        - Compaction:
            - Discards old values for the key only keeping new one

    2. Page Oriented Storage:
        - Traditional approach used by most RDBs
        - B Trees break DB into fixed size pages (usually 4/8KB)
        - Note: B Tree is a self-ba82/klancing tree data structure to efficiently store and retrieve large amounts of
          data,
          usually
        - In place updates: B Trees overwrite old data with new in place (unlike compaction which occurs routinely)
    3. Transaction Logs & Crash Recovery:
        - Since these structures overwrite data in place crashes can corrupt DB
        - **Write Ahead Log (WAL):** Write every single transaction to an append only file before updating B tree
        - Note: Since WAL stores all transactions it grows huge, and recovering state could take days replaying logs.
            - Checkpointing: Store WAL log timestamp/linenumber and db state
            - Modern implementations split WAL into segments (e.g. 64MB) and delete old segments after checkpointing is
              finish
    4. Other Indexing Strategies:
        1. Secondary Indexes: For searching using non-primary key
        2. Multi Column Indexes: For filtering by multiple fields simultaneously
        3. Full text Search: Allow searching for keywords within long strings of text
            - How it works:
                - Even before searching system processes the text, tokenizes, normalizes, stopword removed and
                  lemmatize/stem.
                - Builds inverted index of the words i.e Word | Documents containing it
                - On search system uses your words and matches against inverted index using intersection
        4. In memory DB: Keep entire dataset in RAM to avoid disk I/O Bottlenecks
    5. OLTP vs OLAP
        - Online Transaction Processing vs Online Analytical Processing
        - OLTP: Handles day-to-day transactions
            - Small number of records per query (by key)
            - Users: End users (customers, clerks)
            - Queries Simple, fast (INSERT, UPDATE}, DELETE)
            - Very Fast Real time execution
        - OLAP: Handle analytical data
            - Large volumes of past data
            - Users: Managers and analysts
            - Queries: Are complex and heavy and time-consuming
            - Slower but optimized for analysis, don't need to be instant
    6. Row vs Column Oriented Storage
        - Rows:
            - Al columns for a single row are stored together contiguously
            - Best For OLTP
            - Faster for Transactions like INSERT, SELECT, DELETE
            - 🟢Fast Single Record Look up, simple storage model
            - 🔴Inefficient for analytics that scan only a few columns
            - e.g. mySQL, PostgreSQL
        - Columns:
            - Each column is stored separately contiguously
            - Reads only required columns thus speeds up when only few columns are needed
            - Much faster for aggregations
            - Row alignment is maintained by position
            - e.g. Amazon Redshift, Snowflake

4. ### Encoding and Evolution
    1. Compatibility:
        - Backward Compatibility is often easier to achieve as we can reference past
        - Forward Compatibility significantly harder, needs foresight. Needs older code to ignore future changes
    2. Formats:
        - Note: Programs usually work with in memory i.e. RAM and pointers for variable location. These stop working as
          soon as you store them and retrieve them next time since they are all reset.
        - Applications usually use two different formats
            - Data structure or object in memory
            - binary encoded for transmission
        - **Encoding**: Data structure → Binary Encoded process
            - Built into most modern languages:
                - Java has serializable
                - Python Pickle
                - Note:Using language specific encoding and transmitting in the same locks you into using same language at decoding
                - Note: Also another security risk if hacker can get you to decrypt arbitrary code, needs to have a well-defined schema
                - Often lack versioning and backward forward compatibility 
        - Language Independent Formats:
            - JSON:
              - 🟢 Most popular by far due to standard of internet
              - 🔴 Doesn't distinguish between integer, float or specify precision
              - 🔴 No binary support (need to BASE64 Encode ballooning size by 33%)
            - XML
              - 🔴 Doesn't distinguish number and string
              - 🔴 No binary support (need to BASE64 Encode ballooning size by 33%)
            - Binary Variants like BSON, MessagePack
            - Thrift by Facebook
            - Protocol Buffers by Google
            - Avro:
        - Note: Both Thrift and Protocol Buffers use schema i.e. they don't store field names with data instead using numbered field tags, they are
          backward and forward compatible where mapping ignore tags which don't exist on either
        - Note: Avro uses different schemas at reader and writer resolved by schema library i.e. very compact because it doesn't carry any schema definition with it
        - Note: Avro writes schema at start of file when storing. But in transit uses no schema which is stored at schema registry i.e. the library
    3. Data Flow Modes:
        - Through DBs:
            - One process writes to a DB, another reads it
            - DB effectively acts as a message to the future
            - Challenge faced:
                - Data outliving code i.e. new apps built on new FWs must be able to read the same old data
                - Need to make sure your older code is written in a way that if it reads new fields it writes them back intact 
        - Through Services (REST and RPC):
            - REST: Uses JSON over HTTP, using simple URLs and resources
            - RPC (Remote Procedure Call): Make remote network request look like a local function call.
                - Powerful but flawed since they might look like local functions their latency, data transfer of objects
                  like requests which don't serialize well is unpredictable
        - Message Passing DataFlow: Use of MQs like Apache Kafka, RabbitMQ where message sent to broker and consumer
          picks up from broker
    4. Distributed Actor Framework:
       - Architecture that uses stateful actors which act often 1:1 for each user
       - Don't need to talk to external DB as often or quick as can perform actor to actor communication (on crash uses append only log to recreate state)
       - Useful for instant chat/trading apps, used in whatsapp
       - Each actor is like a virtual thread with its own independent memory (state)
    5. Schema Merits:
        - Use of schema decouples objects, make them more compact, provide more documentation in common schema store,
          enforce rules on compatibility both ways

1 Liners

- Redis also used a MQ
- Kafka provides data durability