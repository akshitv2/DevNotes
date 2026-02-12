# Netty

1. ## What is netty?
    - Asynchronous event driven networking framework for Java
    - Built on Java NIO

2. ## Architecture:
    1. Reactor Pattern:
        - Consists of 2 groups of threads:
            1. BossGroup:
                - Usually one thread accepting connections and designating it to worker
            2. WorkerGroup:
                - Group of threads that perform actual I/O, execute logic
                - Run the eventLoop
        - EventLoop And EventLoopGroup:
            - EventLoop:
                - Single thread that runs in infinite loop
                - Waits for events (IO, tasks, timers) processes and goes back to waiting
                - Runs on the worker thread
                - Each connection (called channel) only goes on one thread (so no thread switching issues) but each
                  thread has more than one
                  connection (many-to-one relationship)
                - OS notifies netty on change/response which thread checks on loop and works on
            - EventLoopGroup:
                - group of these threads
    2. ChannelPipeline
        - Uses interceptor filter pattern
        - Handlers process data:
            - InboundHandlers: example: Bytes to json
            - OutboundHandlers: example: Json to bytes
        - ChannelHandlerContext:
            - Dynamic handler flow control
        - This is where you define custom handlers to create your own software
            - example: Command handlers, Decoder in lettuce
    3. ByteBuf Memory buffer:
        - Native ByteBuffer is criticized (for requiring flip())
        - Note: ByteBuffer uses one pointer for both read and write. If you write to buffer and want to read you need to
          call `flip()` which moves pointer back (the amount of data you wrote). Without this you are just reading next
          garbage bytes.
          - Leads to double flip where you need to track which method flipped at end and which didn't.
        - ByteBuf from Netty has separate read and write pointers (thus no flip)