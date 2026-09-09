---
parent: System Design
layout: default
title: Components
---

## Open Systems Interconnection Model

- Theoretical framework used for teaching developed by the International Organization for Standardization (ISO) in 1984
- Data propagation flows downward from Layer 7 to Layer 1 at the transmitting node, and upward from Layer 1 to Layer 7
  at the receiving node.
- Real-world Internet networking is based largely on the *TCP/IP model*, which does not maintain separate Session and
  Presentation layers.

# OSI Model Layers

| Layer | Name             | Primary Function                                                                                                                       | Common Protocols / Technologies                  | Key Concepts & Examples                                                                                                                                                                                                                                                                                    |
|------:|------------------|----------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **7** | **Application**  | It is the interface between application and network                                                                                    | HTTP, FTP, SMTP, DNS                             | Defines **what the application wants to do** over the network. For example, an HTTP request specifies a resource and action: `GET /index.html`. HTTP itself does not handle the underlying transport; it relies on lower layers such as TCP/IP.                                                            |
| **6** | **Presentation** | Translates, formats, encrypts, and compresses data so applications can use it. Essentially gets data to application in a usable format | TLS/SSL, JSON, XML, ASN.1                        | In practice, these responsibilities are distributed across modern protocols rather than being a distinct OSI layer.                                                                                                                                                                                        |
| **5** | **Session**      | Establishes, manages, synchronizes, and terminates communication sessions between applications.                                        | NetBIOS, RPC, PPTP                               | Manages the **dialogue between applications**, including maintaining and terminating sessions. Communication can be **simplex**, **half-duplex**, or **full-duplex**. In modern TCP/IP networking, Session, Presentation, and Application functions are generally combined into the **Application layer**. |
| **4** | **Transport**    | Provides end-to-end delivery between hosts and manages data transfer between applications.                                             | TCP, UDP                                         | Performs **segmentation and reassembly**. TCP provides reliable, ordered delivery and flow/congestion control; UDP provides a simpler, connectionless transport with minimal overhead.                                                                                                                     |
| **3** | **Network**      | Routes packets between different networks using logical addressing.                                                                    | IPv4, IPv6, ICMP, OSPF, BGP                      | Uses **logical addresses (IP addresses)** to determine where packets should go. Routing protocols such as OSPF and BGP help determine paths through interconnected networks.                                                                                                                               |
| **2** | **Data Link**    | Provides frame-based, node-to-node delivery over a single network link or segment.                                                     | Ethernet (802.3), Wi-Fi (802.11), PPP, ARP*      | Handles **frames**, MAC addressing, and access to the local network medium. Provides delivery between directly connected nodes.                                                                                                                                                                            |
| **1** | **Physical**     | Transmits raw bits over a physical medium.                                                                                             | Copper (Cat6), fiber optics, RF, hubs, repeaters | Defines the **electrical, mechanical, and signaling characteristics** of physical communication: voltages, connectors, frequencies, cables, and transmission of `0`s and `1`s.                                                                                                                             |

# TCP/IP Model

The **TCP/IP model** is the practical protocol architecture underlying the modern Internet. It is commonly represented
as a **4-layer model**, combining some of the responsibilities separated into distinct layers in the OSI model.

| Layer | Name                      | Primary Function                                                                           | Common Protocols / Technologies            | Key Concepts & Examples                                                                                                                                                                                                                                                                                          |
|------:|---------------------------|--------------------------------------------------------------------------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **4** | **Application**           | Provides protocols and services that applications use to communicate over a network.       | HTTP/HTTPS, SMTP, IMAP, FTP, DNS, SSH, TLS | Handles **application-level communication**, including data representation, encoding, and application-level dialogue. TLS encryption and compression are generally treated as Application-layer functions in the TCP/IP model because they are implemented as part of application protocols/software and not OS. |
| **3** | **Transport**             | Provides **end-to-end communication** between applications running on hosts.               | TCP, UDP                                   | Handles segmentation, reassembly, port numbers, and transport-level error handling. TCP provides reliable, ordered delivery with flow and congestion control; UDP provides a simpler connectionless transport.                                                                                                   |
| **2** | **Internet**              | Provides **logical addressing and routing** of packets between networks.                   | IPv4, IPv6, ICMP                           | Determines how packets are addressed and delivered across multiple interconnected networks. IP provides addressing and routing; ICMP is used for network control and diagnostic messages.                                                                                                                        |
| **1** | **Network Access / Link** | Handles communication over the local network and transmission through the physical medium. | Ethernet, Wi-Fi, PPP, ARP                  | Defines how data is **framed and transmitted on a local network**, including interaction with network hardware and physical media such as copper, fiber, and radio.                                                                                                                                              |

## Core Architectural Components

1. ### DNS
    - Domain Name System (Base-level DNS) distributed hierarchical database (with each layer consisting of thousands of
      servers) that translates human-readable url into
      machine IP address
    - **Hierarchy**:
        - **Root Nameservers** (.): Top of hierarchy, 13 worldwide containing same data for redundancy, link to TLD. Our
          device routes to the closest one (in terms of network hops)
        - **Top Level Domain (TLD) Nameservers**: Maintain records for all domains under their extension, point to the
          Authoritative server  (for e.g. only one tld for .com)
        - **Authoritative Server**: Hold the actual DNS records mapping the domain to the IP address
    - Resolution Flow:
        - The client (browser/OS) asks the **Recursive Resolver** e.g. 8.8.8.8 checks cache first else polls the
          hierarchy step by step
    - Note: When we set DNS on device manually we choose a different resolver than our ISPs
        - If you use a poorly distributed IP resolver it can break all geo-routing and cdn optimization by routing you
          to IPs far away
    - **Geographical / Latency-Based Routing**: Smart DNS providers look at the incoming resolver's IP and return record
      pointing to the data center physically closest to user.<br> If you use a poorly distributed IP resolver it can
      break all geo-routing optimization by routing to far away IPs

### 2. Load Balancer:

- Acts as reverse proxy to distribute incoming network across a cluster of servers to optimize resource utilization,
  maximize throughput, fault tolerance and remove bottleneck on one server
- Act as middle man proxies (not like dns servers which tell where to go)
- For security load balancers use private IPs to communicate with servers, i.e. user never talks to server directly
- Process:
    1. Request Arrives
    2. Health checks servers (using heartbeats); If server fails heartbeat it is removed from the rotation
    3. Based on algo chooses best one
    4. Forwards to said server
    5. Once response received sends back to client
- Session Persistence (Sticky Session):  If configured, ensures all requests from same user go to same backend
  server to maintain state
- **Routing Algorithms**: Round Robin, Least Connections; i.e. Server with least active sessions, IP Hash: Hash user's
  ip to
  reliably route to same ,Least Response Time, Weights: Assign weight to server with higher capacity (  RAM/compute)
  giving more requests to more weight
- Load balancers operate mainly at Layer 4 (TCP/UDP, IP/port-based routing) or Layer 7 (HTTP-aware routing using
  headers, cookies, URLs, etc.).
- Note: Proxy vs reverse proxy:
    1. Forward Proxy: Sits in front of the clients, requests to any website goes through proxy first i.e. Handles
       outbound requests for either anonymity by masking traffic or block access to certain sites especially
       in companies
    2. Reverse Proxy: Sits in front of multiple servers taking requests and routes to appropriate backend server.
       Clients do not know which specific backend server handle their request

### 3. API Gateway:

- Acts as single entry point ( reverse proxy) for defined set of microservices handling north-south traffic i.e. client
  to service
- Core Technical Functions:
    - Request Routing: Maintains a routing table (often integrated with a **Service Registry** like Consul or Eureka)
      and matches and sends requests to specific services
    - Protocol Translation: External protocol could be internet safe, internal could be performance oriented for
      example: Convert REST to gRPC
    - Security & Auth: Validate keys and JWTs at a common gateway before reaching services
    - Others: Rate Limiting, Load balancing, Circuit Breaker (If a service is failing can stop calls to it to prevent
      further overwhelming)

### 3. Service Mesh:

- Dedicated infra layer for handling calls in distributed microservice architecture; Manages service-to-service (
  east-west) communication
- Abstracts the networking logic—such as service discovery, load balancing, encryption, and observability—away from
  the application code and into a decentralized data plane
- Components:
    - Data Plane: Consists of lightweight network proxies (commonly referred to as Sidecars, e.g., Envoy) deployed
      alongside
      each service instance containing routing, logging logic. Gets it's config from control plane which it then caches
    - Control Plane: Central management component: Injects config into data plane which is then used at data plane. This
      way it doesn't intercept calls but lets data plane implement the rules it injects

### 4. CDN

- Geographically dispersed servers used to deliver static contentt that cache static content like images videos css js,
  they are critical for reducing latency, offloading traffic from origin servers, and mitigating DDoS attacks.
- **Architecture**: Consist of Origin Server, Edge Servers which are strategically located data centers to cache content
  close to users or Reverse Proxy Servers: kind of edge servers, intercept call before it reaches origin
- **Routing Algos**:
    - Anycast Routing: Multiple servers share some IP, when user makes request routes to the closest node based on BGP
    - Latency-Based DNS Routing: The CDN’s DNS server resolves to server with the lowest latency to user's ISP
- **Push Vs Pull CDN**
    - Push: Origin server pushes content to CDN explicitly, does not expire on max age
    - Pull: Lazy operation, caches when user requests file based on headers. Pull Cdn is **dynamic caching** and uses
      the **cache control headers**. (Push doesn't)
- **Dynamic Caching**: If on first try the file doesn't exist on cdn, cdn fetches from origin server and caches to
  return it on second request for the same
- Cache-control headers: `Cache-Control`,`max-age`(tells browser to cache for how long),
  `s-maxage`: (s:shared tells CDN to keep file for how long),`public` vs `private` (Private i.e. only for user's
  browser, public for all), `no-cache`: don't cache it
- ETag Validation: If file hasn't changed on server just compare hash before discarding from CDN  
  **Key Considerations**:
- Run by 3rd Party: Charged for data transfer in and out of CDN, do not cache infrequent use items
- Set appropriate cache expiry to reduce refetching, but still be fresh
- Fallback: CDNs can fail, clients should have ability to connect to origin if they do

### 5. Rate Limiter:

- //todo Definition
- Hard vs soft rate limiting.
    - Hard: The number of requests cannot exceed the threshold.
    - Soft: Requests can exceed the threshold for a short period.
- Algorithms:
    - Token bucket
        - Each request uses one token in bucket, overflows(drops) when limit reached
        - Params:
            - Bucket Size
            - Refill Rate: i.e. how many tokens added back per second
    - Leaking bucket
        - Similar to token but requests are taken from bucket and queued (FIFO) at a fixed rate (as opposed to as
          required)
    - Fixed window counter
        - Timeline is divided into fixed segments
        - Only processes n number of request in that segment rest are dropped
        - For next request need to wait for next window
        - 🔴 User can double their quota for a bit by targeting edge of two windows (half in each)
    - Sliding window log
        - Uses a sliding window by caching timestamps of requests and removing those older than allowed period (when
          next comes in)
        - Fixes doubling of quota
    - Sliding window counter
- DB used for keeping track:
    - high speed cache i.e. Redis
- Error returned to client:
    - Return error code 429 on exceeding rate limit
    - Returns headers to client to give them info
    - X-Ratelimit-Limit
    - X-Ratelimit-Remaining
    - X-Ratelimit-Retry-After
- Distributed Architecture:
    - i.e. multiple rate limiters exist, thus rate limits need to be consistent
    - Solutions:
    - Sticky session
    - Shared Redis Cache

### 7. Base 64 Encoding

Way of representing binary data using only ordinary text characters by changing them from bytes(0-255) to base 64.
**Base64 is encoding, not encryption.**  
Does this by grouping the bits into 6-bit chunks instead of 8-bit chunks, thus making each 6 bit mappable to 64.
`01000011 01100001 01110100` -> `010000 110110 000101 110100`

### 8. Base 62 Encoding

Base62 encoding is similar in spirit to Base64: it converts data into a string using a fixed set of characters using
base of 62 only using (lowercase + uppercase + numbers 26+26+10 = **62**).   
The absence of +, /, and = makes Base62 particularly convenient for things like URL-safe identifiers compacting integers
very well  
``12345``->``3D7``

- Note: Base64 is generally designed to encode arbitrary binary data, Base62 is often used to encode integers/IDs into
  compact strings which are url safe often used in **URL shortener**

### 9. Hash Functions

A hash function maps arbitrary-sized data to a fixed-size string or numerical value called hash or digest *
*deterministically**.  
Uses: Data partitioning & routing (by hashing to same cluster), Hash table O(1) Lookup, Integrity & Deduplication (MD5
comparison), probabilistic checks (bloom filters)  
A **cryptographic hash function** is designed so that an attacker should have a very hard time finding relationships
between inputs and hashes.  
A **non-cryptographic hash function** is usually designed for speed and practical data structures, rather than resisting
attackers.

| **Category**                                                                    | **Algorithm / Function**   | **Best Used For**                                                                    | **Primary Traits**                                                                                                                                              |
|---------------------------------------------------------------------------------|----------------------------|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Non-Cryptographic**  <br>       (Prioritize extreme speed & low CPU overhead) | **MurmurHash (v2 / v3)**   | High-performance hash maps, Bloom Filters, Cassandra / Solr partitioning             | Fast execution, uniform distribution, non-cryptographic                                                                                                         |
|                                                                                 | **xxHash**                 | In-memory engines (Redis, RocksDB), fast checksums, network packet hashing           | Extremely fast; optimized for modern CPUs                                                                                                                       |
|                                                                                 | **CityHash / FarmHash**    | Large-scale string hashing, search indexes, distributed systems                      | Optimized for short/medium strings and modern hardware                                                                                                          |
| **Cryptographic / Legacy**                                                      | **MD5**                    | Legacy checksums, non-security file identification, compatibility with older systems | 128-bit output, very fast, **cryptographically broken due to collision attacks**; should not be used for passwords, signatures, or security-sensitive integrity |
| **Cryptographic**                                                               | **SHA-256 (SHA-2 Family)** | HMAC auth, API signatures, blockchain, TLS/SSL certificates                          | Strong collision resistance, standardized, hardware-accelerated on many CPUs                                                                                    |
| **Cryptographic**                                                               | **BLAKE3**                 | File checksums, object-storage deduplication, modern secure pipelines                | Very fast, parallelizable, modern cryptographic design                                                                                                          |
| **Password Hashing**                                                            | **bcrypt / Argon2**        | User password hashing and verification                                               | Intentionally slow; designed to resist brute-force and GPU attacks                                                                                              |

### 10. Unique ID Generation

### UUID (Universally Unique Identifier)

Generates 128 bits using pseudo-random bytes. 🟢 Simple Stateless but 🔴Non-sortable

### Twitter Snowflake

Generates 64-bit integer IDs optimized for distributed systems without cross-node coordination.
Contains Millisecond timestamp relative to a custom epoch + Machine/Worker ID (upto 1024) + Sequence number
🟢 Time ordered and high throughput 🔴But incorrect clock sync can cause duplicates

### ULID (Universally Unique Lexicographically Sortable Identifier)

### NanoID

### 11. WebHooks

An automated HTTP callback that sends real-time data from one application to another whenever a specific event occurs.
Unlike traditional APIs where you must repeatedly query (poll) a server for updates, webhooks automatically push data as
soon as an event happens.  
### Process:
1. Registration: You provide a destination URL (endpoint) on your server to the source provider
2. Event Triggers: An event occurs in the source system
3. Payload Delivery: Source system calls your server (simply source server calls your server)
4. Action: Your server receives the HTTP POST request and returns a 200 OK

### 6. Performance Metrics

Describing Performance:

1. Latency
    - Latency is the time it takes for a single request to travel from the source to the destination and return a
      response.
    - If you click a button on a website, and it takes $200\text{ ms}$ for the page to load, the latency
      is $200\text{ ms}$.
    - Goal: Lower is better (low latency means a faster response).
    - For most response times we use percentiles over average, p95, p99, p999 being common describing % users
      time taken avg
    - Often defined clearly in SLAs (Service Level Agreements) and must be met by companies providing products
    - Note:
        - Important to measure response times on client-side than time taken by server to process
        - Request might sit waiting in queue (head of line blocking)
2. Throughput (Capacity)
    - Throughput is the number of actions, requests, or data units a system can process within a specific timeframe.
    - It measures volume or capacity.
    - Unit of measurement: Requests per second ($RPS$), queries per second ($QPS$), or bits per second ($bps$).

### 7. Cap Theorem

[Read Here](../1_DBMS/Basics.md#10-cap-theorem)

### 8. Consistency

[Read Here](../1_DBMS/Basics.md#11-consistency)

### 9. In-memory data store (Caching):

- DBMS that relies primarily on main memory (RAM) for data storage
    - Opposed to traditional mediums which store in HDD/SSD

## 1. Technologies: Redis vs. Memcached

While both are premier in-memory engines, their underlying architectures and capabilities differ significantly:

- ### Redis (Remote Dictionary Server)
    - Data Structures: Supports more than simple key-value pairs including Strings, Hashes, Lists, Sets, Sorted Sets etc
    - Persistence: Offers durability through **RDB** (Redis Database - point-in-time snapshots) and **AOF** (Append Only
      File - log of every write operation).
    - High Availability: Built-in replication, Redis Sentinel (automatic failover), and Redis Cluster (horizontal
      sharding).

- ### Memcached
    - Data Structures: Strictly a pure key-value store, no complex datatypes
    - Memory Allocation: Utilizes a **Slab Allocator** to combat memory fragmentation. It allocates large chunks of
      memory (Slabs) pre-carved into smaller slots (Slab Classes) of fixed sizes, reducing the overhead of continuous
      dynamic memory allocation (`malloc`/`free`).
    - Persistence & Topology: Restarting process wipes the dataset. Does not natively support replication or clustering

---

## 2. Caching Strategies

- ### Cache-Aside (Lazy Loading)

    - Process:
        1. The application queries the cache.
        2. **Cache Hit:** Data is returned directly to the client.
        3. **Cache Miss:**App queries DB, writes returned data to cache for future requests, and returns to client.

      -🟢 Resilient to cache failures; optimal memory usage (only requested data is cached).
      -🔴 Cache miss penalty on the first request;
      -🔴 Risk of stale data if db updated in background

        - **Cache Stampede (Thundering Herd Problem):** A systemic failure that occurs when a highly popular cache key
          expires,
          causing massive numbers of concurrent application threads to simultaneously hit the backing database.

- ### Write-Through

    - The cache acts as the primary data interface.
    - When updated, app writes to cache which writes synchronously to DB

      -🟢 Data consistency between cache and database guaranteed
      -🔴 High write latency: every write requires a synchronous dual-write to memory and disk.

- ### Write-Back (Write-Behind)

    - App writes data only to cache which acknowledges
    - Cache asynchronously flushes these updates to the database in batches or after a delay.
    - 🟢 Extremely low write latency and high write throughput, shielding the database from write spikes.
    - 🔴 Risk of data loss. If in-memory layer crashes flush completes, updates are permanently lost.

---

- ## 3. Cache Eviction Policies
    - When RAM reaches its capacity limit, the engine must evict existing keys to accommodate incoming data
    - Policies:
    - ### LRU (Least Recently Used)
        - Tracks the *age* of access. Evicts keys not used for longest time
            - Note: Implementation: Often done in Redis by sampling a small pool of keys and evicting from them instead
              of heavy
              global list of keys

    - ### LFU (Least Frequently Used)
        - Tracks *frequency* of access.
            - Evicts keys with the lowest counter of hits, regardless of how recently they were touched.
            - **Implementation:** Redis implements this using a logarithmic counter per key alongside a decay time
              interval.
                - Counter decays automatically if key isn't requested, evicting old, historically popular keys

### 14. 