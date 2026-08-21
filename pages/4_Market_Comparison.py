"""Page 4: Market Comparison — fully localized."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import APP_NAME, MARKETS, MARKET_DETAILS, CROP_DETAILS
from utils.translations import t, t_crop, t_market
from src.data_fetcher import DataFetcher
from src.data_cleaner import DataCleaner
from src.predictor import PricePredictor
from src.market_comparison import MarketComparison

st.set_page_config(page_title=APP_NAME, page_icon="🏪", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&display=swap');
*{font-family:'Noto Sans Tamil','Latha',sans-serif;}
.block-container{padding-top:1.5rem;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a472a 0%,#2d5a3f 100%);}
[data-testid="stSidebar"] *{color:white !important;}
.best-market-card{background:linear-gradient(135deg,#1a472a,#2d7a4f);border-radius:14px;padding:1.5rem 2rem;text-align:center;color:white;box-shadow:0 6px 20px rgba(26,71,42,0.3);margin:1rem 0;}
.best-market-card h3{color:white;margin:0;}.best-market-card p{color:#c6f6d5;margin:0.3rem 0 0 0;font-size:1.1rem;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

L = st.session_state.get('lang', 'en')
st.markdown(f"## 🏪 {t('mkt_title', L)}")
st.markdown(t("mkt_subtitle", L))

if 'farmer_input' not in st.session_state:
    st.warning(t("fill_input_first", L)); st.stop()

inputs = st.session_state['farmer_input']
crop = inputs['crop']; current_market = inputs['market']
quantity_kg = inputs['quantity_kg']; transport_cost_per_km = inputs['transport_cost']
max_distance = inputs['max_distance']; storage_cost = inputs['storage_cost']

st.markdown(f"**{CROP_DETAILS[crop]['icon']} {t_crop(crop,L)}** | **{quantity_kg} {t('kg',L)}** | {t('market',L)}: **{t_market(current_market,L)}**")
st.markdown("---")

@st.cache_data(ttl=300)
def get_mkt_preds(crop):
    fetcher=DataFetcher(); cleaner=DataCleaner(); predictor=PricePredictor(); preds={}
    for mkt in MARKETS:
        df=fetcher.get_data(crop=crop,market=mkt)
        if df is None or df.empty: continue
        df=cleaner.clean(df); df['date']=pd.to_datetime(df['date']); df=df.sort_values('date')
        r=predictor.predict(crop,mkt,df) if predictor.is_ready() else predictor._fallback_prediction(df)
        if r: preds[mkt]=r['predictions']['1d']
    return preds

predictions_by_market = get_mkt_preds(crop)
if not predictions_by_market:
    st.error(t("no_data", L)); st.stop()

comparator = MarketComparison()
comparison = comparator.compare_markets(crop=crop, current_market=current_market, quantity_kg=quantity_kg,
    predictions_by_market=predictions_by_market, transport_cost_per_km=transport_cost_per_km,
    max_distance=max_distance, storage_cost_per_day=storage_cost, wait_days=0)
st.session_state['market_comparison'] = comparison
st.session_state['predictions_by_market'] = predictions_by_market
markets_data = comparison['markets']; summary = comparison['summary']

# Best market card
if markets_data:
    best = markets_data[0]
    st.markdown(f'<div class="best-market-card"><h3>⭐ {t("recommended",L)}: {t_market(best["market"],L)}</h3><p>{t("est_net_revenue",L)}: <strong>₹{best["net_revenue"]:,.0f}</strong></p></div>', unsafe_allow_html=True)
    if summary.get('should_switch'):
        adv = summary['advantage']; pct = summary['advantage_pct']
        from_m = t_market(summary['current_market_name'], L)
        to_m = t_market(summary['best_market_name'], L)
        if L == "en":
            st.info(f"💡 Switching from **{from_m}** to **{to_m}** could earn you **₹{adv:,.0f}** more ({pct:.1f}% increase).")
        else:
            st.info(f"💡 **{from_m}** இலிருந்து **{to_m}** க்கு மாறுவது உங்களுக்கு **₹{adv:,.0f}** அதிகம் கிடைக்கும் ({pct:.1f}% அதிகரிப்பு).")
    else:
        st.success(f"✅ {t('current_market_best', L)}")

st.markdown("---")
st.markdown(f"### 📊 {t('detailed_comparison', L)}")

if markets_data:
    tbl = []
    for m in markets_data:
        tag = " ⭐" if m['recommended'] else ""
        tbl.append({
            t("market",L): f"{t_market(m['market'],L)}{tag}",
            t("location",L): f"{m['district']}, {m['state']}",
            t("predicted_price",L): f"₹{m['predicted_price']:,.0f}",
            t("distance_km",L): m['distance_km'],
            t("transport_cost_col",L): f"₹{m['transport_cost']:,.0f}",
            t("gross_revenue",L): f"₹{m['gross_revenue']:,.0f}",
            t("net_revenue",L): f"₹{m['net_revenue']:,.0f}",
        })
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

st.markdown("---")
c1, c2 = st.columns(2)
mkt_names = [t_market(m['market'], L) for m in markets_data]
net_revs = [m['net_revenue'] for m in markets_data]
colors = ['#2d7a4f' if m['recommended'] else '#a0aec0' for m in markets_data]

with c1:
    st.markdown(f"#### 💰 {t('net_revenue_comparison', L)}")
    fig1 = go.Figure(data=[go.Bar(x=mkt_names, y=net_revs, marker_color=colors,
        text=[f"₹{r:,.0f}" for r in net_revs], textposition='outside')])
    fig1.update_layout(yaxis_title=t("net_revenue",L), template='plotly_white', height=320, margin=dict(l=40,r=20,t=20,b=40))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown(f"#### 📊 {t('revenue_vs_costs', L)}")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name=t("net_revenue",L), x=mkt_names, y=[m['net_revenue'] for m in markets_data], marker_color='#2d7a4f'))
    fig2.add_trace(go.Bar(name=t("transport_cost_col",L), x=mkt_names, y=[m['transport_cost'] for m in markets_data], marker_color='#e53e3e'))
    fig2.update_layout(barmode='group', template='plotly_white', height=320, margin=dict(l=40,r=20,t=20,b=40),
        legend=dict(orientation="h",yanchor="bottom",y=1.02))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"> 💡 {t('key_insight_text', L)}")
st.markdown(f'<div style="background:#fffbeb;border:1px solid #f6e05e;border-radius:8px;padding:0.8rem;font-size:0.82rem;color:#744210;margin-top:1rem;">⚠️ {t("estimates_note",L)}</div>', unsafe_allow_html=True)
