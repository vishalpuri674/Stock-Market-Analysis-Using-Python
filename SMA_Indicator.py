# SMA : Simple Moving Average
# SMA20 : Simple Moving Average of 20 Days

import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpdates
import numpy as np


stocks = input('The Name Of  Stock: ')
stock = yf.Ticker(stocks)


# get historical market data

num_days = input("Number of Days :")
df = stock.history(num_days+'D')


df['Date'] = df.index

# Remove rows having np.NaN
df.dropna()


df = df[['Date','Open', 'High', 
         'Low', 'Close']]
  
# convert into datetime object
df['Date'] = pd.to_datetime(df['Date'])
  
# apply map function
df['Date'] = df['Date'].map(mpdates.date2num)
  
# creating Subplots
fig, ax = plt.subplots()
  
# plotting the data
candlestick_ohlc(ax, df.values, width = 0.6,
                 colorup = 'green', colordown = 'red', 
                 alpha = 0.8)
  
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
  


# Create SMA Indiacator
SMA20 = pd.DataFrame()
SMA20['Price'] = df['Close'].rolling(window = 20).mean()
SMA50 = pd.DataFrame()
SMA50['Price'] = df['Close'].rolling(window = 50).mean()


# Store all Data in new DataFrame
Data = pd.DataFrame()
Data['Price'] =(( df['Close'] + df['Open'])/2).rolling(window=10).mean()
Data['SMA20'] = SMA20['Price']
Data['SMA50'] = SMA50['Price']
Data['funds'] = 100000         # Initialize funds so that it could be later modified


# Create a function to signal when to buy and when to sell
def buy_sell_signal(data):
  buy_signal = []
  sell_signal = []
  open_position = []
  funds = [100000] * len(data)
  last_funds = 100000
  flag = 0  # flag = 0 means sell_flag and flag = 1 means buy_flag

  for i in range(len(data)):
    if data['SMA20'][i] > data['SMA50'][i]:
      if flag == 0:
        flag = 1
        buy_signal.append(data['Price'][i])
        last_pos = last_funds / data['Price'][i]
        funds[i] = last_funds
        open_position.append(last_pos)     # buy_quantity with 1 Lac Capital
        sell_signal.append(np.NaN)
      else:
        buy_signal.append(np.NaN)
        last_funds = data['Price'][i] * last_pos
        funds[i] = last_funds
        open_position.append(last_pos)
        sell_signal.append(np.NaN)
    elif data['SMA20'][i] < data['SMA50'][i]:
      if flag == 1:
        flag = 0
        buy_signal.append(np.NaN)
        last_funds = last_pos * data['Price'][i]
        funds[i] = last_funds
        open_position.append(0)
        sell_signal.append(data['Price'][i])
      else:
        buy_signal.append(np.NaN)
        funds[i] = last_funds
        open_position.append(0)
        sell_signal.append(np.NaN)
    else:
      buy_signal.append(np.NaN)
      open_position.append(0)
      sell_signal.append(np.NaN)
  return buy_signal, sell_signal, open_position, funds, flag

# Store buy and sell in Data
buy_sell = buy_sell_signal(Data)

Data['Buy_price'] = buy_sell[0]
Data['Sell_price'] = buy_sell[1]
Data['Open_pos'] = buy_sell[2]
Data['live_pos'] = Data['Open_pos'].multiply(Data['Price'])
Data['funds'] = buy_sell[3]

# Visualize Data and strategy to buy and sell NIFTY

plt.plot(Data['Price'], label = 'Day Average', linewidth = 1)
plt.plot(Data['SMA20'], label = 'SMA20', linewidth = 0.5)
plt.plot(Data['SMA50'], label = 'SMA50', linewidth = 0.5)
plt.scatter(Data.index, Data['Buy_price'], label= 'Buy', marker = '^', color = 'b')
plt.scatter(Data.index, Data['Sell_price'], label= 'Sell', marker = 'v', color = '0')
plt.title(stocks + ' Buy-Sell Signals')
plt.xlabel(num_days)

plt.legend(loc = 'upper left')
plt.show()

