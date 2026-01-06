def get_risk_profile(risk_level):
    """
    Returns asset allocation weights based on user's risk appetite.
    """

    if risk_level == "Low":
        return {
            "Equity": 0.2,
            "Bonds": 0.5,
            "Gold": 0.2,
            "Cash": 0.1
        }

    elif risk_level == "Medium":
        return {
            "Equity": 0.4,
            "Bonds": 0.3,
            "Gold": 0.2,
            "Cash": 0.1
        }

    else:  # High Risk
        return {
            "Equity": 0.6,
            "Bonds": 0.2,
            "Gold": 0.1,
            "Cash": 0.1
        }
