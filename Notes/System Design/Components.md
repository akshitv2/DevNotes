---
parent: System Design
layout: default
title: Components
---

## Open Systems Interconnection Model

- conceptual framework developed by the International Organization for Standardization (ISO) in 1984

### OSI Model Layers

| Layer | Name         | Function                                                                   |
|-------|--------------|----------------------------------------------------------------------------|
| 7     | Application  | Direct interaction with software applications (HTTP, FTP, SMTP).           |
| 6     | Presentation | Data translation, encryption, and compression (SSL, SSH, JPEG).            |
| 5     | Session      | Manages connections (sessions) between applications (NetBIOS, SAP).        |
| 4     | Transport    | End-to-end communication, flow control, and error recovery (TCP, UDP).     |
| 3     | Network      | Routing and forwarding data packets between different networks (IP, ICMP). |
| 2     | Data Link    | Node-to-node data transfer and MAC addressing (Ethernet, Switches).        |
| 1     | Physical     | Physical transmission of raw bitstreams over a medium (Cables, Hubs).      |

- Data Encapsulation  
  As data moves down from Layer 7 to Layer 1, each layer adds a header (and sometimes a trailer) containing control
  information. This process is called encapsulation.
- When the data reaches the destination, it moves up from Layer 1 to Layer 7, and each layer removes its corresponding
  header; this is called decapsulation.

## Core Architectural Components

1. ### Load Balancer:
    - Acts as a reverse proxy to distribute incoming network or application traffic across a cluster of servers
    - to optimize resource utilization, maximize throughput, reduce latency, and ensure fault tolerance by preventing
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

Note: Proxy vs reverse proxy:

1. Forward Proxy:
    - sits in front of the clients, requests to any website goes through proxy first
    - Handles outbound requests for either anonymity by masking traffic or block access to certain sites especially
      in companies
2. Reverse Proxy:
    - Sits in front of multiple servers
    - When user requests a website request goes to reverse proxy which routes to appropriate backend server
    - Provides anonymity:  Clients do not know which specific backend server handled their request; they only interact
      with
      the reverse proxy.
    - Also used for load balancing, authentication and caching

### 2. API Gateway:

- Acts as entry point for defined set of microservices
- Acts as reverse proxy to applications
- Core Technical Functions:
    - Request Routing:
        - Matches and sends to specific services
    - Protocol Translation:
        - for example: Convert REST to gRPC
    - Security & Auth:
        - Validate keys and JWTs at a common gateway before reaching services
    - Rate limiter
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
