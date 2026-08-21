"""
Data Cleaner Module
====================
Handles data cleaning, validation, and preprocessing.
- Missing value handling
- Duplicate removal
- Date conversion
- Outlier handling
- Price validation
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import PROCESSED_DATA_PATH


class DataCleaner:
    """Cleans and validates crop price data."""
    
    def __init__(self):
        self.cleaning_report = {}
    
    def clean(self, df):
        """
        Main cleaning pipeline. Runs all cleaning steps in order.
        
        Args:
            df: Raw DataFrame with crop price data
            
        Returns:
            Cleaned DataFrame
        """
        if df is None or df.empty:
            return df
        
        original_rows = len(df)
        
        # Step 1: Convert date column
        df = self._convert_dates(df)
        
        # Step 2: Remove duplicates
        df = self._remove_duplicates(df)
        
        # Step 3: Handle missing values
        df = self._handle_missing_values(df)
        
        # Step 4: Validate prices (remove negative/invalid)
        df = self._validate_prices(df)
        
        # Step 5: Handle outliers
        df = self._handle_outliers(df)
        
        # Step 6: Sort data
        df = self._sort_data(df)
        
        # Generate report
        self.cleaning_report = {
            "original_rows": original_rows,
            "cleaned_rows": len(df),
            "rows_removed": original_rows - len(df),
            "removal_percentage": round((original_rows - len(df)) / original_rows * 100, 2)
        }
        
        return df
    
    def _convert_dates(self, df):
        """Convert date column to datetime format."""
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            # Remove rows where date conversion failed
            df = df.dropna(subset=['date'])
        return df
    
    def _remove_duplicates(self, df):
        """Remove duplicate rows based on date, crop, and market."""
        key_columns = ['date', 'crop', 'market']
        existing_keys = [col for col in key_columns if col in df.columns]
        
        if existing_keys:
            df = df.drop_duplicates(subset=existing_keys, keep='last')
        else:
            df = df.drop_duplicates()
        
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values with appropriate strategies."""
        # For price columns: forward fill within each crop-market group
        price_columns = ['min_price', 'max_price', 'modal_price']
        
        for col in price_columns:
            if col in df.columns:
                # Replace '-' or empty strings with NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Forward fill within groups
                if 'crop' in df.columns and 'market' in df.columns:
                    df[col] = df.groupby(['crop', 'market'])[col].transform(
                        lambda x: x.fillna(method='ffill').fillna(method='bfill')
                    )
        
        # For arrivals: fill with median of group
        if 'arrivals' in df.columns:
            df['arrivals'] = pd.to_numeric(df['arrivals'], errors='coerce')
            if 'crop' in df.columns and 'market' in df.columns:
                df['arrivals'] = df.groupby(['crop', 'market'])['arrivals'].transform(
                    lambda x: x.fillna(x.median())
                )
        
        # Drop rows where modal_price is still missing (critical column)
        if 'modal_price' in df.columns:
            df = df.dropna(subset=['modal_price'])
        
        return df
    
    def _validate_prices(self, df):
        """Remove rows with invalid or negative prices."""
        price_columns = ['min_price', 'max_price', 'modal_price']
        
        for col in price_columns:
            if col in df.columns:
                # Remove negative prices
                df = df[df[col] >= 0]
                
                # Remove zero modal prices
                if col == 'modal_price':
                    df = df[df[col] > 0]
        
        # Validate: min_price <= modal_price <= max_price
        if all(col in df.columns for col in price_columns):
            # Fix cases where min > modal or modal > max
            mask_min = df['min_price'] > df['modal_price']
            df.loc[mask_min, 'min_price'] = df.loc[mask_min, 'modal_price'] * 0.85
            
            mask_max = df['max_price'] < df['modal_price']
            df.loc[mask_max, 'max_price'] = df.loc[mask_max, 'modal_price'] * 1.15
        
        return df
    
    def _handle_outliers(self, df):
        """Handle extreme outliers using IQR method within each crop group."""
        if 'modal_price' not in df.columns or 'crop' not in df.columns:
            return df
        
        cleaned_dfs = []
        
        for crop in df['crop'].unique():
            crop_df = df[df['crop'] == crop].copy()
            
            Q1 = crop_df['modal_price'].quantile(0.05)
            Q3 = crop_df['modal_price'].quantile(0.95)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 2.0 * IQR
            upper_bound = Q3 + 2.0 * IQR
            
            # Clip rather than remove (preserves data points)
            crop_df['modal_price'] = crop_df['modal_price'].clip(lower_bound, upper_bound)
            cleaned_dfs.append(crop_df)
        
        return pd.concat(cleaned_dfs, ignore_index=True)
    
    def _sort_data(self, df):
        """Sort data by crop, market, and date."""
        sort_columns = []
        if 'crop' in df.columns:
            sort_columns.append('crop')
        if 'market' in df.columns:
            sort_columns.append('market')
        if 'date' in df.columns:
            sort_columns.append('date')
        
        if sort_columns:
            df = df.sort_values(sort_columns).reset_index(drop=True)
        
        return df
    
    def save_cleaned_data(self, df, path=None):
        """Save cleaned data to processed folder."""
        if path is None:
            path = PROCESSED_DATA_PATH
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        df.to_csv(path, index=False)
        return path
    
    def get_cleaning_report(self):
        """Return the cleaning report."""
        return self.cleaning_report
