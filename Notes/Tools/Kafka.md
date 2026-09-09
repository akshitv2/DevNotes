# Kafka

## 1. Kafka

Open stream data processing platform for processing real time data feeds.  
Consists of:

- Event (Message): A record of something, contains key timestamp value metadata
- Topic: Category to which events are published
    - Producers send messages to specific topics & Consumers subscribe to topics to read messages, every kafka event has
      a topic
- Partition: ordered, immutable sequence of events within a topic, divided into partitions for better scalability
    - Order is maintained within partition but not between partitions. e.g. Part 1: [A,C] Part 2:[B,D], then A-> C, B->D
      but A <> B (either)
    - Thus, it becomes important to publish related/dependant events to same partition (not only topic)
    - Partition can be chosen by hashing the key at broker or explicitly by producer
    - Doesn't use fcfs to remove single ordering bottleneck, instead have N different ordered event sets
- Producer: Client applications that write events to Kafka topics.
- Consumer: Client applications that read events from Kafka topics.
- Broker: A single Kafka server. A cluster consists of multiple brokers to handle replication and load balancing.
- Others:
    - Offset: Measure of how far a consumer group is in processing a partition
    - Partition Ext. :     partitions execute parallely and thus are real queues with individual offsets (since a global
      offset doesn't make any sense here)
    - GroupId: Unique string that identifies consumer group. Assigned to each consumer (if not explicitly done then
      assigns random). Kafka tracks the offset of the entire group for a topic (per partition) thus removing double
      processing within the group.
        - Note: Kafka divides partitions between groups for independence

Data is deleted during background cleanup tasks based on configurable retention policies (not immediately upon
consumption)

## Data Workflow:

1. Producer sends a message to a topic.
2. Kafka assigns it to a partition (via key hash, or round-robin if no key).
3. Message is appended to the partition log with an offset.
4. Consumers in a consumer group read messages, each partition consumed by only one consumer in that group at a time.
5. Kafka retains messages for a configured time (or size), regardless of whether they've been read.

## Delivery Guarantees

Kafka supports three semantics:

- At most once – message might be lost, never duplicated (low overhead).
- At least once – message never lost, but might be duplicated (default, most common).
- Exactly once – no loss, no duplication (uses idempotent producers + transactions; more overhead).

### Supported Functions:

1. Event Streaming (Publish-Subscribe Model): 1 to many publishing
2. Message Queue (Point-to-Point Processing): Kafka distributes messages among them, ensuring each message is processed
   only once.
3. Batch Processing: can also handle batch processing by loading events into it to be consumed in batches later

### Zookeeper

Helps manage kafka clusters, leader election, config management etc.
Note: Standalone coordination engine—it was not built strictly for Apache Kafka, though Kafka was historically its most
famous power user.
Note: Manages cluster metadata (older versions use ZooKeeper; newer Kafka uses built-in **KRaft** mode)