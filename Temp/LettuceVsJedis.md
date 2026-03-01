---
parent: Scratch book
nav_order: 4
layout: default
---

# Lettuce vs Jedis

| Feature                    | Lettuce                                                | Jedis                                                             |
|----------------------------|--------------------------------------------------------|-------------------------------------------------------------------|
| Architecture               | Netty Based, full non blocking                         | Blocking/Synchronous                                              |
| ThreadSafety               | Yes, Shared connection                                 | Yes when used with pooling                                        |
| API Options                | Sync, Async, Reactive                                  | Only Synchronous                                                  |
| Cluster topology detection | Automatic + adaptive + periodic                        | Only Synchronous                                                  |
| Read From Replica Support  | Advanced                                               | Not by default                                                    |
| Connection sharing         | Single thread multi connection                         | Simple sync                                                       |
| Speed                      | Fatser when high concurrency, reuse of thread required | Lightweight, faster in single thread single connection comparison |
| First connection speed     | Much higher                                            | Negligible                                                        |


Both know how to follow `MOVED` response to the new node.
Both know to store which node slot has been moved to.
But jedis discovers one by one for each slot only (till periodic refresh).

- Differences
    1. Topology Detection
        - Lettuce:
            - RefreshTopology
            - Need to enable in `ClusterTopologyRefreshOptions`
            - Async so does maintenance in background without stopping traffic
            - Uses **multiplexing** i.e. single thread multiple connections supported
            - Supports adaptive refresh:
                - On getting `MOVED` for a `GET user:123` reroutes to specifiic node to get value
                - Lettuce topology watcher sees `MOVED` and triggers a refresh
                - Refresh is launched in background non-blocking, calls `CLUSTER SLOTS` on any available node
                - Silently swaps old 16,384 Map with new one
            - Supports Periodic Refresh
            - Topology view centralized, so one refresh updates for all
        - Jedis
            - if Jedis received `MOVED` for one slot, updates that in its map only while locking others
            - Prevents a discovery request storm while taking hit on speed
            - Updates in `JedisClusterInfoCache`
            - Support Periodic Refresh

          Note: JedisPool is for one single redis instance, jedisCluster for redis cluster mode with topology
    2. Read from Replica:
       - Lettuce:
        - just requires flipping a config
        - Options: You can set the policy to:
          - MASTER: Default.
          - REPLICA_PREFERRED: Read from replicas.
          - NEAREST: Read from the node with the lowest latency.
          - MASTER_PREFERRED: Read from master, but hit the replica if the master is down.
        - Jedis:
          - Doesn't support by default read/write split, needs custom scripting
          - Cause: Jedis is a very thin wrapper around redis commands
          - 