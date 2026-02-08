# Spring Basics
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
   - Central interface that manages all components
   - It is THE spring container
   - Purpose:
     - Creates Beans
     - Dependency Injection
     - Lifecycle Management
     - Configuration Handling: Converting all properties files, XML, or Java annotations—into a uniform internal format called BeanDefinitions.
       - BeanDefinitions contain all metadata of bean like scope, constructor args, properties
     - Other misc services like event publishing and aop etc
   - ### Bean Factory:
     - Bare metal container
     - Parent of ApplicationContext
     - Only creates and manages beans
5. ### Spring AOP (Aspect Oriented Programming)
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

## Spring Boot Basics
1. Spring vs Spring Boot:
   - Spring Boot is an extension built on top of spring framework
   - Spring contains all low level infra
   - Spring boot's purpose is to make developement quick and easy to start
   - Spring Boot comes with autoconfiguration, embedded server and prewritten boiler plate
   - Spring boot generates FAT Jar that runs on JRE
   - Spring generates war and requires Tomcat server to deploy