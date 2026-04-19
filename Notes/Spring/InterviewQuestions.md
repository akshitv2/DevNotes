---
parent: Spring
nav_order: 10
layout: default
---

# Interview Questions

1. ### Why will you choose Spring Boot over Spring Framework ?
    - I would be choosing spring boot for its ability to accelerate development and simplify deployment.
2. ### What all spring boot starter you have used or what all module you have worked on ?
3. ### What is the purpose of the @SpringBootApplication annotation in a Spring Boot application ?
   The @SpringBootApplication annotation is the main configuration annotation in a Spring Boot app. It combines three
   important annotations:
    1. @Configuration → Marks the class as a source of Spring configuration.
    2. @EnableAutoConfiguration → Automatically configures Spring based on dependencies.
    3. @ComponentScan → Scans the package for components, services, and controllers.
4. ### Can I directly use @EnableAutoConfiguration ,@ComponentScan & @Configuration annotation in my main class , instead of using @SpringBootApplication annotation , if yes will my application work as expected ?
    - Yes, you can directly use these three annotations in your main class:
5. ### How Spring boot run() method works internally ?
    - The run() method of Spring Boot (i.e., SpringApplication.run()) starts and bootstraps the entire application
      internally.
    - Internally it:
        - Creates context
        - Loads config
        - Applies Autoconfig
        - Performs Component Scan
        - Registers Beans
        - Starts Server
6. ### What is Command line runner in spring boot ?
    - In Spring Boot, CommandLineRunner is an interface used to run code automatically before the application starts but
      all the beans are created.
7. ### What is dependency injection ?
    - Dependency Injection (DI) is a concept in which an object receives its dependencies from the container instead of
      creating them itself.
    - the Spring container automatically provides required objects (beans) to a class.
8. ### where you would choose to use setter injection over constructor injection, and vice versa ?
    - Constructor Injection and Setter Injection are used based on whether a dependency is mandatory or optional.
    - Use Constructor Injection when Dependency is required (mandatory) and Object cannot work without it
9. ### What is the difference between application.properties and application.yaml?
    - The most fundamental difference lies in structure: properties files use a flat, key-value pair format where each
      line is independent, whereas YAML uses a hierarchical structure based on indentation.
    - This hierarchy in YAML allows you to group related configurations together without repeating the prefix for every
      single entry, which significantly reduces verbosity and makes complex configurations much easier to scan at a
      glance.
    - YAML is more powerful because it inherently supports lists and maps.
10. ### What is the difference between yml & YAML ?
    - There is no functional difference between .yml and .yaml; they are the same file format
    - Both .yml and .yaml are valid and widely supported. yml exists due to legacy system limitations of three character
      extension names.
11. ### If I will configure same values in both properties then which value will be load in spring boot OR Who will load first properties or yml file ?
    - then application.properties takes higher priority and its value will be loaded
12. ### How to load External Properties in Spring Boot ?
    - Using VM Options or environment variables
13. ### How to map or bind config properties to java Object ?
    - In Spring Boot, you can bind configuration properties to a Java object using the @ConfigurationProperties
      annotation.
    - Steps to map properties to a Java object:

    1. Add properties in application.properties
       ```properties
        app.name=MyApp 
        app.version=1.0
       ```
    2. Create a POJO class
    ```java
    @ConfigurationProperties(prefix = "app")
    @Component
    public class AppConfig {
    
        private String name;
        private String version;
    
        // getters and setters
    }
    ```
14. ### How will you resolve bean dependency ambiguity ?
    - Using @Primary
    - Using @Qualifier (bean name)
    - Using @Resource (variable name)
15. ### What is bean scope & Can you explain different type of bean scope ?
    - Bean Scope defines how many instances of a bean are created and its lifecycle.
    - Types of Bean Scope
        - Singleton (default) → One instance per container
        - Prototype → New instance every time requested
        - Request → One instance per HTTP request (web apps)
        - Session → One instance per HTTP session (web apps)
        - Application → One instance per web application
          WebSocket → One instance per WebSocket session
13. ### How to define custom bean scope ?
    - Implement `Scope` interface and Register scope
    - use it on a bean
    - We define get and remove methods for our custom use case
13. ### Can you provide a few real-time use cases for when to choose Singleton scope and Prototype scope ?
    - 
14. ### Explain interceptors, filter functions
14. ### RestTemplate vs WebcClient
    - Async RT is thread per request
15. Keystore vs Truststore

16. Can you explain the purpose of Stereotype annotations in the Spring Framework ?
17. How can you define bean in spring framework ?
18. What is dependency injection ?

# From anjitagargi

## Core Spring Boot

1. ### What is Spring Boot?

   Spring Boot is an **open-source framework** built on top of the Spring Framework that simplifies the development of
   Java-based applications. It is designed to make it easier to create stand-alone, production-grade Spring-based
   applications with minimal configuration.

2. ### What are the advantages of Spring Boot?

   The main advantages of Spring Boot include:

    - **Auto-configuration**: Automatically configures Spring and third-party libraries based on project dependencies.
    - **Standalone**: Spring Boot applications can run as standalone Java applications.
    - **Production-ready**: Includes features like metrics, health checks, and externalized configuration.
    - **Microservice-ready**: Ideal for building microservices due to its lightweight and modular design.

3. ### What are the differences between Spring and Spring Boot?

    - **Configuration**: Spring requires extensive XML configuration or Java-based configuration. Spring Boot offers
      auto-configuration and minimal setup.
    - **Setup**: Spring projects typically need manual setup and configuration, while Spring Boot provides default
      configurations and embedded servers.
    - **Dependencies**: Spring Boot includes a variety of dependencies and auto-configuration out of the box, reducing
      the need for manual dependency management.
4. ### How to create a Spring Boot application using Maven?

   To create a Spring Boot application using Maven, follow these steps:

    1. Add the Spring Boot dependencies to your `pom.xml`:

       ```xml
       <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter</artifactId>
       </dependency>
       ```

    2. Create the main application class with `@SpringBootApplication` annotation:

       ```java
       import org.springframework.boot.SpringApplication;
       import org.springframework.boot.autoconfigure.SpringBootApplication;
 
       @SpringBootApplication
       public class Application {
         public static void main(String[] args) {
           SpringApplication.run(Application.class, args);
         }
       }
       ```

    3. Run your application using Maven:

       ```bash
       mvn spring-boot:run
       ```

5. ### How to create a Spring Boot project using Spring Initializer?

   To create a Spring Boot project using Spring Initializr:

    1. Visit [Spring Initializr](https://start.spring.io/).
    2. Choose the project metadata (e.g., Project, Language, Spring Boot version).
    3. Add dependencies.
    4. Click "Generate" to download a ZIP file containing your Spring Boot project.

6. ### What are Spring Boot Starters?

   Spring Boot Starters are a set of convenient dependency descriptors you can include in your application. They
   simplify the process of adding commonly used dependencies.

   Example of including a Spring Boot Starter in `pom.xml`:

    ```xml
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    ```
7. ### What is Spring Boot Actuator?

   Spring Boot Actuator provides production-ready features such as monitoring, metrics, and health checks. It helps in
   managing and monitoring your application in production environments.

8. ### How to connect Spring Boot to the database using JPA?
   To connect Spring Boot to a database using JPA:
    1. Add JPA and database dependencies to `pom.xml`:

       ```xml
       <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-data-jpa</artifactId>
       </dependency>
       <dependency>
         <groupId>com.h2database</groupId>
         <artifactId>h2</artifactId>
         <scope>runtime</scope>
       </dependency>
       ```

    2. Configure database settings in `application.properties`:

       ```properties
       spring.datasource.url=jdbc:h2:mem:testdb
       spring.datasource.driver-class-name=org.h2.Driver
       spring.datasource.username=sa
       spring.datasource.password=password
       spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
       ```

    3. Create JPA entity and repository:

       ```java
       @Entity
       public class User {
         @Id
         @GeneratedValue(strategy = GenerationType.AUTO)
         private Long id;
         private String name;
         // Getters and setters
       }
 
       public interface UserRepository extends JpaRepository<User, Long> {}
       ```
9. ### How to connect Spring Boot application to a database using JDBC?
   To connect Spring Boot to a database using JDBC:
    1. Add JDBC dependency to `pom.xml`:

       ```xml
       <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-jdbc</artifactId>
       </dependency>
       ```

    2. Configure database settings in `application.properties`:

       ```properties
       spring.datasource.url=jdbc:mysql://localhost:3306/mydb
       spring.datasource.username=root
       spring.datasource.password=root
       ```

    3. Create a `JdbcTemplate` bean:

       ```java
       import org.springframework.context.annotation.Bean;
       import org.springframework.context.annotation.Configuration;
       import org.springframework.jdbc.core.JdbcTemplate;
       import javax.sql.DataSource;
 
       @Configuration
       public class DataSourceConfig {
         @Bean
         public JdbcTemplate jdbcTemplate(DataSource dataSource) {
           return new JdbcTemplate(dataSource);
         }
       }
       ```
10. ### What is @RestController annotation in Spring Boot?

    The `@RestController` annotation is a combination of `@Controller` and `@ResponseBody`. It is used to create RESTful
    web services by marking a class as a web controller where every method returns a domain object instead of a view.

    Example:

    ```java
    import org.springframework.web.bind.annotation.GetMapping;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;

    @RestController
    @RequestMapping("/api")
    public class HelloController {
      @GetMapping("/hello")
      public String sayHello() {
        return "Hello, Spring Boot!";
      }
    }
    ```
11. ### What is @RequestMapping annotation in Spring Boot?

    The `@RequestMapping` annotation is used to map web requests to specific handler methods. It can be used at the
    class or method level to define the URL patterns for which the methods should be invoked.
12. ### How does Spring Boot simplify dependency management?

    Spring Boot simplifies dependency management by:

    - **Providing Starters**: Pre-configured dependency sets for common use cases.
    - **Auto-Configuration**: Automatically configures application components based on the included dependencies.
    - **Dependency Management**: Uses dependency management to handle version conflicts and ensure compatibility.
13. ### What is the role of embedded servers in Spring Boot?

    Embedded servers in Spring Boot allow applications to be run as standalone Java applications. Spring Boot includes
    embedded servers like Tomcat, Jetty, and Undertow, which simplifies deployment and reduces the need for external web
    server setup.

14. ### What are Profiles in Spring Boot?

    Profiles in Spring Boot are used to segregate parts of your application configuration and make it only available in
    certain environments. They help in managing different configurations for development, testing, and production.

15. ### How to disable a specific auto-configuration class?

    You can exclude a specific auto-configuration class by using the `@SpringBootApplication` annotation with the
    `exclude` attribute:

     ```java
     @SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
     public class MyApplication {
       public static void main(String[] args) {
         SpringApplication.run(MyApplication.class, args);
       }
     }
     ```
16. ### Can we create a non-web application in Spring Boot?

    Yes, you can create a non-web application in Spring Boot by setting the `spring.main.web-application-type` property
    to `none` in `application.properties`:

     ```properties
     spring.main.web-application-type=none
     ```
17. ### Difference between @Controller and @RestController?

    - `@Controller`: Used for creating web controllers that return views (HTML, JSP). Methods typically return the name
      of a view to be rendered.
    - `@RestController`: Used for creating RESTful web services. Methods return domain objects, and the response is
      serialized to JSON or XML.

    **[⬆ Back to Top](#table-of-contents)**

18. What are Profiles in Spring Boot?
    Profiles in Spring Boot allow you to segregate application configuration and make it available only in specific
    environments.

19. ### How do you handle exceptions in a Spring Boot application?

    You can handle exceptions using `@ControllerAdvice` and `@ExceptionHandler` annotations:

    ```java
    @ControllerAdvice
    public class GlobalExceptionHandler {
      @ExceptionHandler(Exception.class)
      public ResponseEntity<String> handleException(Exception ex) {
        return new ResponseEntity<>("An error occurred: " + ex.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
      }
    }
    ```
20. ### What is Swagger in Spring Boot?

    Swagger is a tool used to document and test RESTful APIs. In Spring Boot, you can integrate Swagger using the
    `springfox-swagger2` and `springfox-swagger-ui` dependencies.
    It generates interactive API documentation and provides a user interface for testing endpoints.
21. ### What is the difference between @Component, @Service, and @Repository annotations?

    - `@Component`: Generic stereotype for any Spring-managed component.
    - `@Service`: Specialized form of `@Component`, typically used for service-layer beans.
    - `@Repository`: Specialized form of `@Component`, used for data access layer beans with additional exception
      translation capabilities.
22. ### How do you test RESTful services in Spring Boot?

    You can test RESTful services using `@WebMvcTest` or `@SpringBootTest` with tools like `MockMvc`:

    ```java
    @WebMvcTest(HelloController.class)
    public class HelloControllerTest {
      @Autowired
      private MockMvc mockMvc;

      @Test
      public void testHello() throws Exception {
        mockMvc.perform(get("/api/hello"))
          .andExpect(status().isOk())
          .andExpect(content().string("Hello, Spring Boot!"));
      }
    }
    ```
23. ### What is the purpose of the @Autowired annotation?

    The `@Autowired` annotation is used for dependency injection. It allows Spring to automatically inject the required
    dependencies into a bean.
24. ### How do you handle CORS in Spring Boot?

    You can handle CORS by configuring it globally or at the controller level. For global configuration:

    ```java
    @Configuration
    public class WebConfig implements WebMvcConfigurer {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
          .allowedOrigins("http://localhost:3000")
          .allowedMethods("GET", "POST", "PUT", "DELETE");
      }
    }
    ```

25. ### How to implement caching in Spring Boot?

    To implement caching, add the `spring-boot-starter-cache` dependency and enable caching with `@EnableCaching`:

     ```xml
     <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-cache</artifactId>
     </dependency>
     ```

     ```java
     @Configuration
     @EnableCaching
     public class CacheConfig {
     }
     ```

    Use the `@Cacheable` annotation to cache method results:

     ```java
     @Service
     public class MyService {
       @Cacheable("myCache")
       public String getCachedValue(String key) {
         // Method logic
       }
     }
     ```
26. ### How to configure Spring Boot for asynchronous processing?

    Enable asynchronous processing with `@EnableAsync` and use `@Async` for asynchronous methods:

     ```java
     @Configuration
     @EnableAsync
     public class AsyncConfig {
     }
     ```

     ```java
     @Service
     public class MyService {
       @Async
       public CompletableFuture<String> asyncMethod() {
         // Asynchronous logic
         return CompletableFuture.completedFuture("result");
       }
     }
     ```
27. ### What is the purpose of @ComponentScan in the class files?

    The `@ComponentScan` annotation is used to specify the packages to scan for Spring components, such as `@Component`,
    `@Service`, `@Repository`, and `@Controller`.

     ```java
     @Configuration
     @ComponentScan(basePackages = "com.example.myapp")
     public class AppConfig {
     }
     ```
28. ### How do you enable HTTPS in a Spring Boot application?

    To enable HTTPS, configure SSL in `application.properties`:

    ```properties
    server.port=8443
    server.ssl.key-store=classpath:keystore.p12
    server.ssl.key-store-password=password
    server.ssl.key-store-type=PKCS12
    ```

    Place the `keystore.p12` file in `src/main/resources`.
