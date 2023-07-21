import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpdates



stocks = input('The Name Of Stock:')
stock = yf.Ticker(stocks)


# get historical market data

num_days = input("Number of Days :")
df = stock.history(num_days+'D')

#in line 30
#Here ['Date'] not in index", So I am not able to proceed futher, So we access with INDEX
#https://stackoverflow.com/questions/22991567/pandas-yahoo-finance-datareader

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
# title
plt.title(stocks)
  
# Formatting Date
date_format = mpdates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
  
fig.tight_layout()
#Show The Plot
plt.show()
  
