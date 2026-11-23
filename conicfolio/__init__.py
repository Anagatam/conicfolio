"""
===============================================================================
CONICFOLIO PUBLIC PYTHON SDK
===============================================================================
Official Scikit-Learn compliant client for ConicFolio Hosted Optimization API.
Free tier: 60 requests / minute, up to 100 assets.
===============================================================================
"""

from conicfolio.client import (
    BaseConicClient,
    RiskParity,
    HierarchicalRiskParity,
    HierarchicalEqualRiskContribution,
    NestedClusteredOptimization,
    ConicPortfolio,
    set_api_key,
    set_api_endpoint,
)
from conicfolio.data import load_market_data

__version__ = "2.9.0"
__all__ = [
    "BaseConicClient",
    "RiskParity",
    "HierarchicalRiskParity",
    "HierarchicalEqualRiskContribution",
    "NestedClusteredOptimization",
    "ConicPortfolio",
    "set_api_key",
    "set_api_endpoint",
    "load_market_data",
]
