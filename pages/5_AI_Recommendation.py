"""Page 5: AI Recommendation — fully localized."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import APP_NAME, CROP_DETAILS, MARKETS
from utils.translations import t, t_crop, t_market
from src.data_fetcher import DataFetcher
from src.data_cleaner import DataCleaner
from src.predictor import PricePredictor
from src.market_comparison import MarketComparison
from src.decision_engine import DecisionEngine
from src.risk_calculator import RiskCalculator

st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&display=swap');
*{font-family:'Noto Sans Tamil','Latha',sans-serif;}
.block-container{padding-top:1.5rem;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a472a 0%,#2d5a3f 100%);}
[data-testid="stSidebar"] *{color:white !important;}
.rec-card-sell{background:linear-gradient(135deg,#22543d,#38a169);border-radius:16px;padding:2.5rem;text-align:center;color:white;box-shadow:0 8px 30px rgba(34,84,61,0.3);margin:1rem 0 2rem 0;}
.rec-card-wait{background:linear-gradient(135deg,#744210,#d69e2e);border-radius:16px;padding:2.5rem;text-align:center;color:white;box-shadow:0 8px 30px rgba(116,66,16,0.3);margin:1rem 0 2rem 0;}
.rec-card-try{background:linear-gradient(135deg,#2a4365,#3182ce);border-radius:16px;padding:2.5rem;text-align:center;color:white;box-shadow:0 8px 30px rgba(42,67,101,0.3);margin:1rem 0 2rem 0;}
.rec-card-sell h2,.rec-card-wait h2,.rec-card-try h2{color:white;margin:0;font-size:2.2rem;}
.rec-card-sell p,.rec-card-wait p,.rec-card-try p{color:rgba(255,255,255,0.85);margin:0.5rem 0 0 0;font-size:1rem;}
.reason-item{background:#f7fafc;border-left:3px solid #2d7a4f;padding:0.7rem 1rem;margin:0.4rem 0;border-radius:4px;color:#2d3748;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

L = st.session_state.get('lang', 'en')
st.markdown(f"## 🤖 {t('ai_rec_title', L)}")
st.markdown(t("ai_rec_subtitle", L))

if 'farmer_input' not in st.session_state:
    st.warning(t("fill_input_first", L)); st.stop()

inputs = st.session_state['farmer_input']
crop=inputs['crop']; market=inputs['market']; quantity_kg=inputs['quantity_kg']
storage_available=inputs['storage_available']; storage_cost=inputs['storage_cost']
transport_cost_per_km=inputs['transport_cost']; max_distance=inputs['max_distance']

st.markdown(f"**{CROP_DETAILS[crop]['icon']} {t_crop(crop,L)}** | **{quantity_kg} {t('kg',L)}** | **{t_market(market,L)}**")
st.markdown("---")

@st.cache_data(ttl=300)
def gen_rec(crop, market, quantity_kg, storage_available, storage_cost, transport_cost_per_km, max_distance):
    fetcher=DataFetcher(); cleaner=DataCleaner(); predictor=PricePredictor()
    comparator=MarketComparison(); engine=DecisionEngine(); risk_calc=RiskCalculator()
    df=fetcher.get_data(crop=crop,market=market)
    if df is None or df.empty: return None
    df=cleaner.clean(df); df['date']=pd.to_datetime(df['date']); df=df.sort_values('date')
    pred_result=predictor.predict(crop,market,df) if predictor.is_ready() else predictor._fallback_prediction(df)
    if pred_result is None: return None
    preds_by_mkt={}
    for mkt in MARKETS:
        mdf=fetcher.get_data(crop=crop,market=mkt)
        if mdf is None or mdf.empty: continue
        mdf=cleaner.clean(mdf); mdf['date']=pd.to_datetime(mdf['date']); mdf=mdf.sort_values('date')
        r=predictor.predict(crop,mkt,mdf) if predictor.is_ready() else predictor._fallback_prediction(mdf)
        if r: preds_by_mkt[mkt]=r['predictions']['1d']
    comparison=comparator.compare_markets(crop=crop,current_market=market,quantity_kg=quantity_kg,
        predictions_by_market=preds_by_mkt,transport_cost_per_km=transport_cost_per_km,
        max_distance=max_distance,storage_cost_per_day=storage_cost,wait_days=0)
    recommendation=engine.get_recommendation(pred_result['current_price'],pred_result['predictions'],
        comparison,storage_available,storage_cost,quantity_kg)
    risk=risk_calc.calculate_risk(pred_result['historical_prices'],pred_result['predictions'])
    return {'prediction':pred_result,'comparison':comparison,'recommendation':recommendation,'risk':risk}

result = gen_rec(crop, market, quantity_kg, storage_available, storage_cost, transport_cost_per_km, max_distance)
if result is None:
    st.error(t("insufficient_data", L)); st.stop()

recommendation = result['recommendation']; risk = result['risk']

# Big card
rec_type = recommendation['recommendation']
card_map = {
    "SELL_NOW": ("rec-card-sell", "🟢", "sell_now", "sell_now_desc"),
    "WAIT": ("rec-card-wait", "🟡", "wait", "wait_desc"),
    "TRY_ANOTHER_MARKET": ("rec-card-try", "🔵", "try_another_market", "try_market_desc"),
}
card_cls, emoji, title_key, desc_key = card_map.get(rec_type, card_map["SELL_NOW"])
st.markdown(f'<div class="{card_cls}"><h2>{emoji} {t(title_key, L)}</h2><p>{t(desc_key, L)}</p></div>', unsafe_allow_html=True)

# Metrics
c1,c2,c3,c4 = st.columns(4)
with c1: st.metric(f"💰 {t('revenue_sell_today',L)}", f"₹{recommendation['current_revenue']:,.0f}")
with c2: st.metric(f"📈 {t('best_future_revenue',L)}", f"₹{recommendation['best_future_revenue']:,.0f}")
with c3:
    b=recommendation['wait_benefit']
    st.metric(f"💎 {t('benefit_waiting',L)}", f"₹{b:,.0f}", delta=t("positive",L) if b>0 else t("negative",L))
with c4:
    risk_colors={"LOW":"#c6f6d5","MODERATE":"#fefcbf","HIGH":"#fed7d7"}
    rlabel = {"LOW":t("low_risk",L),"MODERATE":t("moderate_risk",L),"HIGH":t("high_risk",L)}
    st.markdown(f'<div style="background:{risk_colors.get(risk["level"],"#f7fafc")};border-radius:10px;padding:1rem;text-align:center;"><div style="font-size:1.5rem;">{risk["emoji"]}</div><div style="font-weight:700;color:{risk["color"]};">{rlabel.get(risk["level"],risk["level"])}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Why
st.markdown(f"### 💡 {t('why_recommendation', L)}")
for reason in recommendation['reasons']:
    st.markdown(f'<div class="reason-item">{reason}</div>', unsafe_allow_html=True)

st.markdown("---")

# What if
st.markdown(f"### ⏳ {t('what_if_wait', L)}")
wif = recommendation['what_if']
c1, c2 = st.columns([2, 3])
with c1:
    wdf = pd.DataFrame({
        t("option",L): [t("sell_today",L), t("wait_1_day",L), t("wait_3_days",L), t("wait_7_days",L)],
        t("estimated_revenue",L): [f"₹{wif['sell_today']:,.0f}", f"₹{wif['wait_1_day']:,.0f}",
            f"₹{wif['wait_3_days']:,.0f}", f"₹{wif['wait_7_days']:,.0f}"]
    })
    st.dataframe(wdf, use_container_width=True, hide_index=True)
    bw = recommendation['best_selling_window']
    # Translate best window
    bw_map = {"Sell Today": t("sell_today",L), "Wait 1 Day": t("wait_1_day",L),
              "Wait 3 Days": t("wait_3_days",L), "Wait 7 Days": t("wait_7_days",L)}
    bw_t = bw_map.get(bw, bw)
    st.success(f"⭐ **{t('best_selling_window',L)}:** {bw_t}")

with c2:
    fig = go.Figure(data=[go.Bar(
        x=[t("sell_today",L), t("wait_1_day",L), t("wait_3_days",L), t("wait_7_days",L)],
        y=[wif['sell_today'], wif['wait_1_day'], wif['wait_3_days'], wif['wait_7_days']],
        marker_color=['#2d7a4f','#38a169','#d69e2e','#e53e3e'],
        text=[f"₹{v:,.0f}" for v in [wif['sell_today'],wif['wait_1_day'],wif['wait_3_days'],wif['wait_7_days']]],
        textposition='outside')])
    fig.update_layout(yaxis_title=t("estimated_revenue",L), template='plotly_white', height=300, margin=dict(l=40,r=20,t=20,b=40))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Risk
st.markdown(f"### {risk['emoji']} {t('risk_assessment', L)}")
rc1, rc2 = st.columns([1, 2])
with rc1:
    st.markdown(f'<div style="background:{risk_colors.get(risk["level"],"#f7fafc")};border:2px solid {risk["color"]};border-radius:14px;padding:2rem;text-align:center;"><div style="font-size:3rem;">{risk["emoji"]}</div><div style="font-size:1.3rem;font-weight:800;color:{risk["color"]};margin-top:0.5rem;">{rlabel.get(risk["level"],risk["level"])}</div><div style="color:#718096;margin-top:0.3rem;">{t("score",L)}: {risk["score"]:.0%}</div></div>', unsafe_allow_html=True)
with rc2:
    st.markdown(f"**{t('risk_factors', L)}:**")
    for f in risk['factors']:
        st.markdown(f"- {f}")

st.markdown("---")
st.markdown(f'<div style="background:#fffbeb;border:1px solid #f6e05e;border-radius:10px;padding:1.2rem;font-size:0.85rem;color:#744210;">⚠️ <strong>{"Disclaimer" if L=="en" else "பொறுப்புத் துறப்பு"}:</strong> {t("disclaimer",L)}<br><br>{t("disclaimer_footer",L)}</div>', unsafe_allow_html=True)
