import ccxt
import time

# Initialize Binance API (No API Key needed for public data)
exchange = ccxt.binance()

# List of cryptocurrency pairs
COINS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ADA/USDT", "XRP/USDT", "BNB/USDT", "DOGE/USDT", "SHIB/USDT", "TRX/USDT", "TRUMP/USDT"]

# RSI Parameters
TIMEFRAME = "3m"  # Binance supports 8-hour timeframe
RSI_PERIOD = 14  # RSI calculation period
OVERBOUGHT = 70
OVERSOLD = 30


def fetch_ohlcv(symbol):
    """Fetch OHLCV data from Binance."""
    try:
        return exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=RSI_PERIOD + 5)
    except Exception as e:
        print(f"Error fetching OHLCV for {symbol}: {e}")
        return None


def calculate_rsi(prices):
    """Calculate RSI based on closing prices."""
    if len(prices) < RSI_PERIOD + 1:
        return None  # Not enough data

    gains, losses = [], []
    for i in range(1, RSI_PERIOD + 1):
        change = prices[i] - prices[i - 1]
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))

    avg_gain = sum(gains) / RSI_PERIOD
    avg_loss = sum(losses) / RSI_PERIOD

    if avg_loss == 0:
        return 100  # Avoid division by zero, assume max RSI

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return round(rsi, 2)


def fetch_rsi(symbol):
    """Fetch RSI indicator for a given cryptocurrency pair from Binance."""
    ohlcv = fetch_ohlcv(symbol)
    if not ohlcv:
        return None

    prices = [candle[4] for candle in ohlcv]  # Closing prices
    return calculate_rsi(prices)


def fetch_price(symbol):
    """Fetch the latest price for a given cryptocurrency pair."""
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None


def detect_divergence(symbol):
    """Определяет дивергенцию и ее силу"""
    ohlcv = fetch_ohlcv(symbol)
    if not ohlcv:
        return None

    prices = [candle[4] for candle in ohlcv]  # Закрытые цены
    rsi_values = [calculate_rsi(prices[i:i + RSI_PERIOD + 1]) for i in range(len(prices) - RSI_PERIOD)]
    rsi_values = [rsi for rsi in rsi_values if rsi is not None]

    if len(rsi_values) < 3:
        return None

    recent_prices = prices[-3:]
    recent_rsi = rsi_values[-3:]

    price_change = abs(recent_prices[2] - recent_prices[0])
    rsi_change = abs(recent_rsi[2] - recent_rsi[0])

    # Классификация по разнице RSI
    if rsi_change >= 10:
        strength = "Strong 💪"
    elif rsi_change >= 5:
        strength = "Moderate ⚖"
    else:
        strength = "Weak ❌"

    # Бычья дивергенция
    if recent_prices[0] > recent_prices[2] and recent_rsi[0] < recent_rsi[2]:
        return f"Bullish Divergence 🟢 ({strength})"

    # Медвежья дивергенция
    if recent_prices[0] < recent_prices[2] and recent_rsi[0] > recent_rsi[2]:
        return f"Bearish Divergence 🔴 ({strength})"

    return "No Divergence"



def check_rsi_signals():
    """Fetch RSI and price, then print buy/sell signals and divergence."""
    print("\n=== RSI SIGNAL BOT (BINANCE) ===\n")

    for symbol in COINS:
        rsi = fetch_rsi(symbol)
        price = fetch_price(symbol)
        divergence = detect_divergence(symbol)

        if rsi is None or price is None:
            print(f"{symbol}: Unable to retrieve RSI or price data\n")
            continue

        signal = "NEUTRAL"
        if rsi < OVERSOLD:
            signal = "BUY 📈 (Oversold)"
        elif rsi > OVERBOUGHT:
            signal = "SELL 📉 (Overbought)"

        print(f"{symbol} - Price: ${price:.2f} | RSI: {rsi} | Signal: {signal} | {divergence}\n")


while True:
    check_rsi_signals()
    time.sleep(20)
