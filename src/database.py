"""
Database Module (SQLite)
=========================
Handles all database operations for storing market prices and farmer queries.
"""

import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import DATABASE_PATH


class Database:
    """SQLite database operations for Crop Price AI."""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = DATABASE_PATH
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
        
        self.db_path = db_path
        self._create_tables()
    
    def _get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Market prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                crop TEXT NOT NULL,
                variety TEXT,
                market TEXT NOT NULL,
                district TEXT,
                state TEXT,
                min_price REAL,
                max_price REAL,
                modal_price REAL NOT NULL,
                arrivals REAL
            )
        ''')
        
        # Farmer queries table (for analytics, no PII)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farmer_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                crop TEXT NOT NULL,
                selected_market TEXT NOT NULL,
                quantity_kg REAL NOT NULL,
                storage_available INTEGER,
                storage_cost REAL,
                transport_cost REAL,
                recommendation TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_prices(self, df):
        """
        Insert price data from DataFrame into database.
        
        Args:
            df: DataFrame with price data
        """
        conn = self._get_connection()
        
        # Map DataFrame columns to table columns
        columns = ['date', 'crop', 'variety', 'market', 'district', 
                   'state', 'min_price', 'max_price', 'modal_price', 'arrivals']
        
        available_cols = [col for col in columns if col in df.columns]
        df_subset = df[available_cols].copy()
        
        # Convert date to string if datetime
        if 'date' in df_subset.columns:
            df_subset['date'] = pd.to_datetime(df_subset['date']).dt.strftime('%Y-%m-%d')
        
        df_subset.to_sql('market_prices', conn, if_exists='append', index=False)
        conn.close()
    
    def get_prices(self, crop=None, market=None, start_date=None, end_date=None):
        """
        Retrieve price data from database.
        
        Args:
            crop: Filter by crop name
            market: Filter by market name
            start_date: Filter from date (YYYY-MM-DD)
            end_date: Filter to date (YYYY-MM-DD)
            
        Returns:
            DataFrame with matching records
        """
        conn = self._get_connection()
        
        query = "SELECT * FROM market_prices WHERE 1=1"
        params = []
        
        if crop:
            query += " AND crop = ?"
            params.append(crop)
        if market:
            query += " AND market = ?"
            params.append(market)
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date ASC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def log_farmer_query(self, crop, market, quantity_kg, storage_available,
                         storage_cost, transport_cost, recommendation):
        """
        Log a farmer query for analytics (no PII stored).
        
        Args:
            crop: Selected crop
            market: Selected market
            quantity_kg: Quantity in kg
            storage_available: Boolean
            storage_cost: Cost per day
            transport_cost: Cost per km
            recommendation: AI recommendation given
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO farmer_queries 
            (timestamp, crop, selected_market, quantity_kg, storage_available, 
             storage_cost, transport_cost, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            crop,
            market,
            quantity_kg,
            1 if storage_available else 0,
            storage_cost,
            transport_cost,
            recommendation
        ))
        
        conn.commit()
        conn.close()
    
    def get_query_count(self):
        """Get total number of farmer queries logged."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM farmer_queries")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def is_empty(self):
        """Check if the prices table is empty."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM market_prices")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
