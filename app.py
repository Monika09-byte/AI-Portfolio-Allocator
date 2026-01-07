import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from models.return_predictor import predict_returns
from utils.risk_profiler import get_risk_profile
from optimization.portfolio_optimizer import optimize_portfolio


# ---------- Page Config ----------
st.set_page_config(
    page_title="AI Portfolio Allocator",
    page_icon="📊",
    layout="wide"
)

# ---------- Header ----------
st.markdown("## 📊 AI Portfolio Allocator")
st.caption("Smart investment allocation using Machine Learning & risk profiling")

st.divider()

# ---------- Sidebar ----------
st.sidebar.header("🔧 User Input")

risk_level = st.sidebar.selectbox(
    "Risk Appetite",
    ["Low", "Medium", "High"]
)

# 🔹 STEP 1: Risk Explanation Panel (NEW)
risk_info = {
    "Low": "🟢 Capital preservation focused. Low volatility and stable returns. Suitable for conservative investors.",
    "Medium": "🟡 Balanced strategy with moderate risk and steady growth. Suitable for long-term investors.",
    "High": "🔴 Aggressive growth strategy with high volatility and higher return potential."
}

st.sidebar.markdown("### 🧠 Risk Explanation")
st.sidebar.info(risk_info[risk_level])

investment_amount = st.sidebar.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    step=1000,
    value=10000
)

generate = st.sidebar.button("🚀 Generate Portfolio")

# ---------- Main Logic ----------
if generate:
    risk_profile = get_risk_profile(risk_level)
    predicted_returns = predict_returns()
    final_portfolio = optimize_portfolio(predicted_returns, risk_profile)

    # ---------- Metrics ----------
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Investment Amount", f"₹ {investment_amount:,.0f}")
    col2.metric("⚖️ Risk Level", risk_level)
    col3.metric(
        "📈 Avg Expected Return",
        f"{sum(predicted_returns.values()) / len(predicted_returns) * 100:.2f}%"
    )

    st.divider()

    # ---------- Allocation Data ----------
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

    # ---------- Layout ----------
    left, right = st.columns([1.2, 1])

    # ---------- Left: Table ----------
    with left:
        st.subheader("✅ Recommended Allocation")
        st.dataframe(
            df.style.format({
                "Allocation (%)": "{:.2f}",
                "Amount (₹)": "₹ {:,.0f}"
            }),
            use_container_width=True
        )

    # ---------- Right: Pie Chart ----------
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
    st.subheader("📈 Expected Returns (ML Predicted)")

    r1, r2, r3, r4 = st.columns(4)
    returns_items = list(predicted_returns.items())

    r1.metric("Equity", f"{returns_items[0][1]*100:.2f}%")
    r2.metric("Bonds", f"{returns_items[1][1]*100:.2f}%")
    r3.metric("Gold", f"{returns_items[2][1]*100:.2f}%")
    r4.metric("Cash", f"{returns_items[3][1]*100:.2f}%")

else:
    st.info("👈 Select inputs from the sidebar and click **Generate Portfolio**")
