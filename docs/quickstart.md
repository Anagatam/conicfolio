# Quickstart Guide

Get up and running with **ConicFolio** in less than 60 seconds.

---

## 1. Installation

Install the official Python package from [PyPI](https://pypi.org/project/conicfolio/):

```bash
pip install conicfolio
```

---

## 2. Basic Usage (3 Lines of Code)

ConicFolio bundles 5 years (1,257 trading days) of real-world institutional multi-asset market returns.

```python
import conicfolio as cf

# 1. Load institutional market returns
returns = cf.load_market_data(n_assets=10)

# 2. Fit the Equal Risk Contribution model
model = cf.RiskParity()
model.fit(returns)

# 3. Access optimal weights and execution metrics
print("Optimal Allocations:")
for asset, weight in zip(returns.columns, model.weights_):
    print(f"  {asset}: {weight * 100:.2f}%")

print(f"\nSolved in: {model.solve_time_ms_} ms")
```

---

## 3. Configuring Your Free API Key

Anyone can generate a free API key at [conicfolio.com](https://conicfolio.com).

```python
import conicfolio as cf

# Set key globally for your Python session
cf.set_api_key("cf_live_YOUR_FREE_API_KEY")

# Or pass it directly to the estimator
model = cf.RiskParity(api_key="cf_live_YOUR_FREE_API_KEY")
model.fit(returns)
```

---

## 4. Scikit-Learn Pipeline Integration

ConicFolio estimators are 100% compliant with Scikit-Learn:

```python
from sklearn.pipeline import Pipeline
import conicfolio as cf

pipeline = Pipeline([
    ('optimizer', cf.RiskParity())
])

pipeline.fit(returns)
weights = pipeline.named_steps['optimizer'].weights_
```
