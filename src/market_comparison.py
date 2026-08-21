"""
Market Comparison Engine
=========================
Compares net revenue across multiple markets.
Factors in: predicted price, quantity, transport cost, storage cost.

IMPORTANT: Highest price != Best market.
The system recommends based on NET REVENUE (after all costs).
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import (
    MARKETS, MARKET_DETAILS, MARKET_DISTANCES,
    DEFAULT_TRANSPORT_COST_PER_KM
)


class MarketComparison:
    """Compares markets based on estimated net revenue."""
    
    def __init__(self):
        pass
    
    def compare_markets(self, crop, current_market, quantity_kg, 
                        predictions_by_market, transport_cost_per_km,
                        max_distance=None, storage_cost_per_day=0, wait_days=0):
        """
        Compare all available markets for a given crop.
        
        Args:
            crop: Crop name
            current_market: Farmer's current/home market
            quantity_kg: Quantity in kilograms
            predictions_by_market: Dict {market_name: predicted_price_per_quintal}
            transport_cost_per_km: Rs per km per quintal
            max_distance: Maximum distance farmer is willing to travel (km)
            storage_cost_per_day: Rs per quintal per day
            wait_days: Number of days waiting (for storage cost calculation)
            
        Returns:
            Dictionary with comparison results and recommendation
        """
        quantity_quintal = quantity_kg / 100  # Convert kg to quintal
        
        results = []
        
        for market in MARKETS:
            if market not in predictions_by_market:
                continue
            
            predicted_price = predictions_by_market[market]
            
            # Calculate distance from current market
            distance = MARKET_DISTANCES.get(current_market, {}).get(market, 0)
            
            # Skip if beyond max distance
            if max_distance and distance > max_distance and market != current_market:
                continue
            
            # Calculate costs
            transport_cost = distance * transport_cost_per_km * quantity_quintal
            storage_cost = storage_cost_per_day * quantity_quintal * wait_days
            
            # Calculate revenue
            gross_revenue = predicted_price * quantity_quintal
            net_revenue = gross_revenue - transport_cost - storage_cost
            
            results.append({
                "market": market,
                "district": MARKET_DETAILS[market]["district"],
                "state": MARKET_DETAILS[market]["state"],
                "predicted_price": round(predicted_price, 2),
                "distance_km": distance,
                "transport_cost": round(transport_cost, 2),
                "storage_cost": round(storage_cost, 2),
                "gross_revenue": round(gross_revenue, 2),
                "net_revenue": round(net_revenue, 2),
                "is_current_market": market == current_market
            })
        
        # Sort by net revenue (descending)
        results.sort(key=lambda x: x["net_revenue"], reverse=True)
        
        # Mark recommended market
        if results:
            results[0]["recommended"] = True
            for r in results[1:]:
                r["recommended"] = False
        
        # Calculate comparative metrics
        current_market_result = next(
            (r for r in results if r["is_current_market"]), None
        )
        best_market_result = results[0] if results else None
        
        comparison_summary = self._build_summary(
            results, current_market_result, best_market_result
        )
        
        return {
            "markets": results,
            "summary": comparison_summary,
            "quantity_quintal": quantity_quintal,
            "best_market": best_market_result["market"] if best_market_result else None
        }
    
    def _build_summary(self, results, current_result, best_result):
        """Build a human-readable comparison summary."""
        if not results or not current_result or not best_result:
            return {"advantage": 0, "should_switch": False}
        
        current_net = current_result["net_revenue"]
        best_net = best_result["net_revenue"]
        
        advantage = best_net - current_net
        advantage_pct = (advantage / current_net * 100) if current_net > 0 else 0
        
        return {
            "current_market_net": current_net,
            "best_market_net": best_net,
            "advantage": round(advantage, 2),
            "advantage_pct": round(advantage_pct, 2),
            "should_switch": best_result["market"] != current_result["market"],
            "best_market_name": best_result["market"],
            "current_market_name": current_result["market"]
        }
    
    def get_market_distance(self, from_market, to_market):
        """Get distance between two markets in km."""
        return MARKET_DISTANCES.get(from_market, {}).get(to_market, 0)
    
    def calculate_transport_cost(self, from_market, to_market, 
                                  quantity_kg, cost_per_km):
        """Calculate transport cost between two markets."""
        distance = self.get_market_distance(from_market, to_market)
        quantity_quintal = quantity_kg / 100
        return round(distance * cost_per_km * quantity_quintal, 2)
