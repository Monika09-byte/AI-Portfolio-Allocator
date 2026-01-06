import pandas as pd
from sklearn.linear_model import LinearRegression


def predict_returns(data_path="data/market_returns.csv"):
    """
    Predict expected returns for each asset using Linear Regression.
    """
    df = pd.read_csv(data_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    if "Year" not in df.columns:
        raise ValueError(f"Expected 'Year' column, found {df.columns}")

    X = df[["Year"]]
    predictions = {}

    for asset in ["Equity", "Bonds", "Gold", "Cash"]:
        y = df[asset]

        model = LinearRegression()
        model.fit(X, y)

        next_year = pd.DataFrame(
            {"Year": [df["Year"].max() + 1]}
        )

        predictions[asset] = model.predict(next_year)[0]

    return predictions
