# Free API vs Institutional Enterprise

ConicFolio operates under a two-tier delivery model designed for public developers and institutional enterprises:

| Capability | Free Developer API | Institutional Enterprise Enclave |
| :--- | :--- | :--- |
| **Target Audience** | Retail Quants, PhDs, Fintech Startups | \$10B+ Hedge Funds, Prime Brokers, Sovereign Wealth Funds |
| **Delivery Model** | Hosted Cloud API (`api.conicfolio.com`) | Sealed AWS Nitro Enclave Appliance / Native C Wheels |
| **Deployment Location** | ConicFolio Managed Cloud | **100% inside client private VPC / Bare-Metal Linux** |
| **Data Privacy** | TLS 1.3 In-Transit | **Zero Egress (Air-gapped, zero external network adapter)** |
| **Regulatory Compliance** | Standard Terms of Service | **SEC Rule 17a-4, FINRA Rule 4511, MiFID II Article 16** |
| **Execution Latency** | 30 – 80 ms (Internet round-trip) | **< 0.5 ms (Sub-millisecond local Unix/VSOCK IPC)** |
| **Universe Size Cap** | Up to 100 assets | **Unlimited (5,000+ assets supported)** |
| **Rate Limit** | 60 requests / minute | **Unlimited requests (no rate limits)** |
| **Advanced Models** | ERC, HRP, HERC, NCO, CVaR | **3/2 Power Cone Market Impact, Discrete Board Lots, Quantum SQA** |
| **Pricing** | **Free Forever** | **\$75,000 – \$250,000 / year Institutional License** |

---

## Institutional Enclave Architecture

For Tier-1 institutions, ConicFolio is deployed as an encrypted **Enclave Image File (`.eif`)** running inside your own AWS VPC or bare-metal Linux servers:

- **Hardware Silicon RAM Encryption**: The host CPU encrypts memory space using keys managed strictly by the silicon processor (AMD SEV-SNP / Intel SGX / Nitro).
- **Zero-Knowledge Security**: Even root sysadmins or cloud providers cannot dump memory or inspect proprietary models.
- **Audit Attestation**: Emits cryptographic Karush-Kuhn-Tucker duality certification (`< 1.0e-12`) for compliance audits.

To request an institutional trial appliance, contact [support@conicfolio.com](mailto:support@conicfolio.com) or visit [conicfolio.com](https://conicfolio.com).
