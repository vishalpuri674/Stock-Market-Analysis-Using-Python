import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpdates
import numpy as np


stocks = input('The Name of  Stock: ')
stock = yf.Ticker(stocks)



# get historical market data

num_days = input("Number of Days :")
n = int(input("The Number of day's of Volatility Analysis: "))
df = stock.history(num_days+'D')

df['Date'] = df.index

# Remove rows having np.NaN
df.dropna()


df = df[['Date', 'Open', 'High',
         'Low', 'Close']]

# convert into datetime object
df['Date'] = pd.to_datetime(df['Date'])

# apply map function
df['Date'] = df['Date'].map(mpdates.date2num)


# In Finance , logrithimic returns are important
df['Log returns'] = np.log(df['Close']/df['Close'].shift())

df = df.dropna()

# creating Subplots
fig, ax = plt.subplots()

# plotting the data
candlestick_ohlc(ax, df.values, width=0.6,
                 colorup='green', colordown='red',
                 alpha=0.8)

# allow grid
ax.grid(True)

# Setting labels
ax.set_xlabel('Date')
ax.set_ylabel('Price')


# Formatting Date
date_format = mpdates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

fig.tight_layout()
# HOLD the figure, 



log_return = df['Log returns']

# Creating starting N empty Standarad Deviation 
std_n = [np.nan]*n

# After N, using previous N data, we calculate Standard Deviation, till the latest date
for i in range(len(log_return)):

    if i >= n:
        std_n.append(log_return[i-n:i].std())

# adding new DATA
df[f'STD {n}'] = std_n


df['Upper Bond'] = 0.5*(df['Close'] + df['Open'])*np.e**(df[f'STD {n}'])
df['Lower Bond'] = 0.5*(df['Close'] + df['Open'])*np.e**(-df[f'STD {n}'])



df['avg'] = 0.5*(df['Close'] + df['Open'])


SMA50 = pd.DataFrame()
df['SMA50'] = df['Close'].rolling(window=50).mean()
 



plt.plot(df['Upper Bond'], label=f'Upper Bond {n}', color='0', linewidth=0.8)
plt.plot(df['Lower Bond'], label=f'Lower Bond {n}', color='b', linewidth=0.8)
plt.plot(df['SMA50'], label='SMA50', linewidth=0.5)


plt.legend(loc='upper left')
plt.show()
