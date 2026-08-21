"""
Feature Engineering Module
============================
Creates ML features from cleaned price data.
All features use only historical information (no data leakage).

Features created:
- day, month, year, day_of_week (calendar features)
- previous_day_price (lag-1)
- rolling_avg_3d, rolling_avg_7d (moving averages)
- price_change (day-over-day change)
- arrivals (market arrival volume)
- encoded_crop, encoded_market (label-encoded categorical)
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import CROPS, MARKETS


class FeatureEngineer:
    """Creates ML-ready features from cleaned crop price data."""
    
    def __init__(self):
        # Label encoding mappings (consistent across train/test)
        self.crop_encoding = {crop: idx for idx, crop in enumerate(sorted(CROPS))}
        self.market_encoding = {market: idx for idx, market in enumerate(sorted(MARKETS))}
        
        # Feature column names (used by model)
        self.feature_columns = [
            'day', 'month', 'year', 'day_of_week',
            'previous_day_price', 'rolling_avg_3d', 'rolling_avg_7d',
            'price_change', 'arrivals', 'encoded_crop', 'encoded_market'
        ]
        
        self.target_column = 'modal_price'
    
    def create_features(self, df):
        """
        Create all ML features from the cleaned dataset.
        
        Args:
            df: Cleaned DataFrame with columns: date, crop, market, modal_price, arrivals
            
        Returns:
            DataFrame with all features added
        """
        if df is None or df.empty:
            return df
        
        df = df.copy()
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by crop, market, date (critical for lag features)
        df = df.sort_values(['crop', 'market', 'date']).reset_index(drop=True)
        
        # Calendar features
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday, 6=Sunday
        
        # Group-wise lag and rolling features (per crop-market combination)
        df = df.groupby(['crop', 'market'], group_keys=False).apply(
            self._add_lag_features
        ).reset_index(drop=True)
        
        # Encode categorical variables
        df['encoded_crop'] = df['crop'].map(self.crop_encoding).fillna(-1).astype(int)
        df['encoded_market'] = df['market'].map(self.market_encoding).fillna(-1).astype(int)
        
        # Ensure arrivals column exists
        if 'arrivals' not in df.columns:
            df['arrivals'] = 0
        
        # Drop rows where lag features are NaN (first 7 days per group)
        df = df.dropna(subset=['previous_day_price', 'rolling_avg_3d', 'rolling_avg_7d'])
        
        return df.reset_index(drop=True)
    
    def _add_lag_features(self, group):
        """
        Add lag and rolling features for a single crop-market group.
        Only uses past data (no future leakage).
        """
        # Lag-1: Previous day's price
        group['previous_day_price'] = group['modal_price'].shift(1)
        
        # Rolling averages (using past data only, min_periods ensures no NaN filling)
        group['rolling_avg_3d'] = group['modal_price'].shift(1).rolling(
            window=3, min_periods=3
        ).mean()
        
        group['rolling_avg_7d'] = group['modal_price'].shift(1).rolling(
            window=7, min_periods=7
        ).mean()
        
        # Price change (from previous day)
        group['price_change'] = group['modal_price'].shift(1) - group['modal_price'].shift(2)
        
        return group
    
    def get_feature_matrix(self, df):
        """
        Extract feature matrix (X) and target (y) from engineered DataFrame.
        
        Args:
            df: DataFrame with features created
            
        Returns:
            X (DataFrame): Feature matrix
            y (Series): Target variable (modal_price)
        """
        available_features = [col for col in self.feature_columns if col in df.columns]
        
        X = df[available_features].copy()
        y = df[self.target_column].copy()
        
        return X, y
    
    def prepare_prediction_input(self, crop, market, recent_prices, recent_arrivals):
        """
        Prepare a single prediction input from recent data.
        Used during inference (not training).
        
        Args:
            crop: Crop name
            market: Market name
            recent_prices: List of recent modal prices (most recent last)
            recent_arrivals: Most recent arrival value
            
        Returns:
            DataFrame with one row of features for prediction
        """
        if len(recent_prices) < 7:
            return None
        
        today = pd.Timestamp.now()
        
        features = {
            'day': today.day,
            'month': today.month,
            'year': today.year,
            'day_of_week': today.dayofweek,
            'previous_day_price': recent_prices[-1],
            'rolling_avg_3d': np.mean(recent_prices[-3:]),
            'rolling_avg_7d': np.mean(recent_prices[-7:]),
            'price_change': recent_prices[-1] - recent_prices[-2],
            'arrivals': recent_arrivals if recent_arrivals else 0,
            'encoded_crop': self.crop_encoding.get(crop, 0),
            'encoded_market': self.market_encoding.get(market, 0)
        }
        
        return pd.DataFrame([features])
    
    def chronological_split(self, df, train_ratio=0.8):
        """
        Split data chronologically (NO random shuffling).
        Older data -> Training, Newer data -> Testing.
        
        Args:
            df: Feature-engineered DataFrame with 'date' column
            train_ratio: Proportion for training (default 0.8)
            
        Returns:
            train_df, test_df
        """
        df = df.sort_values('date').reset_index(drop=True)
        
        split_idx = int(len(df) * train_ratio)
        
        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()
        
        return train_df, test_df
