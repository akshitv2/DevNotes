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

---

## 1. Public Key Infrastructure (PKI) Details

### The Chain of Trust
- **Root CA**: self-signed, top of the trust chain, kept offline/air-gapped in real deployments because compromise is catastrophic.
- **Intermediate CA**: signed by the root, used for day-to-day certificate issuance. Exists so the root can stay offline and so a compromised intermediate can be revoked without invalidating the entire root's trust.
- **Leaf/end-entity certificate**: the actual server/client cert, signed by an intermediate.
- Browsers/OSes ship a trust store of root CAs; validating a cert means walking the chain leaf → intermediate → root and checking each signature plus validity window.

### Certificate Revocation: CRL vs OCSP
- **CRL (Certificate Revocation List)**: CA periodically publishes a signed list of revoked certificate serial numbers. Clients download and check against it. Downsides: can get large, updates aren't real-time, clients often cache stale lists.
- **OCSP (Online Certificate Status Protocol)**: client (or browser) queries the CA in real time — "is this cert revoked?" — gets a signed yes/no response. Faster/fresher than CRL, but adds a live network dependency and leaks browsing metadata to the CA (privacy concern).
- **OCSP Stapling**: the server itself periodically fetches its own OCSP response from the CA and "staples" it to the TLS handshake — avoids the client contacting the CA directly, improving both privacy and performance while keeping revocation checks fresh. Generally considered best practice today.
- **Fail-open vs fail-closed**: if a revocation check can't complete (CA unreachable), most browsers historically "fail open" (allow the connection) rather than fail-closed (block it) — this is a well-known real-world weakness of revocation checking, worth mentioning as a "known gap" in an interview.

### Other PKI Concepts
- **CSR (Certificate Signing Request)**: generated by the entity needing a cert, contains the public key + identity info, sent to CA for signing (private key never leaves the requester).
- **Certificate Transparency (CT) logs**: public, append-only logs of all issued certs — lets domain owners detect mis-issued certs for their domain.
- **Wildcard vs SAN certs**: wildcard (`*.example.com`) covers one level of subdomains; SAN (Subject Alternative Name) certs list multiple explicit domains/subdomains in one cert.
- **Short-lived certificates**: modern trend (e.g., Let's Encrypt's 90-day certs, even shorter-lived certs in service meshes) — reduces reliance on revocation entirely, since certs simply expire quickly if compromised.

---

## 2. HMAC and Message Authentication Codes

### What Problem MACs Solve
- A **MAC (Message Authentication Code)** proves both **integrity** (message wasn't altered) and **authenticity** (came from someone holding the shared secret) — a plain hash alone only proves integrity, since anyone can compute a hash.

### HMAC (Hash-based MAC)
- Combines a cryptographic hash function (e.g., SHA-256) with a secret key in a specific nested construction. You don't need to memorize the formula for an interview — know *why* it's structured this way: naive approaches like `H(key || message)` are vulnerable to **length-extension attacks** on certain hash constructions; HMAC's nested double-hashing with padding specifically defeats this.
- Common uses: API request signing (e.g., AWS Signature v4), JWT `HS256` signatures, webhook payload verification (e.g., verifying a Stripe/GitHub webhook came from them by checking a signature header).

### MAC vs Digital Signature
- **HMAC**: symmetric — same secret both generates and verifies. Fast, but both parties must share the secret (so either party could have forged it — no non-repudiation).
- **Digital signature** (RSA/ECDSA): asymmetric — private key signs, public key verifies. Provides non-repudiation (only the private key holder could have signed it) at the cost of more compute.
- Interview framing: "use HMAC when both sides trust each other and just need fast integrity/authenticity (e.g., internal service-to-service); use signatures when you need proof of origin to a third party who didn't share a secret (e.g., verifying a software update was published by the vendor)."

### Practical Pitfalls
- **Timing attacks on comparison**: comparing MACs with a naive `==` string comparison can leak information via timing side-channels. Always use a constant-time comparison function (e.g., `hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node).
- **Key management**: HMAC secrets need the same rigor as encryption keys — rotate, store in a secrets manager, never hardcode.

---

## 3. Homomorphic Encryption & Confidential Computing

### Homomorphic Encryption (HE)
- Allows computation directly on **encrypted data** without decrypting it first — the result, once decrypted, matches what you'd get computing on the plaintext.
- **Partially Homomorphic Encryption (PHE)**: supports only one operation (e.g., RSA supports multiplication, Paillier supports addition) — usable today for specific use cases like encrypted vote tallying or private aggregation.
- **Fully Homomorphic Encryption (FHE)**: supports arbitrary computation on encrypted data. Theoretically solved (Craig Gentry's 2009 breakthrough) but still computationally very expensive for general use — active area of research (companies like Zama, Duality, and IBM/Microsoft research groups are pushing practical FHE).
- Use case pitch for interviews: a cloud provider could process sensitive data (e.g., medical or financial) without ever seeing it in plaintext — relevant to privacy-preserving ML and regulated-industry cloud computing.

### Confidential Computing
- A more practically-deployed-today alternative: use hardware-based **Trusted Execution Environments (TEEs)** to keep data encrypted in memory and process it inside a secure, isolated enclave — even the cloud provider's hypervisor/OS can't see inside.
- Examples: **Intel SGX**, **AMD SEV**, **ARM TrustZone**; cloud offerings like AWS Nitro Enclaves, Azure Confidential Computing, Google Confidential VMs.
- Threat model addressed: protects against a malicious/compromised cloud operator or co-tenant, not just external attackers — relevant for highly regulated workloads (finance, healthcare, government) or multi-party data collaboration where no single party should see raw data.
- Interview soundbite: "Confidential computing protects data *in use*, complementing encryption at rest and in transit — closing the last gap in the data lifecycle."

---

## 4. GraphQL API Security

GraphQL's flexibility (clients construct their own queries) introduces attack surface that REST doesn't have in the same way.

- **Query depth/complexity attacks**: a deeply nested or highly repetitive query (e.g., fetching friends-of-friends-of-friends recursively) can cause exponential resource consumption on the server — effectively a self-inflicted DoS vector. Mitigations: enforce **max query depth**, assign a **cost/complexity score** to fields and reject queries above a threshold, apply timeouts.
- **Introspection risks**: GraphQL's introspection feature lets a client query the schema itself — great for development tooling, but in production it hands attackers a full map of your API surface, including fields/mutations not meant to be discovered. Best practice: disable introspection in production (or restrict to authenticated/internal use).
- **Batching attacks**: a single GraphQL request can bundle many operations (aliases/batched queries), which can be used to brute-force (e.g., try many passwords in one HTTP request, bypassing simple per-request rate limits). Mitigate with per-operation cost accounting, not just per-HTTP-request rate limiting.
- **Authorization at the field/resolver level**: REST secures at the endpoint level; GraphQL has one endpoint but many resolvers — authorization checks must happen *per field/resolver*, not just "is this user logged in" at the gateway. Easy to accidentally expose a sensitive field through a nested query if per-field authorization is forgotten.
- **Persisted queries / allowlisting**: for production clients, only allow a pre-approved set of queries (hashes mapped to known query strings) rather than accepting arbitrary client-constructed queries — drastically shrinks attack surface.
- **Error message leakage**: verbose GraphQL error messages (stack traces, resolver internals) can leak schema/implementation details — sanitize errors in production.

---

## 5. WebSocket Security

- WebSockets are long-lived, bidirectional connections — they don't fit the typical per-request auth model (no repeated headers/cookies per message by default).
- **Origin validation**: unlike `fetch`/XHR, browsers don't enforce same-origin restrictions on WebSocket connections the same way — the server *must* explicitly validate the `Origin` header on the handshake to prevent cross-site WebSocket hijacking (a CSRF-equivalent for WebSockets).
- **Authentication at handshake time**: typically done via a token in the initial HTTP upgrade request (query param or header) or cookie — since you can't easily re-authenticate mid-connection, make sure the token has a reasonable expiry and the server re-validates/terminates the connection when it expires or is revoked.
- **`wss://` (TLS) always**, never plain `ws://` in production — same eavesdropping/MITM risks as unencrypted HTTP.
- **Message-level validation**: just like REST bodies, every inbound WebSocket message needs schema validation/sanitization — it's still attacker-controlled input, just over a different transport.
- **Resource exhaustion**: long-lived connections can be abused to hold server resources open — apply connection limits per user/IP, idle timeouts, and message-rate limiting per connection.
- **Authorization per action, not just per connection**: a connection being "authenticated" doesn't mean every message/action on it is authorized — re-check permissions per message if actions have different privilege requirements (e.g., a chat app's "delete message" action needs its own authorization check, not just "is this socket logged in").

---

## 6. Social Engineering & Phishing

- **Phishing**: mass, generic fraudulent messages trying to harvest credentials or deliver malware.
- **Spear phishing**: targeted phishing using personal/organizational details to seem credible (e.g., referencing a real project or colleague's name).
- **Whaling**: spear phishing targeted specifically at executives/high-value targets.
- **Business Email Compromise (BEC)**: attacker impersonates (or compromises the actual account of) an executive or vendor to trick an employee into wiring money or changing payment details — one of the costliest categories of cybercrime, and notably a *social/process* failure rather than a technical exploit.
- **Pretexting**: fabricating a scenario/identity (e.g., posing as IT support) to extract information over phone/chat.
- **Vishing/Smishing**: phishing via voice calls / SMS respectively.
- **Technical mitigations**: email authentication standards — **SPF** (which servers can send mail for a domain), **DKIM** (cryptographically signs outgoing mail), **DMARC** (policy tying SPF/DKIM together and telling receiving servers what to do on failure — reject/quarantine/report) — all three together are the standard anti-spoofing stack for a domain.
- **Human mitigations**: security awareness training, simulated phishing campaigns, clear out-of-band verification procedures for sensitive actions (e.g., "always verbally confirm wire transfer changes via a known phone number, never just email").
- Interview relevance for a tech lead: you're often the one who needs to design the *verification process* for sensitive engineering actions (prod access changes, deploy approvals) resistant to social engineering — not just rely on "employees should know better."

---

## 7. Insider Threat Programs

- Threat actors aren't only external — insider threats include malicious insiders (disgruntled employees), negligent insiders (well-meaning mistakes), and compromised insiders (legitimate credentials stolen/misused).
- **Least privilege + need-to-know access**: minimizes what any single insider can do or see.
- **Separation of duties**: sensitive actions (e.g., deploying to prod, approving payments) require more than one person — no single individual has unchecked end-to-end control.
- **Behavioral monitoring / UEBA (User and Entity Behavior Analytics)**: baseline "normal" access patterns and flag anomalies (e.g., unusual data downloads, access at odd hours, access to systems outside someone's normal role).
- **Offboarding rigor**: immediate access revocation across all systems when someone leaves — a very common real-world gap (stale accounts left active), especially painful when centralized SSO isn't used for every system.
- **Privileged Access Management (PAM)**: just-in-time elevated access (temporary, audited, time-boxed privilege escalation) rather than standing admin rights.
- Balance: insider threat programs must be proportionate and legally/ethically sound — heavy-handed surveillance can damage trust and morale; a tech lead should advocate for controls that are effective without being invasive (e.g., auditing access to sensitive data, not reading every employee's messages).

---

## 8. Chaos Engineering for Resilience & Security

- Traditionally chaos engineering (Netflix's Chaos Monkey and descendants) is about *reliability* — deliberately injecting failures (killing instances, adding latency, partitioning networks) in production or production-like environments to verify systems degrade gracefully.
- **Security-focused chaos engineering ("security chaos engineering")** extends this to deliberately inject *security-relevant* failure conditions to validate defenses actually work, not just that they exist on paper:
    - Revoke a credential/cert mid-flight and verify systems fail safely (not open).
    - Simulate a compromised node and verify detection/alerting actually fires.
    - Intentionally trigger a rate-limit/WAF rule and confirm it blocks as expected.
    - Kill a security-critical dependency (e.g., the auth service) and verify the system fails *closed* (denies access) rather than *open* (grants access) — a critical distinction interviewers like to probe.
- Value proposition: security controls that have never been tested under real failure conditions are often assumed to work but silently don't (e.g., alerts that were quietly broken for months). Chaos-style exercises turn "we think this works" into "we've verified this works."
- Ties into incident response: game days / tabletop exercises simulating a breach scenario build muscle memory for the real thing.

---

## 9. Post-Quantum Cryptography (PQC)

- **The threat**: sufficiently powerful quantum computers running Shor's algorithm could break current asymmetric crypto (RSA, ECC/ECDSA, Diffie-Hellman) by efficiently factoring large numbers / solving discrete logarithms. Symmetric crypto (AES) and hashing are less affected — mainly need larger key sizes (Grover's algorithm gives only a quadratic speedup, addressed by doubling key length, e.g., AES-256 remains fine).
- **"Harvest now, decrypt later"**: adversaries can record encrypted traffic today and decrypt it once quantum computers become capable — relevant *right now* for any data with long confidentiality requirements (state secrets, long-term medical/financial records), even though large-scale cryptographically-relevant quantum computers don't exist yet.
- **NIST PQC Standardization**: NIST ran a multi-year public competition and has standardized new algorithms designed to resist quantum attacks:
    - **ML-KEM** (based on CRYSTALS-Kyber) — key encapsulation/exchange.
    - **ML-DSA** (based on CRYSTALS-Dilithium) — digital signatures.
    - **SLH-DSA** (based on SPHINCS+) — a hash-based signature scheme, conservative/backup choice.
- **Migration strategy discussion points** (good for showing tech-lead-level thinking, not just trivia):
    - **Crypto agility**: design systems so cryptographic algorithms can be swapped without major rearchitecture — avoid hardcoding a single algorithm deep in the stack.
    - **Hybrid schemes**: run classical + post-quantum algorithms together during the transition period, so security holds as long as *either* remains unbroken.
    - Browsers/TLS libraries (e.g., Chrome, OpenSSL, Cloudflare) have already begun rolling out hybrid PQC key exchange in TLS 1.3 as an early real-world deployment example.

---

## 10. API Versioning Security Implications

- Old API versions rarely get the same security attention as the current version — patches, WAF rules, and monitoring often focus on the newest version while older ones quietly stay exposed and unpatched ("zombie APIs").
- **Shadow APIs / forgotten endpoints**: undocumented or deprecated endpoints left reachable are a top real-world breach vector — attackers actively scan for old version paths that may lack newer security controls (auth requirements added later, rate limiting, input validation improvements).
- Mitigations:
    - Maintain an accurate, continuously updated **API inventory** (many orgs are surprised how many undocumented endpoints exist — API discovery tooling helps).
    - Apply a **formal deprecation/sunset policy**: explicit end-of-life dates, `Deprecation`/`Sunset` HTTP headers, and actual removal — not indefinite "soft" deprecation.
    - Ensure security controls (auth, rate limiting, input validation, monitoring) are applied consistently across *all* live versions, not just the newest.
    - Treat API gateway configuration as code/reviewed artifact so an old version can't silently miss a security rule applied to newer ones.
- Interview framing: this is a great example of a "boring but critical" tech-lead responsibility — technical debt (unretired API versions) directly becoming a security liability.

---

## 11. Multi-Tenancy Isolation Strategies (SaaS)

Core challenge: many customers (tenants) share infrastructure — a design/security bug can leak one tenant's data to another, which is often an existential risk for a SaaS company.

### Isolation Models (increasing isolation, increasing cost)
- **Silo model**: fully separate infrastructure per tenant (separate DB, sometimes separate compute). Strongest isolation, highest cost/operational overhead — often used for large enterprise or highly regulated customers.
- **Pool model**: shared infrastructure, tenants distinguished by a `tenant_id` column/attribute in shared tables. Cheapest and most scalable, but *every single query* must correctly filter by tenant — a missed tenant filter is a direct cross-tenant data leak.
- **Bridge/hybrid model**: mix — e.g., shared compute layer but separate schemas or databases per tenant, or silo the largest/most sensitive tenants while pooling smaller ones.

### Enforcing Isolation in the Pool Model
- **Row-Level Security (RLS)**: enforce tenant filtering at the *database* layer (e.g., Postgres RLS policies) so isolation doesn't depend solely on application code remembering to filter correctly — defense in depth against an application-layer bug.
- **Tenant context propagation**: ensure tenant identity flows correctly through every service call, background job, and cache key in a microservices system — a very common real-world bug source is background jobs/queues losing tenant context.
- **Per-tenant encryption keys**: encrypting each tenant's data with a distinct key limits blast radius and supports clean "crypto-shredding" (delete the key to make data unrecoverable) when a tenant offboards, which can also satisfy "right to erasure" requirements.

### Noisy Neighbor Problem
- One tenant's heavy usage (traffic spike, expensive query, resource-hogging job) degrading performance for other tenants on shared infrastructure.
- Mitigations: per-tenant rate limiting/quotas, resource pooling with fair-share scheduling, autoscaling, and (for the worst offenders) migrating them to dedicated/siloed infrastructure.
- Interview framing: "isolation" in multi-tenancy is both a *security* concern (data leakage) and a *reliability* concern (performance leakage) — good answers address both.

---

## 12. Backup Security & Ransomware Recovery Planning

- **The 3-2-1 rule** (classic baseline): 3 copies of data, on 2 different media types, with 1 copy off-site.
- **Immutable/air-gapped backups**: ransomware increasingly targets backups first (to remove the recovery option before encrypting production data) — modern practice requires backups to be **immutable** (write-once, cannot be modified/deleted even by an admin account for a retention period) and ideally logically or physically air-gapped from production credentials/network.
- **Backup access should be separately privileged**: the credentials that can *delete* or *modify retention* on backups should not be the same credentials/roles used for day-to-day production administration — otherwise a compromised admin account can destroy backups too.
- **Test restores regularly**: an untested backup is not a real backup — "we have backups" is meaningless without periodically proving you can actually restore from them within your required recovery time.
- **RTO / RPO**: **Recovery Time Objective** (how long can you tolerate being down) and **Recovery Point Objective** (how much data loss, measured in time, is tolerable) — these numbers should drive backup frequency and architecture decisions, not be decided after the fact during an incident.
- **Ransomware-specific recovery planning**:
    - Maintain offline/out-of-band copies of the incident response plan itself (useless if the plan is only stored on the encrypted network).
    - Pre-negotiate relationships with incident response/forensics firms and legal counsel *before* an incident, not during one.
    - Decide in advance (with legal/leadership) the organization's stance on ransom payment — this is a business/legal decision, not one to make ad hoc under pressure.
    - Segment the backup restore process so you're not restoring the same vulnerability that caused the breach in the first place (patch/rebuild, don't just restore-and-repeat).

---

## 13. Security Champions Programs & Security Culture (Tech Lead Focus)

*This is the most "behavioral interview" relevant section of Part 2 — expect this to come up as "how would you improve security culture on your team," not just as trivia.*

### Security Champions Programs
- Model: designate one engineer per team as a **security champion** — not a separate security-team hire, but a regular engineer given extra security training, a direct line to the central security team, and time allocated to review designs/PRs for security concerns.
- Goal: scale a small central security team's influence across many engineering teams without becoming a bottleneck (security team can't review every PR/design at a large org).
- What good champions actually do: early involvement in design/threat-modeling discussions, act as the first line of triage for "is this a real security concern," and feed real engineering pain points back to the central security team (so security tooling/policy stays practical, not just theoretical).

### Building Security Culture as a Tech Lead
- **Shift-left, but don't shift-blame**: security should be part of design review and story estimation from the start, not a gate that blocks release at the end — teams resent security when it only shows up as a last-minute blocker.
- **Blameless postmortems** applied to security incidents too — punishing people for reporting/causing security issues drives underreporting; the goal is systemic fixes, not scapegoats.
- **Make the secure path the easy path**: invest in paved-road tooling (secure-by-default templates, pre-approved libraries, automated scanning in CI) so doing the secure thing requires *less* effort than doing the insecure thing, not more.
- **Security as part of definition of done**: bake security acceptance criteria into the same process as functional acceptance criteria, rather than a separate/optional checklist.
- **Metrics that matter**: track things like mean-time-to-patch for critical vulnerabilities, percentage of services with up-to-date dependency scans, or time-to-revoke access on offboarding — not just "number of vulnerabilities found" (which can perversely incentivize not looking).
- **Lead by example**: a tech lead who visibly follows secure practices (doesn't bypass code review "just this once," reports their own near-misses) sets the real cultural norm far more effectively than a written policy document.
- Common interview question to prepare for: *"A deadline is at risk and a security review would delay the release — how do you handle it?"* — strong answers acknowledge the real business tension, propose risk-based tradeoffs (e.g., ship with a documented, time-boxed known-risk exception and a tracked follow-up ticket) rather than either blindly ignoring security or being an inflexible blocker.

---

## Quick Cross-Reference to Part 1

Several Part 2 topics connect directly back to Part 1 concepts — worth being able to bridge them in an interview:
- PKI (Part 2) underpins TLS and mTLS (Part 1's cryptography section).
- HMAC (Part 2) is literally what signs a `HS256` JWT (Part 1's JWT section).
- Multi-tenancy isolation (Part 2) is a specialized case of authorization/least-privilege (Part 1's authorization section).
- Chaos engineering (Part 2) is the practical validation layer for incident response planning (Part 1's logging/monitoring section).
- Security culture (Part 2) is what actually makes DevSecOps/shift-left (Part 1's DevSecOps section) work in practice rather than existing only on paper.