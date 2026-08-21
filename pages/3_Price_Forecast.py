"""Page 3: Price Forecast — fully localized."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import APP_NAME, CROP_DETAILS
from utils.translations import t, t_crop, t_market
from src.data_fetcher import DataFetcher
from src.data_cleaner import DataCleaner
from src.predictor import PricePredictor

st.set_page_config(page_title=APP_NAME, page_icon="📈", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&display=swap');
*{font-family:'Noto Sans Tamil','Latha',sans-serif;}
.block-container{padding-top:1.5rem;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a472a 0%,#2d5a3f 100%);}
[data-testid="stSidebar"] *{color:white !important;}
.forecast-card{background:white;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.05);}
.forecast-label{color:#718096;font-size:0.85rem;}.forecast-value{font-size:1.6rem;font-weight:800;color:#1a472a;}
.forecast-delta-up{color:#28a745;font-size:0.9rem;font-weight:600;}
.forecast-delta-down{color:#dc3545;font-size:0.9rem;font-weight:600;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

L = st.session_state.get('lang', 'en')
st.markdown(f"## 📈 {t('forecast_title', L)}")
st.markdown(t("forecast_subtitle", L))

if 'farmer_input' not in st.session_state:
    st.warning(t("fill_input_first", L)); st.stop()

inputs = st.session_state['farmer_input']
crop, market = inputs['crop'], inputs['market']
st.markdown(f"**{CROP_DETAILS[crop]['icon']} {t_crop(crop,L)}** — **{t_market(market,L)}** ({inputs['quantity_kg']} {t('kg',L)})")
st.markdown("---")

@st.cache_data(ttl=300)
def get_preds(crop, market):
    fetcher = DataFetcher(); cleaner = DataCleaner()
    df = fetcher.get_data(crop=crop, market=market)
    if df is None or df.empty: return None, None
    df = cleaner.clean(df); df['date'] = pd.to_datetime(df['date']); df = df.sort_values('date')
    predictor = PricePredictor()
    return (predictor.predict(crop, market, df) if predictor.is_ready() else predictor._fallback_prediction(df)), df

prediction_result, _ = get_preds(crop, market)
if prediction_result is None:
    st.error(t("insufficient_data", L)); st.stop()

current_price = prediction_result['current_price']
predictions = prediction_result['predictions']
trend = prediction_result['trend']
st.session_state['prediction_result'] = prediction_result

trend_map = {"increasing": ("📈", t("increasing",L), "#28a745"),
             "decreasing": ("📉", t("decreasing",L), "#dc3545"),
             "stable": ("➡️", t("stable",L), "#718096")}
te, tt, tc = trend_map.get(trend, ("➡️", t("stable",L), "#718096"))
st.markdown(f"**{t('trend',L)}:** {te} <span style='color:{tc};font-weight:600'>{tt}</span>", unsafe_allow_html=True)
st.markdown("")

# Price cards
c1, c2, c3, c4 = st.columns(4)
def pcard(label, price, delta, col):
    cls = "forecast-delta-up" if delta >= 0 else "forecast-delta-down"
    arr = "▲" if delta >= 0 else "▼"
    with col:
        st.markdown(f'<div class="forecast-card"><div class="forecast-label">{label}</div><div class="forecast-value">₹{price:,.0f}</div><div class="{cls}">{arr} ₹{abs(delta):.0f} ({delta/current_price*100:+.1f}%)</div></div>', unsafe_allow_html=True)

pcard(t("current_price",L), current_price, 0, c1)
pcard(t("tomorrow",L), predictions['1d'], predictions['1d']-current_price, c2)
pcard(t("in_3_days",L), predictions['3d'], predictions['3d']-current_price, c3)
pcard(t("in_7_days",L), predictions['7d'], predictions['7d']-current_price, c4)
st.markdown(""); st.markdown("---")

# Chart
st.markdown(f"### 📊 {t('history_forecast_chart', L)}")
hist_prices = prediction_result['historical_prices']
hist_dates = prediction_result['dates']
last_d = pd.to_datetime(hist_dates[-1])
fc_dates = [(last_d+pd.Timedelta(days=d)).strftime('%Y-%m-%d') for d in [1,3,7]]
fc_prices = [predictions['1d'], predictions['3d'], predictions['7d']]

fig = go.Figure()
fig.add_trace(go.Scatter(x=hist_dates, y=hist_prices, mode='lines', name=t('historical',L),
    line=dict(color='#2d7a4f',width=2.5), fill='tozeroy', fillcolor='rgba(45,122,79,0.05)'))
fig.add_trace(go.Scatter(x=[hist_dates[-1]]+fc_dates, y=[hist_prices[-1]]+fc_prices, mode='lines+markers',
    name=t('ai_forecast',L), line=dict(color='#3182ce',width=3,dash='dash'), marker=dict(size=10,symbol='diamond',color='#3182ce')))
upper=[p*1.05 for p in fc_prices]; lower=[p*0.95 for p in fc_prices]
fig.add_trace(go.Scatter(x=fc_dates+fc_dates[::-1], y=upper+lower[::-1], fill='toself',
    fillcolor='rgba(49,130,206,0.1)', line=dict(color='rgba(0,0,0,0)'), name=t('confidence_range',L)))
fig.add_hline(y=current_price, line_dash="dot", line_color="#e53e3e",
    annotation_text=f"{t('current_price',L)}: ₹{current_price:,.0f}")
fig.update_layout(yaxis_title=t("price_rs_q",L), xaxis_title=t("date_label",L),
    template='plotly_white', height=420, margin=dict(l=50,r=20,t=30,b=50),
    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1), hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

# Summary table
st.markdown(f"### 📋 {t('forecast_summary', L)}")
tom_lbl = t("tomorrow",L); d3=t("in_3_days",L); d7=t("in_7_days",L)
sdf = pd.DataFrame({
    t("horizon",L): [tom_lbl, d3, d7],
    t("predicted_price",L): [f"₹{predictions['1d']:,.0f}", f"₹{predictions['3d']:,.0f}", f"₹{predictions['7d']:,.0f}"],
    t("change",L): [f"₹{predictions['1d']-current_price:+,.0f}", f"₹{predictions['3d']-current_price:+,.0f}", f"₹{predictions['7d']-current_price:+,.0f}"],
    t("pct_change",L): [f"{(predictions['1d']-current_price)/current_price*100:+.2f}%",
        f"{(predictions['3d']-current_price)/current_price*100:+.2f}%",
        f"{(predictions['7d']-current_price)/current_price*100:+.2f}%"]
})
st.dataframe(sdf, use_container_width=True, hide_index=True)
conf = prediction_result['confidence']*100
note = t("forecast_summary",L)
st.caption(f"🤖 Random Forest | {t('trend',L)}: {tt} | {conf:.0f}%")
st.markdown(f'<div style="background:#fffbeb;border:1px solid #f6e05e;border-radius:8px;padding:0.8rem;font-size:0.82rem;color:#744210;margin-top:1rem;">{t("prediction_warning",L)}</div>', unsafe_allow_html=True)
