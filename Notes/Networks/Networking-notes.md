---
parent: Networks
---

# Networking Topics for SDE-2 / SDE-3 Roles

A comprehensive reference of networking concepts expected at senior/staff-adjacent software engineering levels — covering both interview prep and real-world system design fluency.

---

## 1. OSI & TCP/IP Fundamentals

### 1.1 OSI 7-layer model vs TCP/IP 4-layer model

The OSI model is a conceptual, 7-layer reference model. The TCP/IP model (what the internet actually runs on) collapses several of those layers into 4. Interviewers mostly want to see that you know **what problem each layer solves** and can map OSI layers to TCP/IP layers without hesitation.

| OSI Layer | Name | TCP/IP Layer | Examples / PDU |
|---|---|---|---|
| 7 | Application | Application | HTTP, DNS, gRPC, WebSocket — **Data** |
| 6 | Presentation | Application | TLS, encoding (encryption/compression conceptually lives here) |
| 5 | Session | Application | Session establishment (TLS handshake, sockets) |
| 4 | Transport | Transport | TCP, UDP, QUIC — **Segments (TCP) / Datagrams (UDP)** |
| 3 | Network | Internet | IP, ICMP, routing — **Packets** |
| 2 | Data Link | Network Access | Ethernet, ARP, switches — **Frames** |
| 1 | Physical | Network Access | Cables, radio, NICs — **Bits** |

Key point to be able to articulate: **OSI is a teaching/reference model**; **TCP/IP is the model the real internet is built on**. In practice, engineers speak mostly in terms of "L3/L4/L7" (network/transport/application) because that's the vocabulary used by load balancers, firewalls, and cloud networking docs (e.g., "L4 load balancer" vs "L7 load balancer" — see Section 6).

### 1.2 Encapsulation / decapsulation across layers

As data moves **down** the stack on the sender side, each layer wraps ("encapsulates") the data from the layer above it with its own header (and sometimes trailer):

```
Application data
   -> [TCP header | data]                     (Segment)
      -> [IP header | TCP header | data]       (Packet)
         -> [Ethernet header | IP header | TCP header | data | Ethernet trailer/FCS]  (Frame)
            -> bits on the wire
```

On the receiving side, this is reversed layer by layer ("decapsulation") — each layer strips its header, reads the addressing/control info relevant to it, and passes the payload up to the next layer. This is why a switch only needs to look at Layer 2 (MAC), a router only needs Layer 3 (IP), and a load balancer/proxy at L7 needs to fully reassemble and read up to the HTTP layer.

**Why this matters practically:** understanding encapsulation explains overhead (each header adds bytes, which is why MTU/MSS matters — see 1.3), and explains why an L4 load balancer is faster/cheaper than an L7 load balancer: L4 only has to inspect IP/TCP headers, while L7 must terminate and parse the full HTTP request.

### 1.3 What happens at each layer

- **Physical (L1)**: raw bit transmission over a medium (copper, fiber, radio). No addressing, no meaning attached to bits.
- **Data Link (L2)**: framing, MAC addressing, and error detection (checksums/CRC) on a *local* network segment. Switches operate here. ARP (Address Resolution Protocol) maps IP → MAC on the local segment.
- **Network (L3)**: logical addressing (IP) and **routing** — getting a packet from source to destination across multiple networks. Routers operate here. Handles fragmentation when a packet exceeds a link's MTU (Maximum Transmission Unit, typically 1500 bytes on Ethernet).
- **Transport (L4)**: end-to-end communication between processes (via ports), **segmentation** of application data into manageable chunks, reliability (TCP) or lack thereof (UDP), flow/congestion control. MSS (Maximum Segment Size) is derived from MTU minus header overhead.
- **Session/Presentation (L5/L6)**: in practice, mostly folded into "Application" in real systems — TLS session establishment, data encoding/serialization (protobuf, JSON, encryption) conceptually sit here even though real stacks implement them as part of the application or a library like OpenSSL.
- **Application (L7)**: the actual protocol the application speaks — HTTP, gRPC, DNS, SMTP, WebSocket.

**Interview framing tip:** when asked "what happens when you type a URL into a browser," this section (encapsulation + per-layer responsibility) is the backbone of a strong answer, tied together with DNS resolution (Section 2) and the TCP/TLS handshakes (Section 3 & 5).

## 2. Addressing & Naming

### 2.1 IPv4 addressing, subnetting, CIDR notation

- IPv4 addresses are 32-bit, written as 4 octets (e.g., `192.168.1.10`), giving ~4.3 billion addresses — long exhausted for public allocation, which is why NAT and IPv6 exist.
- **CIDR (Classless Inter-Domain Routing)** notation (`10.0.0.0/24`) replaced the old class A/B/C system. The `/24` is the **prefix length** — number of bits used for the network portion; the remaining bits identify hosts.
  - `/24` → 256 addresses (254 usable after network + broadcast)
  - `/16` → 65,536 addresses
  - Smaller prefix number = larger network.
- **Subnetting**: dividing a larger network into smaller sub-networks. Common in cloud VPC design — e.g., splitting a `/16` VPC into `/24` subnets per AZ, with public and private subnets separated by route table configuration.
- Reserved/private ranges worth knowing (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` — these are never publicly routable, which is exactly why NAT is required for private-network hosts to reach the internet.
- **Interview-relevant skill**: being able to quickly reason "does `10.0.5.20` fall inside `10.0.4.0/22`?" — this shows up in VPC/subnet design discussions.

### 2.2 IPv6 basics

- 128-bit addresses, written as 8 groups of hex separated by colons (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`, commonly abbreviated by collapsing leading zeros and using `::` once for consecutive zero groups).
- Motivation: IPv4 exhaustion. IPv6 address space is astronomically larger, removing the *need* for NAT (though NAT-like constructs still exist for other reasons).
- Address types: **unicast** (one-to-one), **multicast** (one-to-many), **anycast** (one-to-nearest — used heavily in CDN/DNS infrastructure, see Section 6).
- No broadcast in IPv6 (multicast replaces it).
- Migration reality: dual-stack (host has both IPv4 and IPv6) is the dominant transition approach; most engineers won't hand-design IPv6 subnets often, but should know it exists, why it exists, and that "AAAA record" = IPv6 equivalent of an "A record" (see DNS below).

### 2.3 MAC addresses vs IP addresses

| | MAC Address | IP Address |
|---|---|---|
| Layer | Data Link (L2) | Network (L3) |
| Scope | Local network segment only | Globally routable (logical) |
| Assigned by | Burned into NIC hardware (vendor) | Assigned by network (DHCP/static) |
| Changes when | Rarely (can be spoofed/overridden) | Changes as device moves networks |
| Format | 48-bit, e.g. `00:1A:2B:3C:4D:5E` | 32-bit (v4) / 128-bit (v6) |

**ARP** bridges the two: when a host on a LAN needs to send a frame to another host's IP, it broadcasts an ARP request ("who has this IP?") and gets back the corresponding MAC address, which it then uses to address the L2 frame.

### 2.4 NAT (Network Address Translation)

NAT rewrites source/destination addresses (and often ports) as traffic crosses a network boundary — most commonly translating private RFC 1918 addresses to a public IP so multiple internal hosts can share one external IP.

- **Static NAT**: fixed 1:1 mapping between a private and public IP.
- **Dynamic NAT**: a pool of public IPs is used, mapped on demand.
- **PAT / NAPT (Port Address Translation, i.e., "NAT overload")**: the common home-router/cloud-NAT-gateway case — many private IPs share **one** public IP, disambiguated by port number. This is what lets an entire office or VPC's private subnet reach the internet through a single NAT gateway.
- Practically relevant for SDE-2/3: understanding why servers in a private subnet can make outbound calls (via a NAT gateway) but can't be reached inbound without a load balancer/public IP — this is a VPC design fundamental (see Section 8/11).

### 2.5 DNS (Domain Name System)

DNS is the internet's naming system — translating human-readable names into IP addresses. This is one of the most commonly tested networking topics at any level, so it's worth knowing cold.

**Resolution flow (recursive vs iterative):**
1. Client asks a **recursive resolver** (usually the ISP's or a public one like `8.8.8.8`/`1.1.1.1`) to resolve `www.example.com`.
2. The recursive resolver does the legwork on the client's behalf, performing a series of **iterative** queries:
   - Ask a **root server** → gets referred to the `.com` **TLD server**.
   - Ask the TLD server → gets referred to `example.com`'s **authoritative nameserver**.
   - Ask the authoritative nameserver → gets the actual `A`/`AAAA` record.
3. The recursive resolver caches the result (per the record's TTL) and returns it to the client.

The distinction: the **client-to-resolver** query is recursive (client wants a final answer, doesn't want to be redirected); the **resolver-to-{root,TLD,authoritative}** queries are iterative (each server either answers or refers to the next one).

**Common record types:**
| Record | Purpose |
|---|---|
| `A` | Hostname → IPv4 address |
| `AAAA` | Hostname → IPv6 address |
| `CNAME` | Alias — hostname → another hostname (can't coexist with other records at the same name) |
| `MX` | Mail exchange server(s) for the domain, with priority |
| `TXT` | Arbitrary text — commonly used for domain verification, SPF/DKIM (email auth) |
| `NS` | Delegates a subdomain/zone to specific nameservers |
| `SRV` | Service location (host + port) for a specific service, e.g. used by some internal service discovery setups |

**TTL, caching, propagation:**
- Each record has a **TTL (time-to-live)**, dictating how long resolvers may cache it before re-querying.
- Lower TTL = faster ability to change/failover (e.g., during a migration or incident) but more DNS query load and slightly higher average latency.
- "DNS propagation delay" after a change is really just **caches at various resolvers around the world expiring at different times** based on the old TTL — there's no single global "propagation" mechanism.

**DNS-based load balancing / GeoDNS:**
- A domain can have multiple `A` records; resolvers/clients pick one (round-robin DNS) — a crude form of load balancing with no health-awareness.
- **GeoDNS** returns different IPs based on the geographic/network location of the resolver making the request, routing users to the nearest regional deployment — commonly paired with **Anycast** (Section 6) at the infrastructure level.

**DNSSEC (brief):** adds cryptographic signatures to DNS records so resolvers can verify responses haven't been tampered with, mitigating DNS spoofing/cache-poisoning attacks (see Section 5). Good to know it exists and what problem it solves; deep protocol mechanics are rarely interview-tested at SDE-2/3.

## 3. Transport Layer

### 3.1 TCP

**3-way handshake (connection establishment):**
1. Client → Server: `SYN` (synchronize, "I want to connect, here's my initial sequence number")
2. Server → Client: `SYN-ACK` (acknowledges client's SYN, sends its own SYN)
3. Client → Server: `ACK` (acknowledges server's SYN)

After this, both sides agree on initial sequence numbers and the connection is `ESTABLISHED`. This handshake is also why TCP has inherent connection-setup latency (1 RTT before any data flows) — a major motivating factor for HTTP/2 connection reuse, TLS session resumption, and QUIC's 0-RTT (see 3.5 and Section 4/5).

**Connection teardown:**
- Graceful close is a **4-way** exchange: `FIN` → `ACK` → `FIN` → `ACK` (each side closes its half of the full-duplex connection independently — this is why `FIN` and `ACK` are sometimes combined but conceptually it's 4 steps).
- `RST` (reset) is an **abrupt** termination — sent when a segment arrives for a connection the receiver doesn't recognize, or to forcibly kill a connection (e.g., connecting to a closed port immediately returns `RST` rather than the usual handshake).

**Flow control (sliding window):**
- Prevents a fast sender from overwhelming a slow receiver.
- The receiver advertises a **window size** (bytes it's willing to buffer) in every ACK; the sender won't send more unacknowledged data than that window allows.
- This is *per-connection* and receiver-driven — distinct from congestion control, which is network-driven.

**Congestion control:**
- Prevents the sender from overwhelming the *network* (not just the receiver).
- **Slow start**: congestion window (`cwnd`) starts small and grows exponentially until a threshold or packet loss is detected.
- **AIMD (Additive Increase, Multiplicative Decrease)**: after slow start, `cwnd` increases linearly (additive) each RTT; on detecting loss, it's slashed (multiplicative decrease) — the classic TCP "sawtooth" pattern.
- **Algorithms**: Reno (classic AIMD-based), Cubic (default on Linux for years — grows `cwnd` based on a cubic function of time since last loss, less RTT-biased than Reno), **BBR** (Google's model-based algorithm — estimates actual bottleneck bandwidth and RTT rather than reacting purely to loss, generally achieving higher throughput on lossy or high-BDP networks). Knowing that **loss-based vs model-based** congestion control is the key distinction is usually enough depth for interviews.

**Retransmission, timeouts, RTT estimation:**
- TCP tracks RTT continuously (via timestamps on ACKed segments) and computes a **dynamic retransmission timeout (RTO)** — not a fixed value — using smoothed RTT and RTT variance (Jacobson's algorithm).
- **Fast retransmit**: if the sender gets 3 duplicate ACKs (receiver repeatedly ACKing the same byte, signaling a gap), it retransmits immediately rather than waiting for the full timeout.

**TCP states worth recognizing** (common in `netstat`/`ss` output and interview questions):
- `LISTEN` — server socket waiting for connections
- `SYN_SENT` / `SYN_RECEIVED` — handshake in progress
- `ESTABLISHED` — connection open, data flowing
- `FIN_WAIT_1` / `FIN_WAIT_2` — local side initiated close
- `CLOSE_WAIT` — remote side closed; local app hasn't closed its end yet (a common source of **socket/FD leaks** if the application doesn't close promptly)
- `TIME_WAIT` — connection closed but socket held briefly (2×MSL) to absorb delayed/duplicate packets before the port can be reused — this is why high-throughput servers can exhaust ephemeral ports under heavy short-lived-connection churn, a real production issue worth knowing.

**Nagle's algorithm & delayed ACK:**
- **Nagle's algorithm**: batches small outgoing writes into fewer, larger segments to avoid flooding the network with tiny packets — but this can add latency for latency-sensitive small messages (which is why it's often disabled via `TCP_NODELAY` for things like real-time gaming, trading systems, or interactive protocols).
- **Delayed ACK**: the receiver holds off sending an ACK briefly, hoping to piggyback it on outgoing data or coalesce multiple ACKs.
- **The classic gotcha**: Nagle's algorithm (sender delaying send) + delayed ACK (receiver delaying ACK) can interact badly, adding up to ~200ms+ latency for certain small-message request/response patterns — a genuinely useful thing to know for debugging unexplained latency.

### 3.2 UDP

- Connectionless, unreliable, no ordering guarantees, no handshake, minimal header overhead (8 bytes vs TCP's 20+).
- No flow/congestion control built in — the application (or a layer built on top, like QUIC) must handle that itself if needed.
- **Use cases**: DNS (small request/response, retry is cheap), video/voice streaming (a late packet is worse than a dropped one), online gaming (state updates are frequently superseded, so retransmission is often pointless), and as the substrate for **QUIC** (see 3.5).

### 3.3 TCP vs UDP — when to use which

| Factor | Favors TCP | Favors UDP |
|---|---|---|
| Data must arrive completely & in order | ✅ (file transfer, API calls, DB replication) | |
| Latency-sensitive, stale data is useless | | ✅ (live video, VoIP, gaming state) |
| Connection setup overhead matters | | ✅ (DNS lookups, single small exchange) |
| Need built-in congestion/flow control | ✅ | (must build your own, or use QUIC) |
| Need custom reliability semantics | | ✅ (build exactly what you need on top of UDP — this is QUIC's whole premise) |

### 3.4 Head-of-line blocking

- **TCP-level HOL blocking**: because TCP guarantees in-order delivery, if one segment is lost, **all** subsequent segments — even ones already received — are held back by the receiver's kernel until the lost one is retransmitted and arrives. This affects anyone multiplexing multiple logical streams over one TCP connection (notably HTTP/2, see Section 4) — a single lost packet stalls *all* multiplexed streams, not just the one that lost data.
- **Application-level HOL blocking**: e.g., HTTP/1.1 without pipelining processing requests strictly in order on a connection, so one slow request blocks everything queued behind it on that connection.

### 3.5 QUIC / HTTP/3 basics

- QUIC is built **on top of UDP** (not a new L4 protocol at the OS/network level, though conceptually it does transport-layer jobs) specifically to solve TCP's HOL blocking and slow handshake:
  - Multiplexes multiple independent streams **within QUIC itself**, so a lost packet only stalls the stream it belongs to, not all streams sharing the connection — solving TCP-level HOL blocking for HTTP/2-style multiplexing.
  - Combines the transport and TLS 1.3 handshake into fewer round trips — supports **0-RTT** resumption (a returning client can send data immediately, before the handshake even fully completes) and typically **1-RTT** for new connections vs TCP+TLS's 2-3 RTTs.
  - **Connection migration**: a QUIC connection is identified by a connection ID rather than the traditional (source IP, source port, dest IP, dest port) 4-tuple, so it survives a client's network change (e.g., WiFi → cellular) without dropping — something TCP cannot do.
- HTTP/3 is HTTP semantics carried over QUIC instead of TCP. Worth knowing this is *why* HTTP/3 exists — not just "a newer HTTP version" but a fundamentally different transport underneath.

## 4. Application Layer Protocols
- HTTP/1.1 vs HTTP/2 vs HTTP/3
  - Persistent connections, pipelining
  - HTTP/2 multiplexing, header compression (HPACK), server push
  - HTTP/3 (QUIC) — 0-RTT, connection migration
- HTTP semantics
  - Methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
  - Status codes (1xx–5xx) and correct usage
  - Headers: caching (Cache-Control, ETag), content negotiation, CORS headers
  - Idempotency and safety of methods
- REST principles and constraints
- WebSockets — handshake (upgrade from HTTP), full-duplex use cases
- gRPC — HTTP/2 based, protobuf, streaming modes (unary, server/client/bidi streaming)
- GraphQL over HTTP considerations
- Long polling vs Server-Sent Events vs WebSockets — tradeoffs

## 5. Security
- TLS/SSL
  - TLS handshake (1.2 vs 1.3 differences)
  - Certificates, Certificate Authorities, chain of trust
  - Symmetric vs asymmetric encryption in TLS
  - mTLS (mutual TLS) for service-to-service auth
- HTTPS end-to-end flow
- Common attacks & mitigations
  - Man-in-the-middle
  - DNS spoofing/cache poisoning
  - DDoS (volumetric, protocol, application-layer) and mitigation strategies
  - SYN flood
  - Replay attacks
- CORS — preflight requests, same-origin policy
- API security: OAuth2, JWT, API keys, rate limiting basics

## 6. Load Balancing & Traffic Management
- L4 vs L7 load balancing
- Load balancing algorithms: round robin, least connections, consistent hashing, weighted
- Reverse proxy vs forward proxy
- Health checks, failover
- Global server load balancing (GSLB), Anycast
- Sticky sessions

## 7. Reliability, Performance & Scalability Concepts
- Latency vs throughput vs bandwidth
- Connection pooling and keep-alive
- Timeouts, retries, exponential backoff, jitter
- Circuit breakers, bulkheads (network-related resilience patterns)
- CDN
  - How CDNs work, edge caching, cache invalidation
  - Origin pull vs push
- Caching layers (browser, CDN, reverse proxy, application)
- Rate limiting algorithms: token bucket, leaky bucket, fixed/sliding window

## 8. Networking in Distributed Systems / Microservices
- Service discovery (client-side vs server-side, DNS-based, service registry)
- API Gateway responsibilities
- Service mesh concepts (sidecar proxy, Envoy, Istio basics)
- Inter-service communication patterns: sync (REST/gRPC) vs async (message queues/event streaming)
- Network partitions and CAP theorem implications
- Multi-region networking, latency-aware routing
- VPC concepts, subnets (public/private), security groups, NACLs (cloud networking)
- Peering, VPNs, Direct Connect/private links (high-level awareness)

## 9. Debugging & Tooling
- Tools: `ping`, `traceroute`/`tracert`, `curl`, `netstat`/`ss`, `dig`/`nslookup`, `tcpdump`/`Wireshark`
- Reading and interpreting packet captures at a basic level
- Diagnosing latency issues, connection resets, DNS failures
- Understanding `netstat` output, socket states
- Debugging CORS issues, TLS handshake failures, timeout vs connection-refused

## 10. Sockets & Low-Level Networking (good to know, less critical at higher levels)
- Socket programming basics (TCP/UDP sockets)
- Blocking vs non-blocking I/O
- Multiplexing I/O: select/poll/epoll (conceptual understanding)
- Connection lifecycle at the socket level

## 11. Cloud/Infra Networking Awareness (common in SDE-2/3 system design)
- Load balancer types offered by cloud providers (ALB/NLB style distinctions)
- Ingress controllers (Kubernetes networking basics)
- Kubernetes networking: Services (ClusterIP, NodePort, LoadBalancer), pod-to-pod networking, Ingress
- Multi-AZ / multi-region failover design
- Network cost/latency tradeoffs in system design interviews

## 12. System Design Application (how it all ties together)
- Designing for high availability across regions
- Choosing protocols for different use cases (chat app, video streaming, file upload, real-time bidding)
- Handling thundering herd, cache stampede at network/cache layer
- Designing rate limiters, API gateways at scale
- Trade-offs: consistency vs latency in geo-distributed systems

---

### Suggested Depth by Level
- **SDE-2**: Solid grasp of sections 1–7, working knowledge of 8–10, basic awareness of 11–12.
- **SDE-3**: Fluency across all sections, especially able to reason through 8, 9, 11, 12 in system design interviews and real production debugging.
