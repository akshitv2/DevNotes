---
parent: System Design
layout: default
title: Components
---

## Open Systems Interconnection Model

- conceptual framework developed by the International Organization for Standardization (ISO) in 1984
- Data propagation flows downward from Layer 7 to Layer 1 at the transmitting node, and upward from Layer 1 to Layer 7
  at the receiving node.

## OSI Model Layers

### 7. Application Layer

- Interface between the software application and the network. (HTTP, FTP, SMTP).
- **Protocols**: HTTP, FTP, SMTP, DNS
- Note: HTTP is a stateless communication protocol. It doesn't actually know how to handle it's own transportation just
  what it wants to execute
    - e.g.
        - ```http request
          GET /index.html HTTP/1.1
          Host: www.example.com
          User-Agent: Mozilla/5.0 (Windows NT 10.0)
          Accept: text/html
      ```

### 6. Presentation Layer

- Data formatting, encryption, and compression.
- Manages syntax and semantics. It ensures that data is in a usable format for the application layer.
- Translates formats into common formats, like XML, json, ASN.1 (Abstract Syntax Notation One) etc.
- Data serialization, encryption/decryption (e.g., TLS/SSL), and compression.
- Note: Encryption and compression might sound like add ons than needed translation, are placed here due to constraints
  of model
    - i.e.
        - Compression must happen after the application creates the data, but before the Transport Layer chops it into
          segments.
        - Encryption must happen after the data is formatted and compressed, but before it is handed to the network
          layers. (lower levels contain routing information needed to send data over which can't be encrypted)
    - This difference occurs because real-world internet does not strictly use the OSI model; it uses the [**TCP/IP
      model**](#TCPIP-MODEL).

### 5. Session Layer

- Establishes, manages, terminates, and synchronizes dialogues between applications on local and remote hosts.
- **Protocols**: NetBIOS, RPC, PPTP
- It handles maintenance and teardown of connections
    - It creates the connection between two applications, ensures it remains stable while data is being exchanged, and
      cleanly closes the connection when the communication ends so resources aren't wasted.
- Uses one of three modes
    - Simplex: One-way communication only (e.g., a radio broadcast).
    - Half-Duplex: Two-way communication, but only one side can talk at a time
    - Full-Duplex: Simultaneous two-way communication
- Note: The functions in reality are arbitrary. The OSI model is an academic framework. The internet runs on the[*
  *TCP/IP model**](#TCPIP-MODEL). In the TCP/IP model, Layers 5 (
  Session), 6 (Presentation), and 7 (Application) are collapsed into a single Application Layer.

### 4. Transport Layer

- Central hinge of the OSI mode bridging gap between hardware and software layers
- Protocols: TCP, UDP.
- Handles segmentation/reassembly of data streams

### 3. Network Layer

- Determines the optimal physical path for data routing across networks based on logical addressing.
- **Protocols**: IPv4, IPv6, ICMP, OSPF, BGP.

### 2. Data Link Layer

- Function: Provides node-to-node data transfer directly between two connected nodes on the same network segment.
- **Protocols**: Ethernet (802.3), Wi-Fi (802.11), PPP, ARP.

### 1. Physical Layer

- Function: Transmits and receives unstructured raw bitstreams over a physical medium.
- Key Technologies: Copper cables (Cat6), Fiber optics, RF (Radio Frequency), Hubs, Repeaters.
- Defines the electrical, mechanical, and functional specifications for the physical links

--- 

- The OSI model is a theoretical 7-layer framework used for teaching
- Data Encapsulation  
  As data moves down from Layer 7 to Layer 1, each layer adds a header (and sometimes a trailer) containing control
  information. This process is called encapsulation.
- When the data reaches the destination, it moves up from Layer 1 to Layer 7, and each layer removes its corresponding
  header; this is called decapsulation.

## TCP/IP Model

- Actual, real-world protocol suite that powers the modern internet.
- Streamlined 4-layer model designed for practical implementation

### 1. Application Layer

- **Function**: Defines the protocols and interface methods used by hosts in a communications network to interact with
  user applications.
- It operates at the very top of the stack, handling high-level protocols, representation, encoding, and dialog control.
  When an application wants to send data over the network, it hands it down to this layer.
- Protocols: HTTP/HTTPS (web browsing), SMTP/IMAP (email), FTP (file transfer), DNS (domain resolution), and SSH (secure
  remote access).
- Also contains TLS and compression since it's something applications perform not OS

### 2. Transport Layer

- Function: Manages host-to-host communication, flow control, error detection, and data segmentation.
- Protocols: * TCP (Transmission Control Protocol), UDP (User Datagram Protocol)

### 3. Internet Layer

- Function: Responsible for addressing, packaging, and routing data across multiple independent networks.
- **Protocols**: IP (IPv4 and IPv6), ICMP

### 4. Network Access Layer (Link Layer)

- Defines how data is physically transmitted through the network media (wires, fiber optics, or radio waves).

### TCP vs UDP

| Feature         | TCP (Transmission Control Protocol)              | UDP (User Datagram Protocol)               |
|-----------------|--------------------------------------------------|--------------------------------------------|
| Connection Type | Connection-oriented (requires a handshake).      | Connectionless (just sends data).          |
| Reliability     | Guaranteed delivery. Resends lost data.          | Best-effort delivery. Lost data is gone.   |
| Data Order      | Guarantees data arrives in the correct sequence. | Data can arrive out of order.              |
| Speed           | Slower (due to tracking and error checking).     | Extremely fast (no overhead).              |
| Data Unit       | Segments                                         | Datagrams                                  |
| Use Cases       | Web browsing (HTTP), Email, File Transfers.      | Video streaming, Online gaming, DNS, VoIP. |

## Core Architectural Components

1. ### DNS
    - Domain Name System (Base-level DNS) distributed hierarchical database that translates human readable url into
      machine IP address
    - Each layer in hierarchy isn't a single server but a layer full of thousand of servers
    - **Hierarchy**:
        - **Root Nameservers** (.):
            - Top of hierarchy, 13 worldwide, link to TLD
            - Our device routes to the closest one (in terms of network hops)
            - All contain same data, 13 Because of distributions between orgs for stability and redundancy
        - **Top Level Domain (TLD) Nameservers**:
            - Managed by registries (for e.g. only one tld for .com)
            - Maintain records for all domains under their extension, point to the Authoritative server
        - **Authoritative Server**:
            - Hold the actual DNS records mapping the domain to the IP address
    - Resolution Flow:
        - The client (browser/OS) asks the **Recursive Resolver** e.g. 8.8.8.8
        - Checks cache first else polls the hierarchy step by step
    - Note: When we set DNS on our device manually we are choosing to use a different resolver than our ISPs
        - If you use a poorly distributed IP resolver it can break all geo-routing and cdn optimization by routing you
          to IPs far away
    - **Geographical / Latency-Based Routing**:
        - Smart DNS providers look at the incoming resolver's IP and return record pointing to the data center
          physically closest to user.
2. ### Load Balancer:
    - Acts as a reverse proxy to distribute incoming network or application traffic across a cluster of servers
    - To optimize resource utilization, maximize throughput, reduce latency, and ensure fault tolerance by preventing
      any single server from becoming a bottleneck.
    - Act as middle man proxies (not like dns servers which tell where to go)
    - For security load balancers use private IPs to communicate with servers, i.e. user never talks to server directly
    - Process:
        1. Request Arrives
        2. Health checks servers (using heartbeats)
            - If server fails heartbeat it is removed from the rotation
        3. Based on algo chooses best one
        4. Forwards to said server
        5. Once response received sends back to client
    - Session Persistence (Sticky Session):
        - If configured, ensures all requests from same user go to same backend server to maintain state
    - Common Routing Algorithms:
        - Round Robin
        - Least Connections; i.e. Server with the least active sessions
        - IP Hash:
            - Hash user's ip to reliably route to same
        - Least Response Time
        - Weighted Algorithms:
            - Assign weight to server with higher capacity (RAM/compute)
            - More weight = more requests
    - OSI Model Classification  
      Load balancers are generally categorized by the layer at which they operate:
        - Layer 4 (L4):
            - Operates at the Transport layer (TCP/UDP).
            - Makes routing decisions based on IP addresses and port numbers
            - Doesn't actually inspect the data
        - Layer 7 (L7):
            - Operates at the Application layer
            - Can inspect HTTP headers, cookies, and URLs to make "content-aware" routing decisions
    - Note:
        - DNS based routing:
            - Load balancing can also be done at dns level by routing users to different servers
            - The user connects directly to the server's IP address.

- Note: Proxy vs reverse proxy:
    1. Forward Proxy:
        - sits in front of the clients, requests to any website goes through proxy first
        - Handles outbound requests for either anonymity by masking traffic or block access to certain sites especially
          in companies
    2. Reverse Proxy:
        - Sits in front of multiple servers
        - When user requests a website request goes to reverse proxy which routes to appropriate backend server
        - Provides anonymity:  Clients do not know which specific backend server handled their request; they only
          interact
          with
          the reverse proxy.
        - Also used for load balancing, authentication and caching

### 2. API Gateway:

- Acts as single entry point for defined set of microservices
- Acts as reverse proxy to applications
- Operates primarily at layer 7 of OSI model
- Handles north south traffic i.e. client to service
- Core Technical Functions:
    - Request Routing:
        - Matches and sends to specific services
        - Maintains a routing table (often integrated with a **Service Registry** like Consul or Eureka).
        - Parses uri of incoming requests and proxies to relevant service
    - Protocol Translation:
        - External protocol could be internet safe, internal could be performance oriented
        - for example: Convert REST to gRPC
    - Security & Auth:
        - Validate keys and JWTs at a common gateway before reaching services
    - Rate limiter
        - Commonly using algorithms like the Token Bucket or Leaky Bucket
            - Token Bucket Algo:
                - R tokens added to bucket every second
                - When packet of size n arrives processed by removing n tokens, else queued or dropped
                - Allows bursts
            - Leaky Bucket Algo:
                - Empties tokens at rate r
                - Only allows packets within a certain size i.e. blocks bursts
    - Load balancing
    - Circuit Breaker:
        - If a service is failing can stop calls to it to prevent further overwhelming

### 3. Service Mesh:

- Dedicated infra layer for handling calls in distributed microservice architecture
- Manages service-to-service (east-west) communication
- Abstracts the networking logic—such as service discovery, load balancing, encryption, and observability—away from
  the application code and into a decentralized data plane
- Components:
    - Data Plane:
        - Consists of lightweight network proxies (commonly referred to as Sidecars, e.g., Envoy) deployed alongside
          each service instance.
        - Contains routing, logging logic. Gets it's config from control plane which it then caches
    - Control Plane:
        - Central management component
        - Injects config into data plane which is then used at data plane
        - Doesn't intercept calls but lets data plane implement the rules it injects

### 4. CDN

- Geographically dispersed servers used to deliver static content
- Cache static content like images videos css js
- critical for reducing latency, offloading traffic from origin servers, and mitigating DDoS attacks.
- **Architecture**:
    - Origin Server: original serving server
    - Edge Servers: Strategically located data centers, cache content close to users.
    - Reverse Proxy Servers: edge servers can act as reverse proxy, intercept call before it reaches origin
- **Routing**:
    - Anycast Routing: Multiple servers share some IP, when user makes request routes to closest node based on BGP
    - Latency-Based DNS Routing: The CDN’s DNS server resolves to server with lowest latency to user's ISP
- **Push Vs Pull CDN**
    - Push: Origin server pushes content to CDN explicitly, does not expire on max age
    - Pull: Lazy operation, caches when user requests file based on headers
        - Pull Cdn is dynamic caching and uses the cache control headers. (Push doesn't)
- **Dynamic Caching**
    - Process:
        - On first try the file doesn't exist on cdn, request goes to CDN but cdn requests Server
        - Fetches from origin server first time then caches based on header
        - On second try by user request
- ### Configuration:
    - Controlled using cache-control headers
        - `Cache-Control`:
        - `max-age`: This one is for browsers to cache file for how many seconds
        - `s-maxage`: (s:shared) tells CDN to keep file for max X seconds
        - `public` vs `private`: Private i.e. only for user's browser, public for all
        - `no-cache`: don't cache it
    - ETag Validation: If file hasn't changed on server just compare hash before discarding from CDN
- ### Considerations:
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

[Read Here](../DBMS/Basics.md#10-cap-theorem)

### 8. Consistency

[Read Here](../DBMS/Basics.md#11-consistency)

### 9. Caching
