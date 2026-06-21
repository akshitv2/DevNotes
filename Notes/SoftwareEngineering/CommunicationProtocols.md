---
parent: Programming Core
nav_order: 2
layout: default
---

# Communication Protocols

---

## 1. Foundational Protocols

These protocols are responsible for the actual transfer of data packets between physical or virtual devices across a
network.

### TCP (Transmission Control Protocol)

* **Mechanism:** Connection-oriented protocol that guarantees reliable, ordered delivery of data.
* **Features:** Utilizes a three-way handshake to establish a connection, performs error checking, and handles
  retransmission of lost packets.
* **Use Cases:** File transfers, emails, and standard web browsing (HTTP/HTTPS).

### UDP (User Datagram Protocol)

* **Mechanism:** Connectionless protocol that prioritizes transmission speed over reliability.
* **Features:** Does not establish a formal connection, track packet state, or check for errors, resulting in minimal
  latency.
* **Use Cases:** Live video streaming, VoIP, and online gaming where minor packet loss has low consequences.

---

## 2. API & Remote Procedure Paradigms

Architectures and frameworks used for structured machine-to-machine communication and data fetching.

### RPC (Remote Procedure Call)

* **Concept:** Allows a program to execute a procedure or function in a remote computer's address space as if it were a
  local function call.
* **Mechanism:** Uses client/server "stubs" to serialize and deserialize parameters into messages sent over a transport
  layer (typically TCP).
* **Modern Implementations:** Frameworks like gRPC utilize Protocol Buffers (Protobuf) for high-efficiency binary
  serialization and support synchronous, asynchronous, or bidirectional streaming.
* **Characteristics:**
    * 🟢 Highly efficient, low latency, and highly readable since it behaves like native code without the overhead of
      building custom interface routing.
    * 🔴 Tight coupling makes services brittle to changes; require both client and server to upgrade simultaneously.
    * 🔴 Unsuitable for cross-organization APIs because it requires exposing internal function signatures
    * 🔴 Tries to mimic local function call which are predictable while rpc can fail due to any number of network issues
    * 🔴 Passing memory pointers locally is trivial, but doing so over RPC requires serializing and sending large amounts
      of heap data over the wire.
    * *Note: Modern frameworks like gRPC explicitly design away from the "hidden network call" illusion by making
      streams and network states clear.*

### SOAP (Simple Object Access Protocol)

* **Concept:** A highly disciplined, XML-based protocol strictly bound to formal contracts.
* **Mechanism:** Transport-independent (can run over HTTP, SMTP, TCP, etc.) and relies on WSDL (Web Services Description
  Language) to define strict interface contracts.
* **Structure:** Each message contains an explicit `Header` (for metadata/security context) and a `Body` (the data
  payload).
* **Characteristics:**
    * 🟢 Highly structured with built-in message delivery guarantees and formal security standards.
    * 🔴 Uses XML, making payloads large, verbose, and computationally expensive to parse.
    * 🔴 Requires managing a complex, strict WSDL tooling ecosystem.
    * 🔴 Extremely poor human readability compared to JSON.

### REST (Representational State Transfer)

* **Concept:** An architectural style (not a protocol) designed around network resources, typically built on top of
  HTTP.
    * *Note: HTTP $\neq$ REST. REST is a paradigm with strict architectural constraints. Raw HTTP calls can be stateful,
      and protocols like SOAP or RPC frequently run over HTTP without adhering to REST principles.*
* **Mechanism:** Utilizes standard HTTP methods for CRUD operations: `GET` (Retrieve), `POST` (Create), `PUT` (
  Update/Replace), `PATCH` (Partial Update), and `DELETE`.
* **Data Format:** Typically standardizes on JSON payloads.
* **Core Architectural Constraints:**
    1. **Statelessness:** Each request from a client must contain all the data necessary to understand and complete the
       request. The server cannot retain any session context.
    2. **Cacheability:** Responses must explicitly define themselves as cacheable or non-cacheable to optimize network
       efficiency.
    3. **Uniform Interface:** Resources are uniquely identified using URIs, representation is decoupled (e.g., JSON
       bodies), and messages are self-describing via HTTP headers (e.g., `Content-Type`).
* **Characteristics:**
    * 🟢 Intuitive, widely adopted, and easy to implement.
    * 🟢 Relies on human-readable formats and semantic HTTP verbs.
    * 🟢 Strict statelessness allows for instant horizontal scaling.
    * 🔴 Can lead to "over-fetching" or "under-fetching," forcing clients to make multiple sequential HTTP requests for
      related resources that could be fetched in a single call via RPC or GraphQL.

### GraphQL

* **Concept:** A strongly typed query language for APIs paired with a server-side runtime engine for executing queries.
* **Mechanism:** Exposes a single endpoint (typically via an HTTP `POST` request) and allows the client to request
  exactly the data fields required, preventing over-fetching or under-fetching.
* **Schema Definition Language (SDL):** A strictly typed schema defining data structures, object relationships,
  operations, and data mutations.
    * *Syntax Key: `!` indicates non-nullable, `[Type]` indicates a list of that type, and `ID` represents a unique
      scalar identifier.*
* **Example Schema:**
    ```graphql
    type User {
      id: ID!
      username: String!
      email: String
      posts: [Post]
    }

    type Post {
      id: ID!
      title: String!
    }

    type Query {
      user(id: ID!): User
    }

    type Mutation {
      createUser(username: String!, email: String!): User!
    }
    ```
* **Example Query & Response:**
    * **Client Query:**
        ```graphql
        query {
          user(id: "1") {
            username
            posts {
              title
            }
          }
        }
        ```
    * **Server JSON Response:**
        ```json
        {
          "data": {
            "user": {
              "username": "Alice",
              "posts": [
                { "title": "Introduction to Protocols" }
              ]
            }
          }
        }
        ```
* **Example Mutation:**
    ```graphql
    mutation {
      createUser(username: "Charlie", email: "charlie@email.com") {
        id
        username
      }
    }
    ```
* **Resolvers:** The underlying server-side glue code that maps individual schema fields to backend databases,
  microservices, or third-party APIs.
    ```javascript
    const resolvers = {
        Query: {
            user: (_, { id }) => db.users.find(u => u.id === id)
        },
        Mutation: {
            createUser: (_, { username, email }) => {
                const newUser = { id: Date.now().toString(), username, email };
                db.users.push(newUser);
                return newUser;
            }
        },
        User: {
            posts: (user) => db.posts.filter(p => p.authorId === user.id)
        }
    };
    ```

---

## 3. Event-Driven & Messaging Paradigms

Asynchronous architecture models used to pass data between isolated backend systems.

### Message Queues

* **Concept:** Form of asynchronous service-to-service communication used to decouple producers from consumers.
* **Point-to-Point Communication:** Designed for direct routing from one sender to a target receiver. If multiple
  consumers exist, messages are distributed using load-balancing algorithms (e.g., round-robin).
* **Acknowledgements (ACKs):** To guarantee at-least-once delivery, consumers must explicitly send an ACK back to the
  queue upon successful processing; otherwise, the message is requeued.
* **Persistence:** Messages are written to disk to ensure no data loss occurs if a broker service crashes mid-flight.
* **Dead Letter Queues (DLQ):** Unprocessable messages (poison messages) that continuously fail delivery are redirected
  to a DLQ to avoid blocking the main pipeline. Triggers include:
    * Exceeding a defined `MaxDeliveryAttempts`.
    * Breaching queue length bounds or timeouts.
    * Data schema mismatch payloads.
* **Legacy vs. Modern Architecture:**
    * *Legacy (Traditional Message Brokers):* Centered on the broker logic (e.g., IBM MQ, RabbitMQ). They rely on a
      destructive consumption model—once an ACK is received, the message is permanently deleted from the queue.
    * *Modern (Event Streams):* Log-centric streaming systems (e.g., Apache Kafka, Apache Pulsar) where messages are
      persistent, immutable append-only logs, allowing multiple consumers to replay historical streams independently.

### Publisher-Subscriber (Pub/Sub)

* **Concept:** An asynchronous, one-to-many broadcasting architecture pattern.
* **Mechanism:** Producers write messages to an isolated channel called a **Topic** managed by a standalone broker
  instance. Any number of isolated consumer systems can register as subscribers to that topic to receive identical
  broadcasted payloads.
* **Message Delivery Semantics:**
    1. **At-Most-Once:** The broker fires the message and immediately forgets it. High throughput and minimal latency,
       but susceptible to silent data loss.
    2. **At-Least-Once:** The broker holds messages in a buffer until a receipt ACK is returned. Requires the downstream
       subscriber to be completely **idempotent** to safely handle re-deliveries.
    3. **Exactly-Once:** Achieved by combining at-least-once mechanics with unique message UUID de-duplication layers to
       ensure data is processed perfectly exactly once.

### Webhooks

* **Concept:** Event-driven, server-to-server communication utilizing automated, user-defined HTTP callbacks.
* **Mechanism:**
    1. **Subscription:** Consumer Server A registers a target URL callback with Provider Server B.
    2. **Trigger:** An event occurs natively on Server B.
    3. **Payload:** Server B initiates an outgoing HTTP `POST` request directly delivering the event data payload to
       Server A's registered URL.
    4. **ACK:** Server A processes the payload and returns an immediate HTTP `2xx` success status. If a `5xx` error is
       received, Server B falls back to a retry strategy.

---

## 4. Real-Time Web Communication Paradigms

Mechanisms utilized to establish low-latency, real-time channels between clients (e.g., web browsers) and backend
servers.

### WebSockets

* **Concept:** A communication protocol providing full-duplex, bidirectional, persistent communication channels over a
  single TCP connection.
* **The Handshake Process:**
    1. **Initiation:** The client initiates a standard HTTP/1.1 request containing an explicit `Upgrade: websocket`
       header along with a unique security key.
    2. **Switching:** If supported, the server returns an `HTTP 101 Switching Protocols` status code response.
    3. **Tunnel Established:** The HTTP abstraction layer is dropped, leaving a raw, long-lived bidirectional TCP tunnel
       open for streaming low-overhead frames.
* *Note: Because server ports are public and client ports are secure/hidden, WebSockets must always be initialized by
  the client.*

### Server-Sent Events (SSE)

* **Concept:** A highly efficient, strictly unidirectional data streaming architecture from server to client over a
  persistent HTTP connection.
* **The Process:**
    1. The client initializes a connection natively via the HTML5 `EventSource` API.
    2. The client expects an HTTP response with a `Content-Type: text/event-stream` header.
    3. The server keeps the HTTP transport channel open indefinitely via standard HTTP keep-alive mechanisms, pushing
       down text data payloads as events occur.
* **Advantage:** Runs natively over HTTP/1.1 or HTTP/2, passing through corporate firewalls and reverse proxies
  seamlessly without complex configuration.

### Long Polling

* **Concept:** A legacy real-time emulation technique (historically grouped under "Comet" solutions) designed to mimic
  instant server push over short-lived HTTP connections.
* **The Process:**
    1. The client issues a standard HTTP request to the server requesting data updates.
    2. If no data is available, the server intentionally blocks/suspends the open response thread, holding the
       connection open until an update occurs or a timeout threshold is met.
    3. As soon as data is available, the server fulfills the pending HTTP request and sends the payload.
    4. The moment the client parses the response, it terminates the connection and immediately spins up a brand-new HTTP
       request, restarting the cycle.