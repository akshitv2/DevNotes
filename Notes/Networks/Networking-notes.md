---
parent: Networks
nav_order: 2
layout: default
---

# Networking Notes

A comprehensive reference of networking concepts expected at senior/staff-adjacent software engineering levels —
covering both interview prep and real-world system design fluency.

---

## 1. OSI & TCP/IP Fundamentals

### 1.1 OSI 7-layer model vs TCP/IP 4-layer model

The OSI model is a conceptual, 7-layer reference model. The TCP/IP model (what the internet actually runs on) collapses
several of those layers into 4. Interviewers mostly want to see that you know **what problem each layer solves** and can
map OSI layers to TCP/IP layers without hesitation.

| OSI Layer | Name         | TCP/IP Layer   | Examples / PDU                                                 |
|-----------|--------------|----------------|----------------------------------------------------------------|
| 7         | Application  | Application    | HTTP, DNS, gRPC, WebSocket — **Data**                          |
| 6         | Presentation | Application    | TLS, encoding (encryption/compression conceptually lives here) |
| 5         | Session      | Application    | Session establishment (TLS handshake, sockets)                 |
| 4         | Transport    | Transport      | TCP, UDP, QUIC — **Segments (TCP) / Datagrams (UDP)**          |
| 3         | Network      | Internet       | IP, ICMP, routing — **Packets**                                |
| 2         | Data Link    | Network Access | Ethernet, ARP, switches — **Frames**                           |
| 1         | Physical     | Network Access | Cables, radio, NICs — **Bits**                                 |

Key point to be able to articulate: **OSI is a teaching/reference model**; **TCP/IP is the model the real internet is
built on**. In practice, engineers speak mostly in terms of "L3/L4/L7" (network/transport/application) because that's
the vocabulary used by load balancers, firewalls, and cloud networking docs (e.g., "L4 load balancer" vs "L7 load
balancer" — see Section 6).

### 1.2 Encapsulation / decapsulation across layers

As data moves **down** the stack on the sender side, each layer wraps ("encapsulates") the data from the layer above it
with its own header (and sometimes trailer):

```
Application data
   -> [TCP header | data]                     (Segment)
      -> [IP header | TCP header | data]       (Packet)
         -> [Ethernet header | IP header | TCP header | data | Ethernet trailer/FCS]  (Frame)
            -> bits on the wire
```

On the receiving side, this is reversed layer by layer ("decapsulation") — each layer strips its header, reads the
addressing/control info relevant to it, and passes the payload up to the next layer. This is why a switch only needs to
look at Layer 2 (MAC), a router only needs Layer 3 (IP), and a load balancer/proxy at L7 needs to fully reassemble and
read up to the HTTP layer.

**Why this matters practically:** understanding encapsulation explains overhead (each header adds bytes, which is why
MTU/MSS matters — see 1.3), and explains why an L4 load balancer is faster/cheaper than an L7 load balancer: L4 only has
to inspect IP/TCP headers, while L7 must terminate and parse the full HTTP request.

### 1.3 What happens at each layer

- **Physical (L1)**: raw bit transmission over a medium (copper, fiber, radio). No addressing, no meaning attached to
  bits.
- **Data Link (L2)**: framing, MAC addressing, and error detection (checksums/CRC) on a *local* network segment.
  Switches operate here. ARP (Address Resolution Protocol) maps IP → MAC on the local segment.
- **Network (L3)**: logical addressing (IP) and **routing** — getting a packet from source to destination across
  multiple networks. Routers operate here. Handles fragmentation when a packet exceeds a link's MTU (Maximum
  Transmission Unit, typically 1500 bytes on Ethernet).
- **Transport (L4)**: end-to-end communication between processes (via ports), **segmentation** of application data into
  manageable chunks, reliability (TCP) or lack thereof (UDP), flow/congestion control. MSS (Maximum Segment Size) is
  derived from MTU minus header overhead.
- **Session/Presentation (L5/L6)**: in practice, mostly folded into "Application" in real systems — TLS session
  establishment, data encoding/serialization (protobuf, JSON, encryption) conceptually sit here even though real stacks
  implement them as part of the application or a library like OpenSSL.
- **Application (L7)**: the actual protocol the application speaks — HTTP, gRPC, DNS, SMTP, WebSocket.

**Interview framing tip:** when asked "what happens when you type a URL into a browser," this section (encapsulation +
per-layer responsibility) is the backbone of a strong answer, tied together with DNS resolution (Section 2) and the
TCP/TLS handshakes (Section 3 & 5).

## 2. Addressing & Naming

### 2.1 IPv4 addressing, subnetting, CIDR notation

- IPv4 addresses are 32-bit, written as 4 octets (e.g., `192.168.1.10`), giving ~4.3 billion addresses — long exhausted
  for public allocation, which is why NAT and IPv6 exist.
- **CIDR (Classless Inter-Domain Routing)** notation (`10.0.0.0/24`) replaced the old class A/B/C system. The `/24` is
  the **prefix length** — number of bits used for the network portion; the remaining bits identify hosts.
    - `/24` → 256 addresses (254 usable after network + broadcast)
    - `/16` → 65,536 addresses
    - Smaller prefix number = larger network.
- **Subnetting**: dividing a larger network into smaller sub-networks. Common in cloud VPC design — e.g., splitting a
  `/16` VPC into `/24` subnets per AZ, with public and private subnets separated by route table configuration.
- Reserved/private ranges worth knowing (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` — these are never
  publicly routable, which is exactly why NAT is required for private-network hosts to reach the internet.
- **Interview-relevant skill**: being able to quickly reason "does `10.0.5.20` fall inside `10.0.4.0/22`?" — this shows
  up in VPC/subnet design discussions.

### 2.2 IPv6 basics

- 128-bit addresses, written as 8 groups of hex separated by colons (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`,
  commonly abbreviated by collapsing leading zeros and using `::` once for consecutive zero groups).
- Motivation: IPv4 exhaustion. IPv6 address space is astronomically larger, removing the *need* for NAT (though NAT-like
  constructs still exist for other reasons).
- Address types: **unicast** (one-to-one), **multicast** (one-to-many), **anycast** (one-to-nearest — used heavily in
  CDN/DNS infrastructure, see Section 6).
- No broadcast in IPv6 (multicast replaces it).
- Migration reality: dual-stack (host has both IPv4 and IPv6) is the dominant transition approach; most engineers won't
  hand-design IPv6 subnets often, but should know it exists, why it exists, and that "AAAA record" = IPv6 equivalent of
  an "A record" (see DNS below).

### 2.3 MAC addresses vs IP addresses

|              | MAC Address                        | IP Address                        |
|--------------|------------------------------------|-----------------------------------|
| Layer        | Data Link (L2)                     | Network (L3)                      |
| Scope        | Local network segment only         | Globally routable (logical)       |
| Assigned by  | Burned into NIC hardware (vendor)  | Assigned by network (DHCP/static) |
| Changes when | Rarely (can be spoofed/overridden) | Changes as device moves networks  |
| Format       | 48-bit, e.g. `00:1A:2B:3C:4D:5E`   | 32-bit (v4) / 128-bit (v6)        |

**ARP** bridges the two: when a host on a LAN needs to send a frame to another host's IP, it broadcasts an ARP
request ("who has this IP?") and gets back the corresponding MAC address, which it then uses to address the L2 frame.

### 2.4 NAT (Network Address Translation)

NAT rewrites source/destination addresses (and often ports) as traffic crosses a network boundary — most commonly
translating private RFC 1918 addresses to a public IP so multiple internal hosts can share one external IP.

- **Static NAT**: fixed 1:1 mapping between a private and public IP.
- **Dynamic NAT**: a pool of public IPs is used, mapped on demand.
- **PAT / NAPT (Port Address Translation, i.e., "NAT overload")**: the common home-router/cloud-NAT-gateway case — many
  private IPs share **one** public IP, disambiguated by port number. This is what lets an entire office or VPC's private
  subnet reach the internet through a single NAT gateway.
- Practically relevant for SDE-2/3: understanding why servers in a private subnet can make outbound calls (via a NAT
  gateway) but can't be reached inbound without a load balancer/public IP — this is a VPC design fundamental (see
  Section 8/11).

### 2.5 DNS (Domain Name System)

DNS is the internet's naming system — translating human-readable names into IP addresses. This is one of the most
commonly tested networking topics at any level, so it's worth knowing cold.

**Resolution flow (recursive vs iterative):**

1. Client asks a **recursive resolver** (usually the ISP's or a public one like `8.8.8.8`/`1.1.1.1`) to resolve
   `www.example.com`.
2. The recursive resolver does the legwork on the client's behalf, performing a series of **iterative** queries:

- Ask a **root server** → gets referred to the `.com` **TLD server**.
- Ask the TLD server → gets referred to `example.com`'s **authoritative nameserver**.
- Ask the authoritative nameserver → gets the actual `A`/`AAAA` record.

3. The recursive resolver caches the result (per the record's TTL) and returns it to the client.

The distinction: the **client-to-resolver** query is recursive (client wants a final answer, doesn't want to be
redirected); the **resolver-to-{root,TLD,authoritative}** queries are iterative (each server either answers or refers to
the next one).

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
- Lower TTL = faster ability to change/failover (e.g., during a migration or incident) but more DNS query load and
  slightly higher average latency.
- "DNS propagation delay" after a change is really just **caches at various resolvers around the world expiring at
  different times** based on the old TTL — there's no single global "propagation" mechanism.

**DNS-based load balancing / GeoDNS:**

- A domain can have multiple `A` records; resolvers/clients pick one (round-robin DNS) — a crude form of load balancing
  with no health-awareness.
- **GeoDNS** returns different IPs based on the geographic/network location of the resolver making the request, routing
  users to the nearest regional deployment — commonly paired with **Anycast** (Section 6) at the infrastructure level.

**DNSSEC (brief):** adds cryptographic signatures to DNS records so resolvers can verify responses haven't been tampered
with, mitigating DNS spoofing/cache-poisoning attacks (see Section 5). Good to know it exists and what problem it
solves; deep protocol mechanics are rarely interview-tested at SDE-2/3.

## 3. Transport Layer

### 3.1 TCP

**3-way handshake (connection establishment):**

1. Client → Server: `SYN` (synchronize, "I want to connect, here's my initial sequence number")
2. Server → Client: `SYN-ACK` (acknowledges client's SYN, sends its own SYN)
3. Client → Server: `ACK` (acknowledges server's SYN)

After this, both sides agree on initial sequence numbers and the connection is `ESTABLISHED`. This handshake is also why
TCP has inherent connection-setup latency (1 RTT before any data flows) — a major motivating factor for HTTP/2
connection reuse, TLS session resumption, and QUIC's 0-RTT (see 3.5 and Section 4/5).

**Connection teardown:**

- Graceful close is a **4-way** exchange: `FIN` → `ACK` → `FIN` → `ACK` (each side closes its half of the full-duplex
  connection independently — this is why `FIN` and `ACK` are sometimes combined but conceptually it's 4 steps).
- `RST` (reset) is an **abrupt** termination — sent when a segment arrives for a connection the receiver doesn't
  recognize, or to forcibly kill a connection (e.g., connecting to a closed port immediately returns `RST` rather than
  the usual handshake).

**Flow control (sliding window):**

- Prevents a fast sender from overwhelming a slow receiver.
- The receiver advertises a **window size** (bytes it's willing to buffer) in every ACK; the sender won't send more
  unacknowledged data than that window allows.
- This is *per-connection* and receiver-driven — distinct from congestion control, which is network-driven.

**Congestion control:**

- Prevents the sender from overwhelming the *network* (not just the receiver).
- **Slow start**: congestion window (`cwnd`) starts small and grows exponentially until a threshold or packet loss is
  detected.
- **AIMD (Additive Increase, Multiplicative Decrease)**: after slow start, `cwnd` increases linearly (additive) each
  RTT; on detecting loss, it's slashed (multiplicative decrease) — the classic TCP "sawtooth" pattern.
- **Algorithms**: Reno (classic AIMD-based), Cubic (default on Linux for years — grows `cwnd` based on a cubic function
  of time since last loss, less RTT-biased than Reno), **BBR** (Google's model-based algorithm — estimates actual
  bottleneck bandwidth and RTT rather than reacting purely to loss, generally achieving higher throughput on lossy or
  high-BDP networks). Knowing that **loss-based vs model-based** congestion control is the key distinction is usually
  enough depth for interviews.

**Retransmission, timeouts, RTT estimation:**

- TCP tracks RTT continuously (via timestamps on ACKed segments) and computes a **dynamic retransmission timeout (RTO)
  ** — not a fixed value — using smoothed RTT and RTT variance (Jacobson's algorithm).
- **Fast retransmit**: if the sender gets 3 duplicate ACKs (receiver repeatedly ACKing the same byte, signaling a gap),
  it retransmits immediately rather than waiting for the full timeout.

**TCP states worth recognizing** (common in `netstat`/`ss` output and interview questions):

- `LISTEN` — server socket waiting for connections
- `SYN_SENT` / `SYN_RECEIVED` — handshake in progress
- `ESTABLISHED` — connection open, data flowing
- `FIN_WAIT_1` / `FIN_WAIT_2` — local side initiated close
- `CLOSE_WAIT` — remote side closed; local app hasn't closed its end yet (a common source of **socket/FD leaks** if the
  application doesn't close promptly)
- `TIME_WAIT` — connection closed but socket held briefly (2×MSL) to absorb delayed/duplicate packets before the port
  can be reused — this is why high-throughput servers can exhaust ephemeral ports under heavy short-lived-connection
  churn, a real production issue worth knowing.

**Nagle's algorithm & delayed ACK:**

- **Nagle's algorithm**: batches small outgoing writes into fewer, larger segments to avoid flooding the network with
  tiny packets — but this can add latency for latency-sensitive small messages (which is why it's often disabled via
  `TCP_NODELAY` for things like real-time gaming, trading systems, or interactive protocols).
- **Delayed ACK**: the receiver holds off sending an ACK briefly, hoping to piggyback it on outgoing data or coalesce
  multiple ACKs.
- **The classic gotcha**: Nagle's algorithm (sender delaying send) + delayed ACK (receiver delaying ACK) can interact
  badly, adding up to ~200ms+ latency for certain small-message request/response patterns — a genuinely useful thing to
  know for debugging unexplained latency.

### 3.2 UDP

- Connectionless, unreliable, no ordering guarantees, no handshake, minimal header overhead (8 bytes vs TCP's 20+).
- No flow/congestion control built in — the application (or a layer built on top, like QUIC) must handle that itself if
  needed.
- **Use cases**: DNS (small request/response, retry is cheap), video/voice streaming (a late packet is worse than a
  dropped one), online gaming (state updates are frequently superseded, so retransmission is often pointless), and as
  the substrate for **QUIC** (see 3.5).

### 3.3 TCP vs UDP — when to use which

| Factor                                   | Favors TCP                                   | Favors UDP                                                                   |
|------------------------------------------|----------------------------------------------|------------------------------------------------------------------------------|
| Data must arrive completely & in order   | ✅ (file transfer, API calls, DB replication) |                                                                              |
| Latency-sensitive, stale data is useless |                                              | ✅ (live video, VoIP, gaming state)                                           |
| Connection setup overhead matters        |                                              | ✅ (DNS lookups, single small exchange)                                       |
| Need built-in congestion/flow control    | ✅                                            | (must build your own, or use QUIC)                                           |
| Need custom reliability semantics        |                                              | ✅ (build exactly what you need on top of UDP — this is QUIC's whole premise) |

### 3.4 Head-of-line blocking

- **TCP-level HOL blocking**: because TCP guarantees in-order delivery, if one segment is lost, **all** subsequent
  segments — even ones already received — are held back by the receiver's kernel until the lost one is retransmitted and
  arrives. This affects anyone multiplexing multiple logical streams over one TCP connection (notably HTTP/2, see
  Section 4) — a single lost packet stalls *all* multiplexed streams, not just the one that lost data.
- **Application-level HOL blocking**: e.g., HTTP/1.1 without pipelining processing requests strictly in order on a
  connection, so one slow request blocks everything queued behind it on that connection.

### 3.5 QUIC / HTTP/3 basics

- QUIC is built **on top of UDP** (not a new L4 protocol at the OS/network level, though conceptually it does
  transport-layer jobs) specifically to solve TCP's HOL blocking and slow handshake:
    - Multiplexes multiple independent streams **within QUIC itself**, so a lost packet only stalls the stream it
      belongs to, not all streams sharing the connection — solving TCP-level HOL blocking for HTTP/2-style multiplexing.
    - Combines the transport and TLS 1.3 handshake into fewer round trips — supports **0-RTT** resumption (a returning
      client can send data immediately, before the handshake even fully completes) and typically **1-RTT** for new
      connections vs TCP+TLS's 2-3 RTTs.
    - **Connection migration**: a QUIC connection is identified by a connection ID rather than the traditional (source
      IP, source port, dest IP, dest port) 4-tuple, so it survives a client's network change (e.g., WiFi → cellular)
      without dropping — something TCP cannot do.
- HTTP/3 is HTTP semantics carried over QUIC instead of TCP. Worth knowing this is *why* HTTP/3 exists — not just "a
  newer HTTP version" but a fundamentally different transport underneath.

## 4. Application Layer Protocols

### 4.1 HTTP/1.1 vs HTTP/2 vs HTTP/3

**HTTP/1.1:**

- Introduced **persistent connections** (`Connection: keep-alive`) as the default, so a TCP connection can be reused
  across multiple requests instead of opening a new one each time (huge win over HTTP/1.0).
- **Pipelining** (sending multiple requests without waiting for each response) was defined but is effectively unusable
  in practice — responses must still return **in order**, so a slow response head-of-line-blocks everything queued
  behind it on that connection. Browsers largely never enabled it. This is the core motivation for HTTP/2.
- Real-world workaround browsers used for years: open **multiple parallel TCP connections** (typically 6 per host) to
  get concurrency, at the cost of extra handshakes, extra congestion-control ramp-ups, and server resource overhead.

**HTTP/2:**

- **Multiplexing**: many logical request/response streams share a **single TCP connection**, interleaved as binary
  frames — solving the "6 connections per host" workaround and its overhead.
- **Header compression (HPACK)**: HTTP headers are repetitive across requests (cookies, user-agent, etc.); HPACK
  maintains a shared compression context between client and server so repeated header fields aren't retransmitted in
  full each time.
- **Server push** (mostly deprecated/removed in practice — Chrome dropped support): allowed a server to proactively send
  resources (e.g., CSS/JS) before the client explicitly requested them, anticipating what the page would need.
- **Caveat / the catch**: because HTTP/2 multiplexes over one TCP connection, it inherits **TCP-level head-of-line
  blocking** (Section 3.4) — one lost packet stalls *all* multiplexed streams, since TCP won't deliver anything out of
  order to the application layer. This is exactly the problem HTTP/3 was designed to fix.

**HTTP/3:**

- Same HTTP semantics (methods, status codes, headers) as HTTP/1.1/2, but carried over **QUIC** (Section 3.5) instead of
  TCP.
- **0-RTT**: a client reconnecting to a previously-visited server can send request data in its very first packet, before
  the handshake fully completes (with some replay-attack caveats — see Section 5).
- **Connection migration**: survives client IP/network changes (WiFi ↔ cellular) without dropping, since QUIC
  connections are keyed by connection ID, not the IP/port 4-tuple.
- Net effect: fewer round trips to first byte, and per-stream loss isolation instead of connection-wide stalls.

### 4.2 HTTP semantics

**Methods** — know not just what they do, but their **safety** and **idempotency** properties, since this comes up
constantly in API design and retry-logic discussions:

| Method    | Safe (no side effects)? | Idempotent (repeat = same effect)? | Typical use                                                 |
|-----------|-------------------------|------------------------------------|-------------------------------------------------------------|
| `GET`     | ✅                       | ✅                                  | Retrieve a resource                                         |
| `HEAD`    | ✅                       | ✅                                  | Like GET, headers only                                      |
| `OPTIONS` | ✅                       | ✅                                  | Discover allowed methods (also used for CORS preflight)     |
| `PUT`     | ❌                       | ✅                                  | Replace a resource entirely                                 |
| `DELETE`  | ❌                       | ✅                                  | Remove a resource (repeating it still leaves it deleted)    |
| `POST`    | ❌                       | ❌                                  | Create a resource / non-idempotent action                   |
| `PATCH`   | ❌                       | ❌ (usually)                        | Partial update — idempotency depends on the patch semantics |

**Why idempotency matters practically**: it's the deciding factor in whether a client (or an infra layer like a load
balancer/retry middleware) can safely **retry** a request after a timeout without risking duplicate side effects (e.g.,
double-charging a payment). This is a frequent system-design and API-design interview thread.

**Status codes** — the categories matter more than memorizing every code:

- `1xx` Informational (e.g., `100 Continue`)
- `2xx` Success (`200 OK`, `201 Created`, `204 No Content`)
- `3xx` Redirection (`301` permanent vs `302`/`307` temporary — matters for caching and SEO; `304 Not Modified` for
  conditional caching)
- `4xx` Client error (`400` bad request, `401` unauthenticated, `403` forbidden/unauthorized, `404` not found, `409`
  conflict, `429` too many requests)
- `5xx` Server error (`500` generic, `502` bad gateway — upstream returned an invalid response, `503` service
  unavailable, `504` gateway timeout)
- **Interview-relevant nuance**: correctly distinguishing `502` vs `503` vs `504` shows real debugging experience —
  `502` means the proxy got a malformed/invalid response from upstream, `503` means the service itself is
  overloaded/down, `504` means the proxy timed out waiting for upstream.

**Headers worth knowing in depth:**

- **Caching**: `Cache-Control` (directives like `max-age`, `no-cache`, `no-store`, `private`/`public`), `ETag` (a
  content fingerprint enabling conditional requests via `If-None-Match` — server responds `304` if unchanged, saving
  bandwidth), `Last-Modified`/`If-Modified-Since` as a coarser alternative.
- **Content negotiation**: `Accept`, `Accept-Language`, `Accept-Encoding` (e.g., client advertising it can handle
  `gzip`/`br` compression) and the server's corresponding `Content-Type`, `Content-Encoding` in the response.
- **CORS headers**: `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers` —
  covered in depth in Section 5.3.

### 4.3 REST principles and constraints

REST (Representational State Transfer) is a set of architectural constraints, not a protocol:

- **Statelessness**: each request contains all information needed to process it; server holds no client session state
  between requests (any session state lives client-side, e.g., in a token).
- **Resource-based**: URLs identify resources (nouns), HTTP methods express the action (verbs) — `GET /users/123`, not
  `/getUser?id=123`.
- **Uniform interface**: consistent use of HTTP methods/status codes/media types across the API.
- **Cacheability**: responses should explicitly indicate whether they're cacheable (ties back to `Cache-Control`).
- **Client-server separation** and (optionally) **layered system** (client shouldn't need to know if it's talking
  directly to the origin server or through intermediaries like a gateway/CDN).
- Interview framing: REST is popular because statelessness + cacheability + the uniform interface map cleanly onto how
  HTTP, CDNs, and load balancers already work — which is *why* REST scales well, not just a stylistic preference.

### 4.4 WebSockets

- Starts as a normal HTTP request with an `Upgrade: websocket` header; if the server agrees, the HTTP connection is *
  *upgraded in place** to a persistent, full-duplex WebSocket connection over the same underlying TCP socket (no new
  connection is opened).
- Once upgraded, either side can push messages at any time — unlike HTTP's strict request/response model.
- **Use cases**: chat apps, live collaborative editing, real-time dashboards, multiplayer game state — anything needing
  low-latency bidirectional messaging where the server needs to push unprompted.
- Tradeoffs vs HTTP polling: much lower latency and overhead per message once established, but the connection is
  stateful and "sticky" to whichever server instance handled the upgrade — a real consideration for load balancing (see
  Section 6) and horizontal scaling (need a way to route/broadcast messages across server instances, e.g., via a pub/sub
  backplane).

### 4.5 gRPC

- Built on **HTTP/2**, so it inherits multiplexing or its underlying TCP HOL-blocking caveat.
- Uses **Protocol Buffers (protobuf)** as the interface definition language and wire format — strongly typed, compact
  binary serialization, contract-first API design (`.proto` files generate client/server stubs in many languages).
- **Streaming modes**:
    - **Unary**: classic single request → single response (like a normal REST call).
    - **Server streaming**: one request → stream of responses (e.g., subscribing to updates).
    - **Client streaming**: stream of requests → one response (e.g., uploading chunks then getting a final result).
    - **Bidirectional streaming**: both sides stream independently over one connection (e.g., real-time chat, live
      translation).
- Common in **internal service-to-service communication** (microservices) where you control both client and server and
  want strong typing + performance; less common for public-facing browser APIs (though grpc-web exists) since browsers
  historically had limited raw HTTP/2 frame control.

### 4.6 GraphQL over HTTP

- Typically exposed over a **single HTTP endpoint** (commonly `POST /graphql`) rather than many resource-based URLs like
  REST — the query itself (sent in the request body) determines what data comes back.
- Shifts the "shape of the response" decision to the client, solving REST's common **over-fetching/under-fetching**
  problem (getting more or less data than needed, or needing multiple round trips to assemble a view).
- Networking-relevant tradeoff: because it's usually a single `POST` endpoint, standard HTTP caching (which keys off
  method + URL) doesn't work out of the box the way it does for `GET`-based REST APIs — caching has to be handled at the
  application/query layer instead (e.g., persisted queries, client-side normalized caches).

### 4.7 Long polling vs Server-Sent Events vs WebSockets

| Approach                     | Direction                  | Mechanism                                                                                                           | Good for                                                                                                                                                                       |
|------------------------------|----------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Long polling**             | Client → Server (repeated) | Client sends a request; server holds it open until there's data (or a timeout), then client immediately re-requests | Simple to implement over plain HTTP, works everywhere, but has per-message request overhead and latency                                                                        |
| **Server-Sent Events (SSE)** | Server → Client only       | A single long-lived HTTP connection where the server streams `text/event-stream` formatted events                   | One-directional server push (e.g., live notifications, stock tickers) with simpler infra than WebSockets (plain HTTP/1.1 or HTTP/2, auto-reconnect built into the browser API) |
| **WebSockets**               | Full-duplex                | Upgraded persistent connection                                                                                      | True bidirectional real-time (chat, gaming, collaborative editing)                                                                                                             |

**Decision framing for interviews**: if you only need server → client push and don't need the client to send much back,
SSE is simpler and rides on plain HTTP infrastructure (proxies, load balancers, CDNs understand it better). If you need
true bidirectional low-latency messaging, WebSockets are the right tool. Long polling is the fallback for constrained
environments but is the least efficient of the three.

## 5. Security

### 5.1 TLS/SSL

TLS (Transport Layer Security; SSL is its deprecated predecessor — nobody should be using SSL today, but the term is
still used colloquially) provides **confidentiality, integrity, and authentication** for data in transit.

**TLS handshake — conceptual flow (TLS 1.2):**

1. Client sends `ClientHello` — supported TLS versions, cipher suites, a random value.
2. Server responds with `ServerHello` (chosen cipher suite, its own random value), its **certificate** (containing its
   public key), and optionally requests a client certificate (mTLS).
3. Client verifies the certificate against trusted CAs (chain of trust, below), generates a **pre-master secret**,
   encrypts it with the server's public key, and sends it over.
4. Both sides derive the same **symmetric session keys** from the pre-master secret + the exchanged random values.
5. `Finished` messages are exchanged (encrypted with the new session keys) to confirm the handshake succeeded.

- This takes **~2 round trips** before any application data flows.

**TLS 1.3 — what changed and why it matters:**

- Reduces the handshake to **1 RTT** for new connections by having the client guess/send its preferred key share in the
  `ClientHello` itself, rather than negotiating first.
- Supports **0-RTT resumption** for returning clients (using a previously established session ticket) — but 0-RTT data
  is replayable by an attacker (since there's no fresh handshake to prevent replay), so it's typically restricted to
  idempotent requests only.
- Removes support for known-weak/legacy ciphers and features (e.g., static RSA key exchange, which doesn't provide
  forward secrecy) — TLS 1.3 mandates **forward secrecy** (compromise of the server's long-term private key later doesn'
  t let an attacker decrypt past recorded sessions, because session keys are derived from ephemeral Diffie-Hellman
  exchanges).

**Certificates, CAs, chain of trust:**

- A certificate binds a public key to an identity (domain name), signed by a **Certificate Authority (CA)**.
- **Chain of trust**: browsers/OSes ship with a set of trusted **root CAs**. Root CAs sign **intermediate CAs**, which
  sign the actual **leaf/server certificates**. The server presents the leaf cert plus intermediates; the client walks
  the chain up to a root it already trusts.
- If any link is broken (expired cert, untrusted CA, hostname mismatch, revoked cert) → the handshake fails and the
  browser shows a warning.

**Symmetric vs asymmetric encryption in TLS:**

- **Asymmetric** (public/private key pairs) is used only for the **initial key exchange and authentication** — it's
  computationally expensive.
- Once both sides derive a shared **symmetric session key**, all actual application data is encrypted with fast
  symmetric ciphers (e.g., AES-GCM, ChaCha20-Poly1305) for the rest of the connection.
- This hybrid approach — asymmetric for setup, symmetric for bulk data — is a very commonly tested "why does TLS do it
  this way" concept.

**mTLS (mutual TLS):**

- Normal TLS only authenticates the **server** to the client. **mTLS** adds the reverse: the client also presents a
  certificate, and the server verifies it.
- Common in **service-to-service communication** inside a service mesh (Section 8) — each service has its own
  certificate (often issued/rotated automatically by the mesh's control plane), so services cryptographically
  authenticate each other without relying on network-location trust alone (i.e., "zero trust networking").

### 5.2 HTTPS end-to-end flow

Putting it together for "what happens when you visit `https://example.com`":

1. DNS resolution (Section 2.5) → get the server's IP.
2. TCP handshake (Section 3.1) — or QUIC's combined handshake if HTTP/3.
3. TLS handshake (above) — establishes an encrypted channel and authenticates the server (and optionally the client).
4. HTTP request/response flows **inside** the encrypted TLS channel — this is why TLS is described as "sitting between"
   the transport and application layers (roughly OSI's presentation layer).
5. Connection is reused for subsequent requests (persistent connections / HTTP/2 multiplexing) to avoid repeating the
   handshake cost.

### 5.3 Common attacks & mitigations

- **Man-in-the-middle (MITM)**: an attacker intercepts/alters traffic between two parties. TLS's certificate
  verification is the primary defense — an attacker without the server's private key can't forge a valid certificate for
  the domain (assuming CAs and the client's trust store aren't themselves compromised).
- **DNS spoofing / cache poisoning**: an attacker injects forged DNS responses so a resolver caches an incorrect IP for
  a domain, redirecting users to a malicious server. Mitigated by **DNSSEC** (cryptographically signed DNS records) and
  by resolvers using randomized query IDs/source ports to make forged responses harder to guess.
- **DDoS (Distributed Denial of Service)** — categorized by which layer they target:
    - **Volumetric**: simply overwhelm bandwidth (e.g., UDP/DNS/NTP amplification floods). Mitigation: upstream
      scrubbing centers, Anycast to spread load across many edge locations (Section 6).
    - **Protocol attacks**: exploit protocol behavior to exhaust server/network resources (classic example: **SYN flood
      **, below).
    - **Application-layer**: mimic legitimate requests but at high volume to exhaust application resources (e.g.,
      hammering an expensive search endpoint). Mitigation: rate limiting (Section 7.4), WAFs, behavioral/bot detection.
- **SYN flood**: attacker sends many `SYN` packets (often with spoofed source IPs) and never completes the handshake,
  exhausting the server's half-open connection table. Mitigated with **SYN cookies** (server doesn't allocate state for
  a half-open connection; instead encodes the necessary state into the `SYN-ACK`'s sequence number itself, and only
  allocates real resources once the final `ACK` returns and validates).
- **Replay attacks**: attacker captures a valid message/request and resends it later to fraudulently repeat its effect.
  Relevant to TLS 1.3's 0-RTT data (mentioned above) and to API design generally — mitigated with nonces, timestamps +
  short validity windows, and idempotency keys.

### 5.4 CORS (Cross-Origin Resource Sharing)

- Browsers enforce the **same-origin policy** by default: a page served from `https://a.com` cannot read responses from
  `https://b.com` via JS (`fetch`/`XHR`) unless `b.com` explicitly opts in.
- **Origin** = scheme + host + port — changing any of these counts as a different origin.
- **Simple requests** (basic GET/POST with limited headers/content-types) go straight through, with the browser checking
  the `Access-Control-Allow-Origin` header on the response before letting JS read it.
- **Preflight requests**: for "non-simple" requests (custom headers, methods like `PUT`/`DELETE`,
  `Content-Type: application/json`, etc.), the browser first sends an `OPTIONS` request asking the server "would you
  allow this actual request?" — the server responds with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`,
  `Access-Control-Allow-Headers`; only if that succeeds does the browser send the real request.
- **Key point for interviews**: CORS is a **browser-enforced** client-side security mechanism — it does nothing to
  protect a server from non-browser clients (curl, server-to-server calls, mobile apps) hitting it directly. It's not a
  substitute for server-side authentication/authorization.

### 5.5 API security basics

- **OAuth2**: an **authorization** framework (not authentication itself) — lets a user grant a third-party app limited
  access to their resources on another service without sharing credentials, via access tokens obtained through defined "
  grant" flows (authorization code, client credentials, etc.).
- **JWT (JSON Web Token)**: a compact, self-contained, signed token format (header.payload.signature) commonly used to
  carry auth claims — the server can verify the signature without a database lookup, which is great for stateless
  scaling but means a JWT **can't be easily revoked** before it expires (a real tradeoff worth mentioning: short
  expiry + refresh tokens is the common mitigation).
- **API keys**: a simpler, long-lived shared-secret credential — less flexible than OAuth2 but common for
  server-to-server or third-party API access where user-delegated authorization isn't the model.
- **Rate limiting** as a security control (in addition to reliability, Section 7.4): protects against
  brute-force/credential-stuffing attacks and API abuse, often applied per-API-key/per-IP/per-user at the gateway layer.

## 6. Load Balancing & Traffic Management

### 6.1 L4 vs L7 load balancing

- **L4 (transport layer)**: makes routing decisions based only on IP/port info (and TCP/UDP-level state) — it doesn't
  look at HTTP content at all. Faster, lower overhead, protocol-agnostic (works for any TCP/UDP traffic, not just HTTP).
  It essentially forwards packets/connections to a backend without terminating them.
- **L7 (application layer)**: terminates the connection, actually parses the HTTP request (or gRPC/WebSocket), and can
  route based on path, headers, cookies, hostname, etc. (e.g., `/api/*` → service A, `/static/*` → CDN/service B).
  Enables smarter behavior — content-based routing, request rewriting, SSL termination, retries — at the cost of more
  CPU/latency per request.
- **Interview framing**: this maps directly to real cloud offerings — AWS's NLB (Network Load Balancer, L4) vs ALB (
  Application Load Balancer, L7) is the canonical example to cite.

### 6.2 Load balancing algorithms

| Algorithm                | How it works                                                                                                                                           | Good for                                                                                                                                               |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Round robin**          | Requests distributed sequentially across backends                                                                                                      | Simple, uniform backends with similar capacity/request cost                                                                                            |
| **Weighted round robin** | Like round robin, but backends with more capacity get proportionally more requests                                                                     | Heterogeneous backend capacity                                                                                                                         |
| **Least connections**    | Route to the backend with the fewest active connections                                                                                                | Requests with variable/long processing time (round robin can overload a backend stuck on slow requests)                                                |
| **Consistent hashing**   | Hash a key (e.g., client IP, session ID, cache key) to consistently map it to the same backend, with minimal remapping when backends are added/removed | Caching layers, sharding, and **sticky sessions** without central state — critical for minimizing cache-miss storms or reshuffling when scaling in/out |

**Consistent hashing deserves extra depth** since it shows up repeatedly in distributed systems interviews: naive
`hash(key) % N` remaps almost *all* keys when `N` changes (a server added/removed); consistent hashing arranges backends
and keys on a conceptual ring so only a small fraction of keys need to move when the backend set changes — this is the
backbone of systems like distributed caches (Memcached client-side hashing), CDN request routing, and sharded databases.

### 6.3 Reverse proxy vs forward proxy

- **Forward proxy**: sits in front of **clients**, making requests *on their behalf* to the internet — the destination
  server sees the proxy, not the original client (e.g., corporate proxies, VPNs for anonymity/access control).
- **Reverse proxy**: sits in front of **servers**, receiving client requests and forwarding them to one of possibly many
  backend servers — clients only ever see the reverse proxy (e.g., Nginx, load balancers, API gateways). Handles
  concerns like SSL termination, caching, compression, and load distribution on behalf of the backends.
- **Simple mental model**: forward proxy protects/represents the *client*; reverse proxy protects/represents the
  *server*.

### 6.4 Health checks & failover

- Load balancers periodically probe backends (via TCP connect, HTTP `GET /health`, or protocol-specific checks) to
  determine liveness before routing traffic to them.
- **Active health checks**: LB proactively polls a health endpoint on an interval.
- **Passive health checks**: LB infers health from real traffic (e.g., a backend returning consecutive 5xx or timing out
  gets temporarily removed from rotation).
- Failover: when a backend (or entire AZ/region) fails health checks, traffic is automatically rerouted to healthy
  backends/regions — this is the mechanism underlying most "automatic failover" claims in system design answers, and
  it's worth being able to describe concretely rather than hand-waving "it just fails over."

### 6.5 Global server load balancing (GSLB) & Anycast

- **GSLB**: load balancing across **geographically distributed** deployments (multiple regions/data centers), typically
  implemented via GeoDNS (Section 2.5) or Anycast — routing users to the nearest/healthiest region.
- **Anycast**: the same IP address is announced from multiple physical locations via BGP; network routing naturally
  sends a client's traffic to the topologically nearest announcing location. Used heavily by CDNs and public DNS
  resolvers (e.g., `1.1.1.1`, `8.8.8.8`) to give low-latency access from anywhere without client-side logic — the
  network itself handles the routing.

### 6.6 Sticky sessions

- Ensures a given client's requests keep landing on the **same backend instance**, typically via a cookie (LB sets a
  cookie identifying the chosen backend) or via **consistent hashing** on client IP/session ID.
- Necessary when a backend holds **in-memory session state** that isn't shared across instances, or for stateful
  protocols like WebSockets.
- Tradeoff worth articulating: sticky sessions reduce flexibility for load balancing (can create hot spots) and
  complicate scaling/failover (losing that specific backend loses the session state). The more scalable alternative is
  making backends **stateless** and externalizing session state (e.g., to Redis) so any backend can serve any request —
  a recurring theme in system design interviews.

---

## 7. Reliability, Performance & Scalability Concepts

### 7.1 Latency vs throughput vs bandwidth

- **Latency**: time for a single unit of data (e.g., one request) to travel from source to destination — measured in
  time (ms).
- **Throughput**: amount of data/requests successfully processed per unit time — measured in requests/sec or bytes/sec.
  High latency doesn't necessarily mean low throughput (you can have many slow requests in flight concurrently and still
  achieve high throughput) — this distinction ("a highway can have high latency per car but still high throughput with
  many lanes") is a classic interview clarifying point.
- **Bandwidth**: the maximum theoretical capacity of a link (bytes/sec) — throughput is bounded by bandwidth but usually
  lower in practice due to protocol overhead, congestion, etc.

### 7.2 Connection pooling and keep-alive

- Establishing a TCP (and especially TLS) connection is expensive (handshake round trips, Section 3.1/5.1). **Connection
  pooling** reuses a small set of already-established connections across many logical requests instead of
  opening/closing one per request — standard practice for database clients, HTTP clients calling downstream services,
  etc.
- **Keep-alive**: the underlying mechanism that keeps a connection open between requests instead of closing it
  immediately (HTTP's `Connection: keep-alive`, or TCP keep-alive probes that detect a dead peer on an otherwise idle
  connection).
- Practical sizing consideration often probed in interviews: pool size needs to balance connection reuse against
  exhausting backend resources (e.g., a DB has a max connection limit) or ephemeral port exhaustion (Section 3.1's
  `TIME_WAIT` discussion) under high request volume.

### 7.3 Timeouts, retries, exponential backoff, jitter

- **Timeouts**: every network call needs one — without a timeout, a hung downstream call can exhaust the caller's own
  resources (threads, connections) waiting indefinitely, a very common real production incident pattern ("cascading
  failure" from one slow dependency).
- **Retries**: should generally only be applied to **idempotent** requests (Section 4.2) or requests protected by an
  idempotency key, to avoid duplicating side effects.
- **Exponential backoff**: increase the wait time between retries exponentially (e.g., 100ms, 200ms, 400ms...) rather
  than retrying immediately, to avoid hammering an already-struggling service.
- **Jitter**: add randomness to backoff intervals so many clients retrying simultaneously (e.g., after a shared
  dependency recovers) don't all retry in lockstep and re-cause the exact overload they're recovering from ("thundering
  herd," also relevant in Section 12).

### 7.4 Circuit breakers, bulkheads

- **Circuit breaker**: after a downstream dependency fails repeatedly, the caller "opens the circuit" and stops calling
  it for a cooldown period (failing fast locally instead), then periodically allows a trial request through ("half-open"
  state) to check if the dependency has recovered before fully closing the circuit again. Prevents wasting resources on
  calls that are very likely to fail, and gives the failing dependency room to recover instead of being hit by continued
  retry traffic.
- **Bulkheads**: isolate resources (thread pools, connection pools) per-dependency so that one slow/failing downstream
  service can't exhaust resources shared with calls to other, healthy dependencies — named after ship
  compartmentalization, where one flooded compartment doesn't sink the whole ship.

### 7.5 CDN (Content Delivery Network)

- A geographically distributed set of edge servers that cache content **closer to users**, reducing latency and
  offloading the origin server.
- **How it works**: DNS (often GeoDNS/Anycast, Sections 2.5/6.5) routes a user to the nearest edge location; if that
  edge already has the requested content cached, it serves it directly ("cache hit"); otherwise it fetches from the
  origin, caches it, and serves it ("cache miss").
- **Origin pull vs push**:
    - **Pull**: edge servers fetch and cache content **on-demand** the first time it's requested (lazy) — simpler, most
      common default.
    - **Push**: content is proactively uploaded/synced to edge servers **ahead of time** — used when you want to
      guarantee content is warm everywhere before traffic arrives (e.g., a big scheduled release).
- **Cache invalidation**: because content is now duplicated across many edge locations, updating/removing it requires
  explicit invalidation (purge API call) or relying on TTL expiry — "cache invalidation is one of the two hard problems
  in computer science" is a cliché for a reason; being able to discuss versioned URLs/cache-busting (e.g.,
  content-hashed filenames) as an alternative to explicit purging is a good practical point.

### 7.6 Caching layers

Requests can be satisfied at multiple layers before ever reaching the origin server — worth being able to enumerate them
in order:

1. **Browser cache** — client-side, governed by `Cache-Control`/`ETag` (Section 4.2).
2. **CDN / edge cache** — shared across users, geographically distributed.
3. **Reverse proxy cache** (e.g., Nginx, Varnish in front of app servers) — shared across users hitting a given data
   center/region.
4. **Application-level cache** (e.g., Redis/Memcached) — application-controlled, often used for computed/derived data,
   not just raw HTTP responses.

Each layer trades off staleness risk against reduced load on the layer behind it — a good system design answer
identifies which layer is appropriate for which kind of data (highly personalized data generally can't sit in a shared
CDN cache; public, rarely-changing assets are ideal for it).

### 7.7 Rate limiting algorithms

| Algorithm          | How it works                                                                                                                                         | Notes                                                                                                                                                                 |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Token bucket**   | Bucket refills with tokens at a fixed rate, up to a max capacity; each request consumes a token; no token = request rejected/delayed                 | Allows controlled **bursts** up to the bucket size while enforcing a long-term average rate — the most commonly used approach in practice                             |
| **Leaky bucket**   | Requests enqueue into a fixed-size bucket and are processed ("leak out") at a constant rate                                                          | Smooths bursts into a strictly steady output rate — good when downstream truly cannot handle bursts at all                                                            |
| **Fixed window**   | Count requests in fixed time windows (e.g., per calendar minute); reset the counter each window                                                      | Simple, but allows request bursts at window boundaries (e.g., a spike straddling the end of one window and start of the next can briefly allow ~2x the intended rate) |
| **Sliding window** | Smooths the fixed-window boundary problem by weighting the previous window's count based on overlap, or tracking a rolling log of request timestamps | More accurate rate enforcement at the cost of more bookkeeping                                                                                                        |

Rate limiting typically gets applied at the **API gateway/edge layer** (Section 8) so abusive/excessive traffic is
rejected before consuming backend resources — tying directly back to the DDoS/API-security discussion in Section
5.3/5.5.

---

## 8. Networking in Distributed Systems / Microservices

### 8.1 Service discovery

In a dynamic environment where service instances scale up/down and get rescheduled (containers, autoscaling), hardcoded
IPs don't work — services need a way to find each other:

- **Client-side discovery**: the calling service queries a registry directly and chooses which instance to call (and can
  apply its own load balancing) — e.g., Netflix Eureka-style patterns.
- **Server-side discovery**: the caller just calls a stable endpoint (e.g., a load balancer or DNS name); something
  else (the LB, the mesh's sidecar) looks up the registry and routes the request — simpler for clients, more infra to
  run.
- **DNS-based discovery**: services register themselves under a DNS name (common in Kubernetes — every Service gets a
  cluster-internal DNS name); simplest to integrate but limited by DNS caching/TTL granularity for fast-changing
  membership.
- **Service registry**: the backing store of "which instances are currently healthy and where" (e.g., Consul, etcd, or
  Kubernetes' own API server + kube-dns) — typically updated via health checks and instance registration/deregistration
  on startup/shutdown.

### 8.2 API Gateway

A single entry point that sits in front of a collection of backend services, commonly handling:

- Routing requests to the correct backend service (often L7, path/host-based)
- Authentication/authorization enforcement in one place rather than duplicated per service
- Rate limiting, request/response transformation, and aggregation (e.g., a mobile client makes one gateway call that
  fans out to multiple backend services and combines the results — sometimes called the "Backend for Frontend" pattern)
- TLS termination, centralized logging/metrics for cross-cutting observability

### 8.3 Service mesh

- Adds a **sidecar proxy** (commonly Envoy) next to every service instance; all inter-service traffic flows through
  these sidecars rather than directly service-to-service.
- The sidecars are managed by a **control plane** (e.g., Istio) that pushes configuration — enabling mesh-wide
  capabilities without changing application code: automatic **mTLS** between services (Section 5.1),
  retries/timeouts/circuit breaking (Section 7.3/7.4) enforced consistently, fine-grained traffic shifting (canary
  releases, A/B routing), and rich observability (every hop is instrumented uniformly).
- **Interview framing**: a service mesh essentially moves cross-cutting networking concerns (security, resilience,
  observability) out of application code and into shared infrastructure — a natural follow-up to "how would you add
  mTLS/retries consistently across 50 microservices without touching each one's code."

### 8.4 Sync vs async inter-service communication

- **Synchronous** (REST/gRPC): caller waits for a response; simpler mental model and easier to reason about, but couples
  the caller's availability/latency to the callee's, and can cascade failures.
- **Asynchronous** (message queues like SQS/RabbitMQ, event streaming like Kafka): caller publishes and moves on;
  decouples services in time (callee doesn't need to be up *right now*) and load (buffers bursts), at the cost of added
  complexity — eventual consistency, harder request tracing, and needing to design for at-least-once/idempotent message
  processing.
- Real systems mix both: synchronous for user-facing request/response paths where an immediate answer is needed,
  asynchronous for background processing, cross-service side effects, and decoupling write-heavy from read-heavy paths.

### 8.5 Network partitions and CAP theorem

- **CAP theorem**: during a **network partition** (P — which *will* happen in any real distributed system), a system
  must choose between **Consistency** (every read gets the latest write) and **Availability** (every request gets a
  response, possibly stale) — you cannot have both during the partition.
- This is a networking-grounded concept, not just a database one: it's directly a consequence of the network being
  unreliable (partitions, dropped/delayed messages) — worth connecting explicitly in interviews rather than reciting CAP
  as pure trivia.
- Practical framing: most real systems are **CP** or **AP** by design choice for specific data (e.g., a leader-based
  system rejecting writes without quorum is choosing C over A during a partition; a system serving possibly-stale cached
  data during an outage is choosing A over C).

### 8.6 Multi-region networking & latency-aware routing

- Placing services/data closer to users reduces latency but introduces cross-region replication lag, consistency
  tradeoffs (ties back to CAP), and more complex failover logic.
- **Latency-aware routing**: directing a user's request to the nearest/lowest-latency healthy region — implemented via
  GeoDNS, Anycast, or an L7 global load balancer that's latency-aware, all covered in Section 6.5.
- Also worth knowing: cross-region network calls incur real, physically-bounded latency (speed of light over fiber) — a
  good sanity check in interviews when reasoning about whether synchronous cross-region calls are viable for a
  latency-sensitive path.

### 8.7 VPC concepts (cloud networking)

- **VPC (Virtual Private Cloud)**: an isolated, logically-defined virtual network within a cloud provider, typically
  carved into a CIDR range (Section 2.1) that you subnet further.
- **Public vs private subnets**: public subnets have a route to an internet gateway (instances can have public IPs / be
  reached from the internet); private subnets don't — instances there can only reach the internet outbound via a NAT
  gateway (Section 2.4), and can't be reached inbound directly, which is the standard pattern for databases/internal
  services.
- **Security groups**: stateful, instance-level firewalls (allow rules only — return traffic is automatically
  permitted).
- **NACLs (Network ACLs)**: stateless, subnet-level firewalls (both inbound and outbound rules must be explicitly
  defined, since return traffic isn't automatically allowed) — a common interview distinction: "stateful vs stateless,
  instance-level vs subnet-level."

### 8.8 Peering, VPNs, private links

- **VPC peering**: directly connects two VPCs so resources in each can communicate using private IPs, without traversing
  the public internet.
- **VPN**: encrypted tunnel over the public internet connecting, e.g., an on-prem data center to a cloud VPC, or a
  remote worker to internal infrastructure.
- **Direct Connect / private link style services**: dedicated, non-internet physical/logical connections between on-prem
  infrastructure and the cloud (or between VPCs), offering more predictable latency/bandwidth and avoiding public
  internet exposure entirely — high-level awareness that this category exists (and why you'd pay for it over a VPN) is
  generally sufficient depth for SDE-2/3.

---

## 9. Debugging & Tooling

### 9.1 Core tools and what each one tells you

| Tool                     | Layer / purpose        | What it tells you                                                                                                                                                                 |
|--------------------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ping`                   | ICMP, L3               | Basic reachability + round-trip latency to a host                                                                                                                                 |
| `traceroute` / `tracert` | ICMP/UDP, L3           | The hop-by-hop path packets take to a destination, and where latency/loss is introduced along the way                                                                             |
| `curl`                   | L7 (HTTP)              | Lets you inspect exact request/response including headers, status codes, timing breakdown (`curl -w`), and TLS handshake details (`-v`) — the go-to tool for HTTP-level debugging |
| `netstat` / `ss`         | L4                     | Active connections, their states (Section 3.1), listening ports, which process owns a socket                                                                                      |
| `dig` / `nslookup`       | DNS                    | Query DNS records directly, inspect TTLs, confirm which resolver/authoritative server answered, diagnose propagation/caching issues                                               |
| `tcpdump` / `Wireshark`  | L2–L7 (packet capture) | Captures actual packets on the wire for deep inspection — `tcpdump` for CLI capture/filtering, `Wireshark` for GUI analysis of the capture                                        |

### 9.2 Reading packet captures (basic level)

- Being able to identify, at a glance, a TCP handshake (`SYN` → `SYN-ACK` → `ACK`) vs a reset (`RST`) vs a graceful
  close (`FIN`) in a capture is a genuinely useful, commonly-tested skill.
- Spotting retransmissions (same sequence number appearing more than once) or duplicate ACKs in a capture directly
  signals packet loss or an unreachable/slow peer.
- For TLS, being able to identify the `ClientHello`/`ServerHello` and recognize a handshake failure (e.g., an alert
  message) vs the connection working fine but the *application* returning an error — this distinction (network/TLS-layer
  failure vs application-layer failure) is a very common real debugging fork.

### 9.3 Diagnosing common issues

- **Latency issues**: use `traceroute` to see where hops are slow, `curl -w` to break down DNS/connect/TLS/TTFB timing
  separately (rather than just "the request was slow" — knowing *which phase* was slow narrows the cause dramatically).
- **Connection resets**: often indicate the server (or an intermediate LB/firewall) actively rejected/killed the
  connection — vs. a **timeout**, which indicates no response was received at all. This distinction (
  `Connection refused` vs `Connection reset` vs timing out) maps to different root causes: refused = nothing listening
  on that port; reset = something actively tore down the connection (crash, firewall rule, idle timeout); timeout =
  packets aren't arriving/being answered at all (routing issue, firewall silently dropping, or an overloaded server not
  accepting new connections).
- **DNS failures**: use `dig`/`nslookup` to check whether the record resolves at all, whether it's returning a
  stale/incorrect IP (cache/TTL issue), or whether the authoritative server itself is misconfigured.

### 9.4 Socket states in practice

- `ss -tan` (or `netstat -tan`) showing a large number of connections stuck in `CLOSE_WAIT` on a server usually points
  to an **application bug** — the remote side closed, but the app never called `close()` on its end, leaking file
  descriptors over time until it hits the OS's FD limit.
- A large number of `TIME_WAIT` entries on a server making many short-lived outbound connections (e.g., to a downstream)
  can signal **ephemeral port exhaustion** risk (Section 3.1) — often mitigated with connection pooling/keep-alive (
  Section 7.2) rather than opening a fresh connection per call.

### 9.5 Debugging CORS, TLS, and timeout vs connection-refused

- **CORS issues**: always check whether it's a **preflight** failure (browser DevTools Network tab will show a separate
  `OPTIONS` request) vs the actual request succeeding but the browser blocking JS from reading the response due to a
  missing/incorrect `Access-Control-Allow-Origin`. Curl won't show you a CORS error at all (Section 5.4) — CORS is
  enforced by the *browser*, so reproducing "it works in curl but not the browser" is expected and doesn't mean the bug
  report is wrong.
- **TLS handshake failures**: `curl -v` or Wireshark will show exactly where the handshake failed — expired/untrusted
  certificate, hostname mismatch (SNI issue), or unsupported protocol version/cipher suite mismatch between client and
  server.
- **Timeout vs connection-refused**: a fast, immediate `Connection refused` means a host actively responded that
  nothing's listening on that port (or a firewall sent a `RST`); a hang until timeout means packets are going
  nowhere/being silently dropped (no response at all) — this single distinction is often the fastest way to bisect "is
  this a routing/firewall problem or an application problem" in a live incident.

---

## 10. Sockets & Low-Level Networking

### 10.1 Socket programming basics

- A **socket** is the OS-level abstraction representing one endpoint of a network connection, identified by a (protocol,
  local IP, local port, remote IP, remote port) tuple for a connected TCP socket.
- Basic server-side flow (TCP): `socket()` → `bind()` (attach to an address/port) → `listen()` (mark as ready to accept
  connections) → `accept()` (blocks until a client connects, returns a new socket for that specific connection) →
  `read()`/`write()` → `close()`.
- Basic client-side flow: `socket()` → `connect()` → `read()`/`write()` → `close()`.
- Most SDE-2/3 engineers won't hand-write raw socket code often (frameworks/libraries abstract this), but understanding
  this flow demystifies what's actually happening underneath every HTTP client/server library.

### 10.2 Blocking vs non-blocking I/O

- **Blocking I/O**: a call like `read()` halts the calling thread until data is available — simple to reason about, but
  means "one thread per connection" doesn't scale well to tens of thousands of concurrent connections (thread overhead,
  context-switching cost).
- **Non-blocking I/O**: a call returns immediately (with an indication that no data is ready yet, if that's the case)
  rather than halting the thread, allowing a single thread to juggle many connections — the foundation of
  high-concurrency servers (Node.js's event loop, Nginx's worker model, async frameworks generally).

### 10.3 I/O multiplexing: select/poll/epoll

- These are OS mechanisms letting a single thread **monitor many sockets at once** and get notified which ones are ready
  for reading/writing, instead of blocking on each individually or busy-polling.
- **`select`**: oldest, works everywhere, but scales poorly — O(n) scan over all monitored file descriptors on every
  call, and has a hard limit on the number of FDs it can watch.
- **`poll`**: similar O(n) scan, but removes the FD count limit of `select`.
- **`epoll`** (Linux): the modern approach — the kernel maintains the set of watched FDs and only returns the ones that
  are actually ready, making it much more efficient at high connection counts (O(active FDs) rather than O(all watched
  FDs)). This is *why* modern high-performance servers (Nginx, most async runtimes on Linux) can handle tens/hundreds of
  thousands of concurrent connections on modest hardware — sometimes called "the C10K problem" solution.
- **Interview framing**: you generally don't need to write epoll code yourself, but understanding that this is *what
  your async framework is doing under the hood* explains why event-loop-based servers handle high concurrency so much
  more efficiently than a thread-per-connection model.

### 10.4 Connection lifecycle at the socket level

- Tying back to Section 3.1: the socket-level lifecycle (`connect`/`accept` → data transfer → `close`) is the
  application-visible surface of the TCP state machine — e.g., calling `close()` triggers the `FIN` exchange, and a
  socket left un-closed after the remote end closes is exactly what produces the lingering `CLOSE_WAIT` states discussed
  in Section 9.4.

## 11. Cloud/Infra Networking Awareness

### 11.1 Cloud load balancer types

- Cloud providers typically offer both an L4 and L7 managed load balancer (Section 6.1), and being able to name the
  distinction with a concrete example is enough depth for most interviews — e.g., AWS's **NLB** (Network Load Balancer,
  L4 — extremely high throughput, preserves client IP, handles raw TCP/UDP) vs **ALB** (Application Load Balancer, L7 —
  path/host-based routing, native support for WebSockets, gRPC, and Lambda targets).
- Managed load balancers also typically integrate directly with the platform's health checks, auto-scaling groups, and
  certificate management (auto-provisioning/renewing TLS certs) — worth knowing these exist as managed capabilities
  rather than something you'd build yourself in a modern cloud-native stack.

### 11.2 Kubernetes networking basics

- **Pod-to-pod networking**: every pod gets its own IP, and the cluster networking layer (a CNI plugin) ensures any pod
  can reach any other pod's IP directly, cluster-wide, without manual NAT configuration — a foundational assumption of
  the Kubernetes networking model.
- **Services** — the abstraction for stable access to a set of (ephemeral, replaced-on-redeploy) pods:
    - **ClusterIP** (default): a stable virtual IP + DNS name, reachable only *within* the cluster — used for internal
      service-to-service calls.
    - **NodePort**: exposes the service on a static port on every node's IP — a basic way to reach it from outside the
      cluster, mostly used for dev/testing or as a building block for other exposure methods.
    - **LoadBalancer**: provisions an actual cloud load balancer (Section 11.1) pointing at the service — the standard
      way to expose a service externally in a cloud environment.
- **Ingress**: an L7 routing layer sitting in front of Services, handling host/path-based routing to different Services
  and (commonly) TLS termination — conceptually the Kubernetes-native equivalent of an API gateway/reverse proxy (
  Section 6.3/8.2), implemented by an **Ingress controller** (e.g., Nginx Ingress, Envoy-based controllers).
- **Interview framing**: Service = stable internal identity for a shifting set of pod IPs (solving service discovery,
  Section 8.1, within the cluster); Ingress = the entry point handling how external traffic gets routed in.

### 11.3 Multi-AZ / multi-region failover design

- **Multi-AZ (Availability Zone)**: AZs within a region are physically separate data centers with independent
  power/networking but low-latency links between them — the standard baseline for high availability within a region (
  e.g., a database with a synchronous standby in another AZ, or backend instances spread across AZs behind a load
  balancer so a single AZ outage doesn't take the service down).
- **Multi-region**: goes further — protects against an entire region being unavailable, at the cost of much higher
  replication latency between regions (ties back to Section 8.6's physical latency point) and harder consistency
  guarantees (ties back to CAP, Section 8.5).
- A good system design answer distinguishes *why* you'd reach for multi-region (disaster recovery for a whole-region
  outage, or serving genuinely global users with low latency everywhere) versus when multi-AZ alone is sufficient (most
  services, most of the time) — reaching for multi-region by default adds substantial complexity that isn't always
  justified.

### 11.4 Network cost/latency tradeoffs

- Cross-AZ and especially cross-region data transfer typically carries **real dollar cost** on cloud platforms in
  addition to latency cost — a detail worth mentioning in system design interviews when justifying architecture
  choices (e.g., keeping chatty services that call each other frequently within the same AZ, or using a regional cache
  to avoid repeated cross-region reads).
- NAT gateways, load balancers, and cross-AZ traffic are common, easy-to-overlook line items in real infrastructure
  cost — being able to say "this design would also incur cross-AZ/cross-region transfer costs" signals production
  experience beyond pure textbook correctness.

---

## 12. System Design Application

This section is less a set of standalone facts and more about **applying** Sections 1–11 together — the way these topics
actually get tested in system design interviews and show up in real production work.

### 12.1 Designing for high availability across regions

Pulling together Sections 6, 8, and 11: a highly-available multi-region design typically layers:

- **GSLB/Anycast/GeoDNS** (6.5) to route users to their nearest healthy region.
- **Health-check-driven failover** (6.4) so a region/AZ failure automatically redirects traffic elsewhere.
- An explicit **consistency vs availability** choice (CAP, 8.5) for cross-region data — e.g., active-active with
  eventual consistency and conflict resolution, vs active-passive with a clear single source of truth and a defined (and
  tested!) failover procedure with an accepted RPO/RTO.
- A good interview answer names the specific mechanism at each layer rather than saying "it auto-fails-over" — e.g., "
  Route 53 health checks + failover routing policy" or "a global load balancer with per-region health checks" shows
  concrete understanding.

### 12.2 Choosing protocols for different use cases

Directly applying Sections 3 and 4's protocol tradeoffs to concrete scenarios — a very common interview thread ("design
a chat app," "design a video streaming service"):

| Use case                        | Likely protocol choice                                                                                               | Why                                                                                                                                                                                             |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Chat app                        | WebSockets (or long-lived HTTP/2/QUIC streams)                                                                       | Full-duplex, low-latency, server needs to push unprompted (4.4)                                                                                                                                 |
| Live video streaming            | UDP-based (e.g., WebRTC) for real-time, or HTTP-based adaptive streaming (HLS/DASH over TCP) for on-demand/broadcast | Real-time favors UDP (stale frames are useless, 3.3); on-demand/broadcast favors HTTP because CDN caching (7.5) and client-side adaptive bitrate matter more than absolute lowest latency       |
| File upload (large files)       | HTTP/TCP, often chunked/resumable                                                                                    | Reliability and ordered delivery matter far more than latency; chunking allows resuming after a failure without restarting                                                                      |
| Real-time bidding (ad auctions) | Often custom protocols over TCP/UDP with very tight timeout budgets                                                  | Extremely latency-sensitive with strict SLAs (often single-digit ms) — timeouts, connection pooling (7.2/7.3), and sometimes UDP with application-level reliability are relevant considerations |
| Internal microservice calls     | gRPC (4.5) or REST                                                                                                   | gRPC when you control both ends and want performance/strong typing; REST for broader compatibility/simplicity                                                                                   |

The underlying skill being tested isn't memorizing this table — it's demonstrating the **reasoning process**: identify
the latency/reliability/ordering requirements of the use case first, then pick the protocol whose tradeoffs match,
citing the specific mechanism (e.g., "WebSockets because the server needs to push messages without the client polling").

### 12.3 Thundering herd & cache stampede

- **Thundering herd**: many clients/processes simultaneously woken up or retrying at once (e.g., after a shared
  dependency recovers, or many cron jobs firing at the same time), overwhelming the resource they're all converging on.
  Mitigated with **jitter** (7.3) so retries/wake-ups spread out instead of clustering.
- **Cache stampede** (a specific thundering-herd case): a popular cache key expires, and many concurrent requests all
  miss the cache simultaneously and hammer the origin/database at once to recompute the same value. Mitigations:
    - **Request coalescing/locking**: only let one request actually recompute the value; others wait for that result
      instead of all hitting the origin.
    - **Stale-while-revalidate**: keep serving the (slightly) stale cached value while one request refreshes it in the
      background, rather than letting the cache go fully empty.
    - **Jittered TTLs**: randomize expiration times slightly across keys so many keys don't expire in the exact same
      instant.
- This directly connects Sections 7.3 (backoff/jitter) and 7.6 (caching layers) into a single, very commonly-asked
  interview scenario.

### 12.4 Designing rate limiters & API gateways at scale

- At small scale, an in-process rate limiter (Section 7.7's algorithms) is enough; at scale, rate limiting needs to be *
  *coordinated across many gateway/API instances**, which usually means the counters live in a shared, fast store (e.g.,
  Redis) rather than each instance's local memory — otherwise a client could exceed the intended global limit by simply
  getting load-balanced across many instances that each think they're under budget.
- Distributed rate limiting introduces its own tradeoffs: a strictly accurate global counter requires a round trip to
  the shared store on every request (added latency, and the store itself becomes a critical dependency needing its own
  availability story); approximate approaches (e.g., each instance tracking a local budget synced periodically) trade
  strict accuracy for lower latency and reduced load on the shared store.
- API gateways at scale (Section 8.2) typically apply rate limiting **before** requests reach backend services —
  combining it with authentication and request validation at the edge means abusive/invalid traffic is rejected as early
  and cheaply as possible, before consuming any backend or database capacity.

### 12.5 Consistency vs latency in geo-distributed systems

- The closer you want strong consistency (every read reflects the latest write, globally), the more cross-region
  coordination/round trips are required before a write can be acknowledged — directly trading against latency, and again
  a direct consequence of physical network latency between regions (8.6) and the CAP theorem framing (8.5).
- Common real-world resolutions worth being able to name:
    - **Regional leader / single source of truth**: writes go to one region (lowest latency for that region's users,
      consistent globally), other regions read replicas that may lag slightly — simple, but non-leader regions get
      slower writes (extra round trip to the leader region) or must accept eventual consistency for local writes.
    - **Multi-leader / active-active with conflict resolution**: every region can accept writes locally (fast
      everywhere), but conflicting concurrent writes to the same data need a resolution strategy (last-write-wins,
      CRDTs, application-level merge logic) — trades implementation complexity for lower write latency everywhere.
    - **Tunable consistency per operation**: some systems let you choose consistency level per-request (e.g., "read from
      nearest replica, possibly stale" vs "read from quorum, guaranteed fresh") — putting the latency/consistency
      tradeoff decision at the point of use rather than baking one global choice into the whole system.
- **Interview framing**: the strongest answers explicitly state which specific data needs strong consistency (e.g.,
  financial balances, inventory counts) versus which can tolerate eventual consistency (e.g., view counts, activity
  feeds) — rather than applying one consistency model uniformly across an entire system.

---

### Suggested Depth by Level

- **SDE-2**: Solid grasp of sections 1–7, working knowledge of 8–10, basic awareness of 11–12.
- **SDE-3**: Fluency across all sections, especially able to reason through 8, 9, 11, 12 in system design interviews and
  real production debugging.
