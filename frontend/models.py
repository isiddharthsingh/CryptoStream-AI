#models.py
import pandas as pd
import numpy as np
import pickle
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.api import VAR
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Paths for saved models
MODEL_SAVE_PATH = "/Users/siddharth/Desktop/BigData_Project/saved_models"
SCALER_SAVE_PATH = "/Users/siddharth/Desktop/BigData_Project/saved_models/scalers.pkl"

# ARIMA Forecast Function
def arima_hourly_forecast(data, steps):
    data = data.groupby('Date').mean().sort_index()
    data = data.asfreq('h', method='pad')

    model = ARIMA(data['Price'].dropna(), order=(5, 1, 0))
    results = model.fit()

    forecast = results.forecast(steps=steps)
    forecast_index = pd.date_range(start=data.index[-1], periods=steps + 1, freq='h')[1:]
    forecast_df = pd.DataFrame({'Forecast': forecast}, index=forecast_index)
    return forecast_df

# VAR Forecast Function
def var_forecast(df, coin1, coin2, steps):
    coin1_df = df[df['base_currency'] == coin1][['timestamp', 'amount']].rename(columns={'amount': coin1})
    coin2_df = df[df['base_currency'] == coin2][['timestamp', 'amount']].rename(columns={'amount': coin2})

    merged_df = pd.merge(coin1_df, coin2_df, on='timestamp', how='inner').set_index('timestamp')
    if merged_df.empty:
        raise ValueError("No overlapping timestamps between the selected coins. Cannot proceed.")

    scaler = MinMaxScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(merged_df), columns=merged_df.columns, index=merged_df.index)

    model = VAR(scaled_data)
    results = model.fit(maxlags=5)

    forecast = results.forecast(scaled_data.values[-5:], steps=steps)
    forecast_df = pd.DataFrame(forecast, columns=[coin1, coin2])
    forecast_df.index = pd.date_range(start=scaled_data.index[-1], periods=steps + 1, freq='h')[1:]
    return scaled_data, forecast_df

# Moving Averages Forecast Function
def moving_averages_forecast(data):
    sma = data.rolling(window=5).mean().rename(columns={'Price': 'SMA'})
    ema = data.ewm(span=5, adjust=False).mean().rename(columns={'Price': 'EMA'})
    return sma, ema

# LSTM Forecast Function
def lstm_forecast(data, coin_name, steps=10):
    import tensorflow as tf
    
    # Load scaler and saved model
    with open(SCALER_SAVE_PATH, 'rb') as f:
        scalers = pickle.load(f)
    scaler = scalers[coin_name]
    model = load_model(f"{MODEL_SAVE_PATH}/{coin_name}_lstm.h5")

    # Prepare last sequence for prediction
    seq_length = 10
    last_data = data['Price'].values[-seq_length:]
    last_data_scaled = scaler.transform(last_data.reshape(-1, 1))
    input_seq = last_data_scaled.reshape(1, seq_length, 1)

    forecast_scaled = []
    for _ in range(steps):
        # Predict next step
        next_step = model.predict(input_seq, verbose=0)[0, 0]  # Extract scalar value
        forecast_scaled.append(next_step)

        # Update input sequence (ensure the shape is consistent)
        next_step_reshaped = np.array([[next_step]])  # Shape (1, 1)
        input_seq = np.append(input_seq[:, 1:, :], next_step_reshaped.reshape(1, 1, 1), axis=1)

    # Scale back to original values
    forecast_values = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten()
    forecast_index = pd.date_range(start=data.index[-1], periods=steps + 1, freq='h')[1:]
    return pd.DataFrame({'Forecast': forecast_values}, index=forecast_index)