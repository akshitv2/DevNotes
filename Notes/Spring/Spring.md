---
parent: Spring
nav_order: 1
layout: default
---

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
        - There are two types of IoC containers in Spring:
            1. BeanFactory
            2. ApplicationContext
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
    4. Aware Interfaces:
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
3. ### Bean Scopes
    - Singleton (default), Prototype, Request, Session, and Application
4. ### IOC Containers:
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
5. ### Spring AOP (Aspect Oriented Programming)
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

## Spring Boot Basics

1. ### Spring vs Spring Boot:
    - Spring Boot is an extension built on top of spring framework
    - Spring contains all low level infra
    - Spring boot's purpose is to make development quick and easy to start
    - Spring Boot comes with autoconfiguration, embedded server and prewritten boiler plate
    - Spring boot generates FAT Jar that runs on JRE
    - Spring generates war and requires Tomcat server to deploy
2. ### Auto-Configuration
    - Springboot handles configuring components for you based on Jars available
    - Components:
        1. Classpath:
            - Scans pom.xml/build.gradle
            - Autoconfigures JARs that you've added (as opposed to Spring where you also have to configure and use them
              yourself)
        2. Annotations:
            - Requires `@EnableAutoConfiguration` Annotation to work
            - Implicitly present in `@SpringBootApplication`
        3. Conditional Logic:
            - Also has logic to not create beans if user created ones exist
    - Can also be disabled selectively using
        - `@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })`
3. ### SpringBoot Starters
    - Essentially preconfigured templates bundling in all necessary dependencies
    - Are actually POM (Project Object Model)
    - Common Starters:
        1. `spring-boot-starter-web`
            - For building RESTful APIs
            - Contains Spring MVC, Embedded Tomcat, Jackson
        2. `spring-boot-starter-data-jpa`
            - For Relational DBs
            - Hibernate, Spring Data Jpa, HikariCP
        3. `spring-boot-starter-data-security`
            - For Authentication and Authorization
            - Spring Security core, web security configs
        4. `spring-boot-starter-test`
            - junit5, Mockito, assertj
        5. `spring-boot-starter-actuator`
            - for monitoring and management
            - health checks, metrics, env info endpoints

        - Third Party Starters:
            - Usually follow the pattern *-spring-boot-starter (e.g., mybatis-spring-boot-starter
4. ### Annotations:
    1. ### `@SpringBootApplication`:
        - Actually combines 3:
            1. @Configuration: Marks this class as source
            2. @EnableAutoConfiguration: Explained above
            3. @ComponentScan: Tells springboot to discover application's (user code's) beans
    2. ### Component Beans:
        - @Component:
            - Any general purpose bean
        - @Service:
            - Business Logic Layer
            - Specialized Component Bean
            - Intended to contain business logic with @Transactional and security (can also be done in component)
            - Mostly Smentantically different from Component
        - @Repository
            - Classes that talk to DB
            - Specialized Component Bean
            - Adds extra exception handling (JDBC, JPA, Hibernate)
    3. ### @Bean
        - Not used on classes like above but instead on method which returns an object you want Bean-ified
    4. ### @Configuration:
        - Advanced version of @Component
        - Does class proxying
        - Safe way to use @Bean annotation
        - Handles interbean dependencies in FULL MODE:
            - Full-Mode:
                - If beans are to be wired within one another
                - Singletons shouldn't have more than one instance
                - Ensures creation of beans with the wiring in correct order
                - Not used everywhere since this consumes more cpu and memory
                - Generates a proxy layer for referencing calling CGLib (Code generation Lib) proxy instead of actual
                  class at runtime
            - Lite Mode:
                - In component where you just need to wire in dependencies
                - Where there isn't scope of interwiring
                - otherwise will cause more than one instance
    5. ### @Controller/@RestController:
       - Both are controller
       - @Controller for serving webpage using JSP/Thymeleaf
       - @RestController for JSON REST APIs
5. ### Profiles:
   - 