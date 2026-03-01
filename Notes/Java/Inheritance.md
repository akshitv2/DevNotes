---
parent: Java
nav_order: 2
layout: default
---

# Inheritance

- Fundamental Mechanic of OOP (Object Oriented Programming)
- Allows a new class to acquire fields and methods of existing class
- Inheritance implemented through `extends` for classes
- Constructors are not inherited, subclass constructor needs to call `super()` as first statement to init
- Subclass can override existing method
- In java one class can only extend one parent class

### Quirks:

- Constructors are not inherited but invoked (implicitly or explicitly depending on child class)
- A class declared `final` cannot be extended
- A method declared `final` cannot be overridden in a subclass
- No Multiple inheritance: Only one parent, avoids ambiguity when two parent classes have same method
- Method Hiding:If a subclass defines a static method with the same signature as a static method in the superclass, the
  subclass method hides the superclass method, rather than overriding it
  - i.e. Parent method can no longer be accessed through child class name

### Inheritance and Abstract Classes
- ### Abstract Class:
  - Class declared with abstract keyword
  - cannot be instantiated
  - Acts as template for subclasses (can contain both abstract (without a body) and non-abstract (with a body) methods)
  - To **inherit**, A subclass must override all abstract methods or also must be abstract
  - Used to share code amoing closely related classes
- ### Interfaces:
  - Reference type with only method signatures (abstract)
  - Defines the contract for what a class can do but provides no implementation
  - Use by using `implements` keyword