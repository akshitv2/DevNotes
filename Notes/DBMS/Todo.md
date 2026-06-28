---
parent: DBMS
nav_order: 1
layout: default
title: Todo
---

1. 2 Phase Locking
2. Multi-Version Concurrency Control (MVCC)
3. ANSI SQL Isolation Levels

- Replication Topologies: The document outlines Leader-Follower, but completely misses Leaderless Replication (
  Dynamo-style, hints at quorum but doesn't explain how writes work without a single coordinator) and Multi-Leader
  Replication (along with collaborative editing conflict resolution).
- Write Paths (Caching Topologies): * Cache-aside, Write-through, Write-behind (Write-back).
- Database Migrations: How to execute zero-downtime database schema migrations in production (e.g., dual-writing,
  backfilling, cutting over).
  - Section 6 covers the structural types of indices well, but misses practical aspects frequently tested in coding and engineering rounds.

Clustered vs. Non-Clustered Indexes: How data physically sits on disk versus secondary index pointers.

Composite/Compound Indexes: * Left-Deep / Leftmost Prefix Rule: Why an index on (A, B, C) optimizes queries for WHERE A = 1 AND B = 2, but fails for WHERE B = 2.

Covering Indexes: Queries that can be satisfied entirely by looking at the index without fetching the actual row pages from disk.

Query Execution Plans: Basic understanding of terms like Seq Scan (Table Scan) vs. Index Scan vs. Index Only Scan.