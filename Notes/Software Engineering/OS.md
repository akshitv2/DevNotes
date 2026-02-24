# OS

1. ## Port and Socket
    - Port:
        - 16 bit numerical identifier assigned to a process on host
        - Exist at TCP layer of OSI
        - Range from 0 to 65535
    - Socket:
        - Endpoint for bidirectional flow of data
        - Contains:
            - $$\text{\{Protocol, Source IP, Source Port, Destination IP, Destination Port\}}$$
        - To OS whenever OS needs to talk, OS opens a socket, returns a read() and write() operations (similar to disk)
    - Port vs Socket:
        - Port: Whenever starting an app we get the error (bind/ port in use), port is already assigned to a different
          process
        - Socket: OS has a limit to how many sockets a process can have open (1024 by default but configurable). If the
          limit is reached by too many requests we get Denial of Service (DOS)
          - (In reality you'll probably hit thread worker limit first)

2. ## Process vs Service
3. ## Processor Architectures:
   - Common Architectures:
      - x86 (32 Bit architecture)
        - Named after 8086
        - Only address max 4gb RAM
        - Process data in smaller 32 bit chunks
        - Struggles with heavy tasks
        - No longer being made (pre-2005)
      - x64 (64 bit architecture):
        - Modern standard
        - Supports far more RAM
        - Data in 64 bit chunks, much more powerful
      - ARM (32 Bit)
        - 32 Bit smaller version of 64
        - Aimed for lower power consumption for e.g. Raspberry Pi,IoT
      - ARM64
        - 64 bit version
   -  x64 vs ARM64:
     - x64 CISC (Complex Instruction Set Computing):
       - Single command can contain complex instructions
       - Variable length instructions: 1 to 15 bytes
         - OS Needs complex decoders to parse commands and eat up energy
       - Modern chips actually translate CISC ops to simpler RISC Ops
       - Have discrete gpu, cpu, memory units requiring travel time and coordination
     - ARM64 RISC (Reduced Instruction Set Computing):
       - Simpler shorter instructions, which execute much quicker
       - Uses less power
       - Uniform instruction set, no complex parsing required
       - Use BigLittle Cores: Assigned based on process's requirements
       - Usually have Soc (System on Chip) Design:
         - CPU GPU and Memory all baked into one
         - Data transfer between is almost instant