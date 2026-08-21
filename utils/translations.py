"""
Complete Localization System for CropSmart AI
===============================================
Centralized English/Tamil translation dictionary.
Every user-facing string uses t(), t_crop(), t_market(), t_category().

Usage:
    from utils.translations import t, t_crop, t_market, t_category
    t("todays_crop_prices", lang)
    t_crop("Bajra", lang)
"""

# =============================================================================
# MAIN UI TRANSLATIONS
# =============================================================================

_T = {
    # APP
    "app_name": ("CropSmart AI", "CropSmart AI"),
    "tagline": ("Know when. Know where. Sell smarter.", "எப்போது என்று அறியுங்கள். எங்கே என்று அறியுங்கள். புத்திசாலியாக விற்கவும்."),
    "hero_stat": ("24 Crops • 5 Markets • AI-Powered Recommendations", "24 பயிர்கள் • 5 சந்தைகள் • AI அடிப்படையிலான பரிந்துரைகள்"),

    # SIDEBAR
    "sidebar_crops_markets": ("📊 **24 Crops** | **5 Markets**", "📊 **24 பயிர்கள்** | **5 சந்தைகள்**"),
    "sidebar_model": ("🤖 Model: Random Forest", "🤖 மாதிரி: Random Forest"),
    "sidebar_data": ("📅 Data: Feb-Aug 2026", "📅 தரவு: பிப்-ஆக 2026"),

    # NAVIGATION
    "nav_home": ("Home Dashboard", "முகப்பு"),
    "nav_farmer_input": ("Farmer Input", "விவசாயி தகவல்"),
    "nav_price_forecast": ("Price Forecast", "விலை முன்னறிவிப்பு"),
    "nav_market_comparison": ("Market Comparison", "சந்தை ஒப்பீடு"),
    "nav_ai_recommendation": ("AI Recommendation", "AI பரிந்துரை"),

    # DASHBOARD / HOME
    "todays_crop_prices": ("Today's Crop Prices", "இன்றைய பயிர் விலைகள்"),
    "all_categories": ("All Categories", "அனைத்து வகைகளும்"),
    "prev": ("◀ Prev", "◀ முந்தையது"),
    "next": ("Next ▶", "அடுத்தது ▶"),
    "total_records": ("Total Records", "மொத்த பதிவுகள்"),
    "crops_tracked": ("Crops Tracked", "கண்காணிக்கப்படும் பயிர்கள்"),
    "markets_count": ("Markets", "சந்தைகள்"),
    "days_of_data": ("Days of Data", "தரவு நாட்கள்"),
    "latest_prices_header": ("Latest Prices (Rs/Quintal)", "சமீபத்திய விலைகள் (ரூ/குவிண்டால்)"),
    "vs_yesterday": ("vs yesterday", "நேற்றுடன் ஒப்பிடும்போது"),
    "price_by_market_all": ("Latest Prices by Market (All Crops)", "சந்தை வாரியாக சமீபத்திய விலைகள் (அனைத்து பயிர்கள்)"),
    "green_highest": ("🟢 Green = Highest price for that crop across markets", "🟢 பச்சை = அந்த பயிருக்கு சந்தைகளில் அதிக விலை"),
    "30_day_trend": ("30-Day Price Trend", "30 நாள் விலை போக்கு"),
    "select_crop_trend": ("Select Crop for Trend", "போக்குக்கான பயிரை தேர்ந்தெடுக்கவும்"),
    "no_msp": ("No MSP", "MSP இல்லை"),
    "dashboard_title": ("Dashboard — All Crops", "முகப்பு — அனைத்து பயிர்கள்"),
    "dashboard_subtitle": ("Real-time market prices for all **24 commodities** tracked by AGMARKNET.", "AGMARKNET கண்காணிக்கும் அனைத்து **24 பொருட்களின்** சந்தை விலைகள்."),

    # WHAT IT DOES / FEATURES
    "what_does_it_do": ("What CropSmart AI Does", "CropSmart AI என்ன செய்கிறது"),
    "feat_forecast_title": ("🤖 AI Forecasting", "🤖 AI முன்னறிவிப்பு"),
    "feat_forecast_desc": ("Predicts prices for 1, 3, and 7 days using Random Forest trained on 180 days of data for all 24 crops.", "180 நாள் தரவில் பயிற்சி பெற்ற Random Forest மூலம் 24 பயிர்களுக்கும் 1, 3, 7 நாள் விலையை கணிக்கிறது."),
    "feat_compare_title": ("📊 Market Compare", "📊 சந்தை ஒப்பீடு"),
    "feat_compare_desc": ("Compares 5 major markets. Calculates NET revenue after transport & storage. Finds the most profitable one.", "5 முக்கிய சந்தைகளை ஒப்பிடுகிறது. போக்குவரத்து & சேமிப்பு செலவுகளுக்குப் பின் நிகர வருவாயை கணக்கிடுகிறது."),
    "feat_advice_title": ("💡 Smart Advice", "💡 புத்திசாலி ஆலோசனை"),
    "feat_advice_desc": ("SELL NOW / WAIT / TRY ANOTHER MARKET — personalized to your quantity, costs, and storage situation.", "இப்போது விற்கவும் / காத்திருக்கவும் / வேறு சந்தை — உங்கள் அளவு, செலவு, சேமிப்பு நிலைக்கு ஏற்ப."),
    "feat_risk_title": ("⚖️ Risk Analysis", "⚖️ ஆபத்து பகுப்பாய்வு"),
    "feat_risk_desc": ('"What if I wait?" analysis with price volatility risk. Transparent estimates with explanations.', '"நான் காத்திருந்தால்?" பகுப்பாய்வு. விலை ஏற்ற இறக்க ஆபத்து. விளக்கத்துடன் மதிப்பீடுகள்.'),
    "how_it_works": ("How It Works", "இது எப்படி வேலை செய்கிறது"),
    "step1_title": ("Enter Details", "விவரங்களை உள்ளிடுங்கள்"),
    "step1_desc": ("Crop, quantity, market & costs", "பயிர், அளவு, சந்தை & செலவுகள்"),
    "step2_title": ("View Forecast", "முன்னறிவிப்பை பாருங்கள்"),
    "step2_desc": ("AI predictions with charts", "AI கணிப்புகள் வரைபடங்களுடன்"),
    "step3_title": ("Compare Markets", "சந்தைகளை ஒப்பிடுங்கள்"),
    "step3_desc": ("Best market by net revenue", "நிகர வருவாயின்படி சிறந்த சந்தை"),
    "step4_title": ("Get Advice", "ஆலோசனை பெறுங்கள்"),
    "step4_desc": ("SELL / WAIT / TRY decision", "விற்க / காத்திருக்க / முயற்சிக்க முடிவு"),
    "start_prompt": ("👉 **Start here:** Go to **Farmer Input** from the sidebar to enter your details.", "👉 **இங்கே தொடங்குங்கள்:** பக்கப்பட்டியில் **விவசாயி தகவல்** பக்கத்திற்கு செல்லுங்கள்."),

    # FARMER INPUT PAGE
    "farmer_input_title": ("Farmer Input", "விவசாயி தகவல்"),
    "farmer_input_subtitle": ("Enter your details to get a personalized selling recommendation.", "தனிப்பயன் விற்பனை பரிந்துரை பெற உங்கள் விவரங்களை உள்ளிடுங்கள்."),
    "crop_market_section": ("Crop & Market", "பயிர் & சந்தை"),
    "storage_transport_section": ("Storage & Transport", "சேமிப்பு & போக்குவரத்து"),
    "crop": ("Crop", "பயிர்"),
    "market": ("Market", "சந்தை"),
    "quantity_kg": ("Quantity (kg)", "அளவு (கிலோ)"),
    "quantity_help": ("Total quantity you want to sell in kilograms", "நீங்கள் விற்க விரும்பும் மொத்த அளவு (கிலோகிராம்)"),
    "storage_available": ("Storage Available?", "சேமிப்பு வசதி உள்ளதா?"),
    "yes": ("Yes", "ஆம்"),
    "no": ("No", "இல்லை"),
    "storage_cost": ("Storage Cost (Rs/Quintal/Day)", "சேமிப்பு செலவு (ரூ/குவிண்டால்/நாள்)"),
    "storage_cost_help": ("Daily storage cost per quintal", "ஒரு குவிண்டாலுக்கு தினசரி சேமிப்பு செலவு"),
    "no_storage_note": ("No storage cost — selling immediately.", "சேமிப்பு செலவு இல்லை — உடனடியாக விற்பனை."),
    "transport_cost": ("Transport Cost (Rs/km/Quintal)", "போக்குவரத்து செலவு (ரூ/கி.மீ/குவிண்டால்)"),
    "transport_cost_help": ("Transport cost per kilometer per quintal", "ஒரு குவிண்டாலுக்கு கி.மீ-க்கு போக்குவரத்து செலவு"),
    "max_distance": ("Maximum Travel Distance (km)", "அதிகபட்ச பயண தூரம் (கி.மீ)"),
    "max_distance_help": ("Maximum distance you're willing to transport", "நீங்கள் கொண்டு செல்ல தயாராக உள்ள அதிகபட்ச தூரம்"),
    "analyze_button": ("🔍 Analyze Best Selling Option", "🔍 சிறந்த விற்பனை விருப்பத்தை பகுப்பாய்வு செய்"),
    "input_saved": ("✅ **Input saved successfully!**", "✅ **தகவல் வெற்றிகரமாக சேமிக்கப்பட்டது!**"),
    "input_summary": ("Your Input Summary", "உங்கள் தகவல் சுருக்கம்"),
    "navigate_prompt": ("👉 Now navigate to **Price Forecast**, **Market Comparison**, or **AI Recommendation** from the sidebar.", "👉 இப்போது பக்கப்பட்டியில் **விலை முன்னறிவிப்பு**, **சந்தை ஒப்பீடு**, அல்லது **AI பரிந்துரை** பக்கத்திற்கு செல்லுங்கள்."),
    "storage_yes": ("✅ Available", "✅ கிடைக்கும்"),
    "storage_no": ("❌ No", "❌ இல்லை"),
    "error_quantity": ("❌ Quantity must be greater than 0.", "❌ அளவு 0-ஐ விட அதிகமாக இருக்க வேண்டும்."),
    "error_cost_negative": ("❌ Costs cannot be negative.", "❌ செலவுகள் எதிர்மறையாக இருக்க முடியாது."),

    # PRICE FORECAST PAGE
    "forecast_title": ("Price Forecast", "விலை முன்னறிவிப்பு"),
    "forecast_subtitle": ("AI-powered price predictions for your selected crop and market.", "நீங்கள் தேர்ந்தெடுத்த பயிர் மற்றும் சந்தைக்கான AI விலை கணிப்புகள்."),
    "trend": ("Trend", "போக்கு"),
    "increasing": ("Increasing", "அதிகரிக்கிறது"),
    "decreasing": ("Decreasing", "குறைகிறது"),
    "stable": ("Stable", "நிலையானது"),
    "current_price": ("Current Price", "தற்போதைய விலை"),
    "tomorrow": ("Tomorrow", "நாளை"),
    "in_3_days": ("In 3 Days", "3 நாட்களில்"),
    "in_7_days": ("In 7 Days", "7 நாட்களில்"),
    "history_forecast_chart": ("Historical Prices + AI Forecast", "வரலாற்று விலைகள் + AI முன்னறிவிப்பு"),
    "historical": ("Historical", "வரலாறு"),
    "ai_forecast": ("AI Forecast", "AI முன்னறிவிப்பு"),
    "confidence_range": ("±5% Range", "±5% வரம்பு"),
    "forecast_summary": ("Forecast Summary", "முன்னறிவிப்பு சுருக்கம்"),
    "horizon": ("Horizon", "காலம்"),
    "predicted_price": ("Predicted Price", "கணிக்கப்பட்ட விலை"),
    "change": ("Change", "மாற்றம்"),
    "pct_change": ("% Change", "% மாற்றம்"),
    "prediction_warning": ("⚠️ Predictions are statistical estimates. Actual market prices may differ.", "⚠️ கணிப்புகள் புள்ளிவிவர மதிப்பீடுகள். உண்மையான சந்தை விலைகள் வேறுபடலாம்."),
    "price_rs_q": ("Price (Rs/Quintal)", "விலை (ரூ/குவிண்டால்)"),
    "date_label": ("Date", "தேதி"),

    # MARKET COMPARISON PAGE
    "mkt_title": ("Market Comparison", "சந்தை ஒப்பீடு"),
    "mkt_subtitle": ("Compare **net revenue** across markets — highest price ≠ best market.", "சந்தைகள் முழுவதும் **நிகர வருவாயை** ஒப்பிடுங்கள் — அதிக விலை ≠ சிறந்த சந்தை."),
    "recommended": ("Recommended", "பரிந்துரைக்கப்பட்டது"),
    "est_net_revenue": ("Estimated Net Revenue", "மதிப்பிடப்பட்ட நிகர வருவாய்"),
    "detailed_comparison": ("Detailed Comparison", "விரிவான ஒப்பீடு"),
    "location": ("Location", "இடம்"),
    "distance_km": ("Distance (km)", "தூரம் (கி.மீ)"),
    "transport_cost_col": ("Transport Cost (₹)", "போக்குவரத்து செலவு (₹)"),
    "gross_revenue": ("Gross Revenue (₹)", "மொத்த வருவாய் (₹)"),
    "net_revenue": ("Net Revenue (₹)", "நிகர வருவாய் (₹)"),
    "net_revenue_comparison": ("Net Revenue Comparison", "நிகர வருவாய் ஒப்பீடு"),
    "revenue_vs_costs": ("Revenue vs Costs Breakdown", "வருவாய் vs செலவு விவரம்"),
    "key_insight_text": ("Transport costs can significantly reduce your profit. A market with a slightly lower price but closer to you may give better net revenue.", "போக்குவரத்து செலவுகள் உங்கள் லாபத்தை கணிசமாக குறைக்கலாம். சற்று குறைந்த விலை ஆனால் அருகில் உள்ள சந்தை சிறந்த நிகர வருவாயை தரலாம்."),
    "current_market_best": ("Your current market is already the best option!", "உங்கள் தற்போதைய சந்தை ஏற்கனவே சிறந்த தேர்வு!"),

    # AI RECOMMENDATION PAGE
    "ai_rec_title": ("AI Recommendation", "AI பரிந்துரை"),
    "ai_rec_subtitle": ("Your personalized selling recommendation based on AI analysis.", "AI பகுப்பாய்வின் அடிப்படையில் உங்கள் தனிப்பயன் விற்பனை பரிந்துரை."),
    "sell_now": ("SELL NOW", "இப்போது விற்கவும்"),
    "wait": ("WAIT", "காத்திருக்கவும்"),
    "try_another_market": ("TRY ANOTHER MARKET", "வேறு சந்தையை முயற்சிக்கவும்"),
    "sell_now_desc": ("Current conditions favor immediate selling.", "தற்போதைய நிலைமைகள் உடனடி விற்பனைக்கு சாதகம்."),
    "wait_desc": ("Prices are expected to rise enough to cover storage costs.", "சேமிப்பு செலவை ஈடுகட்ட போதுமான அளவு விலை உயரும் என எதிர்பார்க்கப்படுகிறது."),
    "try_market_desc": ("A nearby market offers significantly better net revenue.", "அருகிலுள்ள சந்தை கணிசமாக சிறந்த நிகர வருவாயை வழங்குகிறது."),
    "revenue_sell_today": ("Revenue (Sell Today)", "வருவாய் (இன்று விற்றால்)"),
    "best_future_revenue": ("Best Future Revenue", "சிறந்த எதிர்கால வருவாய்"),
    "benefit_waiting": ("Benefit of Waiting", "காத்திருப்பின் பலன்"),
    "positive": ("Positive", "நேர்மறை"),
    "negative": ("Negative", "எதிர்மறை"),
    "risk_level": ("Risk Level", "ஆபத்து நிலை"),
    "low_risk": ("LOW RISK", "குறைந்த ஆபத்து"),
    "moderate_risk": ("MODERATE RISK", "மிதமான ஆபத்து"),
    "high_risk": ("HIGH RISK", "அதிக ஆபத்து"),
    "why_recommendation": ("Why this recommendation?", "ஏன் இந்த பரிந்துரை?"),
    "what_if_wait": ("What if I wait?", "நான் காத்திருந்தால் என்ன?"),
    "option": ("Option", "விருப்பம்"),
    "estimated_revenue": ("Estimated Revenue", "மதிப்பிடப்பட்ட வருவாய்"),
    "sell_today": ("Sell Today", "இன்று விற்கவும்"),
    "wait_1_day": ("Wait 1 Day", "1 நாள் காத்திருக்கவும்"),
    "wait_3_days": ("Wait 3 Days", "3 நாட்கள் காத்திருக்கவும்"),
    "wait_7_days": ("Wait 7 Days", "7 நாட்கள் காத்திருக்கவும்"),
    "best_selling_window": ("Estimated Best Selling Window", "மதிப்பிடப்பட்ட சிறந்த விற்பனை நேரம்"),
    "risk_assessment": ("Risk Assessment", "ஆபத்து மதிப்பீடு"),
    "risk_factors": ("Risk Factors", "ஆபத்து காரணிகள்"),
    "score": ("Score", "மதிப்பெண்"),

    # COMMON / SHARED
    "no_data": ("No data available for the selected combination.", "தேர்ந்தெடுக்கப்பட்ட கலவைக்கு தரவு கிடைக்கவில்லை."),
    "fill_input_first": ("⚠️ Please fill in the **Farmer Input** page first.", "⚠️ முதலில் **விவசாயி தகவல்** பக்கத்தை நிரப்பவும்."),
    "no_data_error": ("No data available. Please ensure demo_prices.csv exists.", "தரவு கிடைக்கவில்லை. demo_prices.csv கோப்பு உள்ளதா உறுதிப்படுத்தவும்."),
    "insufficient_data": ("Could not generate predictions. Insufficient data.", "கணிப்புகளை உருவாக்க முடியவில்லை. போதுமான தரவு இல்லை."),
    "disclaimer": (
        "All forecasts, recommendations, and revenue estimates shown by this system are based on historical data patterns and statistical models. They are estimates only and should not be treated as guaranteed outcomes. Real-world market conditions may differ significantly.",
        "இந்த அமைப்பு காட்டும் அனைத்து முன்னறிவிப்புகள், பரிந்துரைகள் மற்றும் வருவாய் மதிப்பீடுகள் வரலாற்று தரவு மற்றும் புள்ளிவிவர மாதிரிகளின் அடிப்படையில் உள்ளன. இவை மதிப்பீடுகள் மட்டுமே, உத்தரவாதமான முடிவுகளாக கருதக்கூடாது."
    ),
    "disclaimer_footer": (
        "This tool assists decision-making but does not replace professional agricultural advisory services.",
        "இந்த கருவி முடிவெடுப்பதற்கு உதவுகிறது, ஆனால் தொழில்முறை விவசாய ஆலோசனை சேவைகளை மாற்றாது."
    ),
    "estimates_note": ("All values are estimates based on predicted prices and user-provided costs.", "அனைத்து மதிப்புகளும் கணிக்கப்பட்ட விலைகள் மற்றும் பயனர் வழங்கிய செலவுகளின் அடிப்படையில் மதிப்பீடுகள்."),
    "filter": ("Filter", "வடிகட்டி"),
    "quintal": ("Quintal", "குவிண்டால்"),
    "kg": ("kg", "கிலோ"),
}

# =============================================================================
# CROP NAME TRANSLATIONS
# =============================================================================

_CROPS = {
    "Bajra": ("Bajra", "கம்பு"),
    "Barley": ("Barley", "பார்லி"),
    "Jowar": ("Jowar", "சோளம்"),
    "Maize": ("Maize", "மக்காச்சோளம்"),
    "Paddy": ("Paddy", "நெல்"),
    "Ragi": ("Ragi", "கேழ்வரகு"),
    "Wheat": ("Wheat", "கோதுமை"),
    "Cotton": ("Cotton", "பருத்தி"),
    "Copra": ("Copra", "கொப்பரை"),
    "Groundnut": ("Groundnut", "நிலக்கடலை"),
    "Mustard": ("Mustard", "கடுகு"),
    "Niger Seed": ("Niger Seed", "உச்சிலு"),
    "Safflower": ("Safflower", "குசும்பா"),
    "Sesamum": ("Sesamum", "எள்"),
    "Soyabean": ("Soyabean", "சோயாபீன்"),
    "Sunflower": ("Sunflower", "சூரியகாந்தி"),
    "Bengal Gram": ("Bengal Gram", "கடலை பருப்பு"),
    "Black Gram": ("Black Gram", "உளுந்து"),
    "Green Gram": ("Green Gram", "பயறு"),
    "Lentil": ("Lentil", "மசூர் பருப்பு"),
    "Red Gram": ("Red Gram", "துவரை"),
    "Onion": ("Onion", "வெங்காயம்"),
    "Potato": ("Potato", "உருளைக்கிழங்கு"),
    "Tomato": ("Tomato", "தக்காளி"),
}

# =============================================================================
# CATEGORY TRANSLATIONS
# =============================================================================

_CATEGORIES = {
    "Cereals": ("Cereals", "தானியங்கள்"),
    "Fibre Crops": ("Fibre Crops", "நார் பயிர்கள்"),
    "Oil Seeds": ("Oil Seeds", "எண்ணெய் வித்துக்கள்"),
    "Pulses": ("Pulses", "பருப்பு வகைகள்"),
    "Vegetables": ("Vegetables", "காய்கறிகள்"),
}

# =============================================================================
# MARKET TRANSLATIONS
# =============================================================================

_MARKETS = {
    "Koyambedu": ("Koyambedu", "கோயம்பேடு"),
    "Azadpur": ("Azadpur", "ஆசாத்பூர்"),
    "Vashi": ("Vashi", "வாசி"),
    "Bowenpally": ("Bowenpally", "போவன்பள்ளி"),
    "Yeshwanthpur": ("Yeshwanthpur", "யேஷ்வந்தபூர்"),
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def t(key, lang="en"):
    """Get translated UI text. Returns English if key not found."""
    entry = _T.get(key)
    if entry is None:
        return key
    return entry[1] if lang == "ta" else entry[0]


def t_crop(name, lang="en"):
    """Translate crop name."""
    entry = _CROPS.get(name)
    if entry is None:
        return name
    return entry[1] if lang == "ta" else entry[0]


def t_category(name, lang="en"):
    """Translate category name."""
    entry = _CATEGORIES.get(name)
    if entry is None:
        return name
    return entry[1] if lang == "ta" else entry[0]


def t_market(name, lang="en"):
    """Translate market name."""
    entry = _MARKETS.get(name)
    if entry is None:
        return name
    return entry[1] if lang == "ta" else entry[0]


# Legacy compat
def get_text(key, lang="en"):
    return t(key, lang)
