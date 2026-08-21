"""
Constants and Configuration for Crop Price AI System
=====================================================
Central configuration file for crops, markets, and system parameters.
All 24 crops from AGMARKNET data included.
"""

# =============================================================================
# SUPPORTED CROPS - All crops from AGMARKNET Market-Wise Report
# =============================================================================

CROPS = [
    "Bajra", "Barley", "Jowar", "Maize", "Paddy", "Ragi", "Wheat",
    "Cotton",
    "Copra", "Groundnut", "Mustard", "Niger Seed", "Safflower",
    "Sesamum", "Soyabean", "Sunflower",
    "Bengal Gram", "Black Gram", "Green Gram", "Lentil", "Red Gram",
    "Onion", "Potato", "Tomato"
]

CROP_DETAILS = {
    # Cereals
    "Bajra": {
        "full_name": "Bajra (Pearl Millet/Cumbu)",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 2775.0,
        "icon": "🌾",
        "category": "Cereals",
        "base_price": 2253,
        "volatility": 0.04,
        "seasonal_amplitude": 200,
        "peak_month": 11,
        "min_price": 1800,
        "max_price": 3200,
        "base_arrivals": 1050
    },
    "Barley": {
        "full_name": "Barley (Jau)",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 2150.0,
        "icon": "🌾",
        "category": "Cereals",
        "base_price": 2327,
        "volatility": 0.03,
        "seasonal_amplitude": 150,
        "peak_month": 3,
        "min_price": 1900,
        "max_price": 2800,
        "base_arrivals": 150
    },
    "Jowar": {
        "full_name": "Jowar (Sorghum)",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 3699.0,
        "icon": "🌾",
        "category": "Cereals",
        "base_price": 3680,
        "volatility": 0.06,
        "seasonal_amplitude": 400,
        "peak_month": 5,
        "min_price": 2500,
        "max_price": 5000,
        "base_arrivals": 300
    },
    "Maize": {
        "full_name": "Maize",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 2400.0,
        "icon": "�",
        "category": "Cereals",
        "base_price": 2121,
        "volatility": 0.04,
        "seasonal_amplitude": 250,
        "peak_month": 10,
        "min_price": 1700,
        "max_price": 3000,
        "base_arrivals": 15000
    },
    "Paddy": {
        "full_name": "Paddy (Rice - Common)",
        "variety": "Common",
        "unit": "Rs/Quintal",
        "msp": 2369.0,
        "icon": "🍚",
        "category": "Cereals",
        "base_price": 2767,
        "volatility": 0.03,
        "seasonal_amplitude": 200,
        "peak_month": 3,
        "min_price": 2300,
        "max_price": 3500,
        "base_arrivals": 12000
    },
    "Ragi": {
        "full_name": "Ragi (Finger Millet)",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 4886.0,
        "icon": "🌾",
        "category": "Cereals",
        "base_price": 3664,
        "volatility": 0.04,
        "seasonal_amplitude": 300,
        "peak_month": 4,
        "min_price": 3000,
        "max_price": 5500,
        "base_arrivals": 80
    },
    "Wheat": {
        "full_name": "Wheat",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 2585.0,
        "icon": "🌾",
        "category": "Cereals",
        "base_price": 2589,
        "volatility": 0.03,
        "seasonal_amplitude": 180,
        "peak_month": 4,
        "min_price": 2200,
        "max_price": 3100,
        "base_arrivals": 35000
    },
    # Fibre Crops
    "Cotton": {
        "full_name": "Cotton",
        "variety": "Medium Staple",
        "unit": "Rs/Quintal",
        "msp": 7710.0,
        "icon": "🧶",
        "category": "Fibre Crops",
        "base_price": 9550,
        "volatility": 0.05,
        "seasonal_amplitude": 600,
        "peak_month": 12,
        "min_price": 7000,
        "max_price": 12000,
        "base_arrivals": 200
    },
    # Oil Seeds
    "Copra": {
        "full_name": "Copra",
        "variety": "Milling",
        "unit": "Rs/Quintal",
        "msp": 12100.0,
        "icon": "🥥",
        "category": "Oil Seeds",
        "base_price": 19984,
        "volatility": 0.04,
        "seasonal_amplitude": 1500,
        "peak_month": 6,
        "min_price": 15000,
        "max_price": 25000,
        "base_arrivals": 120
    },
    "Groundnut": {
        "full_name": "Groundnut",
        "variety": "Bold",
        "unit": "Rs/Quintal",
        "msp": 7263.0,
        "icon": "🥜",
        "category": "Oil Seeds",
        "base_price": 7281,
        "volatility": 0.05,
        "seasonal_amplitude": 500,
        "peak_month": 11,
        "min_price": 5500,
        "max_price": 9500,
        "base_arrivals": 800
    },
    "Mustard": {
        "full_name": "Mustard",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 6200.0,
        "icon": "🌻",
        "category": "Oil Seeds",
        "base_price": 7308,
        "volatility": 0.04,
        "seasonal_amplitude": 400,
        "peak_month": 3,
        "min_price": 5500,
        "max_price": 9000,
        "base_arrivals": 2000
    },
    "Niger Seed": {
        "full_name": "Niger Seed (Ramtil)",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 9537.0,
        "icon": "🌱",
        "category": "Oil Seeds",
        "base_price": 12000,
        "volatility": 0.05,
        "seasonal_amplitude": 800,
        "peak_month": 2,
        "min_price": 9000,
        "max_price": 15000,
        "base_arrivals": 15
    },
    "Safflower": {
        "full_name": "Safflower",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 6540.0,
        "icon": "🌼",
        "category": "Oil Seeds",
        "base_price": 5000,
        "volatility": 0.05,
        "seasonal_amplitude": 400,
        "peak_month": 4,
        "min_price": 4000,
        "max_price": 7500,
        "base_arrivals": 35
    },
    "Sesamum": {
        "full_name": "Sesamum (Sesame/Gingelly/Til)",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 9846.0,
        "icon": "🌱",
        "category": "Oil Seeds",
        "base_price": 11940,
        "volatility": 0.06,
        "seasonal_amplitude": 1000,
        "peak_month": 7,
        "min_price": 8000,
        "max_price": 15000,
        "base_arrivals": 170
    },
    "Soyabean": {
        "full_name": "Soyabean",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 5328.0,
        "icon": "🫘",
        "category": "Oil Seeds",
        "base_price": 6365,
        "volatility": 0.04,
        "seasonal_amplitude": 400,
        "peak_month": 10,
        "min_price": 4800,
        "max_price": 8000,
        "base_arrivals": 4500
    },
    "Sunflower": {
        "full_name": "Sunflower / Sunflower Seed",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": 7721.0,
        "icon": "🌻",
        "category": "Oil Seeds",
        "base_price": 7956,
        "volatility": 0.04,
        "seasonal_amplitude": 400,
        "peak_month": 5,
        "min_price": 6500,
        "max_price": 9500,
        "base_arrivals": 110
    },
    # Pulses
    "Bengal Gram": {
        "full_name": "Bengal Gram (Chana - Whole)",
        "variety": "Whole",
        "unit": "Rs/Quintal",
        "msp": 5875.0,
        "icon": "🫘",
        "category": "Pulses",
        "base_price": 6225,
        "volatility": 0.04,
        "seasonal_amplitude": 350,
        "peak_month": 6,
        "min_price": 5000,
        "max_price": 7500,
        "base_arrivals": 2500
    },
    "Black Gram": {
        "full_name": "Black Gram (Urad - Whole)",
        "variety": "Whole",
        "unit": "Rs/Quintal",
        "msp": 7800.0,
        "icon": "🫘",
        "category": "Pulses",
        "base_price": 8187,
        "volatility": 0.05,
        "seasonal_amplitude": 500,
        "peak_month": 9,
        "min_price": 6500,
        "max_price": 10000,
        "base_arrivals": 250
    },
    "Green Gram": {
        "full_name": "Green Gram (Moong - Whole)",
        "variety": "Whole",
        "unit": "Rs/Quintal",
        "msp": 8768.0,
        "icon": "🫘",
        "category": "Pulses",
        "base_price": 7368,
        "volatility": 0.05,
        "seasonal_amplitude": 500,
        "peak_month": 8,
        "min_price": 6000,
        "max_price": 10000,
        "base_arrivals": 5500
    },
    "Lentil": {
        "full_name": "Lentil (Masoor - Whole)",
        "variety": "Whole",
        "unit": "Rs/Quintal",
        "msp": 7000.0,
        "icon": "🫘",
        "category": "Pulses",
        "base_price": 7854,
        "volatility": 0.05,
        "seasonal_amplitude": 500,
        "peak_month": 5,
        "min_price": 6000,
        "max_price": 9500,
        "base_arrivals": 450
    },
    "Red Gram": {
        "full_name": "Red Gram (Arhar/Tur - Whole)",
        "variety": "Whole",
        "unit": "Rs/Quintal",
        "msp": 8000.0,
        "icon": "🫘",
        "category": "Pulses",
        "base_price": 7495,
        "volatility": 0.04,
        "seasonal_amplitude": 400,
        "peak_month": 7,
        "min_price": 6000,
        "max_price": 9500,
        "base_arrivals": 750
    },
    # Vegetables
    "Onion": {
        "full_name": "Onion",
        "variety": "Nasik Red",
        "unit": "Rs/Quintal",
        "msp": None,
        "icon": "🧅",
        "category": "Vegetables",
        "base_price": 2545,
        "volatility": 0.06,
        "seasonal_amplitude": 500,
        "peak_month": 10,
        "min_price": 1200,
        "max_price": 4500,
        "base_arrivals": 26000
    },
    "Potato": {
        "full_name": "Potato",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": None,
        "icon": "🥔",
        "category": "Vegetables",
        "base_price": 668,
        "volatility": 0.06,
        "seasonal_amplitude": 200,
        "peak_month": 8,
        "min_price": 300,
        "max_price": 1500,
        "base_arrivals": 30000
    },
    "Tomato": {
        "full_name": "Tomato",
        "variety": "Local",
        "unit": "Rs/Quintal",
        "msp": None,
        "icon": "�",
        "category": "Vegetables",
        "base_price": 1729,
        "volatility": 0.08,
        "seasonal_amplitude": 400,
        "peak_month": 5,
        "min_price": 500,
        "max_price": 4000,
        "base_arrivals": 8000
    },
}

# Crop categories for grouping in UI
CROP_CATEGORIES = {
    "Cereals": ["Bajra", "Barley", "Jowar", "Maize", "Paddy", "Ragi", "Wheat"],
    "Fibre Crops": ["Cotton"],
    "Oil Seeds": ["Copra", "Groundnut", "Mustard", "Niger Seed", "Safflower",
                  "Sesamum", "Soyabean", "Sunflower"],
    "Pulses": ["Bengal Gram", "Black Gram", "Green Gram", "Lentil", "Red Gram"],
    "Vegetables": ["Onion", "Potato", "Tomato"],
}

# =============================================================================
# SUPPORTED MARKETS
# =============================================================================

MARKETS = ["Koyambedu", "Azadpur", "Vashi", "Bowenpally", "Yeshwanthpur"]

MARKET_DETAILS = {
    "Koyambedu": {
        "district": "Chennai",
        "state": "Tamil Nadu",
        "lat": 13.0694,
        "lon": 80.1948
    },
    "Azadpur": {
        "district": "New Delhi",
        "state": "Delhi",
        "lat": 28.7136,
        "lon": 77.1770
    },
    "Vashi": {
        "district": "Mumbai",
        "state": "Maharashtra",
        "lat": 19.0771,
        "lon": 73.0071
    },
    "Bowenpally": {
        "district": "Hyderabad",
        "state": "Telangana",
        "lat": 17.4700,
        "lon": 78.4800
    },
    "Yeshwanthpur": {
        "district": "Bangalore",
        "state": "Karnataka",
        "lat": 13.0206,
        "lon": 77.5330
    }
}

# Approximate distances between markets (km)
MARKET_DISTANCES = {
    "Koyambedu": {"Koyambedu": 0, "Azadpur": 2175, "Vashi": 1330, "Bowenpally": 625, "Yeshwanthpur": 350},
    "Azadpur": {"Koyambedu": 2175, "Azadpur": 0, "Vashi": 1400, "Bowenpally": 1550, "Yeshwanthpur": 2100},
    "Vashi": {"Koyambedu": 1330, "Azadpur": 1400, "Vashi": 0, "Bowenpally": 710, "Yeshwanthpur": 980},
    "Bowenpally": {"Koyambedu": 625, "Azadpur": 1550, "Vashi": 710, "Bowenpally": 0, "Yeshwanthpur": 570},
    "Yeshwanthpur": {"Koyambedu": 350, "Azadpur": 2100, "Vashi": 980, "Bowenpally": 570, "Yeshwanthpur": 0},
}

# =============================================================================
# DECISION ENGINE THRESHOLDS
# =============================================================================

MARKET_SWITCH_THRESHOLD = 0.10  # 10%
MIN_WAIT_BENEFIT = 500  # Rs total
DEFAULT_STORAGE_COST_PER_DAY = 5.0  # Rs/quintal/day
DEFAULT_TRANSPORT_COST_PER_KM = 2.5  # Rs/km/quintal

# =============================================================================
# ML MODEL CONFIGURATION
# =============================================================================

MODEL_CONFIG = {
    "n_estimators": 100,
    "max_depth": 15,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "random_state": 42,
    "train_test_split_ratio": 0.8,
}

FORECAST_HORIZONS = [1, 3, 7]

# =============================================================================
# RISK THRESHOLDS
# =============================================================================

RISK_LOW_THRESHOLD = 0.05
RISK_MODERATE_THRESHOLD = 0.10

# =============================================================================
# DATA PATHS
# =============================================================================

DEMO_DATA_PATH = "data/raw/demo_prices.csv"
RECENT_DATA_PATH = "data/raw/recent_prices.csv"
PROCESSED_DATA_PATH = "data/processed/cleaned_prices.csv"
MODEL_DIR = "models/"
DATABASE_PATH = "data/crop_prices.db"

# =============================================================================
# APPLICATION CONFIG
# =============================================================================

APP_NAME = "CropSmart AI"
APP_TAGLINE = "Know when. Know where. Sell smarter."
APP_VERSION = "1.0.0-MVP"

# Pagination
CROPS_PER_PAGE = 8  # Number of crop cards per page on dashboard

DISCLAIMER = (
    "All forecasts, recommendations, and revenue estimates shown by this system are "
    "based on historical data patterns and statistical models. They are estimates only "
    "and should not be treated as guaranteed outcomes. Real-world market conditions may "
    "differ significantly."
)
