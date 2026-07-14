---
parent: DBMS
nav_order: 1
layout: default
title: RealWorld Implementations
---

1. Banks
   - Use Relational DBs which can be horizontally partitioned based on account number (or its surrogate key)
   - Transactions often sit with the Account Number to enable join
   - Often use Hot And Cold DB system where everyday an ETL pipeline moves transactions older than 90 days to OLAP DBs
   - Note:
     - Historically OLAP DBs worked as analytics sandboxes for Analysts
     - Modern OLAP and data lakes actually serve dual purpose as cold data storage as well
   - In case of transactions when horizontally sharded, normally a trans between two diff shards would require 2 phase commit
     - Instead of doing this in db this is pushed up to app
     - Funds are blocked from the sender then db executes separately on receiver, completes and then funds are removed permanently from sender
     - Rolled back in case of issue