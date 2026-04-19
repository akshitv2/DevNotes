---
parent: Spring
nav_order: 5
layout: default
---

# Spring Boot Starters

1. `Spring-boot-starter-security`
    - Provides authentication, authorization, and protection against common exploits (like CSRF).
    - Operates as a series of Servlet Filters that intercept requests before they reach your controllers.
    - Handles:
        - Authentication
        - Authorization
        - Principal
        - Grant Authority
    - Use security filter chain
        - **SecurityContextHolder**: The heart of Spring Security’s storage mechanism. It uses a ThreadLocal to store the
          SecurityContext, which contains the Authentication object of the currently logged-in user.
        - **AuthenticationManager**: The API that defines how Spring Security’s filters perform authentication. The most
          common implementation is ProviderManager.
        - **AuthenticationProvider**: These are responsible for specific types of authentication (e.g.,
          DaoAuthenticationProvider for username/password, JwtAuthenticationProvider for tokens).
        - **UserDetailsService**: A core interface used to retrieve user-related data. It has one method,
          loadUserByUsername, which returns a UserDetails object.
        - **GrantedAuthority**: Represents a permission or "role" granted to the principal.