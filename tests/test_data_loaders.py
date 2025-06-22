# import the class files
from stockanalysis import getstockdata as gd
from stockanalysis import helpers, test

# run module tests
# run module tests
test.test_data_load()

# load the settings file
settings = helpers.load_settings_stocks()
print(settings)
# <single ticker mode>
tickr='VNQ'

# initialize instance of the class by passing the stock ticker
stockobj = gd.GetStockData(tickr)

# call getdata() method to access last 20 years of data
df = stockobj.getdata(period='20y')

# <multi ticker mode>
tickers=['SPY', 'VNQ', 'BND', 'DBX']

# initialize instance of the class by passing the stock ticker
stockobj = gd.GetStockData(tickers)

# call getdata() method to access last 20 years of data
df = stockobj.getdata(period='20y')
print(df)
# Use cache only mode to perform offline analysis
stockobj = gd.GetStockData(tickers, cache_only=True)
