---
parent: Spring
nav_order: 3
layout: default
---

# Libraries

1. ## JDBC
    - Java Database Connectivity
    - Low-level standard API used to connect Java applications to relational databases.
    - It requires writing manual SQL queries and handling the mapping between database rows and Java objects.
    - Example:
        - ```java
      String sql = "SELECT name FROM users WHERE id = ?";
      PreparedStatement ps = connection.prepareStatement(sql);
      ps.setInt(1, 101);
      ResultSet rs = ps.executeQuery();
      if (rs.next()) {
      String name = rs.getString("name");
      }
        ```
2. ## JPA
    - Jakarta Persistence API
    - High-level specification for Object-Relational Mapping (ORM).
    - It is a set of interfaces and guidelines that describe how to manage relational data in Java applications using an
      Object-Relational Mapping (ORM) approach. (i.e. contains no code or implementation)
    - It allows developers to interact with the database using Java objects directly, with a provider (like Hibernate)
      automatically generating the SQL and managing the mapping.
    - JPA is built on top of JDBC, doesn't come with its own separate implementation.
    - Thus you can execute low-level SQL within a JPA-based project. This is often referred to as using Native Queries.
    - Example:
        - ```java
      User user = entityManager.find(User.class, 101);
      String name = user.getName();
        ```
3. ## Hibernate
    - Hibernate is an ORM Framework that implements the JPA specification.
    - While it follows JPA rules, it also includes additional features that JPA does not define.
    - Hibernate is a comprehensive framework that includes several modules to manage the lifecycle of Java objects in
      relation to a database.
    - Contains:
        1. The Persistence Engine
           This is the heart of Hibernate. It contains the logic to automate the mapping between Java classes and
           database tables.
        2. Session Management
           Hibernate provides a state-management system to track objects through their lifecycle.