import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from models.return_predictor import predict_returns
from utils.risk_profiler import get_risk_profile
from optimization.portfolio_optimizer import optimize_portfolio


# ================== Helper Function ==================
def calculate_portfolio_metrics(weights, returns):
    """
    Calculate expected return, volatility, and Sharpe ratio.
    """
    w = []
    r = []

    for asset in weights:
        w.append(weights[asset])
        r.append(returns[asset])

    w = pd.Series(w)
    r = pd.Series(r)

    expected_return = (w * r).sum()

    # Simple volatility proxy (academic-friendly)
    volatility = (w * (r - r.mean()) ** 2).sum() ** 0.5

    # Risk-free rate assumption (Cash = 4%)
    risk_free_rate = 0.04
    sharpe_ratio = (
        (expected_return - risk_free_rate) / volatility
        if volatility != 0 else 0
    )

    return expected_return, volatility, sharpe_ratio


# ================== Page Config ==================
st.set_page_config(
    page_title="AI Portfolio Allocator",
    page_icon="📊",
    layout="wide"
)

# ================== Header ==================
st.markdown("## 📊 AI Portfolio Allocator")
st.caption("Smart investment allocation using Machine Learning, risk profiling, and scenario analysis")

st.divider()

# ================== Sidebar ==================
st.sidebar.header("🔧 User Input")

risk_level = st.sidebar.selectbox(
    "Risk Appetite",
    ["Low", "Medium", "High"]
)

# ---------- Risk Explanation (STEP 1) ----------
risk_info = {
    "Low": "🟢 Capital preservation focused. Low volatility and stable returns.",
    "Medium": "🟡 Balanced growth with moderate risk.",
    "High": "🔴 Aggressive growth with high volatility and return potential."
}

st.sidebar.markdown("### 🧠 Risk Explanation")
st.sidebar.info(risk_info[risk_level])

investment_amount = st.sidebar.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    step=1000,
    value=10000
)

# ---------- Scenario Selector (STEP 4) ----------
market_scenario = st.sidebar.selectbox(
    "Market Scenario",
    ["Normal", "Bull", "Bear"]
)

generate = st.sidebar.button("🚀 Generate Portfolio")

# ================== Main Logic ==================
if generate:
    # ---------- Core Logic ----------
    risk_profile = get_risk_profile(risk_level)
    predicted_returns = predict_returns()

    # ---------- Scenario Adjustment ----------
    scenario_multiplier = {
        "Bull": 1.15,
        "Normal": 1.0,
        "Bear": 0.85
    }

    multiplier = scenario_multiplier[market_scenario]

    adjusted_returns = {
        asset: ret * multiplier
        for asset, ret in predicted_returns.items()
    }

    # ---------- Optimization ----------
    final_portfolio = optimize_portfolio(adjusted_returns, risk_profile)

    # ---------- Risk Metrics (STEP 3) ----------
    portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_metrics(
        final_portfolio, adjusted_returns
    )

    # ---------- Top Metrics ----------
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Investment Amount", f"₹ {investment_amount:,.0f}")
    col2.metric("📈 Expected Return", f"{portfolio_return * 100:.2f}%")
    col3.metric("⚠️ Portfolio Risk", f"{portfolio_volatility * 100:.2f}%")

    st.caption(
        f"📊 Sharpe Ratio: **{sharpe_ratio:.2f}** | "
        f"Scenario: **{market_scenario}**"
    )

    st.divider()

    # ---------- Allocation Table ----------
    allocation_rows = []
    for asset, weight in final_portfolio.items():
        allocation_rows.append([
            asset,
            weight * 100,
            weight * investment_amount
        ])

    df = pd.DataFrame(
        allocation_rows,
        columns=["Asset", "Allocation (%)", "Amount (₹)"]
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("✅ Recommended Allocation")
        st.dataframe(
            df.style.format({
                "Allocation (%)": "{:.2f}",
                "Amount (₹)": "₹ {:,.0f}"
            }),
            use_container_width=True
        )

    # ---------- Pie Chart ----------
    with right:
        st.subheader("📊 Portfolio Distribution")

        fig, ax = plt.subplots()
        ax.pie(
            df["Allocation (%)"],
            labels=df["Asset"],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": "white"}
        )
        ax.axis("equal")
        st.pyplot(fig)

    st.divider()

    # ---------- Returns ----------
    st.subheader(f"📈 Expected Returns (Scenario: {market_scenario})")

    r1, r2, r3, r4 = st.columns(4)
    items = list(adjusted_returns.items())

    r1.metric("Equity", f"{items[0][1] * 100:.2f}%")
    r2.metric("Bonds", f"{items[1][1] * 100:.2f}%")
    r3.metric("Gold", f"{items[2][1] * 100:.2f}%")
    r4.metric("Cash", f"{items[3][1] * 100:.2f}%")

else:
    st.info("👈 Select inputs from the sidebar and click **Generate Portfolio**")
