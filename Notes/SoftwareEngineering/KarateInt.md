# Integration Testing Documentation: Spring Boot, Karate, and WireMock

This documentation outlines how to design, write, and optimize integration tests for a Java Spring Boot API using
Karate (BDD syntax) and WireMock (JSON-based file stubs).

---

## 1. Core Framework Features

### Karate

Karate is an open-source test automation framework that combines API test orchestration, assertions, and BDD principles
into a single engine without requiring Java boilerplate code for HTTP clients.

* **Native BDD Syntax (Gherkin):** Tests are written in standard Gherkin (`Given`, `When`, `Then`) within plain text
  `.feature` files.
* **Built-in HTTP Engine:** Eliminates the need for libraries like REST Assured or Apache HTTP client.
* **JSON/XML as First-Class Citizens:** Contains native engine tools to validate, parse, and deeply assert payloads
  using JSONPath expressions without object mapping logic.
* **Interoperability:** Can invoke standard Java utilities directly inside a `.feature` file via Java Interop if custom
  generation (e.g., encryption keys, complex tokens) is needed.

### WireMock

WireMock is an HTTP mock server simulator used to isolate the Spring Boot API from its downstream dependencies (e.g.,
external REST services, third-party payment gateways).

* **File-Based Stubbing Engine:** Scans specific paths (`src/test/resources/mappings` and `src/test/resources/__files`)
  to initialize stubs declaratively via JSON templates without writing Java configuration code.
* **Advanced Request Matching:** Evaluates runtime requests based on HTTP method, headers, cookies, query parameters,
  URL patterns, or exact JSON body structures.
* **Response Templating:** Leverages the Handlebars engine to read dynamic components of incoming requests and mirror
  them back inside the response payload.
* **Stateful Simulation (Scenarios):** Uses internal finite state machines (FSM) to alter mock behaviors dynamically
  across a chain of sequential HTTP invocations.

---

## 2. Environment Architecture & Setup

During integration testing, the Karate runner starts the Spring Boot context on a random port. Concurrently, an
in-memory WireMock server boots up, reading external network simulation mappings from static files. The Spring Boot
application property keys are mutated to route downstream HTTP clients directly into WireMock's address.

### Directory Structure

```text
src/test/resources/
├── karate-config.js          # Global initialization configuration for Karate
├── karate/                   # Feature files containing the API scenarios
│   └── user-registration.feature
└── wiremock/                 # WireMock asset root
    ├── mappings/             # JSON Stub descriptors
    │   └── get_user_profile.json
    └── __files/              # Static payload body templates
        └── user_profile_response.json

```

---

## 3. Recreating Complex Coverage Scenarios

To maximize code branch coverage (e.g., validation rules, fallback patterns, network retries, structural errors), use
these file-based WireMock mapping configurations.

### Scenario A: Matching by Correlation-ID / Unique Headers

To test edge cases or tracing logic without altering global mock payloads, restrict a stub's scope to requests featuring
a specific header pattern.

```json
{
  "request": {
    "method": "POST",
    "url": "/api/v1/payments",
    "headers": {
      "X-Correlation-ID": {
        "equalTo": "CORR-ERR-503"
      }
    }
  },
  "response": {
    "status": 503,
    "headers": {
      "Content-Type": "application/json"
    },
    "jsonBody": {
      "error": "Downstream Gateway Timeout",
      "code": "GW_TIMEOUT"
    }
  }
}

```

### Scenario B: Stateful Flows via WireMock Scenarios

To test features like polling status hooks, sequential state workflows, or account locking mechanisms, use WireMock's
state machine properties (`scenarioName`, `requiredScenarioState`, `newScenarioState`).

#### Step 1: Initial Polling (State: `Started`)

```json
{
  "scenarioName": "Order Process Delivery",
  "requiredScenarioState": "Started",
  "newScenarioState": "ORDER_PROCESSED",
  "request": {
    "method": "GET",
    "url": "/external/orders/456"
  },
  "response": {
    "status": 200,
    "jsonBody": {
      "orderId": "456",
      "status": "PENDING"
    }
  }
}

```

#### Step 2: Next Execution (State: `ORDER_PROCESSED`)

```json
{
  "scenarioName": "Order Process Delivery",
  "requiredScenarioState": "ORDER_PROCESSED",
  "request": {
    "method": "GET",
    "url": "/external/orders/456"
  },
  "response": {
    "status": 200,
    "jsonBody": {
      "orderId": "456",
      "status": "COMPLETED"
    }
  }
}

```

### Scenario C: Dynamic Response via Response Templating

To prevent maintaining thousands of distinct JSON mock variations, configure WireMock to echo dynamic inputs using
Handlebars variables.

> **Note:** Ensure response templating is enabled globally in your WireMock server configuration (
`--global-response-templating` or programmatic equivalent).

```json
{
  "request": {
    "method": "POST",
    "urlPattern": "/external/customers/([0-9]+)"
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "bodyFileName": "dynamic_customer_response.json",
    "transformers": [
      "response-template"
    ]
  }
}

```

Inside `__files/dynamic_customer_response.json`:

```json
{
  "customerId": "{{request.pathSegments.[2]}}",
  "transactionId": "{{request.headers.X-Request-ID}}",
  "processedTimestamp": "{{now format='yyyy-MM-dd\'T\'HH:mm:ss\'Z\''}}",
  "requestedEmail": "{{jsonPath request.body '$.email'}}"
}

```

---

## 4. End-to-End Test Implementation Example

### 1. Karate Feature File

Create your test definition at `src/test/resources/karate/user-registration.feature`:

```gherkin
Feature: User Registration Integration Flow

  Background:
    * url baseUrl
    * def uniqueId = "TEST-" + java.util.UUID.randomUUID().toString()

  Scenario: Verify successful user creation when downstream third-party validation passes
    Given path '/api/users'
    And header X-Correlation-ID = uniqueId
    And request { username: 'dev_engineer', email: 'test@domain.com' }
    When method post
    Then status 201
    And match response.userId == '#notnull'
    And match response.status == 'ACTIVE'

  Scenario: Handle downstream service failure cleanly
    Given path '/api/users'
    And header X-Correlation-ID = 'CORR-ERR-503'
    And request { username: 'dev_engineer', email: 'test@domain.com' }
    When method post
    Then status 502
    And match response.errorMessage == 'Dependency validation failed'

```

### 2. Spring Boot Bootstrapping Class

Use JUnit 5 to spin up the context, map properties, and automatically track branch coverage through standard execution.

```java
package com.company.api.integration;

import com.intuit.karate.junit5.Karate;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class IntegrationTestRunner {

    @LocalServerPort
    private int localPort;

    private static WireMockServer wireMockServer;

    @BeforeAll
    static void startWireMock() {
        wireMockServer = new WireMockServer(WireMockConfiguration.wireMockConfig()
                .port(8089)
                .usingFilesUnderClasspath("wiremock")
        );
        wireMockServer.start();
    }

    @AfterAll
    static void stopWireMock() {
        if (wireMockServer != null) {
            wireMockServer.stop();
        }
    }

    @Karate.Test
    Karate runAllTests() {
        // Pass local randomized application port to karate-config.js
        System.setProperty("demo.server.port", String.valueOf(localPort));
        return Karate.run("classpath:karate/user-registration.feature");
    }
}

```

---

## 5. Strategic Guide to Reaching Maximum Branch Coverage

To maximize your branch coverage percentage (e.g., targeting >90% code coverage in execution matrices like Jacoco),
structure testing targets against structural logic branches:

| Code Structural Branch Target            | WireMock Setup Tactic                                                                               | Karate Verification Pattern                                                       |
|------------------------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| **Happy Path Execution**                 | Normal stub matching with a valid status code 200/201 payload.                                      | Assert HTTP 200/201 alongside structure schema signatures.                        |
| **Input Parsing/Validation Constraints** | Stub configured to trigger when fields drop below schema limits.                                    | Supply malicious payloads and assert HTTP 400 Bad Request patterns.               |
| **Downstream Timeouts & Retries**        | Use WireMock's `"fixedDelayMilliseconds"` attribute in the mapping file response configuration.     | Ensure retry interceptors execute correctly and log clean fallback responses.     |
| **Upstream Service Crash**               | WireMock configured to supply an invalid payload signature or standard internal error 500.          | Check exception handlers block leaking structural exception traces back to users. |
| **Conditional Code Flags**               | Provide varying unique values in custom headers to trigger separate paths based on request content. | Orchestrate separate scenarios passing specific `X-Correlation-ID` values.        |

To achieve comprehensive branch coverage using integration tests, you must systematically map the control flow of your
Java application to your test inputs (Karate payloads) and downstream dependencies (WireMock stubs).

The following structured methodology details how to identify, target, and execute tests for every conditional branch in
your code.

---

## 1. Map Code Branches to Test Dimensions

Before writing tests, analyze the target feature code for conditional entry points. In a typical Spring Boot
application, branches exist across three main layers:

1. **Controller Layer:** Request validation, query param combinations, header checks.
2. **Service Layer:** Business logic rules, `if/else` conditions, `switch` statements, state transitions.
3. **Client/Gateway Layer:** `catch` blocks for HTTP errors, timeout handling, circuit breaker fallbacks.

To cover these systematically, use a **Branch Matrix Mapping** strategy:

| Business Condition      | Controller Input (Karate) | Downstream State (WireMock)        | Expected Target Branch Hit                    |
|-------------------------|---------------------------|------------------------------------|-----------------------------------------------|
| **Happy Path**          | Valid payload             | Returns `200 OK`                   | Core logic execution block                    |
| **Insufficient Funds**  | Valid payload             | Returns `422 Unprocessable Entity` | Business error exception branch               |
| **Gateway Timeout**     | Valid payload             | `FixedDelay(5000)` (Timeout)       | Circuit breaker / Fallback branch             |
| **Invalid Client Data** | Malformed payload         | Not invoked                        | Spring Validator / `@ControllerAdvice` branch |

---

## 2. Implement Data-Driven Testing in Karate

Instead of writing separate BDD files for every branch, use Karate's **`Scenario Outline`** feature. This allows you to
inject different permutations of inputs, expected headers, and WireMock states into a single test structure, ensuring
all branches are systematically executed.

### Example: Target Feature Code to Cover

```java
// Inside PaymentService.java
if(request.getAmount() >10000){
        logger.

warn("High value transaction requiring manual review");
    return PaymentStatus.PENDING_REVIEW; // Branch A
}

        try{
ResponseEntity<ExternalResponse> response = externalClient.call();
    if(response.

getBody().

isApproved()){
        return PaymentStatus.SUCCESS; // Branch B
    }else{
            return PaymentStatus.DECLINED; // Branch C
    }
            }catch(
ResourceAccessException e){
        return PaymentStatus.RETRY_LATER; // Branch D
}

```

### Corresponding Karate BDD Setup

By passing a flag or header (`X-Scenario`) from Karate, your application can route calls to specific WireMock stubs set
up to trigger the corresponding branches.

```gherkin
Feature: Comprehensive Branch Coverage for Payments

  Scenario Outline: Execute specific path for <condition>
    Given url baseUrl
    And path '/api/v1/payments'
    # Use the scenario header to let WireMock know which stub to match
    And header X-Scenario = '<scenarioHeader>'
    And request { orderId: 'ORD-100', amount: <amount> }
    When method post
    Then status <expectedStatus>
    And match response.status == '<expectedAppStatus>'

    Examples:
      | condition          | amount | scenarioHeader   | expectedStatus | expectedAppStatus |
      | High Value Limit   | 15000  | NO_WIRE_MOCK     | 201            | PENDING_REVIEW    |
      | Gateway Approved   | 250    | GATEWAY_APPROVE  | 200            | SUCCESS           |
      | Gateway Declined   | 250    | GATEWAY_DECLINE  | 200            | DECLINED          |
      | Gateway Timeout    | 250    | GATEWAY_TIMEOUT  | 503            | RETRY_LATER       |

```

---

## 3. Configure Multi-Scenario Stubs in WireMock

To support the data-driven approach above, configure WireMock to differentiate requests using headers, query parameters,
or body contents via `request.headers`.

```java
public void setupBranchCoverageStubs() {
    // Stub for Branch B (Approved)
    stubFor(post(urlEqualTo("/external/authorize"))
            .withHeader("X-Scenario", equalTo("GATEWAY_APPROVE"))
            .willReturn(aResponse()
                    .withStatus(200)
                    .withHeader("Content-Type", "application/json")
                    .withBody("{ \"approved\": true }")));

    // Stub for Branch C (Declined)
    stubFor(post(urlEqualTo("/external/authorize"))
            .withHeader("X-Scenario", equalTo("GATEWAY_DECLINE"))
            .willReturn(aResponse()
                    .withStatus(200)
                    .withHeader("Content-Type", "application/json")
                    .withBody("{ \"approved\": false }")));

    // Stub for Branch D (Timeout)
    stubFor(post(urlEqualTo("/external/authorize"))
            .withHeader("X-Scenario", equalTo("GATEWAY_TIMEOUT"))
            .willReturn(aResponse()
                    .withFixedDelay(5000))); // Triggers the ResourceAccessException catch block
}

```

---

## 4. Best Practices for Branch Coverage Verification

* **Isolate Database State:** If a branch changes its behavior based on database records (e.g., checking if a user
  exists), use Karate's `Background` block or a custom Java interop utility to clear and pre-populate the database
  before each scenario executes.
* **Assert Hidden Side-Effects:** Branch coverage isn't just about the HTTP response status. If a specific branch
  triggers an asynchronous event (like emitting a Kafka message or saving an audit log), query an explicit test endpoint
  or verification utility within Karate to confirm the action took place.
* **Monitor Live Reports:** Run your tests locally using `mvn clean test jacoco:report`. Open the target HTML index
  output (`target/site/jacoco/index.html`) immediately after execution to visually track exactly which lines/branches
  are highlighted in red (uncovered) vs green (covered).

Would you like to see how to write a custom Java utility helper that Karate can invoke directly to clean or seed your
database state between these scenario loops?