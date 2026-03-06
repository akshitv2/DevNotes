---
parent: Programming Core
nav_order: 2
layout: default
---

# Communication Protocols:

1. ### Foundational Protocols:
    - These are responsible for the actual transfer of data packets between devices:
        1. TCP (Transmission Control Protocol):
            - Communication oriented protocol that guarantees reliability and order
            - Use three-way handshake, performs error checks and retransmission of lost packets
            - Used in all things, files, emails, websites
        2. UDP (User Datagram Protocol)
            - Focuses on speed of data transfer over reliability
            - Doesn't establish connection or check for errors, focuses on minimal latency
            - Used in live video, online gaming anywhere where packet loss has no/low consequences
2. ### Communication Paradigms:
    1. ### RPC
        - Remote Procedure Call
        - Allows one program to execute a procedure in a different computer's address space as if it's a local function
          call
        - Uses stubs which serialize the parameters into a message sent through tcp to server
        - Modern implementations like gRPC use Protocol Buffers for efficiency and bidirectional streaming
        - Can work synchronously, asynchronously, streaming unidirectionally or bidirectionally
        - Pro Cons:
            - 🟢 Efficient, low latency, no requirements to create interfaces (looks like native code)
            - 🔴 Tight coupling, brittle to changes
            - 🔴 Not usable across orgs due to Tight coupling and requires exposing internal functions i.e. only when
              both are in same high security env
            - 🔴 Are strictly typed thus requiring both ends to upgrade together
    2. ### SOAP:
        - Simple Object Access Protocol
        - Highly disciplined XML based protocol
        - Independent of transport protocol (HTTP,SMTP,TCP), uses WSDL (Web Services Description Language) to define
          contracts
        - Each soap message has Header (for metadata) and Body (payload)
        - 🔴 Uses XML which makes messages large and verbose, slower to parse
        - 🔴 Requires stricter WSDL Ecosystem
        - 🔴 Lack of human readability
        - 🟢 Highly structured with message delivery guarantees
    3. ### REST
        - Representational State Transfer
        - Built on top of REST
            - Note: HTTP ≠ REST: Rest is a paradigm with strict statelessness constraints. Http calls can be stateful.
              RPC and SOAP often run on http but don't look like it because they are meant for machine to machine
              communication
            - It is actually an architectural standard not a protocol
        - Utilizes standard HTTP methods: `GET` (Retrieve), `POST` (Create), `PUT` (Update/Replace), `PATCH` (Partial
          Update), and `DELETE`
        - Data usually in JSON Format
        - Constraints to be RESTful:
            1. Statelessness: Each request from client to server must contain all information necessary to complete the
               request without the server using stored context i.e. session
            2. Cacheability: Responses must implicitly or explicitly state themselves as cacheable or non cacheable
            3. Uniform interface: using Uri for resource id, resource i.e. json body, header contains its own
               description in how to process i.e. Content-Type
        - 🟢 Easy to understand and implement
        - 🟢 Uses user understandable language and methods
        - 🟢 Statelessness makes it instantly scalable
        - 🔴 Causes division into multiple requests for related resources which can be done in less in rpc or GraphQL
    4. ### GraphQL
        - Strongly typed Query language for APIs with a runtime for fulfilling these queries
        - Powerful in terms of controlling exactly how much data you need, no over or under fetching like REST APIs
        - Provides a single endpoint unlike REST
        - Uses SDL(Schema Definition Language) which is a strongly typed schema
        - Schema:
            - The schema defines data types and their relationship as well as queries and mutations allowed
            - Example:
                - ```graphql
                  # 1. The Schema (SDL)
                  type User{
                    id: ID!
                    username: String!
                    email: String
                  }
                  type Query{
                    user(id: ID!): User
                  }
                  type Mutation {
                    createUser(name: String!, email: String!): User!
                  }
              ```
            - Note: ! → Non-nullable, [Type] → List of Type, ID → Unique identifier scalar
        - Queries:
            - Client sends a POST request containing exactly what they want
                - Example:
                    - ```graphql
                      query {
                        users {
                          id
                          name
                          }
                      }
                  ```
                - Response:
                    - ```graphql
                      query {
                        user(id: "1") {
                          name
                          posts {
                            title
                          }
                        }
                      }
                    ```
        - Mutations (Write Data/Modify)
            - ```graphql
                mutation {
                  createUser(name: "Charlie", email: "charlie@email.com") {
                    id
                    name
                  }
                }
              ```
        - Resolvers:
            - Connect schema fields to actual data sources, essentially glue code connecting the query to actual DBs
            - example:
                - ```javascript
                     const resolvers = {
                         Query: {
                             users: () => db.users,
                             user: (_, {
                                 id
                             }) => db.users.find(u => u.id === id)
                         },
                         Mutation: {
                             createUser: (_, {
                                 name,
                                 email
                             }) => {
                                 const newUser = {
                                     id: Date.now().toString(),
                                     name,
                                     email
                                 };
                                 db.users.push(newUser);
                                 return newUser;
                             }
                         },
                         User: {
                             posts: (user) => db.posts.filter(p => p.authorId === user.id)
                         }
                     };
                  ```
    5. ## Message Queue:
        - Form of asynchronous service to service communication
        - Decouple the Producer and Consumer
        - Point to Point Communication: Allow for communication between one to another async
            - Allow round-robin/least loaded algos to distribute
            - Acknowledgements (ACKs): Ensure least once delivery, consumer sends ACK to publisher or else message is
              requeued
            - Persistence: Messages are often stored on disk to ensure they aren't lost if a service crashes before
              processing them.
        - Examples: RabbitMQ, IBM Mq
        - ### Message Brokers:
            - More complex orchestration pattern
            - Supports broadcasting i.e. more than point to point:
                - Can have publisher subscriber where one publishes to multiple
                - Can have brokers use routing logic to send to specific consumer based on some logic
            - Can translate data between different messaging protocols
        - ### Dead Letter Queues:
            - In case of message failing to be consumed i.e. no ACK being received on multiple attempts can become
              poison
              message
            - Eats up resources over and over again and blocks others
            - Routed to Dead Letter Queue based on:
                - Exceeding `MaxDeliveryAttemps`
                - Queue length limit: Exceeds the max number of messages in queue
                - Schema mismatch
        - ### Modern vs Legacy:
            - Legacy:
                - Simple Point to point communication
                - IBM MQ, RabbitMQ
                - Publish, Consume model, with destructive consumption on ACK
                - Logic is centred on broker
            - Modern Alternative: Message Streams