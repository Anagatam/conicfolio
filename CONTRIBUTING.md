# Contributing to ConicFolio

Thank you for your interest in contributing to the **ConicFolio Public Python SDK**!

We welcome community contributions to improve our Python client SDK, data connectors, documentation, benchmarks, and Jupyter tutorials.

---

## 🛠️ Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Anagatam/conicfolio.git
cd conicfolio
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 3. Run the Test Suite
```bash
pytest tests -q
```

---

## 📜 Contribution Guidelines

1. **Standard Estimator API**: All portfolio models must inherit from `BaseConicClient` and implement `fit(X, y)` and `predict(X)`.
2. **Type Hints & Clean Code**: Use Python 3.9+ type annotations on all public functions.
3. **Tests Required**: Every bug fix or feature addition must include a corresponding test in `tests/test_sdk.py`.
4. **Zero Solver Code**: Remember that this repository is the public thin-client SDK. Mathematical interior-point kernels are executed via the hosted API or on-premise enclaves.

---

## 📄 License
By contributing to ConicFolio, you agree that your contributions will be licensed under the [Apache-2.0 License](LICENSE).
