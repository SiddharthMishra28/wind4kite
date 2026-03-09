import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import re

def get_market_news(query: str = "India stock market"):
    """Fetches news related to the query from multiple sources."""
    news_items = []

    # Try Google News RSS for more structured data
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        response = requests.get(rss_url, timeout=10)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        for item in items[:10]:
            news_items.append({
                "title": item.title.text,
                "link": item.link.text,
                "pub_date": item.pubDate.text,
                "summary": "" # RSS often doesn't have full summary
            })
    except Exception as e:
        print(f"RSS fetch failed: {e}")

    return news_items

def analyze_stock_trend(symbol: str, period: str = "6mo"):
    """Advanced trend analysis using multiple indicators."""
    if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
        symbol += ".NS"

    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)

        if hist.empty:
            return {"symbol": symbol, "error": "No data found"}

        # Calculate Technical Indicators
        # SMA
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA200'] = hist['Close'].rolling(window=200).mean()

        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))

        current_price = hist['Close'].iloc[-1]
        rsi = hist['RSI'].iloc[-1]
        sma50 = hist['SMA50'].iloc[-1]
        sma200 = hist['SMA200'].iloc[-1]

        # Trend Evaluation
        trend = "Neutral"
        if current_price > sma50 > sma200:
            trend = "Strong Bullish"
        elif current_price > sma50:
            trend = "Bullish"
        elif current_price < sma50 < sma200:
            trend = "Strong Bearish"
        elif current_price < sma50:
            trend = "Bearish"

        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "rsi": round(rsi, 2) if not pd.isna(rsi) else None,
            "sma50": round(sma50, 2) if not pd.isna(sma50) else None,
            "sma200": round(sma200, 2) if not pd.isna(sma200) else None,
            "trend": trend,
            "high_52w": round(hist['High'].max(), 2),
            "low_52w": round(hist['Low'].min(), 2)
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}

def get_indian_market_indices():
    """Fetches current status of major Indian market indices."""
    indices = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "NIFTY BANK": "^NSEBANK"}
    results = {}
    for name, ticker in indices.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_close = hist['Close'].iloc[-1]
                change = curr_close - prev_close
                change_pct = (change / prev_close) * 100
                results[name] = {
                    "price": round(curr_close, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2)
                }
        except:
            continue
    return results
