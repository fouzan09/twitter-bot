
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from talib import *

# Get the historical data
data = pd.read_csv('nifty_data.csv')

# Calculate the technical indicators
data['macd'], data['macdsignal'], data['macdhist'] = MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
data['rsi'] = RSI(data['Close'], timeperiod=14)
data['stoch_k'], data['stoch_d'] = STOCH(data['High'], data['Low'], data['Close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
data['bbands'] = BBANDS(data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# Set the trading parameters
entry_threshold = 0.2
exit_threshold = 0.1
stop_loss = 0.5

# Initialize the trading signals
signals = pd.DataFrame(index=data.index)
signals['Buy'] = 0
signals['Sell'] = 0

# Generate the trading signals
for i in range(len(data)):
    if data['macd'][i] < data['macdsignal'][i] and data['macdhist'][i] > 0 and data['rsi'][i] > 70 and data['stoch_k'][i] > 80:
        signals['Buy'][i] = 1
    elif data['macd'][i] > data['macdsignal'][i] and data['macdhist'][i] < 0 and data['rsi'][i] < 30 and data['stoch_k'][i] < 20:
        signals['Sell'][i] = 1

# Calculate the trading performance
performance = pd.DataFrame(index=data.index)
performance['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
performance['Strategy Returns'] = performance['Returns'] * signals['Buy'] - performance['Returns'] * signals['Sell']
performance['Cumulative Returns'] = performance['Strategy Returns'].cumsum()
performance['Drawdown'] = (performance['Cumulative Returns'] - performance['Cumulative Returns'].cummax()) / performance['Cumulative Returns'].cummax()

# Plot the trading performance
plt.plot(performance['Cumulative Returns'])
plt.plot(performance['Drawdown'])
plt.legend(['Cumulative Returns', 'Drawdown'])
plt.show()

# Print the trading performance statistics
print('Total Trades:', len(signals[(signals['Buy'] == 1) | (signals['Sell'] == 1)]))
print('Winning Trades:', len(signals[(signals['Buy'] == 1) & (performance['Returns'] > 0)]))
print('Losing Trades:', len(signals[(signals['Sell'] == 1) & (performance['Returns'] < 0)]))
print('Average Win:', performance['Returns'][(signals['Buy'] == 1) & (performance['Returns'] > 0)].mean())
print('Average Loss:', performance['Returns'][(signals['Sell'] == 1) & (performance['Returns'] < 0)].mean())
print('Profit Factor:', performance['Returns'][(signals['Buy'] == 1) & (performance['Returns'] > 0)].mean() / abs(performance['Returns'][(signals['Sell'] == 1) & (performance['Returns'] < 0)].mean()))
print('Maximum Drawdown:', performance['Drawdown'].min())
