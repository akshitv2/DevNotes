---
title: Software
nav_order: 3
layout: default
parent: Tools
---

## 1. Build Tools

### 1.1 Gradle

### 1.2 Maven

### 1.3 POM VS BOM

| Aspect                      | POM                         | BOM                        |
|-----------------------------|-----------------------------|----------------------------|
| Purpose                     | Build & configure a project | Manage dependency versions |
| Has code                    | Yes                         | Usually no                 |
| Produces artifact           | Yes (jar/war)               | No (pom only)              |
| Uses `dependencyManagement` | Optional                    | Required                   |
| One per project             | Yes                         | Shared across projects     |


## 1. Kafka 

## 1. Netty

1. ## What is netty?
    - Asynchronous event driven networking framework for Java
    - Built on Java NIO

2. ## Architecture:
    1. Reactor Pattern:
        - Consists of 2 groups of threads:
            1. BossGroup:
                - Usually one thread accepting connections and designating it to worker
            2. WorkerGroup:
                - Group of threads that perform actual I/O, execute logic
                - Run the eventLoop
        - EventLoop And EventLoopGroup:
            - EventLoop:
                - Single thread that runs in infinite loop
                - Waits for events (IO, tasks, timers) processes and goes back to waiting
                - Runs on the worker thread
                - Each connection (called channel) only goes on one thread (so no thread switching issues) but each
                  thread has more than one
                  connection (many-to-one relationship)
                - OS notifies netty on change/response which thread checks on loop and works on
            - EventLoopGroup:
                - group of these threads
    2. ChannelPipeline
        - Uses interceptor filter pattern
        - Handlers process data:
            - InboundHandlers: example: Bytes to json
            - OutboundHandlers: example: Json to bytes
        - ChannelHandlerContext:
            - Dynamic handler flow control
        - This is where you define custom handlers to create your own software
            - example: Command handlers, Decoder in lettuce
    3. ByteBuf Memory buffer:
        - Native ByteBuffer is criticized (for requiring flip())
        - Note: ByteBuffer uses one pointer for both read and write. If you write to buffer and want to read you need to
          call `flip()` which moves pointer back (the amount of data you wrote). Without this you are just reading next
          garbage bytes.
            - Leads to double flip where you need to track which method flipped at end and which didn't.
        - ByteBuf from Netty has separate read and write pointers (thus no flip)

---

## 2. Redis

1. ## Basics

   [//]: # (todo)

2. ## Redis Cluster
    1.  ### Redis Cluster vs Node:
        - ### Node:
            - Single instance of redis-server
            - Can be primary (master) handles writes/read or replica (secondary/slave) (copies master for scaling and
              backup)
            - ### Cluster:
            - Collection of multiple Redis nodes linked together
            - Data is sharded i.e. cluster is split across multiple nodes
            - Uses [**hash slots**](#Hash-Slots), 16,384 in total divided among master nodes
            - If one node fails, cluster can promote replica in its place
            - Scaled horizontally (add more nodes instead of more memory)
        - ### Hash Slots:
            - Redis divides entire keyspace into 16,384 slots
            - Each slot is a bucket (with millions of keys limited by RAM)
            - Split slots across nodes (nodes-replicas actually)
            - Use formula CRC16
            - for example: Key `user:100`
            - $$\text{slot} = \text{CRC16}(\text{"user:100"}) \pmod{16384}$$
            - 16,384 is chosen as a middle point between scalability and overhead
            - Since formula is deterministic every node knows which node holds key
            - **Issues**:
            - HotSlot:
                - One slot can become "heavier" and significantly skewed in usage
                - Called hot slot
                - Not an issue usually with CRC distribution
                - Problem with [**hashtags**](#Hashtags)
    2. ### Failover (Master node):
        - Failure Detection (PING/PONG Heartbeat)
            - Every node talks to every node using gossip protocol
            - Usually on port 10000 + running port
            - if NodeA stops responding to pings from Node B, Node B marks A `PFAIL` (possible failure)
            - If consensus reached, A marked `FAIL`
        - Election:
            - Replica needs to be promoted, elected by remaining master nodes
            - Choose most up-to-date replica as master
        - Promotion:
            - Chosen replica becomes master and broadcasts config update
        - Note: If original master comes back up it joins cluster and demotes itself to Replica
        - Requirements:
            - At least 3 master nodes with one replica for each
3. ## Features:
    1. ## Hashtags:
        - Usage: key containing {}
        - Essentially tells calculate hashes based on text inside {}
        - Example:
            - Keys which will go to different slots
                - `user:1001:name`
                - `user:1001:email`
            - Keys which will go to same slot
                - `user:{1001}:name`
                - `user:{1001}:email`
            - Note: Only first {} is valid and empty {} is ignored
        - Issues:
            - ### Hot Slot:
                - Explained above
                - How to avoid?
                    - Avoid using too general hashtags
                        - user:{**1001**}:name ok
                        - user:{**google**}:1001:name not ok
            - Increased Performance Load:
                - Due to hot slot rebalancing becomes heavier
        - Operations that require same slot:
            - MGET, MSET, MULTI/EXEC, Lua Scripts, SUNION, SINTER,SDIFF, RENAME
            - Transactions
4. ### Clients:
    1. ### Lettuce
        - Default client in spring-boot-starter-data-redis
        - High throughput asynchronous built on netty, reactive
    2. ### Jedis
        - Straightforward Blocking I/O (Synchronous)
        - Not thread safe, requires connection pool
    3. ### Redisson
    4. Lettuce vs Jedis