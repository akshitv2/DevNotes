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
   - Restricts which other classes or interfaces may extend or implement them
   