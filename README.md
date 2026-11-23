# ConicFolio: Quantitative Portfolio Optimization Python SDK

[![PyPI version](https://img.shields.io/badge/pypi-v2.9.0-blue.svg)](https://pypi.org/project/conicfolio/)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://pypi.org/project/conicfolio/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/github-Anagatam%2Fconicfolio-black.svg)](https://github.com/Anagatam/conicfolio)
[![Benchmarks](https://img.shields.io/badge/speed-34x%20faster-orange.svg)](https://conicfolio.com)
[![Status](https://img.shields.io/badge/API-Online%20(Free%20Tier)-emerald.svg)](https://conicfolio.com)

ConicFolio is the high-performance quantitative portfolio optimization suite for modern finance. Powered by exact interior-point second-order cone programming (SOCP), exponential cones, and Spinu Newton-Raphson solvers.

- **34x Faster Risk Parity**: Solves a 15-asset universe in **0.29 ms** (vs 9.94 ms in public alternatives).
- **Zero Local Solver Dependencies**: Works immediately on any operating system without complex C/C++ compiler setup.
- **Scikit-Learn Standard API**: Seamless `fit(returns)` and `predict()` integration.

---

## ⚡ Quickstart

### 1. Install via pip
```bash
pip install conicfolio
```

### 2. Run in 3 Lines of Python
```python
import conicfolio as cf

# Load institutional 5-year real market dataset
returns = cf.load_market_data(n_assets=10)

# Fit Equal Risk Contribution (ERC) model
model = cf.RiskParity()
model.fit(returns)

print("Optimal Allocations:", model.weights_)
print(f"Solved in: {model.solve_time_ms_} ms")
```

---

## 🚀 Free Developer API Tier

Anyone can use ConicFolio for free. Get an API key at [conicfolio.com](https://conicfolio.com).

| Free Tier Attribute | Limit |
| :--- | :--- |
| **Rate Limit** | **60 requests / minute** |
| **Max Asset Universe** | **Up to 100 assets** |
| **Monthly Quota** | **10,000 optimizations / month** |
| **Included Models** | Risk Parity (Spinu Newton), HRP, HERC, Min-Variance, Max-Sharpe, CVaR |

```python
import conicfolio as cf

# Set your free API key
cf.set_api_key("cf_live_YOUR_API_KEY")

model = cf.HierarchicalEqualRiskContribution(n_clusters=3)
model.fit(returns)
```

---

## 🏛️ ConicFolio Enterprise (For Hedge Funds & Banks)

For institutional clients requiring:
- **Air-Gapped Confidential Enclaves**: Runs 100% inside your own AWS VPC or bare-metal servers. Zero portfolio data leaves your perimeter.
- **Hardware RAM Encryption**: Silicon-level protection (AWS Nitro / Intel SGX / AMD SEV).
- **Sub-Millisecond Execution**: Local IPC latency under **0.5 milliseconds** for intraday trading.
- **Unlimited Assets**: 5,000+ assets simultaneously.
- **Institutional Models**: 3/2 Power Cone Market Impact, Discrete Board Lot Cardinality, Multi-Period Dykstra, Quantum SQA.

Contact our institutional quantitative engineering desk at [enterprise@conicfolio.com](mailto:enterprise@conicfolio.com) or visit [conicfolio.com](https://conicfolio.com).

---

## 📄 License
The public client SDK is licensed under the [Apache-2.0 License](LICENSE).
