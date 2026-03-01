---
parent: Java
nav_order: 2
layout: default
---

# Java Features

1. Streams
    - Introduced in java 8, Functional framework
    - Used to process collections
    - Do not modify original data, only produce results
    - Two Types of operations
        - **Intermediate operations** (filter,map) return another stream to be chained
        - **Terminal operations** (collect, for each, count) ends stream and give final result
    - Important operations:
        - Terminal:
            - `.collect(Collections.toList())` or to another collection
            - `reduce(_)`
            - `forEach(_)`
        - Intermediate:
            - `sorted()`
            - `peek()`
            - `distinct()`
            - `map()`
            - `flatMap()`
    - Note: Streams are generally slower than manual iteration or at best equal to.
        - WHY?
            - Built on abstraction layer, creates several objects
            - Boxing and Unboxing of primitives
            - JIT is extremely proficient at optimizing `for` loops
    - Note: Parallel Streams are mor efficient than manual iteration though

2. Records:
    - Class for transport of immutable data
    - Java automatically generates several standard members based on:
        - Immutable Fields: Creates a private final field
        - Constructor: Generates equivalent constructor
        - Getter (no setters)
        - Equals and Hashcode
        - toString
    - Difference:
        - Old DTOs:
            - ```java
              // 1. Traditional POJO (Plain Old Java Object)
              public class UserDTO {

              private final long id;
              private final String username;

                  public UserDTO(long id, String username) {
                      this.id = id;
                      this.username = username;
                  }

                  public long getId() { return id; }
                  public String getUsername() { return username; }

                  @Override
                  public boolean equals(Object o) { /* Boilerplate equals */ }
                  @Override
                  public int hashCode() { /* Boilerplate hashCode */ }
                  @Override
                  public String toString() { /* Boilerplate toString */ }

              }
              ```
        - Equivalent Record:
            - ```java 
                  public record UserRecord(long id, String username) {}
              ```
    - Can declare a constructor using compact construction
        - ```java
      record EmployeeSecond(int id, String name, String position){
      public EmployeeSecond {
      if (id < 0 ){
      throw new RuntimeException("Invalid ID");
      }
      }
      }
        ```

3. Sealed Classes:
    - Introduced in java 15
    - Restricts which other classes or interfaces may extend or implement them
    - Enhances modeling and scope of each class
    - A sealed class or interface uses the `sealed` modifier
    - `permits` keyword lists the classes authorized to extend it
    - Constraint:
        - All subclasses must be accessible by sealed class
        - Permitted subclass must directly extend the sealed class or interface
        - All subclasses must reside in same package
    - Why?
        - Sealed classes acts like an extension to final keyword in inheritance
        - Controlled inheritance limiting extending
        - Must be shipped together otherwise user could just substitute their own definition
    - Example:
        - ```java
             public sealed class Shape
                     permits Circle, Triangle {
                     public double area(){
                         return 0.0;
                     }
             }

               // Final subclass: cannot be extended further
                public final class Circle extends Shape{
                private final double radius;
                public Circle(double radius) { this.radius = radius; }

                     @Override
                     public double area() { return Math.PI * radius * radius; }
                }

                // Non-sealed subclass: opens inheritance back up
                public non-sealed class Triangle extends Shape {
                // Anyone can extend Triangle
                }
          ```

4. ### Java Modules (Project Jigsaw)
    - Introduced in JAVA 9, introduced a module system (against traditional classpath)
    - Need:
        - Move away from classpath, JVM would load the first found JAR at classpath with the same name be it right or
          wrong even if other jars exist
        - Strong encapsulation: Developers could access low level internal APIs, modules makes devs declare what is
          accessible outside
        - Modularisation: Move away from monolithic entity JRE to smaller moulds like java.base java.sql
    - Note: Low level APIs had been set as public because hundreds of low level libs are supposed to work together but
      not high level apps.
        - Strong encapsulation is like Sealed classes, fine-tuning and customizing access rather than 0 or 1 logic
    - Note: Java uses Module path not classpath:
      - Classpath Approach:
        - `java -cp "app.jar:connector.jar:driver-v1.jar:driver-v2.jar" com.example.Main`
        -  Finding classes is done lazily so two of the same can exist or none and Java doesn't know until it needs at runtime
      - Module Approach:
        - JVM builds a graph of modules before starting
        - looks for the needed class in module path
        - if multiple or none exist throws exception and fails to start
    - How to use?
        - Define descriptor - `module-info.java`
            - Example:
                - ```java
                       // Example: src/com.mycompany.service/module-info.java
                      module com.mycompany.service {
                      // Requires another module to function
                      requires java.sql;
                          // Exports a package to be accessible by other modules
                          exports com.mycompany.service.api;
                      }
                     ```
        - Needs a strict structure to be followed:
            - Root: `src/`
                - Module Name Directory: `com.mycompany.service/`
                    - Module Descriptor: `module-info.java`
                    - Package Directories: `com/mycompany/service/api/MyService.java`
        - Compile:
          - `javac -d mods/com.mycompany.service --module-source-path src $(find src -name "*.java")`
    - Note: Why isn't this popular?
      - Modern devs rarely manage dependencies manually, so no rush to migrate following this expensive process
5. Virtual Threads (Project Loon) [🔗](Threading.md#virtual-threads-project-loon) 
6. Scoped Values