"""
===============================================================================
CONICFOLIO PUBLIC THIN-CLIENT CORE
===============================================================================
Official Scikit-Learn wrapper for ConicFolio Hosted Optimization API.
===============================================================================
"""

from typing import Optional, Dict, Any, Union, List
import os
import numpy as np
import requests
from sklearn.base import BaseEstimator


_DEFAULT_ENDPOINT = os.getenv("CONICFOLIO_API_URL", "https://api.conicfolio.com/v1/optimize/solve")
_GLOBAL_API_KEY = os.getenv("CONICFOLIO_API_KEY", None)


def set_api_key(api_key: str):
    """Set global ConicFolio API key for the current Python session."""
    global _GLOBAL_API_KEY
    _GLOBAL_API_KEY = api_key


def set_api_endpoint(endpoint_url: str):
    """Set custom endpoint URL (useful for local testing or private proxy)."""
    global _DEFAULT_ENDPOINT
    _DEFAULT_ENDPOINT = endpoint_url


class BaseConicClient(BaseEstimator):
    """
    Base estimator sending convex/conic portfolio tasks to the hosted API.
    """
    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        **parameters
    ):
        self.model_name = model_name
        self.api_key = api_key or _GLOBAL_API_KEY
        self.endpoint_url = endpoint_url or _DEFAULT_ENDPOINT
        self.parameters = parameters

        self.weights_: Optional[np.ndarray] = None
        self.solve_time_ms_: Optional[float] = None
        self.effective_assets_: Optional[float] = None
        self.rate_limit_info_: Optional[Dict[str, Any]] = None

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None):
        """
        Send optimization payload to ConicFolio API.
        
        Args:
            X: Asset returns matrix (T x N) or square covariance matrix (N x N).
            y: Optional expected return vector (N-length).
        """
        mat = np.asarray(X, dtype=np.float64)

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "parameters": self.parameters,
        }

        if mat.shape[0] == mat.shape[1]:
            payload["covariance_matrix"] = mat.tolist()
        else:
            payload["returns_matrix"] = mat.tolist()

        if y is not None:
            payload["expected_returns"] = np.asarray(y, dtype=np.float64).tolist()

        headers = {"Content-Type": "application/json"}
        active_key = self.api_key or _GLOBAL_API_KEY
        if active_key:
            headers["X-API-Key"] = active_key

        try:
            resp = requests.post(
                self.endpoint_url,
                json=payload,
                headers=headers,
                timeout=15.0
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to ConicFolio Optimization API: {e}")

        if resp.status_code == 429:
            data = resp.json().get("detail", {})
            retry_sec = data.get("retry_after_seconds", 60)
            raise RuntimeError(
                f"Rate limit exceeded (60 req/min). Retry in {retry_sec} seconds. "
                f"Upgrade key at https://conicfolio.com"
            )

        if resp.status_code == 403:
            raise PermissionError(f"ConicFolio API Error (403 Forbidden): {resp.text}")

        if resp.status_code != 200:
            raise RuntimeError(f"ConicFolio API Error ({resp.status_code}): {resp.text}")

        res = resp.json()
        self.weights_ = np.asarray(res["weights"], dtype=np.float64)
        self.solve_time_ms_ = res.get("solve_time_ms")
        self.effective_assets_ = res.get("effective_assets")
        self.rate_limit_info_ = res.get("rate_limit", {})
        return self

    def predict(self, X: Optional[np.ndarray] = None) -> np.ndarray:
        if self.weights_ is None:
            raise RuntimeError("Model is not fitted. Call fit() first.")
        return self.weights_

    def fit_predict(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> np.ndarray:
        return self.fit(X, y).predict()


class RiskParity(BaseConicClient):
    """Equal Risk Contribution (Spinu Newton Engine)."""
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__("risk_parity", api_key=api_key, **kwargs)


class HierarchicalRiskParity(BaseConicClient):
    """Hierarchical Risk Parity (HRP)."""
    def __init__(self, linkage: str = "ward", api_key: Optional[str] = None, **kwargs):
        super().__init__("hrp", api_key=api_key, parameters={"linkage": linkage}, **kwargs)


class HierarchicalEqualRiskContribution(BaseConicClient):
    """Hierarchical Equal Risk Contribution (HERC)."""
    def __init__(self, n_clusters: int = 3, api_key: Optional[str] = None, **kwargs):
        super().__init__("herc", api_key=api_key, parameters={"n_clusters": n_clusters}, **kwargs)


class NestedClusteredOptimization(BaseConicClient):
    """Nested Clustered Optimization (NCO)."""
    def __init__(self, n_clusters: int = 3, api_key: Optional[str] = None, **kwargs):
        super().__init__("nco", api_key=api_key, parameters={"n_clusters": n_clusters}, **kwargs)


class ConicPortfolio(BaseConicClient):
    """Conic Portfolio (min_variance, max_sharpe, cvar, evar)."""
    def __init__(self, objective: str = "min_variance", api_key: Optional[str] = None, **kwargs):
        super().__init__(objective, api_key=api_key, **kwargs)
