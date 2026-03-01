---
parent: Java
nav_order: 1
layout: default
---

# Java Basics

1. ### Access Modifiers
    - Determine where a particular class, method or variable can be used within code
    - Crucial for encapsulation
    - Table:
    - <table>
        <tr><th>Modifier</th><th>Class</th><th>Package</th><th>Subclass</th><th>World</th></tr>
        <tr><td><b>public</b></td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
        <tr><td><b>protected</b></td><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td></tr>
        <tr><td><b>Default</b> (no keyword)</td><td>Yes</td><td>Yes</td><td>No</td><td>No</td></tr>
        <tr><td><b>private</b></td><td>Yes</td><td>No</td><td>No</td><td>No</td></tr>      
      </table>
    - Package Private:
      - Also called default, member only accessible within same package
      
      - Note: Class path is not the same as same package:
      - Two classes could be at path `com.google.transcoder` but they can't access each either if they don't belong to same package
2. ###  