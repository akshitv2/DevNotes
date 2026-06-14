---
parent: Security
nav_order: 1
layout: default
title: Basics
---

# Basics

1. CSRF (Cross Site Request Forgery):
2. Cookie Security

### 1. Authentication Vs Authorization
- :
  - Authentication (AuthN) is the process of verifying who a user is.
  - Authorization (AuthZ) is the process of verifying what a validated user has permission to do.
  - Analogy: Authentication is showing your passport at security to prove your identity. Authorization is your
  boarding pass, which dictates whether you are allowed to enter the first-class lounge or board a specific plane.
  - Authentication Protocols: OpenID Connect (OIDC), SAML (Security Assertion Markup Language).
  - Authorization Protocols: OAuth 2.0 (which issues access tokens to grant specific application permissions).
- Authentication:
- Authorization:
  - Usually done by means of a JWT which contains allowed permissions
  - This is usually separate from Authentication JWT but can be combined
  - for e.g. {'drive':'user'}
    - Since this is signed, JWT can be verified by the receiving subsystem without needing to validate with authorization server 