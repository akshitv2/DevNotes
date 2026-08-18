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

### 4.1 HTTP/1.1 vs HTTP/2 vs HTTP/3

**HTTP/1.1:**
- Introduced **persistent connections** (`Connection: keep-alive`) as the default, so a TCP connection can be reused across multiple requests instead of opening a new one each time (huge win over HTTP/1.0).
- **Pipelining** (sending multiple requests without waiting for each response) was defined but is effectively unusable in practice — responses must still return **in order**, so a slow response head-of-line-blocks everything queued behind it on that connection. Browsers largely never enabled it. This is the core motivation for HTTP/2.
- Real-world workaround browsers used for years: open **multiple parallel TCP connections** (typically 6 per host) to get concurrency, at the cost of extra handshakes, extra congestion-control ramp-ups, and server resource overhead.

**HTTP/2:**
- **Multiplexing**: many logical request/response streams share a **single TCP connection**, interleaved as binary frames — solving the "6 connections per host" workaround and its overhead.
- **Header compression (HPACK)**: HTTP headers are repetitive across requests (cookies, user-agent, etc.); HPACK maintains a shared compression context between client and server so repeated header fields aren't retransmitted in full each time.
- **Server push** (mostly deprecated/removed in practice — Chrome dropped support): allowed a server to proactively send resources (e.g., CSS/JS) before the client explicitly requested them, anticipating what the page would need.
- **Caveat / the catch**: because HTTP/2 multiplexes over one TCP connection, it inherits **TCP-level head-of-line blocking** (Section 3.4) — one lost packet stalls *all* multiplexed streams, since TCP won't deliver anything out of order to the application layer. This is exactly the problem HTTP/3 was designed to fix.

**HTTP/3:**
- Same HTTP semantics (methods, status codes, headers) as HTTP/1.1/2, but carried over **QUIC** (Section 3.5) instead of TCP.
- **0-RTT**: a client reconnecting to a previously-visited server can send request data in its very first packet, before the handshake fully completes (with some replay-attack caveats — see Section 5).
- **Connection migration**: survives client IP/network changes (WiFi ↔ cellular) without dropping, since QUIC connections are keyed by connection ID, not the IP/port 4-tuple.
- Net effect: fewer round trips to first byte, and per-stream loss isolation instead of connection-wide stalls.

### 4.2 HTTP semantics

**Methods** — know not just what they do, but their **safety** and **idempotency** properties, since this comes up constantly in API design and retry-logic discussions:

| Method | Safe (no side effects)? | Idempotent (repeat = same effect)? | Typical use |
|---|---|---|---|
| `GET` | ✅ | ✅ | Retrieve a resource |
| `HEAD` | ✅ | ✅ | Like GET, headers only |
| `OPTIONS` | ✅ | ✅ | Discover allowed methods (also used for CORS preflight) |
| `PUT` | ❌ | ✅ | Replace a resource entirely |
| `DELETE` | ❌ | ✅ | Remove a resource (repeating it still leaves it deleted) |
| `POST` | ❌ | ❌ | Create a resource / non-idempotent action |
| `PATCH` | ❌ | ❌ (usually) | Partial update — idempotency depends on the patch semantics |

**Why idempotency matters practically**: it's the deciding factor in whether a client (or an infra layer like a load balancer/retry middleware) can safely **retry** a request after a timeout without risking duplicate side effects (e.g., double-charging a payment). This is a frequent system-design and API-design interview thread.

**Status codes** — the categories matter more than memorizing every code:
- `1xx` Informational (e.g., `100 Continue`)
- `2xx` Success (`200 OK`, `201 Created`, `204 No Content`)
- `3xx` Redirection (`301` permanent vs `302`/`307` temporary — matters for caching and SEO; `304 Not Modified` for conditional caching)
- `4xx` Client error (`400` bad request, `401` unauthenticated, `403` forbidden/unauthorized, `404` not found, `409` conflict, `429` too many requests)
- `5xx` Server error (`500` generic, `502` bad gateway — upstream returned an invalid response, `503` service unavailable, `504` gateway timeout)
- **Interview-relevant nuance**: correctly distinguishing `502` vs `503` vs `504` shows real debugging experience — `502` means the proxy got a malformed/invalid response from upstream, `503` means the service itself is overloaded/down, `504` means the proxy timed out waiting for upstream.

**Headers worth knowing in depth:**
- **Caching**: `Cache-Control` (directives like `max-age`, `no-cache`, `no-store`, `private`/`public`), `ETag` (a content fingerprint enabling conditional requests via `If-None-Match` — server responds `304` if unchanged, saving bandwidth), `Last-Modified`/`If-Modified-Since` as a coarser alternative.
- **Content negotiation**: `Accept`, `Accept-Language`, `Accept-Encoding` (e.g., client advertising it can handle `gzip`/`br` compression) and the server's corresponding `Content-Type`, `Content-Encoding` in the response.
- **CORS headers**: `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers` — covered in depth in Section 5.3.

### 4.3 REST principles and constraints

REST (Representational State Transfer) is a set of architectural constraints, not a protocol:
- **Statelessness**: each request contains all information needed to process it; server holds no client session state between requests (any session state lives client-side, e.g., in a token).
- **Resource-based**: URLs identify resources (nouns), HTTP methods express the action (verbs) — `GET /users/123`, not `/getUser?id=123`.
- **Uniform interface**: consistent use of HTTP methods/status codes/media types across the API.
- **Cacheability**: responses should explicitly indicate whether they're cacheable (ties back to `Cache-Control`).
- **Client-server separation** and (optionally) **layered system** (client shouldn't need to know if it's talking directly to the origin server or through intermediaries like a gateway/CDN).
- Interview framing: REST is popular because statelessness + cacheability + the uniform interface map cleanly onto how HTTP, CDNs, and load balancers already work — which is *why* REST scales well, not just a stylistic preference.

### 4.4 WebSockets

- Starts as a normal HTTP request with an `Upgrade: websocket` header; if the server agrees, the HTTP connection is **upgraded in place** to a persistent, full-duplex WebSocket connection over the same underlying TCP socket (no new connection is opened).
- Once upgraded, either side can push messages at any time — unlike HTTP's strict request/response model.
- **Use cases**: chat apps, live collaborative editing, real-time dashboards, multiplayer game state — anything needing low-latency bidirectional messaging where the server needs to push unprompted.
- Tradeoffs vs HTTP polling: much lower latency and overhead per message once established, but the connection is stateful and "sticky" to whichever server instance handled the upgrade — a real consideration for load balancing (see Section 6) and horizontal scaling (need a way to route/broadcast messages across server instances, e.g., via a pub/sub backplane).

### 4.5 gRPC

- Built on **HTTP/2**, so it inherits multiplexing or its underlying TCP HOL-blocking caveat.
- Uses **Protocol Buffers (protobuf)** as the interface definition language and wire format — strongly typed, compact binary serialization, contract-first API design (`.proto` files generate client/server stubs in many languages).
- **Streaming modes**:
  - **Unary**: classic single request → single response (like a normal REST call).
  - **Server streaming**: one request → stream of responses (e.g., subscribing to updates).
  - **Client streaming**: stream of requests → one response (e.g., uploading chunks then getting a final result).
  - **Bidirectional streaming**: both sides stream independently over one connection (e.g., real-time chat, live translation).
- Common in **internal service-to-service communication** (microservices) where you control both client and server and want strong typing + performance; less common for public-facing browser APIs (though grpc-web exists) since browsers historically had limited raw HTTP/2 frame control.

### 4.6 GraphQL over HTTP

- Typically exposed over a **single HTTP endpoint** (commonly `POST /graphql`) rather than many resource-based URLs like REST — the query itself (sent in the request body) determines what data comes back.
- Shifts the "shape of the response" decision to the client, solving REST's common **over-fetching/under-fetching** problem (getting more or less data than needed, or needing multiple round trips to assemble a view).
- Networking-relevant tradeoff: because it's usually a single `POST` endpoint, standard HTTP caching (which keys off method + URL) doesn't work out of the box the way it does for `GET`-based REST APIs — caching has to be handled at the application/query layer instead (e.g., persisted queries, client-side normalized caches).

### 4.7 Long polling vs Server-Sent Events vs WebSockets

| Approach | Direction | Mechanism | Good for |
|---|---|---|---|
| **Long polling** | Client → Server (repeated) | Client sends a request; server holds it open until there's data (or a timeout), then client immediately re-requests | Simple to implement over plain HTTP, works everywhere, but has per-message request overhead and latency |
| **Server-Sent Events (SSE)** | Server → Client only | A single long-lived HTTP connection where the server streams `text/event-stream` formatted events | One-directional server push (e.g., live notifications, stock tickers) with simpler infra than WebSockets (plain HTTP/1.1 or HTTP/2, auto-reconnect built into the browser API) |
| **WebSockets** | Full-duplex | Upgraded persistent connection | True bidirectional real-time (chat, gaming, collaborative editing) |

**Decision framing for interviews**: if you only need server → client push and don't need the client to send much back, SSE is simpler and rides on plain HTTP infrastructure (proxies, load balancers, CDNs understand it better). If you need true bidirectional low-latency messaging, WebSockets are the right tool. Long polling is the fallback for constrained environments but is the least efficient of the three.

## 5. Security

### 5.1 TLS/SSL

TLS (Transport Layer Security; SSL is its deprecated predecessor — nobody should be using SSL today, but the term is still used colloquially) provides **confidentiality, integrity, and authentication** for data in transit.

**TLS handshake — conceptual flow (TLS 1.2):**
1. Client sends `ClientHello` — supported TLS versions, cipher suites, a random value.
2. Server responds with `ServerHello` (chosen cipher suite, its own random value), its **certificate** (containing its public key), and optionally requests a client certificate (mTLS).
3. Client verifies the certificate against trusted CAs (chain of trust, below), generates a **pre-master secret**, encrypts it with the server's public key, and sends it over.
4. Both sides derive the same **symmetric session keys** from the pre-master secret + the exchanged random values.
5. `Finished` messages are exchanged (encrypted with the new session keys) to confirm the handshake succeeded.
- This takes **~2 round trips** before any application data flows.

**TLS 1.3 — what changed and why it matters:**
- Reduces the handshake to **1 RTT** for new connections by having the client guess/send its preferred key share in the `ClientHello` itself, rather than negotiating first.
- Supports **0-RTT resumption** for returning clients (using a previously established session ticket) — but 0-RTT data is replayable by an attacker (since there's no fresh handshake to prevent replay), so it's typically restricted to idempotent requests only.
- Removes support for known-weak/legacy ciphers and features (e.g., static RSA key exchange, which doesn't provide forward secrecy) — TLS 1.3 mandates **forward secrecy** (compromise of the server's long-term private key later doesn't let an attacker decrypt past recorded sessions, because session keys are derived from ephemeral Diffie-Hellman exchanges).

**Certificates, CAs, chain of trust:**
- A certificate binds a public key to an identity (domain name), signed by a **Certificate Authority (CA)**.
- **Chain of trust**: browsers/OSes ship with a set of trusted **root CAs**. Root CAs sign **intermediate CAs**, which sign the actual **leaf/server certificates**. The server presents the leaf cert plus intermediates; the client walks the chain up to a root it already trusts.
- If any link is broken (expired cert, untrusted CA, hostname mismatch, revoked cert) → the handshake fails and the browser shows a warning.

**Symmetric vs asymmetric encryption in TLS:**
- **Asymmetric** (public/private key pairs) is used only for the **initial key exchange and authentication** — it's computationally expensive.
- Once both sides derive a shared **symmetric session key**, all actual application data is encrypted with fast symmetric ciphers (e.g., AES-GCM, ChaCha20-Poly1305) for the rest of the connection.
- This hybrid approach — asymmetric for setup, symmetric for bulk data — is a very commonly tested "why does TLS do it this way" concept.

**mTLS (mutual TLS):**
- Normal TLS only authenticates the **server** to the client. **mTLS** adds the reverse: the client also presents a certificate, and the server verifies it.
- Common in **service-to-service communication** inside a service mesh (Section 8) — each service has its own certificate (often issued/rotated automatically by the mesh's control plane), so services cryptographically authenticate each other without relying on network-location trust alone (i.e., "zero trust networking").

### 5.2 HTTPS end-to-end flow

Putting it together for "what happens when you visit `https://example.com`":
1. DNS resolution (Section 2.5) → get the server's IP.
2. TCP handshake (Section 3.1) — or QUIC's combined handshake if HTTP/3.
3. TLS handshake (above) — establishes an encrypted channel and authenticates the server (and optionally the client).
4. HTTP request/response flows **inside** the encrypted TLS channel — this is why TLS is described as "sitting between" the transport and application layers (roughly OSI's presentation layer).
5. Connection is reused for subsequent requests (persistent connections / HTTP/2 multiplexing) to avoid repeating the handshake cost.

### 5.3 Common attacks & mitigations

- **Man-in-the-middle (MITM)**: an attacker intercepts/alters traffic between two parties. TLS's certificate verification is the primary defense — an attacker without the server's private key can't forge a valid certificate for the domain (assuming CAs and the client's trust store aren't themselves compromised).
- **DNS spoofing / cache poisoning**: an attacker injects forged DNS responses so a resolver caches an incorrect IP for a domain, redirecting users to a malicious server. Mitigated by **DNSSEC** (cryptographically signed DNS records) and by resolvers using randomized query IDs/source ports to make forged responses harder to guess.
- **DDoS (Distributed Denial of Service)** — categorized by which layer they target:
  - **Volumetric**: simply overwhelm bandwidth (e.g., UDP/DNS/NTP amplification floods). Mitigation: upstream scrubbing centers, Anycast to spread load across many edge locations (Section 6).
  - **Protocol attacks**: exploit protocol behavior to exhaust server/network resources (classic example: **SYN flood**, below).
  - **Application-layer**: mimic legitimate requests but at high volume to exhaust application resources (e.g., hammering an expensive search endpoint). Mitigation: rate limiting (Section 7.4), WAFs, behavioral/bot detection.
- **SYN flood**: attacker sends many `SYN` packets (often with spoofed source IPs) and never completes the handshake, exhausting the server's half-open connection table. Mitigated with **SYN cookies** (server doesn't allocate state for a half-open connection; instead encodes the necessary state into the `SYN-ACK`'s sequence number itself, and only allocates real resources once the final `ACK` returns and validates).
- **Replay attacks**: attacker captures a valid message/request and resends it later to fraudulently repeat its effect. Relevant to TLS 1.3's 0-RTT data (mentioned above) and to API design generally — mitigated with nonces, timestamps + short validity windows, and idempotency keys.

### 5.4 CORS (Cross-Origin Resource Sharing)

- Browsers enforce the **same-origin policy** by default: a page served from `https://a.com` cannot read responses from `https://b.com` via JS (`fetch`/`XHR`) unless `b.com` explicitly opts in.
- **Origin** = scheme + host + port — changing any of these counts as a different origin.
- **Simple requests** (basic GET/POST with limited headers/content-types) go straight through, with the browser checking the `Access-Control-Allow-Origin` header on the response before letting JS read it.
- **Preflight requests**: for "non-simple" requests (custom headers, methods like `PUT`/`DELETE`, `Content-Type: application/json`, etc.), the browser first sends an `OPTIONS` request asking the server "would you allow this actual request?" — the server responds with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`; only if that succeeds does the browser send the real request.
- **Key point for interviews**: CORS is a **browser-enforced** client-side security mechanism — it does nothing to protect a server from non-browser clients (curl, server-to-server calls, mobile apps) hitting it directly. It's not a substitute for server-side authentication/authorization.

### 5.5 API security basics

- **OAuth2**: an **authorization** framework (not authentication itself) — lets a user grant a third-party app limited access to their resources on another service without sharing credentials, via access tokens obtained through defined "grant" flows (authorization code, client credentials, etc.).
- **JWT (JSON Web Token)**: a compact, self-contained, signed token format (header.payload.signature) commonly used to carry auth claims — the server can verify the signature without a database lookup, which is great for stateless scaling but means a JWT **can't be easily revoked** before it expires (a real tradeoff worth mentioning: short expiry + refresh tokens is the common mitigation).
- **API keys**: a simpler, long-lived shared-secret credential — less flexible than OAuth2 but common for server-to-server or third-party API access where user-delegated authorization isn't the model.
- **Rate limiting** as a security control (in addition to reliability, Section 7.4): protects against brute-force/credential-stuffing attacks and API abuse, often applied per-API-key/per-IP/per-user at the gateway layer.

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
