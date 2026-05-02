---
parent: Programming Core
nav_order: 2
layout: default
---

# Concepts

1. ### POM vs BOM
   - Project Object Model vs Bill of Materials
   - <table border="1">
     <thead>
       <tr>
         <th>Aspect</th>
         <th>POM</th>
         <th>BOM</th>
       </tr>
     </thead>
     <tbody>
       <tr>
         <td>Purpose</td>
         <td>Build &amp; configure a project</td>
         <td>Manage dependency versions</td>
       </tr>
       <tr>
         <td>Has code</td>
         <td>Yes</td>
         <td>Usually no</td>
       </tr>
       <tr>
         <td>Produces artifact</td>
         <td>Yes (jar/war)</td>
         <td>No (pom only)</td>
       </tr>
       <tr>
         <td>Uses <code>dependencyManagement</code></td>
         <td>Optional</td>
         <td>Required</td>
       </tr>
       <tr>
         <td>One per project</td>
         <td>Yes</td>
         <td>Shared across projects</td>
       </tr>
     </tbody>
   </table>
2. ### Object-Oriented Programming (OOP)
   - Four Pillars of Object-Oriented Programming
     1. Abstraction
        - Hiding complex implementation details and showing only the essential features of an object.
        - Reduces complexity by allowing the user to interact with a high-level interface
     2. Encapsulation
        - Bundling data (variables) and the methods that operate on that data into a single unit (a class)
        - restricts direct access to some of an object's components, which prevents accidental interference and misuse of data
     3. Inheritance
        - The mechanism by which one class (subclass) acquires the properties and behaviors of another class (superclass)
        - Promotes code reusability
     4. Polymorphism
        - Ability of a single interface to represent different underlying forms
        - 