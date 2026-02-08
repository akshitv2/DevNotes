1. ## IOC & DI
   1. ### Inversion of Control (IoC)
      - Traditionally programmer dictates flow calls libraries
      - in IoC library code calls your code
      - The Spring Container:
        - Instantiates beans
        - Configures them
        - Assembles dependencies
        - Manages Lifecycle
   2. ### Dependency Injection
       - Method to provide an object with other objects it needs to function
       - Done using:
         - Constructor Injection (most recommended)
         - Field Injection (`@Autowired`): For prototyping
         - Setter Injection: Good for optional fields
   3.  ### How these changed EE:
       - Before IoC two problems existed:
         1. Tight Coupling: 
            - Since user had to implement libs, user code was polluted with framework logic
         2. Lookup Problem: 
            - Objects had to manually locate their dependencies i.e. find instance in memory
            - Used serviceLocator to find
         3. Not unit testable
       - Now:
         - Spring IOC injects dependencies into user code
         - No more boilerplate code to create a server
         - Can inflate and unit test each bean now
2. ## Bean Lifecycle
   1. ### Container Init:
      - Start of Spring IoC Container (not actual bean lifecycle yet)
   2. ### Bean Instantiation:
      - Container creates instance using definition (XML/Annotation)
   3. ### Population (Dependency Injection)
      - Injects dependencies
   4. ### Initialization Callback:
      - For executing custom init logic
      - Init Methods:
        - `postProcessBeforeInitialization()` is first called for all registered beans by spring (not for user)
        - `@PostConstruct` Recommended approach
        - `@Bean(initMethod = "...")` another way of calling specific code on init
      - BeanPostProcessor
        - Similarly `postProcessAfterInitialization()` is called by spring
        - Here for `@Transactional` and `@Async` Spring wraps bean in proxy
   5. ### Bean Ready for use
   6. ### Destruction:
      - When container shuts down
      - Calls `@PreDestroy` first
      - then `destroy()`
3. ### Bean Scopes
   - Singleton (default), Prototype, Request, Session, and Application
4. ### ApplicationContext
4. ### Spring AOP (Aspect Oriented Programming)
   - Way to centralize cross-cutting concerns like logging, security checks etc
   - Modularize all repetitive code to one class
   - Important to not use for business logic (this type of hidden injection can become fatal trying to understand execution order)
   - Makes modifications in these concerns simpler in future (only have to update one class)
   - Essentially run code before/after/around specific methods
   - Components:
     1. Aspect: Modularized cross-cutting concern
     2. Join Point: Point where you join your action like method invoked
     3. Advice: Defines at what point aspect steps in
        - Types:
          1. Before
          2. After
          3. Around
          4. After Returning
          5. After Throwing
   - Example:
     - Service:
       - ```java
         @Service
         public class OrderService {
             public void placeOrder() {
                System.out.println("Placing order");
             }
         }
         ```
     - Aspect:
       - ```java
         @Aspect
         @Component
         public class LoggingAspect{
            @Before("execution(* com.app.service.*.*(..))")
            public void logMethodCall(){
                System.out.println("LOGGING");
            }  
         }
         ```
     - Output:
       - ```text
         LOGGING
         Placing order
         ```
   - Pattern Matching & Annotations:
     - To avoid making lists on aspect end we can define a pattern `"execution(* com.app.service.*.*(..))"`
     - We can also create custom annotation 
5. 