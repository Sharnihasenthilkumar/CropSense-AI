"""
Data Fetcher Module
====================
Handles data loading from APIs (when available) with CSV fallback.
Priority: Live API -> Local CSV Demo Data

The application never crashes due to API unavailability.
"""

import pandas as pd
import os
import requests
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import DEMO_DATA_PATH, RECENT_DATA_PATH


class DataFetcher:
    """Fetches crop price data from API or falls back to CSV."""
    
    def __init__(self):
        self.data_source = "csv"  # Track which source was used
        self.last_fetch_time = None
    
    def fetch_from_api(self, crop=None, market=None, days=180):
        """
        Attempt to fetch data from government API (AGMARKNET/data.gov.in).
        
        Note: In production, this would connect to:
        - https://agmarknet.gov.in/
        - https://api.data.gov.in/resource/
        
        For the hackathon MVP, this returns None and falls back to CSV.
        The architecture supports adding real API integration later.
        """
        try:
            # Placeholder for real API integration
            # API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            # params = {
            #     "api-key": "YOUR_API_KEY",
            #     "format": "json",
            #     "filters[commodity]": crop,
            #     "filters[market]": market,
            #     "limit": days * 5
            # }
            # response = requests.get(API_URL, params=params, timeout=10)
            # if response.status_code == 200:
            #     data = response.json()
            #     df = pd.DataFrame(data['records'])
            #     self.data_source = "api"
            #     return df
            
            # For MVP: API not connected, return None to trigger fallback
            return None
            
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"API fetch failed: {e}")
            return None
    
    def fetch_from_csv(self, use_recent=False):
        """
        Load data from local CSV files (fallback/demo mode).
        
        Args:
            use_recent: If True, load only recent data (faster for predictions)
        """
        try:
            file_path = RECENT_DATA_PATH if use_recent else DEMO_DATA_PATH
            
            if not os.path.exists(file_path):
                # Try absolute path from script location
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                file_path = os.path.join(base_dir, file_path)
            
            if not os.path.exists(file_path):
                print(f"CSV file not found: {file_path}")
                return None
            
            df = pd.read_csv(file_path)
            self.data_source = "csv"
            self.last_fetch_time = datetime.now()
            return df
            
        except Exception as e:
            print(f"CSV loading failed: {e}")
            return None
    
    def get_data(self, crop=None, market=None, use_recent=False):
        """
        Main data retrieval method with automatic fallback.
        
        Priority: API -> CSV
        
        Args:
            crop: Filter by crop name (optional)
            market: Filter by market name (optional)
            use_recent: Use only recent data subset
            
        Returns:
            DataFrame with crop price data, or None if all sources fail
        """
        # Try API first
        df = self.fetch_from_api(crop=crop, market=market)
        
        # Fallback to CSV
        if df is None:
            df = self.fetch_from_csv(use_recent=use_recent)
        
        if df is None:
            return None
        
        # Apply filters if specified
        if crop and 'crop' in df.columns:
            df = df[df['crop'] == crop]
        
        if market and 'market' in df.columns:
            df = df[df['market'] == market]
        
        return df.reset_index(drop=True)
    
    def get_available_crops(self):
        """Get list of crops available in the dataset."""
        df = self.fetch_from_csv()
        if df is not None and 'crop' in df.columns:
            return sorted(df['crop'].unique().tolist())
        return []
    
    def get_available_markets(self):
        """Get list of markets available in the dataset."""
        df = self.fetch_from_csv()
        if df is not None and 'market' in df.columns:
            return sorted(df['market'].unique().tolist())
        return []
    
    def get_data_source_info(self):
        """Return information about the current data source."""
        return {
            "source": self.data_source,
            "last_fetch": self.last_fetch_time,
            "is_live": self.data_source == "api"
        }
