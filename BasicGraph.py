import matplotlib.pyplot as plt
# import matplotlib.dates as mpdates
import yfinance as yf

stocks = input('The Name of Stock: ')

# Ticker ==Symbol of Stock( )

stock = yf.Ticker(stocks)


# get historical market data

num_days = input("Number of Days :")

#Extracton of Data, using Number of Days from Now
df = stock.history(num_days+'D')

# Remove rows having np.NaN
df.dropna()


plt.figure(figsize=(15, 8))
plt.plot(df['Close'], label = stocks, linewidth = 0.5)
plt.title('Adjacent close price history')
plt.xlabel('Previous ' + str(num_days) + ' days')
plt.ylabel('Adj. close price (₹)')
plt.legend(loc = 'upper left')
plt.show()