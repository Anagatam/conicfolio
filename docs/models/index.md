# Model Selection Guide

Choosing the optimal portfolio optimization model depends on your strategy mandate, asset universe characteristics, and risk constraints:

| Objective / Mandate | Recommended Model | Python Estimator | Key Strength |
| :--- | :--- | :--- | :--- |
| **All-Weather Multi-Asset** | Equal Risk Contribution | `cf.RiskParity()` | Balances true risk across equities, fixed income, gold, and commodities. |
| **High-Dimensional Equities** | Hierarchical Risk Parity | `cf.HierarchicalRiskParity()` | Machine learning tree clustering; zero matrix inversion errors. |
| **Sector / Cluster Allocation**| Hierarchical Equal Risk | `cf.HierarchicalEqualRiskContribution()` | Equalizes risk contributions across hierarchical clusters. |
| **Multicollinear Factor Portfolios** | Nested Clustered Opt | `cf.NestedClusteredOptimization()` | De-noises in-cluster and out-of-cluster correlation structures. |
| **Conservative Capital Preservation** | Minimum Variance | `cf.ConicPortfolio(objective="min_variance")` | Lowest possible portfolio volatility without expected returns. |
| **Downside Crash Protection** | Conditional Value at Risk | `cf.ConicPortfolio(objective="cvar")` | Directly minimizes the expected shortfall in severe tail regimes. |

---

## Model Deep Dives
- **[Equal Risk Contribution (Risk Parity)](risk_parity.md)**: Overcoming the 60/40 risk trap.
- **[Hierarchical Tree Allocations (HRP & HERC)](hierarchical.md)**: Tree clustering without matrix inversion.
- **[Downside Tail-Risk Optimization (CVaR)](tail_risk.md)**: Protecting capital during market drawdowns.
