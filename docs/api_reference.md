# API Reference

Complete Python API reference for the `conicfolio` public SDK.

---

## `conicfolio.RiskParity`
```python
class RiskParity(api_key: Optional[str] = None)
```
Equal Risk Contribution (ERC) portfolio solver using the Spinu Newton-Raphson convex engine.

**Parameters:**
- `api_key` *(str, optional)*: Custom ConicFolio API key. If omitted, uses key set by `cf.set_api_key()`.

**Attributes:**
- `weights_` *(np.ndarray)*: Array of optimal portfolio weights summing to 1.0.
- `solve_time_ms_` *(float)*: Latency of the optimization execution in milliseconds.
- `effective_assets_` *(float)*: Herfindahl inverse diversification metric ($N_{eff} = 1 / \sum w_i^2$).

---

## `conicfolio.HierarchicalRiskParity`
```python
class HierarchicalRiskParity(linkage: str = "ward", api_key: Optional[str] = None)
```
Hierarchical Risk Parity (HRP) using tree clustering and recursive bisection.

**Parameters:**
- `linkage` *(str)*: Hierarchical clustering linkage method (`"ward"`, `"single"`, `"complete"`).

---

## `conicfolio.HierarchicalEqualRiskContribution`
```python
class HierarchicalEqualRiskContribution(n_clusters: int = 3, api_key: Optional[str] = None)
```
Hierarchical Equal Risk Contribution (HERC) balancing risk both within and across asset clusters.

---

## `conicfolio.NestedClusteredOptimization`
```python
class NestedClusteredOptimization(n_clusters: int = 3, api_key: Optional[str] = None)
```
Nested Clustered Optimization (NCO) decomposing covariance into block-diagonal structures.

---

## `conicfolio.ConicPortfolio`
```python
class ConicPortfolio(objective: str = "min_variance", api_key: Optional[str] = None)
```
General conic portfolio solver.

**Objectives:**
- `"min_variance"`: Minimum overall portfolio volatility.
- `"max_sharpe"`: Tangency portfolio maximizing return-to-risk ratio.
- `"cvar"`: Downside tail crash protection minimizing Conditional Value at Risk.

---

## Utility Functions

### `conicfolio.set_api_key(api_key: str)`
Configures the global API key for the current Python session.

### `conicfolio.load_market_data(n_assets: int = 15) -> pd.DataFrame`
Loads 5 years (1,257 daily trading sessions) of real institutional asset returns.
