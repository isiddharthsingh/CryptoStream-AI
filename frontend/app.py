import streamlit as st
import pandas as pd
from models import arima_hourly_forecast, var_forecast, moving_averages_forecast, lstm_forecast
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(page_title="Crypto Forecasting", layout="wide")

DATA_PATH = "/Users/siddharth/Desktop/BigData_Project/coinbase_data/cassandra data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp')

# Main App
def main():
    st.title("📈 Cryptocurrency Forecasting App")
    st.sidebar.header("Inputs")
    df = load_data()

    coins = df['base_currency'].unique().tolist()
    models = ["ARIMA", "VAR", "Moving Averages", "LSTM"]

    # Sidebar inputs
    selected_model = st.sidebar.selectbox("Forecasting Model", models)
    forecast_steps = st.sidebar.slider("Forecast Steps", 1, 24, 5)

    if selected_model == "VAR":
        coin1 = st.sidebar.selectbox("Select First Coin", coins)
        coin2 = st.sidebar.selectbox("Select Second Coin", coins)
        if st.sidebar.button("Run Forecast"):
            st.subheader(f"VAR Forecast for {coin1} and {coin2}")
            try:
                scaled_data, forecast_df = var_forecast(df, coin1, coin2, forecast_steps)
                plot_var_forecast(scaled_data, forecast_df, coin1, coin2)
                st.write("### Forecasted Values")
                st.table(forecast_df.head(10))  # Display next 10 forecasts
            except ValueError as e:
                st.error(e)
    else:
        selected_coin = st.sidebar.selectbox("Select a Coin", coins)
        coin_data = df[df['base_currency'] == selected_coin][['timestamp', 'amount']].dropna()
        coin_data = coin_data.rename(columns={'timestamp': 'Date', 'amount': 'Price'}).set_index('Date')

        if st.sidebar.button("Run Forecast"):
            if selected_model == "ARIMA":
                st.subheader(f"🔮 ARIMA Model Forecast for {selected_coin}")
                forecast_df = arima_hourly_forecast(coin_data, forecast_steps)
                plot_forecast(coin_data, forecast_df, selected_coin, "ARIMA")
                st.write("### Forecasted Values")
                st.table(forecast_df.head(10))  # Display next 10 forecasts

            elif selected_model == "LSTM":
                st.subheader(f"🔮 LSTM Forecast for {selected_coin}")
                forecast_df = lstm_forecast(coin_data, selected_coin, forecast_steps)
                plot_forecast(coin_data, forecast_df, selected_coin, "LSTM")
                st.write("### Forecasted Values")
                st.table(forecast_df.head(10))  # Display next 10 forecasts

            elif selected_model == "Moving Averages":
                st.subheader(f"🔮 Moving Averages for {selected_coin}")
                sma, ema = moving_averages_forecast(coin_data)
                plot_moving_averages(coin_data, sma, ema, selected_coin)
                st.write("### Forecasted Moving Averages")
                st.table(pd.concat([sma.tail(10), ema.tail(10)], axis=1))  # Display last 10 moving averages

# Plotting Functions
def plot_forecast(original_data, forecast_data, coin, model_name):
    plt.figure(figsize=(12, 6))
    plt.plot(original_data.index[-500:], original_data['Price'].iloc[-500:], label="Original Data", color="blue")
    plt.plot(forecast_data.index, forecast_data['Forecast'], label=f"{model_name} Forecast", linestyle="--", color="green")
    plt.title(f"{model_name} Forecast for {coin}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    st.pyplot(plt)

def plot_var_forecast(scaled_data, forecast_data, coin1, coin2):
    plt.figure(figsize=(12, 6))
    plt.plot(scaled_data.index, scaled_data[coin1], label=f"Original {coin1}", color="blue")
    plt.plot(forecast_data.index, forecast_data[coin1], label=f"{coin1} Forecast", linestyle="--", color="red")
    plt.plot(scaled_data.index, scaled_data[coin2], label=f"Original {coin2}", color="green")
    plt.plot(forecast_data.index, forecast_data[coin2], label=f"{coin2} Forecast", linestyle="--", color="orange")
    plt.title(f"VAR Forecast for {coin1} and {coin2}")
    plt.xlabel("Time")
    plt.ylabel("Normalized Price")
    plt.legend()
    st.pyplot(plt)

def plot_moving_averages(data, sma, ema, coin):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Price'], label="Original Data", color="blue")
    plt.plot(sma.index, sma['SMA'], label="SMA", linestyle="--", color="red")
    plt.plot(ema.index, ema['EMA'], label="EMA", linestyle="--", color="orange")
    plt.title(f"Moving Averages for {coin}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    st.pyplot(plt)

if __name__ == "__main__":
    main()