---
parent: Spring
nav_order: 1
layout: default
---

# Spring Boot

1. # Spring Boot Starters
    - Definition: They are a set of convenient dependency descriptors. Opinionated templates that bundle all necessary
      libs and transitive dependencies
    - Core:
        1. `spring-boot-starter`: Core starter, provides logging, yaml, basic context
        2. `spring-boot-starter-web`: Core starter to build RESTful apps, mvc, Jackson and tomcat
        3. `spring-boot-starter-webflux`: For building reactive applications, using Netty for non-blocking asynchronous
           web service
    - Data and Persistence:
        1. `spring-boot-starter-data-jpa`: hibernate, jpa, hikariCP
        2. `spring-boot-starter-data-mongodb`
        3. `spring-boot-starter-data-redis`: Lettuce/jedis
    - Security and Operations:
        1. `spring-boot-starter-security`: secures all endpoints using spring security, basic auth, CSRF
        2. `spring-boot-starter-actuator`: provides prod features like health check and metrics
    - Testing:
        1. `spring-boot-starter-test`: Includes junit jupiter, hamcrest, mockito, assertJ
    - Third Party Starters:
        - Usually follow the pattern *-spring-boot-starter (e.g., mybatis-spring-boot-starter

2. ### Spring vs Spring Boot:
    - Spring Boot is an extension built on top of spring framework
    - Spring contains all low level infra
    - Spring boot's purpose is to make development quick and easy to start
    - Spring Boot comes with autoconfiguration, embedded server and prewritten boiler plate
    - Spring boot generates FAT Jar that runs on JRE
    - Spring generates war and requires Tomcat server to deploy
3. ### Auto-Configuration
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
4. ### Annotations:
    1. ### `@SpringBootApplication`:
        - "The springboot special":
        - Actually combines 3:
            1. @Configuration: Marks this class as source
            2. @EnableAutoConfiguration: Explained above [🔗](#Auto-Configuration)
            3. @ComponentScan: Tells springboot to discover application's (user code's) beans
    2. ### Stereotype Annotations:
        - Special annotations in Spring used to auto-detect and register beans in the application context.
        - ### @Component:
            - Any general purpose bean
        - ### @Service:
            - Business Logic Layer
            - Specialized Component Bean
            - Intended to contain business logic with @Transactional and security (can also be done in component)
            - More or less just semantically different from Component
        - ### @Repository
            - Classes that talk to DB
            - Specialized Component Bean
            - Adds extra exception handling (JDBC, JPA, Hibernate) and automatic exception translation
        - ### @Controller/@RestController:
            - Marks a class as a web controller handling HTTP requests
            - [Linked](#controllerrestcontroller)
    3. ### @Bean
        - Not used on classes like above but instead on method which returns an object you want Bean-ified
    4. ### @Configuration:
        - Advanced version of @Component
        - Does class proxying
        - Safe way to use @Bean annotation
        - Handles inter-bean dependencies in FULL MODE:
            - Full-Mode:
                - If beans are to be wired within one another
                - Singletons shouldn't have more than one instance
                - Ensures creation of beans with the wiring in correct order
                - Not used everywhere since this consumes more cpu and memory
                - Generates a proxy layer for referencing calling CGLib (Code generation Lib) proxy instead of actual
                  class at runtime
            - Lite Mode:
                - In component where you just need to wire in dependencies
                - Where there isn't scope of inter-wiring
                - Otherwise, will cause more than one instance
    5. ### @Controller/@RestController:
        - Both are controller
        - @Controller for serving webpage using JSP/Thymeleaf
        - @RestController for JSON REST APIs
5. ### Profiles:
   -