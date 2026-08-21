"""
Model Training Pipeline
========================
Trains RandomForestRegressor on historical crop price data.
Uses chronological train/test split (no data leakage).
Evaluates with MAE, RMSE, R-squared.
Saves trained model to .pkl file.
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import MODEL_CONFIG, MODEL_DIR, DEMO_DATA_PATH
from src.data_fetcher import DataFetcher
from src.data_cleaner import DataCleaner
from src.feature_engineering import FeatureEngineer


class ModelTrainer:
    """Trains and evaluates crop price prediction models."""
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.cleaner = DataCleaner()
        self.feature_engineer = FeatureEngineer()
        self.models = {}  # crop -> trained model
        self.metrics = {}  # crop -> evaluation metrics
    
    def train_all(self):
        """
        Train models for all crops. Returns training metrics.
        """
        print("=" * 60)
        print("CROP PRICE AI - MODEL TRAINING PIPELINE")
        print("=" * 60)
        
        # Load data
        print("\n[1/5] Loading data...")
        df = self.fetcher.get_data()
        if df is None or df.empty:
            print("ERROR: No data available for training!")
            return None
        print(f"  Loaded {len(df)} records")
        
        # Clean data
        print("\n[2/5] Cleaning data...")
        df = self.cleaner.clean(df)
        report = self.cleaner.get_cleaning_report()
        print(f"  Cleaned: {report['original_rows']} -> {report['cleaned_rows']} rows")
        
        # Feature engineering
        print("\n[3/5] Engineering features...")
        df = self.feature_engineer.create_features(df)
        print(f"  Features created: {len(self.feature_engineer.feature_columns)} features")
        print(f"  Records after feature engineering: {len(df)}")
        
        # Train model for each crop
        print("\n[4/5] Training models...")
        crops = df['crop'].unique()
        
        for crop in crops:
            print(f"\n  Training: {crop}")
            crop_df = df[df['crop'] == crop].copy()
            
            metrics = self._train_single_crop(crop, crop_df)
            if metrics:
                self.metrics[crop] = metrics
                print(f"    MAE:  {metrics['mae']:.2f} Rs/Quintal")
                print(f"    RMSE: {metrics['rmse']:.2f} Rs/Quintal")
                print(f"    R²:   {metrics['r2']:.4f}")
                print(f"    Train size: {metrics['train_size']}, Test size: {metrics['test_size']}")
        
        # Save models
        print("\n[5/5] Saving models...")
        self._save_models()
        
        print("\n" + "=" * 60)
        print("TRAINING COMPLETE")
        print("=" * 60)
        
        return self.metrics
    
    def _train_single_crop(self, crop, crop_df):
        """
        Train a model for a single crop using chronological split.
        
        Args:
            crop: Crop name
            crop_df: DataFrame filtered for this crop
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Chronological split
        train_df, test_df = self.feature_engineer.chronological_split(
            crop_df, train_ratio=MODEL_CONFIG['train_test_split_ratio']
        )
        
        if len(train_df) < 50 or len(test_df) < 10:
            print(f"    WARNING: Insufficient data for {crop}")
            return None
        
        # Get feature matrices
        X_train, y_train = self.feature_engineer.get_feature_matrix(train_df)
        X_test, y_test = self.feature_engineer.get_feature_matrix(test_df)
        
        # Train Random Forest
        model = RandomForestRegressor(
            n_estimators=MODEL_CONFIG['n_estimators'],
            max_depth=MODEL_CONFIG['max_depth'],
            min_samples_split=MODEL_CONFIG['min_samples_split'],
            min_samples_leaf=MODEL_CONFIG['min_samples_leaf'],
            random_state=MODEL_CONFIG['random_state'],
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Store model
        self.models[crop] = model
        
        # Feature importance
        feature_importance = dict(zip(
            self.feature_engineer.feature_columns,
            model.feature_importances_
        ))
        
        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'train_size': len(train_df),
            'test_size': len(test_df),
            'feature_importance': feature_importance
        }
    
    def _save_models(self):
        """Save all trained models to disk."""
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        for crop, model in self.models.items():
            filename = f"rf_{crop.lower()}.pkl"
            filepath = os.path.join(MODEL_DIR, filename)
            joblib.dump(model, filepath)
            print(f"  Saved: {filepath}")
        
        # Save feature engineer (for encoding consistency)
        fe_path = os.path.join(MODEL_DIR, "feature_engineer.pkl")
        joblib.dump(self.feature_engineer, fe_path)
        print(f"  Saved: {fe_path}")
        
        # Save metrics
        metrics_path = os.path.join(MODEL_DIR, "metrics.pkl")
        joblib.dump(self.metrics, metrics_path)
        print(f"  Saved: {metrics_path}")
    
    def get_metrics(self):
        """Return training metrics for all crops."""
        return self.metrics


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    trainer = ModelTrainer()
    metrics = trainer.train_all()
    
    if metrics:
        print("\n\nFINAL METRICS SUMMARY:")
        print("-" * 40)
        for crop, m in metrics.items():
            print(f"\n{crop}:")
            print(f"  MAE:  {m['mae']:.2f} Rs/Quintal")
            print(f"  RMSE: {m['rmse']:.2f} Rs/Quintal")
            print(f"  R²:   {m['r2']:.4f}")
