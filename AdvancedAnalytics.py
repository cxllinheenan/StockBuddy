from matplotlib.pylab import norm
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from scipy.stats import norm


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5y")
    return hist

def simple_linear_regression(ticker):
    df = fetch_stock_data(ticker)
    df.reset_index(inplace=True)
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days
    X = df[['Days']]  # Features
    y = df['Close']  # Target variable

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Training the algorithm
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Making predictions
    y_pred = regressor.predict(X_test)

    return y_test, y_pred

def calculate_moving_averages(ticker, short_window=20, long_window=50):
    """
    Calculate short and long moving averages for the given stock ticker.
    """
    df = fetch_stock_data(ticker)
    df['SMA'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
    df['LMA'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
    return df[['Close', 'SMA', 'LMA']]

def monte_carlo_simulation(ticker, days=30, simulations=1000):
    """
    Perform a Monte Carlo simulation to forecast future stock prices.
    """
    df = fetch_stock_data(ticker)
    log_returns = np.log(1 + df['Close'].pct_change())
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()
    
    daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(days, simulations)))
    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = df['Close'].iloc[-1]
    for t in range(1, days):
        price_paths[t] = price_paths[t-1] * daily_returns[t]
    
    return price_paths


def fetch_pair_data(ticker1, ticker2, period='1y'):
    """
    Fetch historical close prices for a pair of tickers.
    """
    stock1 = yf.Ticker(ticker1)
    stock2 = yf.Ticker(ticker2)

    hist1 = stock1.history(period=period)['Close']
    hist2 = stock2.history(period=period)['Close']

    return hist1, hist2

def calculate_spread(hist1, hist2):
    """
    Calculate and normalize the spread between two price series.
    """
    spread = hist1 - hist2
    normalized_spread = (spread - spread.mean()) / spread.std()
    return normalized_spread

