# SMA : Simple Moving Average
# SMA20 : Simple Moving Average of 20 Days

import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpdates
import numpy as np




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



nifty50 =pd.read_csv('ind_niftynext50list.csv')


nifty50= (nifty50['Symbol'] +'.NS')


returns = [];

for i in range(len(nifty50)):
    
    stock = yf.Ticker(nifty50[i])
    


# stocks = input('The Name Of  Stock: ')



# get historical market data

    df = stock.history('1250'+'D')


    df['Date'] = df.index

# Remove rows having np.NaN
    df.dropna()


    df = df[['Date','Open', 'High', 
         'Low', 'Close']]
  
# convert into datetime object
    df['Date'] = pd.to_datetime(df['Date'])
  
# apply map function
    df['Date'] = df['Date'].map(mpdates.date2num)
  

  


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


# Store buy and sell in Data
    buy_sell = buy_sell_signal(Data)

    Data['Buy_price'] = buy_sell[0]
    Data['Sell_price'] = buy_sell[1]
    Data['Open_pos'] = buy_sell[2]
    Data['live_pos'] = Data['Open_pos'].multiply(Data['Price'])
    Data['funds'] = buy_sell[3]

    # print(Data['funds'])
    
    if(len(Data)>2):
        returns.append((Data['funds'][-1] - Data['funds'][0])*100/(5*Data['funds'][0]))
    
        print(nifty50[i][:-3], " ", (Data['funds'][-1] - Data['funds'][0])*100/(5*Data['funds'][0]))


print("MAX return : ",np.max(returns))
print("MIN return : ",np.min(returns))
print("AVG returns : ", np.mean(returns))

    



