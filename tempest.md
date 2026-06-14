## 1. Failover Strategies

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

---

## 2. Replication Strategies

Copies data state updates across multiple storage nodes to preserve data
redundancy and durability. Failover strategies rely heavily on underlying replication architectures.

### Synchronous Replication

In a synchronous replication scheme, when a client submits a data modification or write operation to the primary node,
the transaction is not committed locally until it has been successfully transmitted and acknowledged by the designated
replica nodes.

* **Guarantees:** It guarantees a Zero Data Loss threshold ($RPO = 0$). If the primary node undergoes a sudden
  catastrophic failure, the replica state is perfectly mirror-matched to the primary.
* **Downsides:** This design introduces significant write latency, as the total duration of the write operation is bound
  by the slowest network transaction between the nodes. Furthermore, if a replica node becomes unreachable, the primary
  node's write operations may stall or fail entirely, compromising write availability.

### Asynchronous Replication

In an asynchronous replication scheme, the primary database node executes and logs a transaction locally, returning an
immediate success acknowledgement to the client application before broadcasting the update to its replicas. Data packets
are then propagated downstream across the cluster out-of-band via background processes.

* **Guarantees:** This decouples transaction performance from network throughput, offering low-latency writes and
  shielding the primary node from network blips on the replica side.
* **Downsides:** It creates a window of "data lag" or replication delay. If the primary node fails completely before
  recent transaction logs are pushed downstream, those un-replicated commits are permanently lost during failover,
  resulting in an $RPO > 0$.

### Split-Brain Scenario & Quorum Consensus

A major hazard in active-passive and multi-node clusters is a **split-brain scenario**. This occurs when a network
partition cuts off communication between nodes, but leaves both nodes independently functional. Without a safeguard, a
passive standby node might assume the active node died and promote itself, while the original active node continues to
accept traffic. Both nodes then write conflicting data independently, corrupting the system state.

To prevent this, distributed systems employ **Quorum Consensus**. A cluster partition is only permitted to accept write
operations or execute a failover if it contains a strict majority of the total cluster nodes:

$$\text{Quorum Size} \ge \left\lfloor \frac{N}{2} \right\rfloor + 1$$

Where $N$ represents the total number of voting nodes within the entire cluster architecture. If a sub-partition cannot
establish a majority quorum, it automatically switches to a read-only or safe-stop mode, avoiding conflicting state
mutations.

---

## The Analogy: Airport Operations

To understand these patterns more intuitively, imagine managing the check-in desk operations at a high-volume
international airport terminal:

### The Active-Passive Analogy

Imagine the airport sets up two identical customer check-in desks side-by-side, but opens only **Desk A**. A single
attendant works at Desk A processing the long line of passengers, while **Desk B** sits completely dark and empty. The
attendant at Desk B sits in the back breakroom, constantly peeking through a window (the **Heartbeat**) to see if Desk
A's attendant passes out from exhaustion. If the attendant at Desk A suddenly faints, the attendant from the backroom
rushes out, boots up the computer at Desk B, and shouts to the crowd to change lines (**Failover**).

### The Active-Active Analogy

Instead of keeping a desk dark, the airport opens **both Desk A and Desk B simultaneously**. A queue manager standing at
the front of the line (**Load Balancer**) directs the first passenger to Desk A, the second passenger to Desk B, and
continues alternating. If the attendant at Desk A faints, the queue manager simply stops sending people to Desk A and
seamlessly directs the entire remaining line to Desk B. No time is wasted booting up systems; the operation continues
without pausing.

### The Replication Analogy

* **Synchronous Replication:** Imagine every time a desk attendant prints a boarding pass for a passenger, they are
  strictly forbidden from handing it to the passenger until a runner physically takes a carbon copy of that ticket,
  sprints over to a central filing cabinet, files it, and gives a thumbs-up. The passenger experiences a long wait at
  the counter, but the airport guarantees that the file cabinet is *always* perfectly up to date.
* **Asynchronous Replication:** The attendant hands the boarding pass to the passenger immediately, allowing them to
  proceed to their gate. The attendant throws the carbon copy into an "Outbox" basket on their desk. Every ten minutes,
  a runner clears the basket and takes the pile to the central filing cabinet. The passengers move quickly through the
  line, but if the desk suddenly catches fire, any unfiled copies sitting in the basket are destroyed forever.

---

## Closely Associated Topics

* **Load Balancing Algorithms:** The logical rules (such as layer-4 round-robin, weighted least-connections, or layer-7
  path routing) used to distribute inbound service traffic across an array of active system nodes.
* **Disaster Recovery Metrics (RTO and RPO):** Recovery Time Objective ($RTO$) dictates the maximum acceptable duration
  of system downtime before restoration, while Recovery Point Objective ($RPO$) specifies the maximum age of data loss a
  business can tolerate following an outage.
* **Distributed Consensus (Paxos & Raft):** Highly robust cryptographic and state-machine algorithms used to achieve
  cluster-wide agreement on active nodes, cluster leaders, and sequential data changes in a distributed network.
* **Health Checking and Circuit Breakers:** Automated software patterns that continuously probe system boundaries to
  detect downstream node degradation, systematically tripping open to drop traffic before a failure cascades.