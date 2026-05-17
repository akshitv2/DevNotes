Here is a 3-stage business use case for a banking API, designed to scale from a simple proxy to a complex orchestrator.

---

## Use Case: Retail Loan Eligibility and Offer API

This API helps a frontend application (like a mobile banking app) determine if a customer qualifies for a personal loan
and calculates their personalized interest rate.

### Phase 1: The Minimum Viable Product (MVP)

**Scenario:** A basic check to see if a customer is even allowed to apply for a loan based on their credit score.

* **Downstream System:** **Eligibility Service** (RestTemplate or WebClient call to an Eligibility downstream API).
* **Logic:**
* Accepts `customerId` in the request.
* Calls the Eligibility Service to fetch the customer's credit score.
* Applies a simple hardcoded condition: If `creditScore > 650`, return `eligible: true`; otherwise, return
  `eligible: false`.


* **Purpose:** Validates connection handling, basic error mapping, and simple data transformation.

---

### Phase 2: Advanced Logic with Externalized Configuration

**Scenario:** The bank wants to dynamically adjust its risk appetite and interest rates based on market conditions
without redeploying code.

* **Downstream System:** **Eligibility** (same as Phase 1).
* **Config Data (`application.properties`):**
* `loan.config.min-score-threshold=700` (Dynamic eligibility cut-off).
* `loan.config.base-rate=8.5` (Base interest rate percentage).


* **Logic:**
* Fetches the credit score from the downstream.
* Compares the score against the **configured threshold** (`700`) instead of a hardcoded value.
* If eligible, it applies a tier-based risk premium using logic compared against config:
* Score > 800: Return `base-rate` (8.5%).
* Score 700-790: Return `base-rate + 1.5%` (10.0%).
* Score < 700: Reject.

---

### Phase 3: Enterprise Orchestrator (Multi-Downstream)

**Scenario:** A complete, real-time loan underwriting decision engine. The bank now checks both credit worthiness and
internal financial health (debt-to-income ratio) before generating a formal loan offer.

* **Downstream Systems:**

1. **Eligibility Service** (Downstream).
2. **Core Banking Account Service** (Internal system to fetch the customer's average monthly income and existing monthly
   EMI liabilities).


* **Config Data (`application.properties`):**
* `loan.config.max-dti-ratio=0.45` (Maximum Debt-to-Income ratio allowed, e.g., 45%).
* `loan.config.base-rate=8.5`


* **Logic:**
* Calls both downstream (ideally in parallel using `CompletableFuture` or WebClient reactive streams) using the
  `customerId`.
* **Calculation Logic:** Calculates the Debt-to-Income (DTI) ratio:

$$\text{DTI} = \frac{\text{Existing EMIs}}{\text{Monthly Income}}$$

* **Decision Matrix:**
* If `creditScore` is below the configured threshold OR the calculated DTI exceeds `max-dti-ratio` (0.45), the loan is
  rejected.
* If both conditions pass, it calculates a final interest rate combining the base rate, credit score risk tier, and DTI
  risk factor.


* Returns a structured payload containing: approval status, maximum approved loan amount, and the calculated interest
  rate.