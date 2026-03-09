import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_imports():
    print("Testing imports...")
    try:
        from providers.llm_provider import LLMProvider
        from tools.market_tools import get_market_news, analyze_stock_trend, get_indian_market_indices
        from tools.kite_mcp_tool import KiteMCPWrapper
        from utils.calculator import calculate_profit_viability
        from agents.trading_agent import TradingAgent
        print("✅ All imports successful.")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    return True

def test_calculator():
    print("\nTesting Calculator...")
    from utils.calculator import calculate_profit_viability
    res = calculate_profit_viability(100000, 5, "gpt-4o", 5)
    print(f"Result: {res}")
    if res['is_viable']:
        print("✅ Calculator functional.")
    else:
        print("❌ Calculator check failed.")

def test_market_tools():
    print("\nTesting Market Tools...")
    from tools.market_tools import analyze_stock_trend
    # Test with a known symbol
    res = analyze_stock_trend("RELIANCE")
    print(f"Analysis for RELIANCE: {res.get('trend', 'Error')}")
    if "error" not in res:
        print("✅ Market tools (yfinance) functional.")
    else:
        print(f"⚠️ Market tools data fetch issues: {res.get('error')}")

def test_kite_wrapper():
    print("\nTesting Kite Wrapper (Lifecycle)...")
    from tools.kite_mcp_tool import KiteMCPWrapper
    try:
        wrapper = KiteMCPWrapper()
        # Should start thread and loop
        print("✅ KiteMCPWrapper initialized.")
        # Cleanup
        wrapper.disconnect()
        print("✅ KiteMCPWrapper disconnected.")
    except Exception as e:
        print(f"❌ KiteMCPWrapper test failed: {e}")

if __name__ == "__main__":
    if test_imports():
        test_calculator()
        test_market_tools()
        test_kite_wrapper()
    print("\nVerification complete.")
