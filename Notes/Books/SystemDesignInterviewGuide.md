# System Design Interview

## Chapter 1: Scale from zero to millions of users

1. Single Server Setup:
    - Everything runs on single server
    - Extremely basic
    - User flow:
        - Client queries DNS, gets IP of website
        - Uses IP to connect to website using HTTP
        - Server returns HTML page or JSON response
    - ![img.png](img.png)
2. Single Server With DB:
    - self-explanatory
    - Can use RDB or NoSQL DB
3. Vertical vs Horizontal scaling:
    - Vertical or Scale Up:
        - Upgrade to more powerful machines with more compute/RAM
        - Has diminishing returns in terms of how far you can scale up
        - Comes with the benefit of not rewriting and not needing to parallel your code
    - Horizontal Scaling or Scale Out:
        - Add more machines to execute in parallel
        - Requires your code to be executed parallel
        - Requires load balancing too
4. Load Balancer:
    - Evenly distributes incoming traffic among webservers
    - Act as middle man proxies (not like dns servers which tell where to go)
    - For security load balancers use private IPs to communicate with servers
      - 
    - Process:
        - Request Arrives
        - Health checks servers
        - Based on algo chooses best one
        - Forwards to said server
        - Once response received sends back to client
    - Common Routing Algorithms:
        - Round Robin
        - Least Connections; i.e. Server with the least active sessions
        - IP Hash: To reliably route to same
        - Least Response Time
5. Demilitarized Zone (DMZ) and Virtual Private Cloud (VPC):
    - DMZ:
        - Subnetwork that contains and exposes org's services that are to be exposed to the internet
        - Acts as a buffer zone, this way you don't need to expose your VPC
        - Protects internal networks
        - Usually put inside DMZ with gateway exposing it, one more firewall exists behind it to isolate from main VPC
        - DMZ is a security pattern
    - VPC:
        - Private isolated section of a public cloud e.g. AWS, GCP
        - Locked off from public and provides:
            - Isolation
            - Control: Over ip ranges, subnets and routing tables
        - VPC is an infrastructure construct
    - IGW
6. Database Replication:
   - ![img_1.png](img_1.png)
   - Usually done with a master slave relationship
   - Write operations are only supported by Master node
   - Slave get copies of master DB and only supports read (when enabled)
   - Most applications are read heavy so having limited master works
   - //todo expand
7. Cache
   - Temporary storage area stores result of expensive queries/operations
   - Mitigates repeated calls to db
   - Read through Cache:
     - Web server first checks if cache has result of a query
     - If not queries db, stores response in cache and sends to user
   - Considerations:
     - When to use:
       - Data that is read frequently but modified rarely
       - Should not be used for data that is persisted i.e. cache is volatile
     - Expiration Policy:
       - Should be implemented to prevent data from existing in memory permanently
       - Should be long enough that it saves db calls
       - But short enough that it doesn't in memory for long times
     - Consistency:
       - Keeping data in store and cache in sync
       - Inconsistency: If data modifying transaction for cache and store is separate
     - Eviction Policy:
       - Once cache is full, decide which policy to use to remove items to make space for new
         - Common policies:
           - LRU (Least Recently Used)
           - LFU (Least Frequently Used)
           - FIFO (First in first out)

8. CDN (Content Delivery Networks)
   - ![img_2.png](img_2.png)
   - ![img_3.png](img_3.png)
   - Geographically dispersed servers used to deliver static content
   - Cache static content like images videos css js
   - Dynamic Caching
   - Process:
     - On first try the file doesn't exist on cdn, request goees to CDN but cdn requests Server
     - Fetches from origin server first time then caches based on header
     - On second try by user request 
   - Configuration:
     - Controlled using cache-control headers
     - `Cache-Control`:
       - `max-age`: This one is for browsers to cache file for how many seconds
       - `s-maxage`: (s:shared) tells CDN to keep file for max X seconds
       - `public` vs `private`: Private i.e. only for user's browser, public for all
       - `no-cache`: don't cache it
     - ETag Validation: If file hasn't changed on server just compare hash before discarding from CDN
   - Considerations:
     - Run by 3rd Party: Charged for data transfer in and out of CDN, do not cache infrequent use items
     - Set appropriate cache expiry to reduce refetching, but still be fresh
     - Fallback: CDNs can fail, clients should have ability to connect to origin if they do
   