import yfinance as yf

def validate_stock_data(ticker):
    """
    Validates the availability of key features for a given stock ticker.
    """
    messages = []
    stock = yf.Ticker(ticker)

    # Check for dividends
    if stock.dividends.empty:
        messages.append(f"No dividend data available for {ticker}.")

    # Check for financials
    if stock.financials.empty:
        messages.append(f"No financial data available for {ticker}.")

    # Check for balance sheet data
    if stock.balance_sheet.empty:
        messages.append(f"No balance sheet data available for {ticker}.")

    # Add more checks as necessary...

    return messages
