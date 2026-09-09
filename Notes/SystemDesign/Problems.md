Divide answers into
1. Requirements (Functional and non-functional) & Scope
2. High-Level Estimates (Back-of-the-Envelope)
3. API & Data Model Design
4. High-Level Architecture
5. Detailed Component Design & Deep Dives focusing on key problems and bottle necks
6. Bottlenecks, Trade-offs & Failure Modes


10 commonly asked system design interview problems categorized by their core focus areas:

* **Design URL Shortener (TinyURL)**
* **Focus:** Core CRUD design, hash functions vs. base62 encoding, unique ID generation, database indexing, caching strategies.


* **Design a News Feed (Twitter/Facebook)**
* **Focus:** Fan-out on write vs. fan-out on read (push vs. pull models), timeline generation, caching layers, pagination with cursors.


* **Design a Messaging System (WhatsApp/Slack)**
* **Focus:** WebSockets, persistent connections, message queueing, end-to-end encryption, read receipts, offline delivery storage.


* **Design a Ride-Sharing Service (Uber/Lyft)**
* **Focus:** Geospatial indexing (QuadTree/S2/H3), real-time location tracking, driver-rider matching algorithms, dynamic pricing (surge).


* **Design Video Streaming Platform (YouTube/Netflix)**
* **Focus:** Video chunking/encoding pipelines, Content Delivery Networks (CDNs), blob storage, adaptive bitrate streaming (DASH/HLS).


* **Design Web Crawler**
* **Focus:** Multi-threaded distributed crawling, duplicate detection (Bloom filters/hashing), rate limiting/politeness, URL frontier management.


* **Design API Rate Limiter**
* **Focus:** Algorithms (Token Bucket, Leaky Bucket, Sliding Window), distributed state syncing (Redis), memory consumption vs. precision trade-offs.


* **Design Distributed Key-Value Store (DynamoDB)**
* **Focus:** Consistent hashing, replication, vector clocks, quorum consensus (N, R, W), gossip protocol, failure detection.


* **Design E-commerce Payment/Checkout System (Stripe/Amazon)**
* **Focus:** Strong consistency, ACID transactions, distributed locking, idempotency keys, handling partial failures and retries.


* **Design Distributed File Storage (Dropbox/Google Drive)**
* **Focus:** Chunking large files, deduplication, metadata management vs. block storage, sync protocol, delta sync.