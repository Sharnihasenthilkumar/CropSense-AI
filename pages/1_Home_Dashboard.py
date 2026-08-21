"""Page 1: Home Dashboard — fully localized."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import APP_NAME, CROPS, MARKETS, CROP_DETAILS, CROP_CATEGORIES, CROPS_PER_PAGE
from utils.translations import t, t_crop, t_category, t_market
from src.data_fetcher import DataFetcher
from src.data_cleaner import DataCleaner

st.set_page_config(page_title=APP_NAME, page_icon="🏠", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&display=swap');
*{font-family:'Noto Sans Tamil','Latha',sans-serif;}
.block-container{padding-top:1.5rem;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a472a 0%,#2d5a3f 100%);}
[data-testid="stSidebar"] *{color:white !important;}
.stat-card{background:white;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.05);}
.stat-value{font-size:1.8rem;font-weight:800;color:#1a472a;}
.stat-label{color:#718096;font-size:0.85rem;margin-top:0.2rem;}
.crop-card{background:white;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.05);min-height:150px;}
.crop-icon{font-size:2.2rem;}.crop-name{font-size:1rem;font-weight:700;color:#1a472a;margin:0.3rem 0;}
.crop-price{font-size:1.3rem;font-weight:800;color:#2d7a4f;}
.crop-change-up{color:#28a745;font-size:0.8rem;font-weight:600;}
.crop-change-down{color:#dc3545;font-size:0.8rem;font-weight:600;}
.crop-category{color:#718096;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.5px;}
.page-nav{text-align:center;color:#718096;font-size:0.9rem;margin:1rem 0;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

L = st.session_state.get('lang', 'en')

st.markdown(f"## 🏠 {t('dashboard_title', L)}")
st.markdown(t("dashboard_subtitle", L))
st.markdown("---")

@st.cache_data(ttl=300)
def load_data():
    fetcher = DataFetcher()
    cleaner = DataCleaner()
    df = fetcher.get_data()
    if df is not None:
        df = cleaner.clean(df)
        df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()
if df is None or df.empty:
    st.error(t("no_data_error", L)); st.stop()

latest_date = df['date'].max()
prev_date = df[df['date'] < latest_date]['date'].max()

# Stats row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-value">{len(df):,}</div><div class="stat-label">{t("total_records",L)}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-value">{df["crop"].nunique()}</div><div class="stat-label">{t("crops_tracked",L)}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-value">{df["market"].nunique()}</div><div class="stat-label">{t("markets_count",L)}</div></div>', unsafe_allow_html=True)
with c4:
    days = (df['date'].max() - df['date'].min()).days
    st.markdown(f'<div class="stat-card"><div class="stat-value">{days}</div><div class="stat-label">{t("days_of_data",L)}</div></div>', unsafe_allow_html=True)

st.markdown("")

# Price metrics
st.markdown(f"### 📈 {t('latest_prices_header', L)}")
st.caption(f"{latest_date.strftime('%d %B %Y')}")
cols = st.columns(3)
for idx, crop in enumerate(["Tomato", "Onion", "Paddy"]):
    with cols[idx]:
        cl = df[(df['crop'] == crop) & (df['date'] == latest_date)]
        cp = df[(df['crop'] == crop) & (df['date'] == prev_date)]
        avg = cl['modal_price'].mean() if not cl.empty else 0
        prev_avg = cp['modal_price'].mean() if not cp.empty else avg
        delta = avg - prev_avg
        st.metric(f"{CROP_DETAILS[crop]['icon']} {t_crop(crop, L)}", f"₹{avg:,.0f}", f"₹{delta:+,.0f} {t('vs_yesterday',L)}")

st.markdown("---")

# Full price table
st.markdown(f"### 🏪 {t('price_by_market_all', L)}")
latest_all = df[df['date'] == latest_date][['crop', 'market', 'modal_price']].copy()
pivot = latest_all.pivot_table(values='modal_price', index='crop', columns='market', aggfunc='mean')
if not pivot.empty:
    # Translate index and columns
    pivot.index = [t_crop(c, L) for c in pivot.index]
    pivot.columns = [t_market(m, L) for m in pivot.columns]
    pivot = pivot.round(0).astype(int)
    def hl(s):
        is_max = s == s.max()
        return ['background-color:#c6f6d5;font-weight:bold' if v else '' for v in is_max]
    st.dataframe(pivot.style.apply(hl, axis=1).format("₹{:,}"), use_container_width=True, height=400)
    st.caption(t("green_highest", L))

st.markdown("---")

# Trend chart
st.markdown(f"### 📈 {t('30_day_trend', L)}")
sel_crop = st.selectbox(t("select_crop_trend", L), CROPS, index=CROPS.index("Tomato"),
                        format_func=lambda x: t_crop(x, L))
trend_df = df[df['crop'] == sel_crop].groupby('date')['modal_price'].mean().reset_index().sort_values('date').tail(30)
fig = go.Figure()
fig.add_trace(go.Scatter(x=trend_df['date'], y=trend_df['modal_price'], mode='lines+markers',
    line=dict(color='#2d7a4f', width=3), marker=dict(size=4), fill='tozeroy', fillcolor='rgba(45,122,79,0.08)'))
fig.update_layout(yaxis_title=t("price_rs_q", L), xaxis_title=t("date_label", L),
    template='plotly_white', height=350, margin=dict(l=50,r=20,t=20,b=40), hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

st.markdown(f'<div style="background:#fffbeb;border:1px solid #f6e05e;border-radius:8px;padding:0.8rem;font-size:0.82rem;color:#744210;margin-top:1rem;">⚠️ {t("disclaimer",L)}</div>', unsafe_allow_html=True)
