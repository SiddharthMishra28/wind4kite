# 🚀 Wind4Kite: Advanced AI Stock Trading Bot

Wind4Kite is a state-of-the-art, multi-agent AI trading bot optimized for the Indian Stock Market (NSE/BSE). It leverages the **Model Context Protocol (MCP)** to integrate directly with **Zerodha Kite**, uses **LiteLLM** for vendor-agnostic AI intelligence, and is designed to maximize profit while minimizing API costs.

---

## 🌟 Key Features

*   **Zerodha Kite MCP Integration**: Native support for Zerodha's Model Context Protocol for secure trade execution and portfolio management.
*   **Multi-Agent Orchestration**:
    *   **Market Researcher**: Scrapes Google News RSS and analyzes Indian market sentiment.
    *   **Technical Analyst**: Calculates advanced indicators (RSI, SMA50, SMA200) using `yfinance`.
    *   **Execution Trader**: Orchestrates trades based on LLM decisions with a safety-first approach.
*   **Vendor Agnostic (LiteLLM)**: Support for OpenAI (GPT-4o), Anthropic (Claude 3.5), Ollama (local LLMs), and more.
*   **Profitability Calculator**: Built-in tool to estimate if your strategy is viable after factoring in LLM API token costs.
*   **Dry-Run Mode**: Default safety mode to simulate trades before committing real capital.
*   **Optimized API Usage**: Designed to perform deep analysis in minimal cycles to preserve ROI.

---

## 🏗️ Architecture

```text
[ Market Data ] -> [ Market Researcher ] --+
                                           |
[ Indicators  ] -> [ Technical Analyst ] --+--> [ Trading Agent ] -> [ Kite MCP ] -> [ Zerodha ]
                                           |
[ Portfolio   ] -> [ Kite MCP Client   ] --+
```

---

## 🛠️ Setup Instructions

### 1. Prerequisites
*   Python 3.10+
*   [uv](https://github.com/astral-sh/uv) (Highly recommended for dependency management)
*   Node.js (for running the Kite MCP server via `npx`)
*   Zerodha Kite account with API access (optional for local, but required for hosted MCP)

### 2. Installation
Clone the repository and install dependencies:
```bash
cd trading-bot
uv sync
```

### 3. Environment Configuration
Create a `.env` file in the `trading-bot` directory:
```env
OPENAI_API_KEY=your_openai_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_key_here
# For local LLMs via Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 📈 Usage

### Running the Trading Bot
The bot runs in **Dry-Run** mode by default. To start a trading cycle:
```bash
uv run python agents/trading_agent.py
```
To enable live trading, modify `agents/trading_agent.py`:
```python
agent = TradingAgent(provider, dry_run=False) # SET TO FALSE AT YOUR OWN RISK
```

### Using the Profitability Calculator
Before running the bot, use the calculator to ensure your investment size covers the LLM costs:
```bash
# Usage: uv run python utils/calculator.py <investment_in_inr> <expected_return_pct> <model_name> <cycles_per_day>
uv run python utils/calculator.py 100000 5 gpt-4o 10
```

### Verifying the Setup
Run the built-in verification script to check imports, market data access, and Kite connectivity:
```bash
uv run python verify_bot.py
```

---

## 🤖 Selecting an Inference Provider

Wind4Kite uses LiteLLM, allowing you to switch providers easily in `agents/trading_agent.py`:

| Provider | Model Name | Pros |
| :--- | :--- | :--- |
| **OpenAI** | `gpt-4o` | Highly accurate, reliable. |
| **Anthropic** | `claude-3-5-sonnet-20240620` | Exceptional reasoning for technical analysis. |
| **Ollama** | `ollama/llama3` | **Zero cost**, runs locally, private. |
| **OpenAI Mini**| `gpt-4o-mini` | Extremely low cost, great for frequent cycles. |

---

## 🛡️ Safety & Disclaimer

*   **Risk Warning**: Trading stocks involves significant risk of loss. This bot is provided for educational purposes.
*   **Dry Run**: Always test your strategy in dry-run mode for several days before live execution.
*   **Cost Management**: Monitor your API usage on your provider's dashboard. Use the `utils/calculator.py` frequently.
*   **Kite MCP**: Ensure you are authorized with Zerodha. The hosted version at `mcp.kite.trade` may have restricted write permissions by default.

---

## 📝 License
MIT License. See [LICENSE](LICENSE) for details.
