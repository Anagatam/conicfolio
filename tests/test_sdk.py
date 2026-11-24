"""
Unit tests for the public ConicFolio Python SDK.
Verifies payload serialization, estimator methods, and data loading.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock

import sys
import os
# Ensure public-sdk is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conicfolio import (
    BaseConicClient,
    RiskParity,
    HierarchicalRiskParity,
    HierarchicalEqualRiskContribution,
    NestedClusteredOptimization,
    ConicPortfolio,
    set_api_key,
    set_api_endpoint,
    load_market_data,
    load_real_market_universe,
)
from conicfolio.client import BaseEstimator


def test_public_sdk_data_loader():
    df = load_market_data(n_assets=5)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[1] == 5
    assert df.shape[0] > 100
    
    # Test load_real_market_universe alias
    df_alias = load_real_market_universe(n_assets=3)
    assert df_alias.shape[1] == 3


@patch("os.path.exists")
@patch("pandas.read_parquet")
def test_public_sdk_data_loader_local_parquet(mock_read_parquet, mock_exists):
    mock_exists.return_value = True
    fake_df = pd.DataFrame(np.ones((10, 20)))
    mock_read_parquet.return_value = fake_df
    
    df = load_market_data(n_assets=8)
    assert df.shape == (10, 8)
    mock_read_parquet.assert_called_once()


def test_base_estimator_get_and_set_params():
    est = BaseEstimator()
    est.model_name = "test_model"
    est.parameters = {"param1": 10}
    
    params = est.get_params()
    assert params["model_name"] == "test_model"
    assert params["param1"] == 10
    
    est.set_params(param1=20, param2="new")
    assert est.parameters["param1"] == 20
    assert est.parameters["param2"] == "new"
    
    # Setting an existing attribute directly
    est.set_params(model_name="updated_model")
    assert est.model_name == "updated_model"

    # Branch when self has no parameters dict initialized
    est2 = BaseEstimator()
    est2.set_params(extra_param=123)
    assert est2.parameters["extra_param"] == 123


def test_set_api_endpoint():
    set_api_endpoint("https://custom.endpoint.com/solve")
    client = RiskParity()
    assert client.endpoint_url == "https://custom.endpoint.com/solve"
    # Reset back to default
    set_api_endpoint("https://api.conicfolio.com/v1/optimize/solve")


@patch("requests.post")
def test_public_sdk_risk_parity_serialization(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "status": "OPTIMAL_CERTIFIED",
        "solve_time_ms": 0.28,
        "weights": [0.5, 0.5],
        "effective_assets": 2.0,
        "rate_limit": {"remaining_requests": 59}
    }
    mock_post.return_value = mock_resp

    set_api_key("cf_live_mock_test_key")
    cov = np.array([[0.04, 0.01], [0.01, 0.09]])

    model = RiskParity()
    model.fit(cov)

    assert mock_post.called
    args, kwargs = mock_post.call_args
    assert kwargs["headers"]["X-API-Key"] == "cf_live_mock_test_key"
    payload = kwargs["json"]
    assert payload["model"] == "risk_parity"
    assert len(payload["covariance_matrix"]) == 2

    assert len(model.weights_) == 2
    assert model.solve_time_ms_ == 0.28
    assert model.predict() is not None


@patch("requests.post")
def test_fit_returns_matrix_and_expected_returns(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "weights": [0.4, 0.6],
        "solve_time_ms": 0.15,
        "effective_assets": 1.9,
    }
    mock_post.return_value = mock_resp

    returns = np.random.randn(100, 2)
    expected_ret = np.array([0.05, 0.08])
    
    client = ConicPortfolio(objective="max_sharpe", api_key="my_key")
    weights = client.fit_predict(returns, y=expected_ret)
    
    assert len(weights) == 2
    _, kwargs = mock_post.call_args
    assert "returns_matrix" in kwargs["json"]
    assert "expected_returns" in kwargs["json"]


def test_predict_unfitted_raises():
    client = RiskParity()
    with pytest.raises(RuntimeError, match="Model is not fitted"):
        client.predict()


def test_model_subclasses_init():
    hrp = HierarchicalRiskParity(linkage="single")
    assert hrp.model_name == "hrp"
    assert hrp.parameters.get("parameters", {}).get("linkage") == "single"

    herc = HierarchicalEqualRiskContribution(n_clusters=4)
    assert herc.model_name == "herc"
    assert herc.parameters.get("parameters", {}).get("n_clusters") == 4

    nco = NestedClusteredOptimization(n_clusters=5)
    assert nco.model_name == "nco"
    assert nco.parameters.get("parameters", {}).get("n_clusters") == 5

    cp = ConicPortfolio(objective="cvar")
    assert cp.model_name == "cvar"


@patch("requests.post")
def test_public_sdk_rate_limit_handling(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.json.return_value = {
        "detail": {"retry_after_seconds": 45}
    }
    mock_post.return_value = mock_resp

    model = RiskParity()
    with pytest.raises(RuntimeError) as exc_info:
        model.fit(np.eye(3))
    assert "Rate limit exceeded" in str(exc_info.value)


@patch("requests.post")
def test_connection_error_handling(mock_post):
    import requests
    mock_post.side_effect = requests.exceptions.ConnectionError("Network down")
    model = RiskParity()
    with pytest.raises(ConnectionError, match="Failed to connect"):
        model.fit(np.eye(2))


@patch("requests.post")
def test_permission_error_handling(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 403
    mock_resp.text = "Forbidden key"
    mock_post.return_value = mock_resp

    model = RiskParity()
    with pytest.raises(PermissionError, match="403 Forbidden"):
        model.fit(np.eye(2))


@patch("requests.post")
def test_generic_api_error_handling(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.text = "Internal Server Error"
    mock_post.return_value = mock_resp

    model = RiskParity()
    with pytest.raises(RuntimeError, match="ConicFolio API Error \\(500\\)"):
        model.fit(np.eye(2))
