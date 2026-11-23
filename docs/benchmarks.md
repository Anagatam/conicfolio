# Empirical Benchmarks

Head-to-head empirical benchmark evaluating solve latency across public optimization solvers on identical 5-year institutional daily returns (1,257 sessions across 15 instruments).

---

## Latency Benchmark Table

| Optimization Family | ConicFolio Engine | Solve Latency | Public Open-Source Baseline | Speedup Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Equal Risk Contribution (ERC)** | Spinu Newton-Raphson | **0.29 ms** | 9.94 ms | **34.3x FASTER** |
| **Hierarchical Risk Parity (HRP)** | Recursive Bisection | **0.86 ms** | 7.01 ms | **8.2x FASTER** |
| **Hierarchical Equal Risk (HERC)**| Cluster Risk Parity | **0.59 ms** | 5.91 ms | **10.0x FASTER** |
| **Nested Clustered Opt (NCO)** | Denoised K-Means | **0.89 ms** | 64.59 ms | **72.6x FASTER** |
| **Critical Line Algorithm (CLA)** | Exact Karush-Kuhn-Tucker| **1.73 ms** | 13.67 ms | **7.9x FASTER** |
| **Equal-Weighted (1/N Naive)** | Vectorized SIMD | **0.01 ms** | 0.47 ms | **47.0x FASTER** |

![ConicFolio Speed Benchmark Comparison](assets/benchmark_speed_comparison.png)

---

## Benchmark Reproduction

Benchmarks are 100% reproducible using real market data:

```bash
git clone https://github.com/Anagatam/conicfolio.git
cd conicfolio
python -m pytest tests/test_sdk.py -v
```
