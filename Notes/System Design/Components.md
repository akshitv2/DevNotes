---
parent: System Design
layout: default
---

## Open Systems Interconnection Model

- conceptual framework developed by the International Organization for Standardization (ISO) in 1984
  <table>
  <thead>
    <tr>
      <th>Layer</th>
      <th>Name</th>
      <th>Function</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7</td>
      <td>Application</td>
      <td>Direct interaction with software applications (HTTP, FTP, SMTP).</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Presentation</td>
      <td>Data translation, encryption, and compression (SSL, SSH, JPEG).</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Session</td>
      <td>Manages connections (sessions) between applications (NetBIOS, SAP).</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Transport</td>
      <td>End-to-end communication, flow control, and error recovery (TCP, UDP).</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Network</td>
      <td>Routing and forwarding data packets between different networks (IP, ICMP).</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Data Link</td>
      <td>Node-to-node data transfer and MAC addressing (Ethernet, Switches).</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Physical</td>
      <td>Physical transmission of raw bitstreams over a medium (Cables, Hubs).</td>
    </tr>
  </tbody>
  </table>
- Data Encapsulation  
  As data moves down from Layer 7 to Layer 1, each layer adds a header (and sometimes a trailer) containing control
  information. This process is called encapsulation.
- When the data reaches the destination, it moves up from Layer 1 to Layer 7, and each layer removes its corresponding
  header; this is called decapsulation.

## Core Architectural Components

1. Load Balancer:
    - Acts as a reverse proxy to distribute incoming network or application traffic across a cluster of servers
    - to optimize resource utilization, maximize throughput, reduce latency, and ensure fault tolerance by preventing
      any single server from becoming a bottleneck.
    - Act as middle man proxies (not like dns servers which tell where to go)
    - For security load balancers use private IPs to communicate with servers, i.e. user never talks to server directly
    - Process:
        1. Request Arrives
        2. Health checks servers (using heartbeats)
            - If server fails heartbeat it is removed from the rotation
        3. Based on algo chooses best one
        4. Forwards to said server
        5. Once response received sends back to client
    - Session Persistence (Sticky Session):
        - If configured, ensures all requests from same user go to same backend server to maintain state
    - Common Routing Algorithms:
        - Round Robin
        - Least Connections; i.e. Server with the least active sessions
        - IP Hash:
            - Hash user's ip to reliably route to same
        - Least Response Time
        - Weighted Algorithms:
            - Assign weight to server with higher capacity (RAM/compute)
            - More weight = more requests
    - OSI Model Classification  
      Load balancers are generally categorized by the layer at which they operate:
        - Layer 4 (L4):
            - Operates at the Transport layer (TCP/UDP).
            - Makes routing decisions based on IP addresses and port numbers
            - Doesn't actually inspect the data
        - Layer 7 (L7):
            - Operates at the Application layer
            - Can inspect HTTP headers, cookies, and URLs to make "content-aware" routing decisions
    - Note:
        - DNS based routing:
            - Load balancing can also be done at dns level by routing users to different servers
            - The user connects directly to the server's IP address.

