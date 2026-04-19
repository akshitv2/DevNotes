---
parent: Spring
nav_order: 1
layout: default
---

# Spring Basics

1. # Spring vs SpringBoot
    - Spring is a comprehensive framework for building Java applications
    - SpringBoot is an extension of spring that simplifies the setup and deployment process. Essentially provides
      preconfiguration over spring
    - <table> <thead> <tr> <th>Feature</th> <th>Spring Framework</th> <th>Spring Boot</th> </tr> </thead> <tbody> <tr> <td><strong>Primary Goal</strong></td> <td>Provides a comprehensive model for modern Java apps (DI, AOP).</td> <td>Aims to shorten code length and provide the easiest way to run Spring apps.</td> </tr> <tr> <td><strong>Configuration</strong></td> <td>Manual configuration (XML or Java-based).</td> <td>Auto-configuration based on added dependencies.</td> </tr> <tr> <td><strong>Server</strong></td> <td>Requires an external server (e.g., Tomcat, Glassfish) to run.</td> <td>Comes with embedded servers (Tomcat, Jetty, or Undertow).</td> </tr> <tr> <td><strong>Boilerplate</strong></td> <td>High; requires a lot of setup for every new project.</td> <td>Low; "Starter" dependencies pull in everything you need automatically.</td> </tr> <tr> <td><strong>Approach</strong></td> <td>Un-opinionated (You decide everything).</td> <td>Opinionated (Pre-configured defaults for you).</td> </tr> </tbody> </table>
    - Use Spring only if you are building a highly customized enterprise application where you need granular control
      over every single bean and configuration

2. ## IOC & DI
    1. ### Inversion of Control (IoC)
        - Traditionally programmer dictates flow calls libraries
        - in IoC library code calls your code
        - Done by the spring container [🔗](#IOC-Containers)
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
3. ## Bean Lifecycle
    1. ### Container Init:
        - Start of Spring IoC Container (not actual bean lifecycle yet)
    2. ### Bean Instantiation:
        - Container creates instance using definition (XML/Annotation)
        - Note: If you use constructor-based injection, instantiation and dependency injection happen simultaneously.
    3. ### Population (Dependency Injection)
        - Injects dependencies using setter injection and autowired
    4. ### Aware Interfaces:
        - Set of interfaces that let bean interact with spring container itself:
        - Interfaces:
            1. BeanNameAware:
                - Provides the bean its own name
                - ```java
                   public class MyBean implements BeanNameAware {
                     @Override
                     public void setBeanName(String name) {
                       System.out.println("Bean name is: " + name);
                     }
                   }
                   ```
                - Useful for logging, debugging, or dynamic behavior based on bean name
                - Note: `@Qualifier` is not a sufficient alternative as it only works during dependency injection phase.
                  During runtime, you need the id (the name) of the bean to dynamically refer to it
            2. BeanFactoryAware
                - Gives access to the `BeanFactory`
            3. ApplicationContextAware
                - Gives access to the `ApplicationContext`
            4. EnvironmentAware
                - Gives access to Base environment
                - Mostly legacy and rarely used, instead `@Autowire Environment env` preferred.
                - Note: Same as Dependency injection in terms of what we get
                - Happens even earlier in lifecycle
                - Note:
                    - Order (simplified):
                        1. Bean instantiated
                        2. EnvironmentAware#setEnvironment() called
                        3. Dependency injection (@Autowired, constructor injection)
                            - Note: Spring's "Magic" (like @Autowired and @Value) is handled by a special bean called
                              the `AutowiredAnnotationBeanPostProcessor` which occurs after regular dependency injection
                              thus making `EnvironmentAware` useful since they execute earlier
                        4. @PostConstruct
                        5. Bean ready
            5. ResourceLoaderAware
                - Gives access to Spring ResourceLoader
    5. ### Initialization Callback:
        - For executing custom init logic
        - Init Methods:
            - `postProcessBeforeInitialization()` is first called for all registered beans by spring (not for user)
            - `@PostConstruct` Recommended approach
            - `@Bean(initMethod = "...")` another way of calling specific code on init
        - BeanPostProcessor
            - Similarly `postProcessAfterInitialization()` is called by spring
            - Here for `@Transactional` and `@Async` Spring wraps bean in proxy
    6. ### Bean Ready for use
    7. ### Destruction:
        - When container shuts down
        - Calls `@PreDestroy` first
        - then `destroy()`
4. ### Bean Scopes
    1. ### Singleton:
        - Only one instance of the bean is created per Spring IoC container.
        - Every request for that bean name will return the same cached instance.
        - **Use Case:** Stateless beans, such as Controllers, Services, and Repositories.
    2. ### Prototype:
        - A new bean instance is created every time the container receives a request for it.
        - **Use Case:** Stateful beans where each consumer needs its own independent instance.\
    3. ### Request:
        - A new bean instance is created for each individual HTTP request.
        - Scope: Only valid within a web-aware Spring ApplicationContext.
    4. ### Session
        - A single bean instance exists for the duration of an HTTP Session.
        - Scope: Only valid within a web-aware Spring ApplicationContext.
    5. ### Application
        - A single bean instance is created for the lifecycle of a ServletContext.
        - Scope: Only valid within a web-aware Spring ApplicationContext.

    - ℹ️Note: Meaning of "Only valid within a web-aware Spring ApplicationContext":
        - In a standard Java application (like a command-line tool or a desktop app), Spring doesn't know what an HTTP
          request or a Session is.
        - A "web-aware" context adds this capability by integrating with the Servlet Container:
            - Code is called not via standard method calls but calls with `HttpServletRequest` objects.
        - Singleton and prototype are exempt as they either return same or new at every getBean()
5. ### IOC Containers:
    - They are the Central interface that manages all components
    - It is **THE** spring container

    1. ### Bean Factory:
        - Basic IoC Bare metal container
        - Parent of ApplicationContext
        - Only provides basic functionality like dependency injection and bean lifecycle management
        - Code:
          ```java
          Resource resource = new ClassPathResource("beans.xml");
          BeanFactory factory = new XmlBeanFactory(resource);
          ```
            - This creates `BeanDefinition` from the XML
        - Note: The XML file in question here is old school XML config file
            - Example:
               ```xml
               <?xml version="1.0" encoding="UTF-8"?>
               <beans xmlns="http://www.springframework.org/schema/beans"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="
                      http://www.springframework.org/schema/beans
                      http://www.springframework.org/schema/beans/spring-beans.xsd">
  
                  <bean id="userService" class="com.example.UserService"/>
                  <bean id="userRepository" class="com.example.UserRepository"/>
                  </beans>   
              ```
    2. ### ApplicationContext
        - Advanced Version of `BeanFactory` (Actually extends `BeanFactory`)
        - Purpose:
            - Creates Beans
            - Injects Dependencies
            - Bean Lifecycle Management
            - Configuration Handling: Converting all properties files, XML, or Java annotations—into a uniform internal
              format called BeanDefinitions.
                - BeanDefinitions contain all metadata of bean like scope, constructor args, properties
            - Other misc services like event publishing and aop etc
6. ### Spring AOP (Aspect Oriented Programming)
    - Way to centralize cross-cutting concerns like logging, security checks etc
    - Modularize all repetitive code to one class
    - Important to not use for business logic (this type of hidden injection can become fatal trying to understand
      execution order)
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
7. ### Annotations:
    - Some provided by spring some higher level ones by springboot, all mentioned here [🔗](SpringBoot.md#Annotations)
8. `Filter`/`HandlerInterceptor`/WebFilter:
    - used for cross-cutting concerns
    - utilize the Chain of Responsibility pattern, though they are managed by different entities.
    - They are for server side processing i.e. requests coming to your app. For downstream calls check out
      `ClientHttpRequestInterceptor` and `ExchangeFilterFunction`
    - `HandlerInterceptor` is strictly for non-reactive (Spring MVC) applications. It relies on the Servlet API, which
      uses a thread-per-request model and blocking I/O.
    - A `WebFilter` allows you to intercept the request/response exchange without blocking the execution thread.
    - ### `Filter`:
        - allows you to intercept HTTP requests and responses.
        - The request enters the web container.
        - The filter processes it before it ever hits Spring's servlet. It is ideal for low-level tasks like IP
          blocking, compression, or logging raw request data.
        -
    - ### `HandlerInterceptor`:
        - allows you to intercept HTTP requests and responses at various stages of their lifecycle
        - To create an interceptor, you implement the HandlerInterceptor interface, which provides three key hook
          points:
            - preHandle(): Executed before the request reaches the Controller.
                - Returning true allows the request to proceed.
                - Returning false stops the execution chain (the Controller is never called).
            - postHandle(): Executed after the Controller has processed the request but before the view is rendered. You
              can use this to add extra attributes to the ModelAndView.
            - afterCompletion(): Executed after the entire request is finished and the view is rendered. This is
              typically used for resource cleanup or performance monitoring.
    - ### `WebFilter`:
        - functional interface used to intercept and process HTTP requests and responses in an asynchronous,
          non-blocking manner.
        - Non-Blocking: Built on Project Reactor, utilizing Mono<Void> to handle asynchronous logic without pinning
          threads.
        - Order of Execution: Filters are executed based on the @Order annotation or the Ordered interface. Lower values
          have higher priority.
    - ### When to Use Which?
      Use a Filter for:
        - Authentication and Authorization (agnostic of Spring logic).
        - Logging and Auditing raw HTTP requests.
        - Image/Data compression.
        - CORS (Cross-Origin Resource Sharing) configuration.
        - Use an Interceptor for:
            - Handling application-specific business logic.
            - Modifying the ModelAndView sent to the view.
            - Checking specific Controller annotations or permissions.
            - Performance monitoring of specific API endpoints.
8.  ### Web/Rest Clients
    - RestClient
        - Spring created RestClient recently (Spring 6) as a modern alternative to RestTemplate
        - RestClient is a synchronous, fluent API used to make HTTP requests.
        - Core Features
            - Synchronous Execution
            - Fluent API: Uses a method-chaining style (e.g., .get(), .uri(), .retrieve())
            - Infrastructure Reuse: It uses the same HTTP message converters and request factories as RestTemplate
            - Exception Handling: Provides simplified status code handling via .onStatus()
        - Example:
            - ```java
          // Creation
          RestClient restClient = RestClient.create();

          // GET Request
          String result = restClient.get()
          .uri("https://api.example.com/data")
          .retrieve()
          .body(String.class);

          // POST Request with Error Handling
          restClient.post()
          .uri("https://api.example.com/users")
          .contentType(MediaType.APPLICATION_JSON)
          .body(newUser)
          .retrieve()
          .onStatus(HttpStatusCode::is4xxClientError, (request, response) -> {
          throw new MyCustomException(response.getStatusCode());
          })
          .toBodilessEntity();
         ```
    - WebClient
        - WebClient is a non-blocking, reactive client used to perform HTTP requests
        - part of the Spring WebFlux module, allows use of asynchronous logic without dealing with threads
        - Reactive: It is built on Project Reactor, utilizing Mono (for 0-1 results) and Flux (for 0-N results) to
          handle data streams.
        - Example:
            - ```java
          WebClient client = WebClient.create("https://api.example.com");

          Mono<String> response = client.get()
          .uri("/data")
          .retrieve()
          .bodyToMono(String.class);
          ```

        - Mono and Flux:
            - Flux:
              A Flux represents a stream of 0 to N elements. It is used when you expect a collection of data or a
              continuous stream that may or may not terminate.    
              Can complete successfully (onComplete) or trigger an error (onError).
            - Mono:
              Represents a stream of 0 or 1 element. It is a specialized version of a Flux used when the result is a
              single value or an empty notification.  
              Emits at most one item.
    - Request/Respone Handlers
        - Interceptors:
            - allows you to intercept HTTP requests and responses at various stages of their lifecycle. It is primarily
              used for cross-cutting concerns like logging, authentication, and modifying the model before it reaches
              the view.
        - `ClientHttpRequestInterceptor` and `ExchangeFilterFunction`
          Spring provides two primary mechanisms for intercepting and modifying outgoing HTTP requests, depending on
          whether you are using the synchronous RestTemplate or the reactive WebClient.
        - ClientHttpRequestInterceptor
          This interface is used with RestTemplate (the blocking, synchronous HTTP client). It allows you to intercept a
          request before it is sent and modify the response after it is received.
        - ExchangeFilterFunction
          This interface is used with WebClient (the non-blocking, reactive HTTP client). It serves the same conceptual
          purpose as the interceptor but is designed for asynchronous streams.
        - Both allow for modifying parts of outbound request but you cannot modify request json in place (need to create
          a new one and seal it and replace it)
            - By the time the interceptor receives the byte[] body, the original object has already been serialized into
              a byte stream.
            - Spring WebFlux is built on functional, immutable principles. Both the ClientRequest and the data buffers (
              DataBuffer) are designed to be replaced rather than mutated.