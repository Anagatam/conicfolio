# ConicFolio: Quantitative Portfolio Optimization Python SDK

<div align="center">

[![PyPI version](https://img.shields.io/badge/pypi-v2.9.0-blue.svg)](https://pypi.org/project/conicfolio/)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://pypi.org/project/conicfolio/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![CI Status](https://github.com/Anagatam/conicfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/Anagatam/conicfolio/actions)
[![Speed](https://img.shields.io/badge/benchmark-34.3x%20faster-emerald.svg)](https://conicfolio.com)
[![API Status](https://img.shields.io/badge/API%20Gateway-Online%20(Free%20Tier)-brightgreen.svg)](https://conicfolio.com)

**High-Performance Quantitative Portfolio Optimization Suite for Modern Asset Managers & Systematic Quants.**

[Quickstart](#-quickstart) • [Interactive Visualizations](#-interactive-visualizations-generated-with-plotly) • [Model Selection Guide](#-model-selection-guide) • [Free API Tier](#-free-developer-api-tier) • [Enterprise Enclaves](#-institutional-enterprise-enclaves-hedge-funds--banks)

</div>

---

## ⚡ Overview

**ConicFolio** provides a Scikit-Learn compliant interface for high-speed portfolio optimization. It solves complex asset allocation models—including **Equal Risk Contribution (Risk Parity)**, **Hierarchical Risk Parity (HRP)**, **Hierarchical Equal Risk Contribution (HERC)**, and **Downside Tail-Risk Optimization (CVaR)**—in **under 1 millisecond**.

- 🚀 **34.3x Faster Execution**: Solves a 15-asset universe in **0.29 ms** (vs 9.94 ms to 106.79 ms in public alternatives).
- 🧩 **Zero Solver Compilation Overhead**: Runs immediately on any OS (macOS, Linux, Windows) without C/C++ compiler setup or licensing friction.
- 📉 **Real-World Institutional Data**: Includes 1,257 trading days (2019–2024) of real market returns across 25 institutional instruments.
- 🎯 **Scikit-Learn Standard API**: Seamless `fit(returns)` and `predict()` integration for quantitative backtesting pipelines.

---

## 📊 Interactive Visualizations (Generated with Plotly)

### 1. Solve Latency Benchmark (ConicFolio vs Public Solvers)
ConicFolio delivers sub-millisecond execution, enabling intraday portfolio rebalancing and high-throughput Monte Carlo risk attribution.

<div align="center">
  <img src="assets/benchmark_speed_comparison.png" alt="ConicFolio Speed Benchmark Comparison" width="850"/>
  <p><i>Plotly Interactive Chart: <a href="assets/benchmark_speed_comparison.html">Open Interactive HTML Version</a></i></p>
</div>

---

### 2. Why Quants Use Risk Parity (The 60/40 "Risk Trap")
In a traditional 60/40 capital allocation, **over 90% of total portfolio volatility risk originates from the equity leg**. ConicFolio solves for true equal risk contribution, ensuring that every asset pillar contributes an identical fraction of volatility.

<div align="center">
  <img src="assets/risk_parity_allocation.png" alt="Risk Parity Equal Risk Contribution vs Traditional 60/40" width="850"/>
  <p><i>Plotly Interactive Chart: <a href="assets/risk_parity_allocation.html">Open Interactive HTML Version</a></i></p>
</div>

---

### 3. Real Market Efficient Frontier & Tail-Risk Profiles
Visualizing trade-offs between annualized volatility, expected returns, and downside crash protection (CVaR 95%) on 5 years of daily market returns.

<div align="center">
  <img src="assets/efficient_frontier_cvar.png" alt="Real Market Efficient Frontier" width="850"/>
  <p><i>Plotly Interactive Chart: <a href="assets/efficient_frontier_cvar.html">Open Interactive HTML Version</a></i></p>
</div>

---

### 4. Hierarchical Clustering Asset Allocation (HRP & HERC)
Machine learning graph clustering groups correlated assets hierarchically, eliminating the need for matrix inversion and protecting against noise amplification.

<div align="center">
  <img src="assets/hierarchical_cluster_tree.png" alt="Hierarchical Equal Risk Contribution Sunburst Tree" width="750"/>
  <p><i>Plotly Interactive Chart: <a href="assets/hierarchical_cluster_tree.html">Open Interactive HTML Version</a></i></p>
</div>

---

## ⚡ Quickstart

### 1. Installation
```bash
pip install conicfolio
```

### 2. Equal Risk Contribution (Risk Parity) in 3 Lines
```python
import conicfolio as cf

# 1. Load bundled 5-year real institutional market dataset
returns = cf.load_market_data(n_assets=10)

# 2. Fit model using familiar scikit-learn API
model = cf.RiskParity()
model.fit(returns)

# 3. Inspect optimal weights and solve latency
print("Optimal Allocations:", model.weights_)
print(f"Solved in: {model.solve_time_ms_} ms")
```

---

## 🎯 Model Selection Guide

Choose the right allocation model for your investment mandate:

| Model Class | Python Estimator | Ideal Use-Case | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Equal Risk Contribution** | `cf.RiskParity()` | Multi-Asset Portfolios, All-Weather Funds | Balances true risk across equities, bonds, and gold. |
| **Hierarchical Risk Parity** | `cf.HierarchicalRiskParity()` | Large Universes, Correlated Equities | Machine learning tree clustering; zero matrix inversion. |
| **Hierarchical Equal Risk** | `cf.HierarchicalEqualRiskContribution()` | Sector & Industry Risk Allocation | Equalizes risk contributions across hierarchical clusters. |
| **Nested Clustered Opt** | `cf.NestedClusteredOptimization()` | Highly Multicollinear Assets | De-noises correlations across in-cluster and out-of-cluster. |
| **Minimum Variance** | `cf.ConicPortfolio(objective="min_variance")` | Conservative & Low-Beta Mandates | Minimizes total portfolio variance without expected returns. |
| **Downside Tail-Risk (CVaR)** | `cf.ConicPortfolio(objective="cvar")` | Asymmetric & Crash-Sensitive Funds | Directly minimizes Conditional Value at Risk in fat-tailed assets. |

---

## 💻 Practical Code Examples

### Example 1: Hierarchical Equal Risk Contribution (HERC)
```python
import conicfolio as cf

returns = cf.load_market_data(n_assets=15)

# Cluster assets into 3 distinct economic sectors
herc = cf.HierarchicalEqualRiskContribution(n_clusters=3)
herc.fit(returns)

print(f"HERC Solved in: {herc.solve_time_ms_} ms")
for asset, weight in zip(returns.columns, herc.weights_):
    print(f"  {asset}: {weight * 100:.2f}%")
```

### Example 2: Tail-Risk Protection (CVaR Optimization)
```python
import conicfolio as cf

returns = cf.load_market_data(n_assets=12)

# Minimize expected shortfall in the worst 5% tail scenarios
cvar_model = cf.ConicPortfolio(objective="cvar")
cvar_model.fit(returns)

print(f"CVaR Solved in: {cvar_model.solve_time_ms_} ms")
print("Downside-Protected Allocation:", cvar_model.weights_)
```

---

## 🚀 Free Developer API Tier

Anyone can use ConicFolio for free. You can generate an API key instantly at [conicfolio.com](https://conicfolio.com) without a credit card.

| Free Tier Specification | Limit | Notes |
| :--- | :--- | :--- |
| **Rate Limit** | **60 requests / minute** | Ideal for quantitative backtesting and academic research. |
| **Max Asset Universe** | **Up to 100 assets** | Covers S&P 100, crypto baskets, and sector ETF portfolios. |
| **Monthly Quota** | **10,000 optimizations / month** | Free for developers, students, and early-stage startups. |
| **Included Models** | Risk Parity, HRP, HERC, NCO, Min-Variance, CVaR | Instant cloud solving with zero local compiler dependencies. |

```python
import conicfolio as cf

# Configure your API key
cf.set_api_key("cf_live_YOUR_API_KEY")

model = cf.RiskParity()
model.fit(returns)
```

---

## 🏛️ Institutional Enterprise Enclaves (Hedge Funds & Banks)

For institutional clients requiring:
- **Zero Data Egress (Air-Gapped)**: Deployed inside your own AWS VPC or bare-metal Linux servers. No portfolio positions, alpha weights, or order books ever leave your firewall (fully compliant with **SEC Rule 17a-4**, **FINRA Rule 4511**, and **MiFID II**).
- **Silicon-Level Hardware RAM Encryption**: Delivered as an **AWS Nitro Enclave / Intel SGX Appliance** where RAM is hardware-encrypted at the silicon level. Not even cloud provider admins or root sysadmins can inspect memory.
- **Sub-Millisecond Execution**: Local Unix domain socket / VSOCK latency under **0.5 milliseconds** for live execution desks.
- **Unlimited Universe Size**: Supports **5,000+ assets** simultaneously.
- **Advanced Institutional Models**: 3/2 Power Cone Market Impact (Almgren-Chriss), Discrete Board Lot Cardinality, Multi-Period Dykstra, Quantum SQA.

Contact our institutional desk at [enterprise@conicfolio.com](mailto:enterprise@conicfolio.com) or explore [conicfolio.com](https://conicfolio.com).

---

## 📚 Jupyter Tutorials

Explore hands-on notebooks in the [`notebooks/`](notebooks/) directory:
- [`01_risk_parity_quickstart.ipynb`](notebooks/01_risk_parity_quickstart.ipynb): Solving Equal Risk Contribution step-by-step.
- [`02_hierarchical_clustering_hrp_herc.ipynb`](notebooks/02_hierarchical_clustering_hrp_herc.ipynb): Tree clustering and recursive bisection.

---

## 📄 License & Community
- **License**: The public Python SDK is released under the [Apache-2.0 License](LICENSE).
- **Contributing**: Please review our [Contributing Guidelines](CONTRIBUTING.md).
- **Security**: For vulnerability disclosures and data privacy guarantees, see our [Security Policy](SECURITY.md).
