# Security & Data Handling Architecture

ConicFolio is architected around principles of **data minimization**, **stateless execution**, and **cryptographically verifiable computation**.

This document outlines the security controls, data handling practices, and architectural boundaries governing both the **Hosted Cloud API Gateway** and the **Institutional On-Premise Enclaves**.

---

## 1. Architecture Overview: Two Distinct Deployment Models

To prevent ambiguity during compliance and security reviews, ConicFolio distinguishes between two execution environments:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                               CONICFOLIO EXECUTION ARCHITECTURES                         │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                              │
               ┌──────────────────────────────┴──────────────────────────────┐
               ▼                                                             ▼
┌──────────────────────────────────────────────┐              ┌──────────────────────────────────────────────┐
│ HOSTED CLOUD API GATEWAY                     │              │ INSTITUTIONAL HARDWARE ENCLAVE               │
│ (Public Quants & Developer Evaluation)       │              │ (Tier-1 Banks & Quantitative Hedge Funds)    │
├──────────────────────────────────────────────┤              ├──────────────────────────────────────────────┤
│ • Stateless, ephemeral HTTP request-response │              │ • Air-gapped deployment (`network_mode: none`│
│ • Internet-facing with rate limiting         │              │ • Zero external internet ingress or egress   │
│ • No persistent database attached to solvers │              │ • Local Unix Domain Socket / VSOCK IPC       │
│ • Payloads processed in volatile memory      │              │ • Silicon-level hardware RAM encryption      │
│ • Transport encrypted via HTTPS              │              │ • Deployed 100% inside client VPC perimeter  │
└──────────────────────────────────────────────┘              └──────────────────────────────────────────────┘
```

---

## 2. Hosted Cloud API: Data Handling & Lifecycle

### 2.1 Stateless Processing Model
- **Ephemeral Computation**: The Hosted API operates as a stateless computational proxy. Request payloads (covariance matrices and historical return scenarios) are received over HTTPS, passed into solver memory for optimization, and the resulting weight vectors are returned in the HTTP response.
- **No Persistent Database**: The solver service does not connect to any relational database, document store, or disk-backed cache for client portfolio data.
- **Memory Lifecycle**: Intermediate numerical arrays and optimization variables are managed in runtime memory for the duration of the request. Once the request terminates, references are deallocated in accordance with runtime memory management.

### 2.2 Logging & Sanitization Policy
- **No Payload Logging**: Application-level code explicitly avoids logging request bodies, covariance values, return matrices, or calculated portfolio allocations.
- **Sanitized Metadata**: Server access logs capture only non-sensitive operational metadata:
  - Timestamp (UTC)
  - HTTP method and endpoint (`POST /v1/optimize/solve`)
  - HTTP response status code (e.g. `200`, `429`, `500`)
  - Request execution latency
  - Hashed API key identifier (for rate-limit quota enforcement)
- **Error Handling**: Solver exceptions return structured error categories without echoing raw input matrices or sensitive stack trace contents.

---

## 3. Performance & Latency Measurement Methodology

To ensure transparent and verifiable performance metrics, ConicFolio distinguishes between **Solver Kernel Latency** and **End-to-End API Round-Trip Latency**:

| Metric | Measured Scope | Typical Performance | Measurement Methodology |
| :--- | :--- | :--- | :--- |
| **Solver Kernel Execution** | Core optimization math initiation to optimal solution certificate. Excludes network transport and serialization. | **0.29 ms – 1.8 ms** (15 to 100 assets) | Measured using high-resolution monotonic timers (`time.perf_counter()`) on dedicated x86_64 hardware. |
| **End-to-End API Round-Trip** | Total time from client request dispatch to client response parsing over the public internet. | **35 ms – 90 ms** (network dependent) | Measured at client SDK layer; varies depending on client geographical location and network peering. |
| **Local IPC Enclave Latency** | Inter-process communication within an air-gapped enclave over Unix Domain Sockets or VSOCK. | **< 0.5 ms** | Measured within local container runtime; zero network hop. |

---

## 4. Encryption in Transit & Network Boundaries

- **HTTPS Enforcement**: All communication to the Hosted API Gateway requires HTTPS. Plaintext HTTP requests are rejected or redirected.
- **TLS Configuration**: Supported connections negotiate modern TLS protocols with forward-secret cipher suites (ECDHE key exchange) to protect in-transit payloads from passive eavesdropping.
- **Input Validation**: Request payloads are strictly validated against Pydantic schemas enforcing dimension constraints, finite floating-point checks, and tier-specific universe size caps (e.g., maximum 100 assets on the free tier).

---

## 5. Institutional Enclave: Air-Gapped & Hardware-Isolated Security

For sovereign wealth funds, Tier-1 investment banks, and institutional desks subject to strict regulatory mandates (**SEC Rule 17a-4**, **FINRA Rule 4511**, **MiFID II**):

The term **air-gapped** applies strictly to the **On-Premise / Private Cloud Enclave appliance**:

1. **Network Isolation**: The enclave container runs with `network_mode: none`. It possesses no public IP, no private cloud NAT gateway route, and zero inbound or outbound internet access.
2. **Local IPC Interface**: Communication with client Order Management Systems (OMS) occurs exclusively over local **Unix Domain Sockets** (`/var/run/conicfolio/kernel.sock`) or **AWS Nitro VSOCK** (Virtual Socket).
3. **Silicon-Level Memory Encryption**: Packaged for technologies like **AWS Nitro Enclaves**, **AMD SEV-SNP**, and **Intel SGX**, where CPU silicon encrypts RAM using volatile hardware keys. Neither host operating system administrators, root users, nor cloud hypervisors can read enclave RAM.
4. **Offline Licensing**: Uses offline cryptographic Ed25519 digital signatures tied to the host machine hardware fingerprint. The enclave does not phone home to verify licenses.

---

## 6. Security Verification & Continuous Testing

ConicFolio incorporates continuous automated security and quality testing:

- **Automated Matrix Testing**: Unit and integration test suites run across all supported Python runtimes on every codebase modification.
- **Zero Competitor Trademark Compliance**: Automated repository scans ensure strict adherence to trademark boundaries.
- **Dependency Minimization**: The public thin-client SDK maintains minimal external dependencies (`numpy`, `requests`, `pandas`) to reduce supply-chain attack surface.

---

## 7. Vulnerability Disclosure & Contact

If you identify a potential security vulnerability or have questions regarding data privacy controls:

- **Security Contact**: [security@conicfolio.com](mailto:security@conicfolio.com)
- **PGP / Secure Communications**: Available upon request.
- **Response SLA**: Initial triage within 24 business hours; remediation timelines communicated transparently based on severity.
- Please do not submit vulnerability reports to public GitHub issue trackers.
