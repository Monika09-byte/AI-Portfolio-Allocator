from models.return_predictor import predict_returns
from utils.risk_profiler import get_risk_profile
from optimization.portfolio_optimizer import optimize_portfolio


def main():
    print("=== AI Portfolio Allocator ===\n")

    # User input
    risk_level = input("Enter risk level (Low / Medium / High): ").strip()

    # Step 1: Risk profiling
    risk_profile = get_risk_profile(risk_level)

    # Step 2: ML return prediction
    predicted_returns = predict_returns()

    # Step 3: Portfolio optimization
    final_portfolio = optimize_portfolio(predicted_returns, risk_profile)

    print("\nRecommended Portfolio Allocation:\n")
    for asset, weight in final_portfolio.items():
        print(f"{asset}: {weight * 100:.2f}%")

    print("\nExpected Returns (ML Predicted):")
    for asset, ret in predicted_returns.items():
        print(f"{asset}: {ret:.2%}")


if __name__ == "__main__":
    main()
