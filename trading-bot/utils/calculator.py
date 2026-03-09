import litellm
import sys

def calculate_profit_viability(
    investment_amount: float,
    expected_daily_return_pct: float,
    model: str,
    cycles_per_day: int,
    tokens_per_cycle: int = 3000
):
    """
    Advanced viability calculator considering multiple cycles and token usage.
    """

    # Prices per 1k tokens (approximate)
    model_prices = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "claude-3-5-sonnet-20240620": {"input": 0.003, "output": 0.015},
        "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
        "ollama": {"input": 0.0, "output": 0.0} # Free if local
    }

    # Find matching model price
    price = None
    for k, v in model_prices.items():
        if k in model:
            price = v
            break

    if not price:
        price = {"input": 0.005, "output": 0.015} # Default to gpt-4o pricing

    # Assume 70% input, 30% output tokens
    input_tokens = tokens_per_cycle * 0.7
    output_tokens = tokens_per_cycle * 0.3

    cost_per_cycle = (input_tokens / 1000 * price["input"]) + (output_tokens / 1000 * price["output"])
    daily_llm_cost = cycles_per_day * cost_per_cycle

    daily_gross_profit = investment_amount * (expected_daily_return_pct / 100)
    net_profit = daily_gross_profit - daily_llm_cost

    return {
        "model": model,
        "investment": investment_amount,
        "daily_gross_profit": round(daily_gross_profit, 2),
        "daily_llm_cost": round(daily_llm_cost, 4),
        "net_profit": round(net_profit, 2),
        "break_even_return_pct": round((daily_llm_cost / investment_amount) * 100, 4),
        "is_viable": net_profit > 0
    }

if __name__ == "__main__":
    if len(sys.argv) == 5:
        inv = float(sys.argv[1])
        ret = float(sys.argv[2])
        mod = sys.argv[3]
        cyc = int(sys.argv[4])
        res = calculate_profit_viability(inv, ret, mod, cyc)
        for k, v in res.items():
            print(f"{k:25}: {v}")
    else:
        print("Usage: python calculator.py <investment> <return_pct> <model> <cycles>")
        print("\nExample for 1 Lakh INR with 5% target using GPT-4o:")
        res = calculate_profit_viability(100000, 5, "gpt-4o", 10)
        for k, v in res.items():
            print(f"{k:25}: {v}")
