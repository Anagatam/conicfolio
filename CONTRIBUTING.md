# Contributing to ConicFolio

Thank you for your interest in contributing to the **ConicFolio Public Python SDK**.

We welcome contributions to improve our Python client SDK, data connectors, documentation, benchmarks, and interactive tutorials.

---

## Development Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Anagatam/conicfolio.git
cd conicfolio
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 3. Run the Test Suite

```bash
pytest tests -v --tb=short
```

---

## Code Style & Engineering Standards

All contributions must adhere to our automated code quality standards:

1. **Code Formatting**: Code must be formatted using `black` (88-character column limit) following PEP 8 conventions.
   ```bash
   black --check conicfolio tests
   ```
2. **Static Type Checking**: All public methods and functions must provide complete PEP 484 type annotations and pass `mypy`.
   ```bash
   mypy --strict conicfolio
   ```
3. **Linting**: Code must pass `flake8` and `ruff` checks with zero warnings.
4. **Standard Estimator Conventions**: Estimators must inherit from `BaseConicClient` and implement self-contained `fit(X, y)` and `predict(X)` interfaces with zero third-party ML framework dependencies.
5. **Test Coverage**: Every bug fix, model connector, or parameter update must include corresponding unit tests in `tests/test_sdk.py`.
6. **Zero Solver Code**: This repository is the public thin-client SDK. Mathematical interior-point kernels, cone decompositions, and private algorithms are strictly executed via the hosted API or on-premise enclaves.

---

## Benchmarking Protocol

When submitting performance PRs or benchmark additions:

- Isolate algorithmic computation using monotonic timers (`time.perf_counter()`).
- Perform at least 50 warm-up runs prior to data collection.
- Report results across multiple universe dimensions ($N \in [5, 10, 25, 50, 100]$) citing hardware specifications and runtime environment.

---

## License

By contributing to ConicFolio, you agree that your contributions will be licensed under the [Apache-2.0 License](LICENSE).
