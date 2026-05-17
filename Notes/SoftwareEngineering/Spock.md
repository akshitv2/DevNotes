# Spock Testing Documentation for Java Spring Boot APIs

This guide provides a comprehensive overview of writing unit and integration tests using the **Spock Framework** and **Groovy** for a Java Spring Boot application.

---

## 1. Introduction to Spock

Spock is a testing and specification framework for Java and Groovy applications. It combines the features of tools like JUnit, Mockito, and JBehave into a single, highly readable DSL (Domain Specific Language).

### Why Spock?

* **Expressive DSL**: Uses natural language blocks (`given`, `when`, `then`).
* **Data-Driven Testing**: Built-in support for data tables.
* **Powerful Mocking**: Built-in mocking and spying without needing Mockito.
* **Java Compatibility**: Seamlessly tests Java code using Groovy.

---

## 2. Anatomy of a Spock Specification

Every Spock test class extends `spock.lang.Specification`. Features (test cases) are defined as methods using string literals for names.

```groovy
import spock.lang.Specification

class CalculatorSpec extends Specification {

    def "should add two numbers correctly"() {
        given: "a starting point"
        def a = 5
        def b = 10

        when: "the action occurs"
        def result = a + b

        then: "verify the outcome"
        result == 15
    }
}

```

### Spock Lifecycle Blocks

* **`setup:` / `given:**`: Defines the preconditions and initializes objects.
* **`when:`**: Executes the stimulus (the code under test).
* **`then:`**: Asserts the expected conditions. Every line is an implicit assertion.
* **`expect:`**: Shorthand combining `when` and `then` for simple, stimulus-assertion logic.
* **`cleanup:`**: Releases resources (runs even if the feature fails).
* **`where:`**: Provides data for data-driven tests.

---

## 3. Data-Driven Testing (Spock Tables)

Spock’s `where` block allows you to run the same test logic against multiple datasets using a highly readable table format.

```groovy
class MathSpec extends Specification {

    def "should return the maximum of two numbers"() {
        expect:
        Math.max(a, b) == expected

        where:
        a  | b  || expected
        1  | 3  || 3
        7  | 4  || 7
        0  | 0  || 0
    }
}

```

* Columns are separated by a single pipe `|`.
* Input variables and expected outputs are visually separated by a double pipe `||` (optional, but highly recommended for readability).
* The feature runs once for every row in the table.

---

## 4. Integration Testing with MockMvc

To test Spring Boot controllers without spinning up a full HTTP server, use Spock alongside Spring’s `MockMvc`.

### Setup Dependency Requirements

Ensure your `build.gradle` includes `spock-spring`:

```groovy
testImplementation 'org.spockframework:spock-spring:2.3-groovy-3.0' 

```

### MockMvc Controller Specification

```groovy
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import spock.lang.Specification

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath

@WebMvcTest(UserController.class)
class UserControllerSpec extends Specification {

    @Autowired
    MockMvc mockMvc

    @SpringBean
    UserService userService = Mock()

    def "GET /users/{id} should return user data when found"() {
        given:
        def userId = "123"
        def expectedUser = new User(id: userId, name: "John Doe")

        interaction: "stub the service call"
        1 * userService.getUserById(userId) >> expectedUser

        when:
        def response = mockMvc.perform(get("/users/${userId}")
                                .accept(MediaType.APPLICATION_JSON))

        then:
        response.andExpect(status().isOk())
                .andExpect(jsonPath('$.id').value(userId))
                .andExpect(jsonPath('$.name').value("John Doe"))
    }
}

```

* **`@WebMvcTest`**: Slices the Spring context to load only the web layer components.
* **`@SpringBean`**: A Spock-Spring annotation used to inject a Spock mock into the Spring ApplicationContext, replacing any existing bean of that type.

---

## 5. Notable Spock Features

### Mocking and Stubbing

Spock combines mocking (verifying behavior) and stubbing (providing canned responses) into a unified syntax:

```groovy
// Creation
PaymentGateway gateway = Mock()

// Stubbing (Return a fixed value)
gateway.process(_) >> true 

// Verification (Assert it was called exactly once with specific arguments)
1 * gateway.process({ it.amount > 100 }) >> true

// Sequential Stubbing (Return true on first call, false on second, throw exception on third)
gateway.verify() >>> [true, false] >> { throw new RuntimeException("Network Error") }

```

### Exception Testing

Testing for exceptions in Spock is clean and does not require try-catch blocks or annotations.

```groovy
def "should throw IllegalArgumentException when age is negative"() {
    given:
    def person = new Person()

    when:
    person.setAge(-5)

    then:
    def exception = thrown(IllegalArgumentException)
    exception.message == "Age cannot be negative"
}

```

### `@Unroll`

By default, a data-driven test counts as a single test in build reports. Using `@Unroll` reports each row as an individual test case. You can use variables from the `where` block directly in the method name.

```groovy
import spock.lang.Unroll

@Unroll
def "checking if #number is even should return #expected"() {
    expect:
    NumberUtils.isEven(number) == expected

    where:
    number || expected
    2      || true
    3      || false
}

```

---

## 6. Strategies to Meet Code Coverage Goals

When targeting code coverage metrics (e.g., via **JaCoCo**), Spock and Groovy require specific considerations to avoid synthetic or unreached code traps.

### 1. Handling Groovy Generated Code

Groovy generates metadata and helper methods at compile time (e.g., `getMetaClass()`, `$getCallSiteArray`). To prevent these from skewing JaCoCo metrics:

* Ensure JaCoCo is updated to a recent version that automatically ignores methods annotated with `@groovy.transform.Generated`.
* Prefer writing production code in **Java** and test specifications in **Groovy/Spock**. JaCoCo will measure coverage on the clean compiled Java bytecodes without Groovy overhead.

### 2. Branch Coverage via Data Tables

Branch coverage requires executing every path (e.g., `if`, `else`, `switch` cases). Use Spock tables to structurally target every branch variation in a single feature method.

```groovy
def "should correctly apply discount tiers"() {
    expect:
    DiscountCalculator.calculate(cartValue) == expectedDiscount

    where:
    cartValue || expectedDiscount
    50        || 0.0   // Tests base condition
    150       || 0.1   // Tests Tier 1 branch
    500       || 0.2   // Tests Tier 2 branch
}

```

### 3. Verification of Void Methods

To get coverage on lines inside `void` methods or asynchronous blocks, explicitly verify the side effects or internal mock interactions. If a method does not return a value, asserting the interaction ensures that the block was executed:

```then:
1 * notificationService.sendEmail(*_)

```