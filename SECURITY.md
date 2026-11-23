# Security Policy & Data Privacy

ConicFolio adheres to institutional-grade security standards.

---

## 🔒 Data Privacy & Zero Data Retention

The ConicFolio API operates under strict **air-gapped zero-data-retention principles**:
- **Ephemeral Processing**: Request payloads (covariance matrices and returns) are held in volatile RAM only for the duration of the solver call ($< 5\text{ ms}$) and immediately discarded.
- **No Long-Term Storage**: Zero client portfolio holdings or alpha signals are written to disk or persistent databases.
- **TLS 1.3 Encryption**: All API communication over the internet is encrypted using TLS 1.3 with forward secrecy.

---

## 🏛️ Institutional On-Premise Enclaves
For sovereign wealth funds, Tier-1 investment banks, and quantitative hedge funds that cannot transmit data over the public web under SEC Rule 17a-4 or FINRA 4511:
- ConicFolio is deployable as an **AWS Nitro Enclave / Intel SGX Appliance** inside your own VPC.
- The enclave has **zero external internet access (`network_mode: none`)** and uses hardware memory encryption at the silicon level.

---

## 🛡️ Reporting a Vulnerability

If you discover a security vulnerability in the SDK or API gateway, please report it privately:

- **Security Team**: [security@conicfolio.com](mailto:security@conicfolio.com)
- Please do not open public GitHub issues for security vulnerabilities.
- We acknowledge all reports within 24 hours and issue fixes promptly.
