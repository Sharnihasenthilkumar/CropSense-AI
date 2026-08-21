"""
Price Predictor Module
========================
Loads trained models and generates price forecasts.
Supports 1-day, 3-day, and 7-day predictions.
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import MODEL_DIR, FORECAST_HORIZONS
from src.feature_engineering import FeatureEngineer


class PricePredictor:
    """Generates crop price forecasts using trained models."""
    
    def __init__(self):
        self.models = {}
        self.feature_engineer = None
        self._load_models()
    
    def _load_models(self):
        """Load trained models from disk."""
        try:
            # Load feature engineer
            fe_path = os.path.join(MODEL_DIR, "feature_engineer.pkl")
            if os.path.exists(fe_path):
                self.feature_engineer = joblib.load(fe_path)
            else:
                self.feature_engineer = FeatureEngineer()
            
            # Load crop models
            for filename in os.listdir(MODEL_DIR):
                if filename.startswith("rf_") and filename.endswith(".pkl"):
                    # rf_bengal gram.pkl -> Bengal Gram
                    crop_name = filename[3:-4]  # Remove 'rf_' prefix and '.pkl' suffix
                    crop_name = crop_name.title()  # 'bengal gram' -> 'Bengal Gram'
                    filepath = os.path.join(MODEL_DIR, filename)
                    self.models[crop_name] = joblib.load(filepath)
                    
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
            self.feature_engineer = FeatureEngineer()
    
    def is_ready(self):
        """Check if models are loaded and ready for predictions."""
        return len(self.models) > 0
    
    def predict(self, crop, market, historical_data):
        """
        Generate price forecasts for 1-day, 3-day, and 7-day horizons.
        
        Args:
            crop: Crop name (e.g., 'Tomato')
            market: Market name (e.g., 'Koyambedu')
            historical_data: DataFrame with recent price history for this crop-market
            
        Returns:
            Dictionary with predictions and metadata
        """
        if crop not in self.models:
            return self._fallback_prediction(historical_data)
        
        model = self.models[crop]
        
        # Get recent prices for feature construction
        recent_data = historical_data.sort_values('date').tail(30)
        
        if len(recent_data) < 7:
            return self._fallback_prediction(historical_data)
        
        recent_prices = recent_data['modal_price'].values.tolist()
        recent_arrivals = recent_data['arrivals'].values[-1] if 'arrivals' in recent_data.columns else 0
        current_price = recent_prices[-1]
        
        # Generate predictions for each horizon
        predictions = {}
        prediction_prices = list(recent_prices)  # Running list of prices
        
        for horizon in FORECAST_HORIZONS:
            # Iterative prediction for multi-day forecasts
            pred_price = self._predict_horizon(
                model, crop, market, prediction_prices, recent_arrivals, horizon
            )
            predictions[f"{horizon}d"] = round(pred_price, 2)
            
            # Add prediction to running list for next iteration
            prediction_prices.append(pred_price)
        
        # Determine price trend
        trend = self._detect_trend(recent_prices, predictions)
        
        return {
            "current_price": round(current_price, 2),
            "predictions": predictions,  # {"1d": price, "3d": price, "7d": price}
            "trend": trend,
            "confidence": self._estimate_confidence(recent_prices),
            "historical_prices": recent_prices[-30:],
            "dates": recent_data['date'].dt.strftime('%Y-%m-%d').tolist()[-30:]
        }
    
    def _predict_horizon(self, model, crop, market, prices, arrivals, horizon):
        """
        Predict price for a specific horizon using iterative forecasting.
        For multi-day forecasts, uses predicted values as inputs for further predictions.
        """
        current_prices = list(prices)
        
        for step in range(horizon):
            # Build features for next day
            features = self.feature_engineer.prepare_prediction_input(
                crop, market, current_prices[-10:], arrivals
            )
            
            if features is None:
                # Fallback: use last known price
                return current_prices[-1]
            
            # Predict next day
            pred = model.predict(features)[0]
            current_prices.append(pred)
        
        # Return the price at the target horizon
        return current_prices[-1]
    
    def _detect_trend(self, recent_prices, predictions):
        """
        Detect the overall price trend.
        
        Returns: 'increasing', 'decreasing', or 'stable'
        """
        current = recent_prices[-1]
        future = predictions.get('3d', predictions.get('1d', current))
        
        pct_change = (future - current) / current
        
        if pct_change > 0.02:  # >2% increase
            return "increasing"
        elif pct_change < -0.02:  # >2% decrease
            return "decreasing"
        else:
            return "stable"
    
    def _estimate_confidence(self, recent_prices):
        """
        Estimate prediction confidence based on recent price stability.
        More stable prices = higher confidence.
        
        Returns: confidence score (0 to 1)
        """
        if len(recent_prices) < 7:
            return 0.5
        
        # Use coefficient of variation of recent prices
        cv = np.std(recent_prices[-14:]) / np.mean(recent_prices[-14:])
        
        # Map CV to confidence (lower CV = higher confidence)
        confidence = max(0.3, min(0.95, 1 - cv * 5))
        
        return round(confidence, 2)
    
    def _fallback_prediction(self, historical_data):
        """
        Fallback prediction when model is not available.
        Uses simple moving average trend.
        """
        if historical_data is None or historical_data.empty:
            return None
        
        recent = historical_data.sort_values('date').tail(14)
        prices = recent['modal_price'].values
        
        if len(prices) < 3:
            return None
        
        current_price = prices[-1]
        avg_change = np.mean(np.diff(prices[-7:]))
        
        predictions = {}
        for horizon in FORECAST_HORIZONS:
            predictions[f"{horizon}d"] = round(current_price + avg_change * horizon, 2)
        
        return {
            "current_price": round(current_price, 2),
            "predictions": predictions,
            "trend": "increasing" if avg_change > 0 else "decreasing" if avg_change < 0 else "stable",
            "confidence": 0.5,
            "historical_prices": prices.tolist(),
            "dates": recent['date'].dt.strftime('%Y-%m-%d').tolist()
        }
    
    def get_available_crops(self):
        """Return list of crops with trained models."""
        return list(self.models.keys())
