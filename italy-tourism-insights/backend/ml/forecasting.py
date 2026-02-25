"""
Machine Learning module for tourism forecasting
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pickle
import os


class TourismForecaster:
    """
    Tourism demand forecasting using multiple algorithms
    """
    
    def __init__(self, model_type: str = "prophet"):
        self.model_type = model_type
        self.models = {}
        self.scaler = None
        
    def prepare_data(self, data: list) -> pd.DataFrame:
        """
        Prepare and format raw tourism data
        """
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df.asfreq('D', fill_value=0)
    
    def train_arima(self, data: pd.DataFrame, order: tuple = (5, 1, 2)):
        """
        Train ARIMA model
        
        ARIMA(p, d, q):
        - p: AR order (AutoRegressive)
        - d: Differencing order (I for Integration)
        - q: MA order (Moving Average)
        """
        try:
            from statsmodels.tsa.arima.model import ARIMA
            model = ARIMA(data['visitor_count'], order=order)
            self.models['arima'] = model.fit()
            return True
        except ImportError:
            print("statsmodels not installed")
            return False
    
    def train_prophet(self, data: pd.DataFrame):
        """
        Train Facebook Prophet model with seasonality
        """
        try:
            from prophet import Prophet
            
            df = data.reset_index()
            df.columns = ['ds', 'y']
            
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )
            model.fit(df)
            self.models['prophet'] = model
            return True
        except ImportError:
            print("prophet not installed")
            return False
    
    def train_lstm(self, data: np.ndarray, look_back: int = 30):
        """
        Train LSTM neural network
        """
        try:
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense
            
            # Prepare sequences
            X, y = [], []
            for i in range(len(data) - look_back):
                X.append(data[i:i+look_back])
                y.append(data[i+look_back])
            
            X = np.array(X).reshape(-1, look_back, 1)
            y = np.array(y)
            
            # Build model
            model = Sequential([
                LSTM(50, activation='relu', input_shape=(look_back, 1)),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            model.fit(X, y, epochs=10, batch_size=32, verbose=0)
            
            self.models['lstm'] = model
            return True
        except ImportError:
            print("tensorflow not installed")
            return False
    
    def forecast_arima(self, steps: int = 30) -> dict:
        """
        Generate ARIMA forecast
        """
        if 'arima' not in self.models:
            return None
        
        model = self.models['arima']
        forecast = model.get_forecast(steps=steps)
        forecast_df = forecast.conf_int()
        
        return {
            'predictions': forecast.predicted_mean.values,
            'lower': forecast_df.iloc[:, 0].values,
            'upper': forecast_df.iloc[:, 1].values,
            'std_error': forecast.se_mean.values
        }
    
    def forecast_prophet(self, periods: int = 30) -> dict:
        """
        Generate Prophet forecast
        """
        if 'prophet' not in self.models:
            return None
        
        model = self.models['prophet']
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        forecast = forecast.tail(periods)
        
        return {
            'dates': forecast['ds'].values,
            'predictions': forecast['yhat'].values,
            'lower': forecast['yhat_lower'].values,
            'upper': forecast['yhat_upper'].values,
            'trend': forecast['trend'].values
        }
    
    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """
        Calculate model performance metrics
        """
        from sklearn.metrics import (
            mean_absolute_error,
            mean_squared_error,
            r2_score
        )
        
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        r2 = r2_score(y_true, y_pred)
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape,
            'r2': r2
        }
    
    def detect_anomalies(self, data: np.ndarray, method: str = "isolation_forest") -> list:
        """
        Detect anomalies in time series data
        """
        if method == "isolation_forest":
            from sklearn.ensemble import IsolationForest
            
            X = data.reshape(-1, 1)
            model = IsolationForest(contamination=0.05)
            predictions = model.fit_predict(X)
            
            anomalies = [i for i, p in enumerate(predictions) if p == -1]
            return anomalies
        
        elif method == "zscore":
            mean = np.mean(data)
            std = np.std(data)
            z_scores = np.abs((data - mean) / std)
            anomalies = [i for i, z in enumerate(z_scores) if z > 3]
            return anomalies
        
        return []
    
    def save_model(self, model_path: str):
        """
        Save trained models to disk
        """
        with open(model_path, 'wb') as f:
            pickle.dump(self.models, f)
    
    def load_model(self, model_path: str):
        """
        Load trained models from disk
        """
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.models = pickle.load(f)


# Global forecaster instance
forecaster = TourismForecaster()
