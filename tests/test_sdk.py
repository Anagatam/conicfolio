"""
Unit tests for the public ConicFolio Python SDK.
Verifies payload serialization, scikit-learn compliance, and data loading.
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
    RiskParity,
    HierarchicalRiskParity,
    HierarchicalEqualRiskContribution,
    ConicPortfolio,
    set_api_key,
    load_market_data,
)


def test_public_sdk_data_loader():
    df = load_market_data(n_assets=5)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[1] == 5
    assert df.shape[0] > 100


@patch("requests.post")
def test_public_sdk_risk_parity_serialization(mock_post):
    # Mock API response from hosted server
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
