from providers.llm_provider import LLMProvider
from tools.market_tools import get_market_news, analyze_stock_trend, get_indian_market_indices
from tools.kite_mcp_tool import KiteMCPWrapper
import json
import os

class TradingAgent:
    def __init__(self, provider: LLMProvider, dry_run: bool = True):
        self.provider = provider
        self.kite = KiteMCPWrapper()
        self.dry_run = dry_run
        self.history = []

    def run_trading_cycle(self, target_profit_pct: float = 5.0):
        print(f"--- Starting trading cycle (Dry Run: {self.dry_run}) ---")

        # 1. Market Research
        indices = get_indian_market_indices()
        news = get_market_news("top performing NSE stocks today")

        research_prompt = f"""
        Current Indian Market Status: {json.dumps(indices)}
        Latest Market News: {json.dumps(news[:5])}

        As an expert Indian stock market analyst, identify 5-7 NSE stock symbols that show strong momentum or are mentioned positively in recent news.
        Provide only a comma-separated list of symbols.
        """

        research_response = self.provider.completion([{"role": "user", "content": research_prompt}])
        suggested_symbols = research_response.choices[0].message.content.strip().split(",")
        suggested_symbols = [s.strip().replace(".NS", "") for s in suggested_symbols if s.strip()]

        print(f"Candidate stocks: {suggested_symbols}")

        # 2. Advanced Technical Analysis
        analysis_results = []
        for symbol in suggested_symbols:
            analysis = analyze_stock_trend(symbol)
            if "error" not in analysis:
                analysis_results.append(analysis)

        # 3. Decision Making
        holdings = self.kite.get_holdings()

        decision_prompt = f"""
        Strategy Goal: {target_profit_pct}% daily return.

        Technical Data for candidates: {json.dumps(analysis_results)}
        Current Portfolio Holdings: {json.dumps(holdings)}

        Instructions:
        1. Analyze the technicals (RSI, Trends, SMA).
        2. Buy stocks with 'Strong Bullish' or 'Bullish' trends and RSI < 70.
        3. Sell stocks in holdings if they show 'Bearish' trends or RSI > 75.
        4. Be aggressive but calculated to reach the {target_profit_pct}% goal.

        Respond ONLY with a JSON list of objects:
        [{"symbol": "TATASTEEL", "action": "BUY", "quantity": 10, "order_type": "MARKET", "product": "MIS"}, ...]
        Valid actions: BUY, SELL. Product: CNC for long term, MIS for intraday.
        """

        decision_response = self.provider.completion([{"role": "user", "content": decision_prompt}])
        try:
            content = decision_response.choices[0].message.content
            # Clean up potential markdown blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            actions = json.loads(content)
            print(f"Decided actions: {len(actions)}")

            # 4. Execution
            for action in actions:
                symbol = action['symbol']
                if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
                    # Kite often expects just the symbol if exchange is specified
                    pass

                print(f"ACTION: {action['action']} {action['quantity']} of {symbol}")

                if not self.dry_run:
                    try:
                        result = self.kite.place_order(
                            variety="regular",
                            exchange="NSE",
                            tradingsymbol=symbol,
                            transaction_type=action['action'],
                            quantity=int(action['quantity']),
                            product=action.get('product', 'MIS'),
                            order_type=action.get('order_type', 'MARKET'),
                            price=action.get('price'),
                            trigger_price=action.get('trigger_price')
                        )
                        print(f"Execution Result: {result}")
                    except Exception as e:
                        print(f"Execution failed for {symbol}: {e}")
                else:
                    print(f"DRY RUN: Order for {symbol} skipped.")

        except Exception as e:
            print(f"Failed to process decisions: {e}")
            print(f"Raw response: {decision_response.choices[0].message.content if decision_response else 'None'}")

        cost = self.provider.get_cost(research_response) + self.provider.get_cost(decision_response)
        print(f"Cycle Cost: ${cost:.4f}")
        return cost

if __name__ == "__main__":
    # Ensure API key exists for testing
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy")

    provider = LLMProvider(model="gpt-4o")
    agent = TradingAgent(provider, dry_run=True)
    agent.run_trading_cycle()
