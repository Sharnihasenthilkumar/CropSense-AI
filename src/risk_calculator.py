"""
Risk Calculator Module
========================
Assesses price risk based on:
- Recent price volatility
- Price fluctuation patterns
- Prediction uncertainty
- Market arrival changes

Risk Levels:
- LOW (Green): Stable prices, low volatility
- MODERATE (Yellow): Normal fluctuations
- HIGH (Red): High volatility, unpredictable market
"""

import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import RISK_LOW_THRESHOLD, RISK_MODERATE_THRESHOLD


class RiskCalculator:
    """Calculates price risk level for crops."""
    
    def __init__(self):
        pass
    
    def calculate_risk(self, historical_prices, predictions, arrivals=None):
        """
        Calculate overall price risk level.
        
        Args:
            historical_prices: List of recent prices (last 14-30 days)
            predictions: Dict {"1d": price, "3d": price, "7d": price}
            arrivals: List of recent arrival data (optional)
            
        Returns:
            Dictionary with risk level, score, and factors
        """
        if not historical_prices or len(historical_prices) < 7:
            return {
                "level": "MODERATE",
                "emoji": "🟡",
                "score": 0.5,
                "factors": ["Insufficient data for accurate risk assessment."],
                "color": "#FFA500"
            }
        
        # Calculate individual risk factors
        volatility_risk = self._calculate_volatility_risk(historical_prices)
        trend_risk = self._calculate_trend_risk(historical_prices, predictions)
        prediction_spread = self._calculate_prediction_spread(predictions, historical_prices[-1])
        arrival_risk = self._calculate_arrival_risk(arrivals) if arrivals else 0.3
        
        # Weighted average risk score (0 to 1)
        # Volatility is the most important factor
        risk_score = (
            volatility_risk * 0.40 +
            trend_risk * 0.25 +
            prediction_spread * 0.20 +
            arrival_risk * 0.15
        )
        
        # Determine risk level
        if risk_score < 0.35:
            level = "LOW"
            emoji = "🟢"
            color = "#28a745"
        elif risk_score < 0.65:
            level = "MODERATE"
            emoji = "🟡"
            color = "#FFA500"
        else:
            level = "HIGH"
            emoji = "🔴"
            color = "#dc3545"
        
        # Build explanatory factors
        factors = self._build_risk_factors(
            volatility_risk, trend_risk, prediction_spread, arrival_risk, level
        )
        
        return {
            "level": level,
            "emoji": emoji,
            "score": round(risk_score, 2),
            "factors": factors,
            "color": color,
            "details": {
                "volatility_risk": round(volatility_risk, 2),
                "trend_risk": round(trend_risk, 2),
                "prediction_spread": round(prediction_spread, 2),
                "arrival_risk": round(arrival_risk, 2)
            }
        }
    
    def _calculate_volatility_risk(self, prices):
        """
        Calculate risk based on price volatility (coefficient of variation).
        Higher CV = Higher risk.
        """
        if len(prices) < 3:
            return 0.5
        
        prices_arr = np.array(prices)
        cv = np.std(prices_arr) / np.mean(prices_arr)
        
        # Normalize: CV of 0.05 = low risk, CV of 0.15+ = high risk
        risk = min(1.0, cv / 0.15)
        
        return risk
    
    def _calculate_trend_risk(self, historical_prices, predictions):
        """
        Calculate risk based on trend reversal potential.
        Strong trends (up or down) have lower risk than erratic patterns.
        """
        prices = np.array(historical_prices[-14:])
        
        if len(prices) < 7:
            return 0.5
        
        # Calculate direction changes (sign of daily differences)
        diffs = np.diff(prices)
        sign_changes = np.sum(np.abs(np.diff(np.sign(diffs))) > 0)
        
        # More direction changes = more erratic = higher risk
        max_possible_changes = len(diffs) - 1
        erratic_score = sign_changes / max_possible_changes if max_possible_changes > 0 else 0
        
        return min(1.0, erratic_score * 1.5)
    
    def _calculate_prediction_spread(self, predictions, current_price):
        """
        Calculate risk based on how far predictions deviate from current price.
        Larger deviations = higher uncertainty = higher risk.
        """
        if not predictions or current_price <= 0:
            return 0.5
        
        pred_values = [v for v in predictions.values() if v is not None]
        if not pred_values:
            return 0.5
        
        # Maximum percentage deviation from current price
        max_deviation = max(abs(p - current_price) / current_price for p in pred_values)
        
        # Normalize: 5% deviation = moderate, 15%+ = high
        risk = min(1.0, max_deviation / 0.15)
        
        return risk
    
    def _calculate_arrival_risk(self, arrivals):
        """
        Calculate risk based on market arrival volatility.
        Sudden changes in arrivals indicate supply disruption risk.
        """
        if not arrivals or len(arrivals) < 5:
            return 0.3
        
        arrivals_arr = np.array(arrivals[-14:])
        
        # CV of arrivals
        cv = np.std(arrivals_arr) / np.mean(arrivals_arr) if np.mean(arrivals_arr) > 0 else 0
        
        # Normalize
        risk = min(1.0, cv / 0.5)
        
        return risk
    
    def _build_risk_factors(self, vol_risk, trend_risk, pred_spread, arr_risk, level):
        """Build human-readable risk factor explanations."""
        factors = []
        
        if vol_risk < 0.3:
            factors.append("Price has been relatively stable recently.")
        elif vol_risk > 0.6:
            factors.append("Price has been volatile with significant fluctuations.")
        
        if trend_risk < 0.3:
            factors.append("Price shows a consistent directional trend.")
        elif trend_risk > 0.6:
            factors.append("Price direction is erratic with frequent reversals.")
        
        if pred_spread < 0.3:
            factors.append("Predicted future prices are close to current levels.")
        elif pred_spread > 0.6:
            factors.append("Large price movement predicted (higher uncertainty).")
        
        if arr_risk > 0.5:
            factors.append("Market arrivals show high variability.")
        
        if level == "LOW":
            factors.append("Overall market conditions appear stable.")
        elif level == "HIGH":
            factors.append("Caution advised: market conditions are unpredictable.")
        
        return factors
