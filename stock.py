import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Streamlit Page Config
st.set_page_config(page_title="Stock Price Trend Analysis", layout="wide")

# Title
st.title("📈 Stock Price Trend Analysis")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file with stock data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.sort_index()

    # Sidebar for User Inputs
    st.sidebar.header("Settings")

    # Stock Name Input
    stock_name = st.sidebar.text_input("Enter Stock Name", "Sample Stock")

    # Calculate Indicators
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['Volatility'] = df['Close'].pct_change().rolling(window=30).std()

    # Select Date Range
    start_date = st.sidebar.date_input("Start Date", df.index.min().date())
    end_date = st.sidebar.date_input("End Date", df.index.max().date())

    # Filter Data
    filtered_df = df.loc[start_date:end_date]

    # Display Stock Overview
    st.subheader(f"📊 {stock_name} - Stock Data Overview")
    st.dataframe(filtered_df.style.format("{:.2f}"), height=300)

    # Stock Price Trend Graph
    st.subheader(f"📈 {stock_name} - Stock Price Trend")

    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1e1e1e')
    ax.plot(filtered_df.index, filtered_df['Close'], label="Closing Price", color='cyan', linewidth=2)
    ax.plot(filtered_df.index, filtered_df['MA50'], label="50-Day MA", color='lime', linestyle="dashed")

    ax.set_xlabel("Date", fontsize=12, color="white")
    ax.set_ylabel("Stock Price", fontsize=12, color="white")
    ax.set_title(f"{stock_name} - Stock Price Trend", fontsize=14, color="white")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    # Dark theme adjustments
    ax.set_facecolor("#1e1e1e")
    fig.patch.set_facecolor("#1e1e1e")
    plt.xticks(color="white")
    plt.yticks(color="white")

    st.pyplot(fig)

    # Summary Statistics
    st.subheader("📊 Summary Statistics")
    st.dataframe(filtered_df.describe().style.format("{:.4f}"), height=300)

    # Download Processed Data
    st.sidebar.subheader("Download Data")
    csv_data = filtered_df.to_csv(index=True).encode('utf-8')
    st.sidebar.download_button(label="📥 Download Processed Data", data=csv_data, file_name="processed_stock_data.csv", mime="text/csv")

else:
    st.info("📤 Please upload a CSV file with 'Date', 'Open', 'High', 'Low', 'Close' columns.")
