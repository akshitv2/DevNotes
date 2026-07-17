---
parent: Security
---

# Security Notes Part 1

---

## 1. Authentication vs Authorization vs Accounting (AAA)

- **Authentication (AuthN)**: Proving *who you are* (login, MFA, biometrics, certificates).
- **Authorization (AuthZ)**: Determining *what you're allowed to do* (permissions, roles, scopes).
- **Accounting/Auditing**: Recording *what happened* (logs, audit trails, non-repudiation).

Interview tip: Interviewers love asking "explain the difference" as a warm-up — answer crisply, then pivot into a real example (e.g., "logging in with a password is AuthN; being blocked from an admin panel because you're not an admin is AuthZ").

---

## 2. Authentication Deep Dive

### 2.1 Factors of Authentication
- **Something you know**: password, PIN, security question
- **Something you have**: phone/OTP device, hardware token (YubiKey), smart card
- **Something you are**: fingerprint, face ID, retina scan
- **MFA/2FA** combines 2+ factors. Note: SMS OTP is a weak second factor (SIM swapping risk) — TOTP apps or hardware keys (FIDO2/WebAuthn) are stronger.

### 2.2 Password Storage
- Never store plaintext or use reversible encryption for passwords.
- Use slow, salted, adaptive hashing: **bcrypt**, **scrypt**, **Argon2** (Argon2id preferred today).
- Salting prevents rainbow-table attacks; per-user salts are mandatory.
- **Peppering**: an additional secret stored separately (e.g., in a KMS) added to the hash input for defense-in-depth.
- Pepper differs from salt: salt is stored with the hash, pepper is stored separately (app config/secret manager).

### 2.3 Passwordless / Modern Auth
- **FIDO2 / WebAuthn**: public-key based, phishing-resistant authentication using platform authenticators (Touch ID, Windows Hello) or roaming authenticators (YubiKey). No shared secret transmitted — server verifies a signed challenge.
- **Magic links**: email-based one-time login links; simpler UX but relies on email account security.
- **Passkeys**: consumer-friendly branding of WebAuthn credentials, syncable across devices via cloud (Apple/Google keychains).

### 2.4 Session vs Token-Based Auth
- **Session-based**: server stores session state (in memory/Redis/DB), client holds an opaque session ID (cookie). Easy to revoke; needs shared/sticky state across servers.
- **Token-based (stateless)**: server issues a signed token (e.g., JWT) containing claims; no server-side state needed to validate. Harder to revoke early (see JWT section).

---

## 3. Authorization Models

- **ACL (Access Control List)**: per-resource list of who can do what. Simple, doesn't scale well with many users.
- **RBAC (Role-Based Access Control)**: users assigned roles; roles have permissions. Easy to reason about, common in enterprise apps.
- **ABAC (Attribute-Based Access Control)**: decisions based on attributes of user, resource, action, and environment (e.g., "allow if user.department == resource.department AND time is business hours"). More flexible, more complex to audit.
- **PBAC / Policy-Based Access Control**: centralized policy engine (e.g., **OPA — Open Policy Agent**, using Rego language) evaluates requests against declarative policies. Popular in microservices/k8s for decoupling policy from code.
- **ReBAC (Relationship-Based Access Control)**: permissions derived from relationships between entities (e.g., Google Zanzibar model — "can view if owner OR shared-with"). Used by Google Drive-style sharing systems.
- **Principle of Least Privilege**: grant only the minimum access necessary.
- **Separation of Duties**: no single person/service should have end-to-end control over a sensitive process.

---

## 4. OAuth 2.0

OAuth 2.0 is an **authorization** framework — NOT an authentication protocol. It lets a third-party app get limited access to a resource on behalf of a user, without the app ever seeing the user's password.

### Key Roles
- **Resource Owner**: the user
- **Client**: the app requesting access
- **Authorization Server**: issues tokens (e.g., Auth0, Okta, Google)
- **Resource Server**: the API holding protected data

### Grant Types (Flows)
- **Authorization Code Grant**: the standard, most secure flow for server-side apps. User is redirected to auth server, logs in, auth server redirects back with a one-time `code`, which the backend exchanges for an access token (using a client secret). Token never touches the browser directly.
- **Authorization Code + PKCE (Proof Key for Code Exchange)**: mandatory extension for public clients (SPAs, mobile apps) that can't safely hold a client secret. Client generates a `code_verifier` and sends its hashed form (`code_challenge`) upfront; prevents authorization code interception attacks.
- **Client Credentials Grant**: machine-to-machine (no user involved) — service authenticates with its own client ID/secret to get a token.
- **Implicit Grant**: (deprecated) returned tokens directly in the URL fragment — vulnerable to leakage via browser history/referrers. Replaced by Auth Code + PKCE.
- **Resource Owner Password Credentials (ROPC)**: (deprecated/discouraged) app collects username/password directly — defeats the purpose of OAuth; only for legacy/trusted first-party apps.
- **Refresh Token Grant**: exchange a long-lived refresh token for a new access token without re-authenticating the user.

### Tokens
- **Access Token**: short-lived, sent with API requests (usually a Bearer token).
- **Refresh Token**: long-lived, used to mint new access tokens; must be stored very securely (httpOnly cookie, secure storage) and should be rotated on use (**refresh token rotation**) to detect theft.
- **Scopes**: define what the access token can do (e.g., `read:contacts`).

### Common Pitfalls
- Confusing OAuth (authorization) with authentication — using access tokens to "identify" users is a classic mistake (that's what OIDC is for).
- Not validating the `redirect_uri` strictly (open redirect / token theft).
- Missing PKCE for public clients.
- Storing tokens in localStorage (XSS-vulnerable) instead of httpOnly, secure cookies.

---

## 5. OpenID Connect (OIDC)

- A thin **authentication** layer built on top of OAuth 2.0.
- Adds an **ID Token** (a JWT) containing identity claims (`sub`, `email`, `name`, `iss`, `aud`, `exp`).
- Adds a standard `/userinfo` endpoint and standardized discovery (`/.well-known/openid-configuration`).
- This is what powers "Sign in with Google/Microsoft/Apple."
- Interview soundbite: "OAuth answers 'can this app access this data?', OIDC answers 'who is this user?'"

---

## 6. JWT (JSON Web Tokens)

### Structure
`header.payload.signature` — all Base64URL-encoded (NOT encrypted by default, just signed and encoded — anyone can decode and read the payload).

- **Header**: algorithm (`alg`) and token type.
- **Payload**: claims — registered (`iss`, `sub`, `aud`, `exp`, `iat`, `nbf`, `jti`), plus custom claims.
- **Signature**: HMAC or RSA/ECDSA signature over header+payload, used to verify integrity.

### Signing Algorithms
- **HS256**: symmetric (HMAC) — same secret signs and verifies. Fine for single-service systems.
- **RS256/ES256**: asymmetric — private key signs, public key verifies. Better for distributed systems (resource servers only need the public key).

### Common JWT Vulnerabilities
- **`alg: none` attack**: some libraries historically accepted unsigned tokens if the header said `alg: none`. Always enforce/whitelist expected algorithms server-side.
- **Algorithm confusion (RS256 → HS256)**: attacker takes a service's public key (often accessible) and uses it as the HMAC secret to forge a token, tricking a naive verifier expecting HS256. Fix: enforce expected algorithm explicitly, never trust the `alg` header from the token itself.
- **No expiration / long-lived tokens**: always set short `exp`.
- **No revocation**: JWTs are stateless — you can't easily invalidate one before expiry. Mitigations: short expiry + refresh tokens, maintain a deny-list/blacklist of revoked `jti`s, or switch to opaque/introspectable tokens for sensitive operations.
- **Sensitive data in payload**: payload is only base64-encoded, NOT encrypted — never put secrets/PII in a JWT unless using JWE (JSON Web Encryption).
- **Weak secret / secret in code**: HMAC secrets must be long, random, and stored in a secrets manager.

### JWT vs Opaque Tokens
- JWT: self-contained, stateless, verifiable without a DB call, but hard to revoke and can bloat request size.
- Opaque token: just a random string; resource server calls the auth server to introspect/validate it. Easy to revoke, adds a network hop/latency.

---

## 7. SAML (Security Assertion Markup Language)

- XML-based protocol for SSO, older than OAuth/OIDC, still dominant in enterprise/B2B (e.g., Okta, ADFS, enterprise SSO into SaaS products).
- Roles: **Identity Provider (IdP)** and **Service Provider (SP)**.
- Flow: user hits SP → SP redirects to IdP → IdP authenticates user → IdP posts a signed **SAML Assertion** (XML) back to SP via browser POST → SP validates signature and creates a session.
- SAML vs OIDC: SAML = XML, heavier, browser-focused, common in enterprise; OIDC = JSON/REST, lighter, mobile/SPA-friendly, common in consumer and modern API-driven systems.

---

## 8. Kerberos

- Ticket-based authentication protocol for trusted networks (classic use: Windows Active Directory, enterprise intranets).
- Core idea: a trusted third party (**KDC — Key Distribution Center**) issues time-limited tickets so a user doesn't send passwords repeatedly to each service.

### Flow (simplified)
1. Client authenticates once to the **Authentication Server (AS)** → receives a **Ticket Granting Ticket (TGT)**, encrypted with the KDC's key.
2. Client presents the TGT to the **Ticket Granting Server (TGS)** when it wants to access a specific service → receives a **Service Ticket**.
3. Client presents the Service Ticket to the target service → service decrypts it (it shares a secret with the KDC) and grants access.
4. All tickets are time-stamped and expire — mitigates replay attacks. Requires reasonably synced clocks between client/server (clock skew is a classic Kerberos troubleshooting issue).

- Single Sign-On within a domain: authenticate once, access many services without re-entering credentials.
- Contrast with OAuth: Kerberos is designed for trusted internal networks/domains; OAuth is designed for the open web/delegated third-party access.

---

## 9. Single Sign-On (SSO) — the Big Picture

- Goal: authenticate once, access multiple applications.
- Enterprise SSO commonly implemented via SAML or OIDC against a central IdP (Okta, Azure AD/Entra ID, Ping, Auth0).
- Benefits: better UX, centralized credential/policy management, easier offboarding (disable one account, lose access everywhere).
- Risks: single point of failure/compromise — if the IdP is breached, everything downstream is exposed. Mitigate with strong IdP hardening + MFA at the IdP.

---

## 10. Session Management

- **Session fixation**: attacker tricks victim into using a known session ID, then hijacks it after victim logs in. Fix: regenerate session ID on privilege change (login).
- **Session hijacking**: stealing a valid session token (via XSS, network sniffing, malware). Fix: HTTPS everywhere, httpOnly + Secure + SameSite cookies, short session lifetimes.
- **CSRF (Cross-Site Request Forgery)**: tricking a logged-in user's browser into making an unwanted request to another site. Fix: CSRF tokens, `SameSite=Lax/Strict` cookies, checking `Origin`/`Referer` headers.
- **Idle vs absolute timeout**: idle timeout logs out after inactivity; absolute timeout forces re-auth after a fixed period regardless of activity.
- **Cookie flags**: `HttpOnly` (JS can't read it, mitigates XSS token theft), `Secure` (HTTPS only), `SameSite` (mitigates CSRF).

---

## 11. Cryptography Essentials

### Symmetric vs Asymmetric
- **Symmetric** (AES): same key encrypts/decrypts. Fast, used for bulk data. Key distribution is the hard problem.
- **Asymmetric** (RSA, ECC): public key encrypts/verifies, private key decrypts/signs. Slower, solves key distribution, used for key exchange, signatures, certificates.
- **Hybrid approach** (what TLS actually does): use asymmetric crypto to securely exchange a symmetric session key, then use symmetric crypto for the actual data transfer (fast + secure).

### Hashing vs Encryption
- **Hashing** is one-way (can't be reversed) — used for integrity checks and password storage.
- **Encryption** is two-way (reversible with the key) — used for confidentiality.
- Never "encrypt" passwords — hash them.

### TLS/SSL
- TLS handshake: negotiate cipher suite → server presents certificate (chain of trust to a root CA) → key exchange (commonly Diffie-Hellman/ECDHE for forward secrecy) → symmetric session established.
- **Perfect Forward Secrecy (PFS)**: session keys aren't derivable even if the server's long-term private key is later compromised (ephemeral key exchange, e.g. ECDHE).
- **mTLS (mutual TLS)**: both client and server present certificates — common in service-to-service auth in microservices/zero-trust architectures (e.g., via a service mesh like Istio/Linkerd).
- Certificates: issued by CAs, contain public key + identity, validated via chain of trust; **certificate pinning** hardcodes an expected cert/key to prevent MITM even if a CA is compromised (common in mobile apps).

### Encryption at Rest vs In Transit
- In transit: TLS.
- At rest: disk/DB-level encryption (e.g., AES-256), envelope encryption using a KMS (data encryption key wrapped by a master key).
- **Tokenization**: replacing sensitive data (e.g., credit card numbers) with a non-sensitive token, mapping stored in a secure vault — common in PCI-DSS compliance to shrink audit scope.

---

## 12. Common Web Vulnerabilities (OWASP Top 10 flavor)

- **Injection (SQLi, NoSQLi, Command Injection)**: untrusted input concatenated into a query/command. Fix: parameterized queries/prepared statements, ORMs, input validation, least-privileged DB accounts.
- **XSS (Cross-Site Scripting)**: injecting malicious script into pages viewed by others. Types: stored, reflected, DOM-based. Fix: output encoding/escaping, Content Security Policy (CSP), avoid `innerHTML` with untrusted data.
- **CSRF**: see Session Management above.
- **SSRF (Server-Side Request Forgery)**: tricking a server into making requests to internal/unintended resources (e.g., cloud metadata endpoints `169.254.169.254`). Fix: allow-list outbound destinations, block internal IP ranges, disable unneeded URL schemes/redirects.
- **IDOR (Insecure Direct Object Reference)**: accessing another user's resource by guessing/changing an ID (e.g., `/invoices/1234` → `/invoices/1235`). Fix: enforce authorization checks on every object access, don't rely on obscurity.
- **Broken Access Control**: consistently ranked #1 in OWASP Top 10 — missing or misconfigured authorization checks.
- **Security Misconfiguration**: default credentials, verbose error messages, unnecessary open ports/services, unpatched software.
- **Insecure Deserialization**: deserializing untrusted data can lead to remote code execution in some languages/libraries.
- **Using Components with Known Vulnerabilities**: outdated dependencies — mitigated via SCA (Software Composition Analysis) tooling (Dependabot, Snyk).
- **Clickjacking**: embedding a site in an invisible iframe to trick users into clicking. Fix: `X-Frame-Options` / `frame-ancestors` CSP directive.
- **Open Redirect**: unvalidated redirect URLs abused for phishing.

---

## 13. Security Headers

- `Content-Security-Policy (CSP)`: restricts sources of scripts/styles/images — the single strongest XSS mitigation.
- `Strict-Transport-Security (HSTS)`: forces HTTPS, prevents downgrade/SSL-stripping attacks.
- `X-Content-Type-Options: nosniff`: prevents MIME-sniffing attacks.
- `X-Frame-Options` / `frame-ancestors`: clickjacking protection.
- `Referrer-Policy`: controls how much URL info leaks to third parties via the Referer header.
- CORS (`Access-Control-Allow-Origin`, etc.): not itself a security header for the server's own protection, but a browser mechanism controlling which origins can read cross-origin responses — a common interview gotcha ("CORS protects users, not servers").

---

## 14. Secrets Management

- Never hardcode secrets/credentials in source code or commit them to git.
- Use dedicated secret managers: **HashiCorp Vault**, **AWS Secrets Manager/KMS**, **Azure Key Vault**, **GCP Secret Manager**.
- **Envelope encryption**: encrypt data with a data key, encrypt the data key with a master key held in a KMS/HSM — limits blast radius and enables key rotation without re-encrypting all data.
- Rotate secrets regularly; use short-lived, dynamically generated credentials where possible (e.g., Vault dynamic DB credentials).
- Principle: secrets should be injected at runtime (env vars from a vault, sidecar injection), not baked into images.

---

## 15. Network & Infrastructure Security

- **Defense in depth**: layered controls so no single failure is catastrophic.
- **Zero Trust**: "never trust, always verify" — no implicit trust based on network location; every request authenticated/authorized regardless of origin (internal or external). Core tenets: verify explicitly, least-privilege access, assume breach.
- **Network segmentation**: separate networks/subnets (e.g., public DMZ vs private app tier vs data tier) to limit lateral movement.
- **Firewalls / Security Groups / NACLs**: control traffic by port/protocol/IP.
- **VPN**: encrypted tunnel for remote access to private networks (being superseded by Zero Trust Network Access / ZTNA in modern architectures).
- **WAF (Web Application Firewall)**: filters HTTP traffic for known attack patterns (SQLi, XSS payloads), often at the CDN/edge (Cloudflare, AWS WAF).
- **DDoS mitigation**: rate limiting, traffic scrubbing, CDN/anycast absorption, autoscaling.
- **API Gateway**: centralizes auth, rate limiting, request validation for all backend services.

---

## 16. Microservices & Cloud-Native Security

- **Service-to-service auth**: mTLS or short-lived JWTs between services, often managed by a **service mesh** (Istio, Linkerd) so app code doesn't handle crypto directly.
- **API Gateway** as the single ingress point enforcing authn/authz, rate limiting, schema validation.
- **IAM roles over static credentials**: cloud workloads should assume roles with temporary credentials (e.g., AWS IAM roles for EC2/Lambda/K8s service accounts) instead of embedding long-lived access keys.
- **Shared Responsibility Model**: cloud provider secures "of the cloud" (physical infra, hypervisor); customer secures "in the cloud" (data, IAM config, app security, network config) — very common interview question, especially the boundary shifting across IaaS/PaaS/SaaS.
- **Container security**: minimal base images, image scanning (Trivy, Clair), don't run containers as root, read-only filesystems, signed images (e.g., Sigstore/cosign) to ensure supply-chain integrity.
- **Kubernetes security**: RBAC for cluster access, network policies for pod-to-pod traffic control, Pod Security Standards/admission controllers, secrets encrypted at rest in etcd.
- **Secure supply chain**: SBOM (Software Bill of Materials), dependency pinning, signed commits/artifacts, provenance attestation (SLSA framework).

---

## 17. DevSecOps / Secure SDLC

- **Shift-left security**: bake security into design and early development, not just pre-release.
- **Threat Modeling**: proactively identify threats. **STRIDE** framework: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.
- **SAST (Static Application Security Testing)**: scans source code for vulnerabilities without executing it.
- **DAST (Dynamic Application Security Testing)**: tests the running application (black-box) for vulnerabilities.
- **IAST**: instrumented testing combining aspects of both, during runtime/test execution.
- **SCA (Software Composition Analysis)**: scans third-party dependencies for known CVEs.
- **Penetration testing / Red teaming / Bug bounty programs**: adversarial testing by humans, complements automated tooling.
- **CI/CD pipeline security**: signed commits, protected branches, least-privilege pipeline credentials, scanning gates before deploy, immutable build artifacts.

---

## 18. Logging, Monitoring & Incident Response

- Centralized logging (ELK/Splunk/cloud-native equivalents) with tamper-evident storage.
- **SIEM (Security Information and Event Management)**: aggregates and correlates security logs/alerts across systems.
- Log security-relevant events: auth successes/failures, permission changes, admin actions — but never log secrets/PII/passwords/full tokens.
- **Non-repudiation**: ensure actions can be tied to an identity and can't be denied later (audit trails, signed logs).
- **Incident Response Plan**: preparation → detection/analysis → containment → eradication → recovery → post-incident review (lessons learned/blameless postmortem).
- **Alerting on anomalies**: impossible travel logins, brute-force patterns, privilege escalations.

---

## 19. Data Privacy & Compliance

- **PII (Personally Identifiable Information)**: needs special handling — encryption, access controls, data minimization.
- **GDPR** (EU): right to access/erasure ("right to be forgotten"), data breach notification within 72 hours, data processing agreements, privacy by design.
- **CCPA/CPRA** (California): similar consumer data rights.
- **HIPAA** (US healthcare): protects health information (PHI), requires safeguards + business associate agreements.
- **PCI-DSS**: standard for handling payment card data — network segmentation, encryption, tokenization, restricted access, regular scanning.
- **SOC 2**: audit framework (Security, Availability, Processing Integrity, Confidentiality, Privacy — the "Trust Service Criteria") common for B2B SaaS vendor due diligence.
- **Data residency/sovereignty**: some regulations require data to stay within specific geographic/legal boundaries.
- **Data minimization**: collect and retain only what's necessary — reduces breach impact and compliance burden.

---

## 20. Rate Limiting & Abuse Prevention

- Protects against brute force, credential stuffing, scraping, and DoS.
- Common algorithms: **Token Bucket**, **Leaky Bucket**, **Fixed/Sliding Window Counters**.
- Apply at multiple layers: edge/CDN, API gateway, application, per-user and per-IP.
- **Account lockout / exponential backoff** after repeated failed logins — balance against enabling attacker-driven denial-of-service on legitimate users (lockout can itself be abused).
- **CAPTCHA** as a friction mechanism against bots (tradeoff: UX cost).
- **Credential stuffing defense**: detect reused breached password/username combos (e.g., via breach-password databases like Have I Been Pwned's API), device fingerprinting, anomaly detection.

---

## 21. Common "Explain This Tradeoff" Interview Questions (with quick framing)

- **JWT vs session tokens**: stateless scalability vs easy revocation — pick based on need for instant revocation vs horizontal scaling simplicity.
- **RBAC vs ABAC**: simplicity/auditability vs fine-grained flexibility.
- **Symmetric vs asymmetric crypto**: speed vs key-distribution/non-repudiation.
- **SAML vs OIDC**: enterprise/legacy fit vs modern/mobile fit.
- **Build vs buy identity (rolling your own auth vs Auth0/Okta/Cognito)**: control & cost vs speed, security expertise, compliance certifications you don't have to build yourself. Most interviewers want you to say "buy/use a managed IdP" for anything beyond a toy project.
- **Blocklist vs allowlist validation**: allowlisting (permit known-good) is almost always more secure than blocklisting (block known-bad), since you can't enumerate all bad inputs.

---

## Additional Important Topics (listed due to space — worth reviewing separately)

- Public Key Infrastructure (PKI) details: certificate revocation (CRL vs OCSP), intermediate CAs
- HMAC and message authentication codes in depth
- Homomorphic encryption / confidential computing (emerging, good for "cutting edge" bonus points)
- Security of GraphQL APIs (query depth/complexity limits, introspection risks)
- WebSocket security considerations
- Mobile app security (certificate pinning, jailbreak/root detection, secure storage — Keychain/Keystore)
- Social engineering & phishing (business email compromise, spear phishing)
- Insider threat programs
- Chaos engineering for resilience/security testing
- Post-quantum cryptography (NIST PQC standards — relevant as forward-looking discussion)
- API versioning security implications (deprecated endpoints left exposed)
- Multi-tenancy isolation strategies (noisy neighbor + data isolation in SaaS)
- Backup security & ransomware recovery planning
- Security champions programs / building a security culture within engineering teams (very relevant for a *tech lead* specifically — expect behavioral questions here, not just technical)
