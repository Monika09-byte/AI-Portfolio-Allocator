import numpy as np


def optimize_portfolio(predicted_returns, risk_profile):
    """
    Combine predicted returns with risk profile
    to generate final portfolio weights.
    """

    assets = list(predicted_returns.keys())

    # Convert to arrays
    returns = np.array([predicted_returns[a] for a in assets])
    base_weights = np.array([risk_profile[a] for a in assets])

    # Risk-adjusted weighting
    adjusted_weights = returns * base_weights

    # Normalize so total = 1
    final_weights = adjusted_weights / np.sum(adjusted_weights)

    return dict(zip(assets, final_weights.round(3)))
