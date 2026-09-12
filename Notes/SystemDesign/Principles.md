# Principles

## 1. SOLID Principles

1. **S**ingle Responsibility Principle: Each class should one have one reason to change i.e. one responsibility
    - e.g. `@Service` manipulates data, `@Repository` does db transactions
2. **O**pen/Closed Principle (OCP): Software entities should be open for extension, but closed for modification
    - Write code that accepts pluggable behavior where change is expected, so we don't change and break the earlier plug
      and play component
3. **L**iskov's Substitution Principle: Subtypes must be substitutable for their base types without altering
   correctness.
    - The idea is that the parent type makes a strong contract/strong set of commitments. The child class should also do
      the same
    - e.g. Transaction should return true only when completed not initiated so InternationalTransaction should do the
      same.
4. **I**nterface Segregation: Clients should not be forced to depend on interfaces they do not use.
    - i.e. create lean interfaces which only suit their purpose
    - .e.g a printer interface with (fax(), scan(), print()) doesn't apply to budget printers\
5. **D**ependency Inversion Principle: High levels modules should not be dependent on lower level ones instead use
   abstractions
    - i.e. bean wiring in spring (Dependency injection is an impl of this design)

### 2. CUPID Principles
Created as a counter to overly technical principles of SOLID which are rarely well applicable to enterprise code
1. C – Composable: Plays well with others. Code should have a small surface area, reveal its intent clearly, and minimize dependencies so it can easily combine with other components.
2. U – Unix philosophy: Does one thing well. Focuses on simple, consistent models with a clear single purpose. 
3. P – Predictable: Does what you expect, consistently. The code should be deterministic, robust, runtime-observable, and free of surprising side effects.  
4. I – Idiomatic: Feels natural. Follows standard language idioms and local team conventions to reduce cognitive load.  
5. D – Domain-based: The code structure and naming reflect the problem domain. Uses ubiquitous domain language and aligns boundaries with real-world business concepts.  