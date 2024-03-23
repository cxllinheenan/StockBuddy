import streamlit as st
import yfinance as yf
import pandas as pd
from AdvancedAnalytics import simple_linear_regression, fetch_stock_data, calculate_moving_averages, monte_carlo_simulation, calculate_spread, fetch_pair_data  # Import functions from the analytics module
from DataValidator import validate_stock_data

# Set page configuration
st.set_page_config(page_title="Stock Buddy📈", layout="wide")

# Title and Introduction 
st.title("StockBuddy📈")
st.markdown("## Comprehensive Equity Analysis Tool")

# Sidebar for user input
st.sidebar.header("User Input Features")
ticker = st.sidebar.text_input("Enter Stock Ticker:", value="AAPL").upper()

validation_messages = validate_stock_data(ticker)
if validation_messages:
    for message in validation_messages:
        st.error(message)

# Initialize yfinance Ticker object
stock = yf.Ticker(ticker)

# Tab layout for organized information
tabs = st.tabs(["Overview", "Financials", "Historical Data", "Advanced Analytics", "Arbitrage"])

with tabs[0]:  # Overview
    st.header(f"Company Overview: {ticker}")

    # Company information
    company_info = stock.info
    st.subheader("Company Description:")
    st.write(company_info.get('longBusinessSummary'))

    # Key financial metrics and ratios
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Market Cap", f"${company_info.get('marketCap'):,}")
    with col2:
        st.metric("P/E Ratio", company_info.get('forwardPE'))
    with col3:
        st.metric("Dividend Yield", f"{company_info.get('dividendYield') * 100:.2f}%")


    with col4:
        st.metric("52 Week High", company_info.get('fiftyTwoWeekHigh'))

    # Recent news
    st.subheader("Recent News")
    news = stock.news
    for article in news[:5]:  # Display the first 5 news articles
        st.write(f"[{article['title']}]({article['link']})", unsafe_allow_html=True)

with tabs[1]:  # Financials Tab
    st.header(f"Financials: {ticker}")

    # Fetch key financial metrics
    metrics = stock.info
    financial_ratios = {
        'Profit Margin': metrics.get('profitMargins'),
        'Return on Assets (ROA)': metrics.get('returnOnAssets'),
        'Return on Equity (ROE)': metrics.get('returnOnEquity'),
        'Price to Earnings (P/E)': metrics.get('forwardPE'),
        'Price to Book (P/B)': metrics.get('priceToBook'),
        'Debt to Equity': metrics.get('debtToEquity'),
        'Current Ratio': metrics.get('currentRatio'),
    }

    # Display financial ratios in two columns
    st.subheader("Key Financial Ratios and Metrics")
    col1, col2 = st.columns(2)
    with col1:
        for key in list(financial_ratios)[:len(financial_ratios)//2]:
            st.metric(label=key, value=f"{financial_ratios[key]:.2f}")
    with col2:
        for key in list(financial_ratios)[len(financial_ratios)//2:]:
            st.metric(label=key, value=f"{financial_ratios[key]:.2f}")

    # Financial Health and Trend Analysis (Example: Revenue and Net Income Trend)
    
    financial_health_data = pd.DataFrame({
        'Revenue': stock.financials.loc['Total Revenue'],
        'Net Income': stock.financials.loc['Net Income']
    })

    # Display Annual and Quarterly Financial Statements
    st.subheader("Annual Financials")
    st.table(stock.financials.T.style.format('${:,.0f}'))  # Transpose for better readability

    st.subheader("Quarterly Financials")
    st.table(stock.quarterly_financials.T.style.format('${:,.0f}'))  # Transpose for better readability

    # Key Financial Ratios and Metrics
    st.subheader("Financial Health and Trend Analysis")
    st.line_chart(financial_health_data)

with tabs[2]:  # Historical Data
    st.header(f"Historical Data: {ticker}")

    # Options for data type and time frame
    data_type = st.radio("Select Data Type:", ('Close', 'Open', 'High', 'Low', 'Volume'), index=0)
    time_frame = st.select_slider("Select Time Frame:", options=['1mo', '3mo', '6mo', '1y', '5y', 'max'], value='1y')

    # Fetch and display historical data based on selected options
    hist_data = stock.history(period=time_frame)[data_type]
    st.line_chart(hist_data)

    # Show data table if user wants
    if st.checkbox("Show Data Table"):
        st.dataframe(hist_data)


with tabs[3]:  # Advanced Analytics
    st.header("Advanced Analytics")
    st.subheader("Predictive Analysis using Linear Regression")
    actual, predicted = simple_linear_regression(ticker)
    st.line_chart({"Actual": actual, "Predicted": predicted})

    # Moving Averages
    st.subheader("Moving Averages")
    ma_data = calculate_moving_averages(ticker)
    st.line_chart(ma_data)

    # Monte Carlo Simulation
    st.subheader("Monte Carlo Price Forecast")
    simulation_days = st.number_input("Days to Forecast", min_value=10, max_value=365, value=30, step=10)
    mc_simulations = monte_carlo_simulation(ticker, days=simulation_days)
    st.line_chart(mc_simulations)

with tabs[4]:  # Adjust the index based on your tabs setup
    st.header("Statistical Arbitrage Research")

    st.subheader("Pair Trading Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        ticker1 = st.text_input("Enter First Ticker:", value="AAPL").upper()
    with col2:
        ticker2 = st.text_input("Enter Second Ticker:", value="MSFT").upper()

    if st.button("Analyze Pair"):
        hist1, hist2 = fetch_pair_data(ticker1, ticker2, period='1y')
        spread = calculate_spread(hist1, hist2)

        st.line_chart(spread, width=0, height=0, use_container_width=True)
        st.write("Spread Analysis between {} and {}".format(ticker1, ticker2))
        st.write(spread.describe())


# Footer
st.sidebar.markdown("StockBuddy 2024 | Made by Collin")
