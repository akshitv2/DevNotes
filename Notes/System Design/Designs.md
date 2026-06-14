---
parent: System Design
layout: default
title: Designs & Arch
---

### 1. ## Vertical vs Horizontal scaling:

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

### 2. Database Replication:

- ![img_1.png](../Books/img_1.png)
- Usually done with a master slave relationship (often called Primary Replica or Leader Follower)
- Write operations are only supported by Master node
- Slave get copies of master DB and only supports read (when enabled)
- Most applications are read heavy so having limited master works
- 🟢Most applications are read heavy so higher availability from slave nodes
- 🟢More Reliable since loss of one db server doesn't mean loss of data

TBC

### 3. Availability Patterns

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
