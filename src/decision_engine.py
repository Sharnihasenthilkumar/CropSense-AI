"""
Decision Engine Module
========================
Converts ML predictions + market comparison into actionable recommendations.

Outputs:
- SELL NOW: Best to sell immediately
- WAIT: Price expected to rise enough to cover storage
- TRY ANOTHER MARKET: Better net revenue available elsewhere

Every recommendation includes an explanation (transparency).
"""

import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import MARKET_SWITCH_THRESHOLD, MIN_WAIT_BENEFIT


class DecisionEngine:
    """Rule-based decision engine for selling recommendations."""
    
    def __init__(self):
        pass
    
    def get_recommendation(self, current_price, predictions, market_comparison,
                           storage_available, storage_cost_per_day, quantity_kg):
        """
        Generate a selling recommendation with explanation.
        
        Args:
            current_price: Current modal price (Rs/Quintal)
            predictions: Dict {"1d": price, "3d": price, "7d": price}
            market_comparison: Output from MarketComparison.compare_markets()
            storage_available: Boolean
            storage_cost_per_day: Rs per quintal per day
            quantity_kg: Quantity in kg
            
        Returns:
            Dictionary with recommendation, explanation, and details
        """
        quantity_quintal = quantity_kg / 100
        
        # Extract key values
        pred_1d = predictions.get("1d", current_price)
        pred_3d = predictions.get("3d", current_price)
        pred_7d = predictions.get("7d", current_price)
        
        summary = market_comparison.get("summary", {})
        best_market = market_comparison.get("best_market")
        
        # Calculate revenue scenarios
        current_revenue = current_price * quantity_quintal
        
        # Revenue if waiting (accounting for storage costs)
        revenue_1d = pred_1d * quantity_quintal - (storage_cost_per_day * quantity_quintal * 1)
        revenue_3d = pred_3d * quantity_quintal - (storage_cost_per_day * quantity_quintal * 3)
        revenue_7d = pred_7d * quantity_quintal - (storage_cost_per_day * quantity_quintal * 7)
        
        # Best future revenue
        future_revenues = {"1d": revenue_1d, "3d": revenue_3d, "7d": revenue_7d}
        best_wait_period = max(future_revenues, key=future_revenues.get)
        best_future_revenue = future_revenues[best_wait_period]
        
        # Wait benefit (how much more we get by waiting vs selling now)
        wait_benefit = best_future_revenue - current_revenue
        
        # Market switch advantage
        market_advantage = summary.get("advantage", 0)
        market_advantage_pct = summary.get("advantage_pct", 0)
        should_switch_market = summary.get("should_switch", False)
        
        # =================================================================
        # DECISION LOGIC
        # =================================================================
        
        reasons = []
        
        # CHECK 1: Is another market significantly better?
        if (should_switch_market and 
            market_advantage_pct > MARKET_SWITCH_THRESHOLD * 100 and
            market_advantage > MIN_WAIT_BENEFIT):
            
            recommendation = "TRY_ANOTHER_MARKET"
            best_mkt_name = summary.get("best_market_name", "another market")
            
            reasons.append(
                f"{best_mkt_name} offers higher estimated net revenue."
            )
            reasons.append(
                f"Even after transportation cost, estimated additional revenue: "
                f"₹{market_advantage:,.0f} ({market_advantage_pct:.1f}% more)."
            )
            reasons.append(
                f"Net revenue at {best_mkt_name}: ₹{summary.get('best_market_net', 0):,.0f} "
                f"vs current market: ₹{summary.get('current_market_net', 0):,.0f}."
            )
            
        # CHECK 2: Should we wait?
        elif (storage_available and 
              wait_benefit > MIN_WAIT_BENEFIT and
              best_future_revenue > current_revenue):
            
            recommendation = "WAIT"
            wait_days = int(best_wait_period.replace('d', ''))
            
            reasons.append(
                f"Predicted price may increase over the next {wait_days} days."
            )
            reasons.append(f"Storage is available.")
            reasons.append(
                f"Estimated additional revenue after storage costs: "
                f"₹{wait_benefit:,.0f}."
            )
            
            # Price trend reason
            if pred_3d > current_price:
                pct_increase = ((pred_3d - current_price) / current_price) * 100
                reasons.append(
                    f"Historical trend shows potential price increase "
                    f"of approximately {pct_increase:.1f}%."
                )
            
            reasons.append(
                f"Estimated revenue if waiting {wait_days} days: "
                f"₹{best_future_revenue:,.0f} (vs selling today: ₹{current_revenue:,.0f})."
            )
            
        # CHECK 3: Default - Sell Now
        else:
            recommendation = "SELL_NOW"
            
            if not storage_available:
                reasons.append("Storage is not available.")
            
            if pred_3d <= current_price:
                reasons.append("Price trend appears flat or declining.")
            
            if wait_benefit <= 0:
                reasons.append(
                    "Predicted future price increase does not compensate "
                    "for storage costs."
                )
            elif wait_benefit <= MIN_WAIT_BENEFIT:
                reasons.append(
                    f"Expected benefit of waiting (₹{wait_benefit:,.0f}) "
                    f"is too small to justify the risk."
                )
            
            reasons.append(
                f"Selling now provides estimated revenue of ₹{current_revenue:,.0f}."
            )
        
        # =================================================================
        # BUILD RESPONSE
        # =================================================================
        
        # What-if comparison
        what_if = {
            "sell_today": round(current_revenue, 2),
            "wait_1_day": round(revenue_1d, 2),
            "wait_3_days": round(revenue_3d, 2),
            "wait_7_days": round(revenue_7d, 2),
        }
        
        # Find best selling window
        all_options = {"today": current_revenue, **future_revenues}
        best_option = max(all_options, key=all_options.get)
        
        if best_option == "today":
            best_window = "Sell Today"
        else:
            days = best_option.replace("d", "")
            best_window = f"Wait {days} Day{'s' if int(days) > 1 else ''}"
        
        return {
            "recommendation": recommendation,
            "reasons": reasons,
            "what_if": what_if,
            "best_selling_window": best_window,
            "current_revenue": round(current_revenue, 2),
            "best_future_revenue": round(best_future_revenue, 2),
            "wait_benefit": round(wait_benefit, 2),
            "market_advantage": round(market_advantage, 2),
            "recommended_market": best_market,
            "details": {
                "current_price": current_price,
                "pred_1d": pred_1d,
                "pred_3d": pred_3d,
                "pred_7d": pred_7d,
                "quantity_quintal": quantity_quintal,
                "storage_available": storage_available,
                "storage_cost_per_day": storage_cost_per_day
            }
        }
    
    def get_recommendation_display(self, recommendation):
        """
        Get display properties for a recommendation.
        
        Returns:
            Dict with color, emoji, and display text
        """
        displays = {
            "SELL_NOW": {
                "color": "green",
                "emoji": "🟢",
                "text": "SELL NOW",
                "description": "Current conditions favor immediate selling."
            },
            "WAIT": {
                "color": "orange",
                "emoji": "🟡",
                "text": "WAIT",
                "description": "Prices are expected to rise enough to cover storage costs."
            },
            "TRY_ANOTHER_MARKET": {
                "color": "blue",
                "emoji": "🔵",
                "text": "TRY ANOTHER MARKET",
                "description": "A nearby market offers better net revenue."
            }
        }
        
        return displays.get(recommendation, displays["SELL_NOW"])
