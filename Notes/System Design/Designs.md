---
parent: System Design
layout: default
title: Designs & Arch
---

## 1. ## Vertical vs Horizontal scaling:

- ### Vertical or Scale Up:
    - Upgrade to more powerful machines with more compute/RAM
    - 🔴Has diminishing returns in terms of how far you can scale up
    - 🔴Comes with hard limit either in terms of compute or IO buses or ports
    - 🟢Comes with the benefit of not rewriting and not needing to parallel your code
    - 🔴Does not have failover or redundancy if main server goes down
- ### Horizontal Scaling or Scale Out:
    - Add more machines to execute in parallel
    - 🔴Requires your code to be executed parallel
    - 🔴Requires load balancing too
    - 🟢Improved Availability and Reliability since if one server goes down other can serve
    - 🟢Virtually Unlimited Growth
    - 🟢More cost-efficient to buy cheaper smaller servers than one giant one and add incrementally

## 2. Database Replication:

- ![img_1.png](../Books/img_1.png)
- Usually done with a master slave relationship (often called Primary Replica or Leader Follower)
- Write operations are only supported by Master node
- Slave get copies of master DB and only supports read (when enabled)
- Most applications are read heavy so having limited master works
- 🟢Most applications are read heavy so higher availability from slave nodes
- 🟢More Reliable since loss of one db server doesn't mean loss of data

TBC

## 3. Availability Patterns

Availability Patterns are architectural strategies designed to maximize system uptime and guarantee that services remain
accessible, even during infrastructure, network, or hardware degradation.  
Focus heavily on reducing the Mean Time to Repair ($MTTR$) and eliminating Single Points of Failure ($SPOF$)

### Failover Strategies

Failover is the process of transitioning service traffic from a compromised or failing system component to a redundant,
healthy component to mitigate operational disruption.

### Active-Passive Configuration

- One node (the **Active** node) actively processes all operational workloads and incoming requests.
- One or more secondary nodes (the **Passive** nodes) remain idle, acting as backups.
- **Heartbeat Mechanisms:**
    - Active and passive nodes continuously exchange small "keep-alive" network packets called heartbeats.
    - If passive node detects a multi-packet dropout, it assumes a primary node outage.
- **Promotion & Traffic Steering:**
    - Upon detecting a fault, standby node is promoted to primary status,
    - Traffic management component (such as an API Gateway, Load Balancer, or DNS route policy) change traffic steering
      to point to the newly promoted node.
- 🟢Provide simpler data state consistency since only one node accepts writes at any given time.
- 🔴Suffer from inefficient resource utilization—since backup infrastructure sits idle

### Active-Active Configuration

- Two or more processing nodes or distinct data centers concurrently service live client transactions
- Split incoming infrastructure loads.
- **Load Distribution:** Intelligent load balancer distributes traffic across active nodes using routing algos
- **Fault Masking:** If a node encounters issues, load balancer detects failure via real-time health checks
    - Removes the failed node from the routing pool.
- 🟢 Provides seamless fault masking and near-zero recovery time
- 🔴 Exponentially increases architectural complexity, demanding distributed concurrency controls

### 2. Consistent Hashing

- hashing technique used to distribute data across a cluster of servers minimizing rehashing when number of server
  changes
- maps both the servers and the keys to a conceptual circular ring
- Hash Ring: hash function maps its output to a fixed range (e.g., $0$ to $2^{32}-1$), which is visualized as a closed
  circle.
- Server Placement: Servers are hashed based on their IP address or name and placed around ring
- Key Assignment: To find which server stores a key, the key is hashed to find its position on the ring
    - moves clockwise from that position until it encounters a server
- If a server leaves/fails: Keys are moved in that server to next one clockwise
- If a server is added: It only takes a fraction of the keys from its immediate counter-clockwise neighbor.
  **Virtual Nodes:**
    - To prevent imbalance each server is hashed multiple times around the circle
    - i.e. you encounter ServerA-Hash1, ServerB-Hash1, ServerA-Hash2
- Used in:
    - Distributed Caching: In Memcached, Distributed NoSQL Databases
    - Load Balancing: HAProxy and NGINX utilize consistent hashing for HTTP load balancing for stickiness

### 3. Rate Limiting Algorithms

- **Token Bucket Algo**:
    - A bucket has a maximum capacity of $B$ tokens.
    - R tokens added to bucket every second
    - When packet of size n arrives processed by removing n tokens, else queued or dropped
    - Allows bursts of Traffic
- **Leaky Bucket Algo**:
    - Bucket leaks from bottom i.e. processes first arriving first
    - holds a maximum queue size. If the queue is full, new requests overflow (are dropped).
    - Processed at a continuous, fixed rate, regardless of when they enter.
    - 🟢Guarantees a stable, consistent output rate, preventing traffic spikes
    - 🔴Burst of traffic can fill the bucket quickly, causing subsequent valid requests to be delayed or dropped
- **Fixed Window Counter**
    - divides time into static windows and tracks request counts within each window
    - Each window has a counter. Every incoming request increments the counter for the current window.
    - If the counter exceeds the threshold, requests are rejected until the next window starts and the counter resets.
    - 🔴"Boundary Problem." A burst of traffic can arrive at the end of one window and the beginning of the next doubling
      requests
- **Sliding Window Counter**
    - This algorithm resolves the boundary problem of the Fixed Window approach by combining a current window count with
      a percentage of the previous window's count.
    - Mitigates the boundary burst problem while remaining relatively memory-efficient
    - assumes traffic in the previous window was evenly distributed

- **Exponential Backoff with Jitter**
    - Problem: If a service goes down, hundreds of thousands of client apps will instantly retry. If they all retry at
      exactly 1s, 2s, and 4s, they will repeatedly crash the recovering server.
    - Solution: Clients wait exponentially longer between retries, plus they add a random delay (Jitter).