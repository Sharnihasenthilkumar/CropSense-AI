"""
CropSmart AI - Main Application Entry Point
=============================================
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.constants import (
    APP_NAME, APP_TAGLINE, APP_VERSION, CROPS, MARKETS,
    CROP_DETAILS, CROP_CATEGORIES, DISCLAIMER, CROPS_PER_PAGE
)
from utils.translations import t, t_crop, t_category, t_market
from src.data_fetcher import DataFetcher
from src.data_cleaner import DataCleaner

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(page_title=APP_NAME, page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

# =============================================================================
# CSS (Tamil font support added)
# =============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&display=swap');
    
    * { font-family: 'Noto Sans Tamil', 'Latha', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a472a 0%, #2d5a3f 100%); }
    [data-testid="stSidebar"] * { color: white !important; }
    .hero-container {
        background: linear-gradient(135deg, #1a472a 0%, #2d7a4f 50%, #38a169 100%);
        border-radius: 16px; padding: 2.5rem 2rem; text-align: center;
        margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(26, 71, 42, 0.25);
    }
    .hero-title { color: white; font-size: 2.5rem; font-weight: 800; margin: 0; }
    .hero-tagline { color: #c6f6d5; font-size: 1.1rem; margin-top: 0.5rem; font-style: italic; }
    .hero-stat { color: white; font-size: 0.9rem; margin-top: 1rem; opacity: 0.85; }
    .crop-card {
        background: white; border-radius: 12px; padding: 1.2rem; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        min-height: 155px; transition: transform 0.2s;
    }
    .crop-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.1); }
    .crop-icon { font-size: 2rem; }
    .crop-name { font-size: 0.95rem; font-weight: 700; color: #1a472a; margin: 0.2rem 0; }
    .crop-price { font-size: 1.2rem; font-weight: 800; color: #2d7a4f; }
    .crop-change-up { color: #28a745; font-size: 0.8rem; font-weight: 600; }
    .crop-change-down { color: #dc3545; font-size: 0.8rem; font-weight: 600; }
    .crop-category { color: #a0aec0; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; }
    .feature-card {
        background: white; border-radius: 12px; padding: 1.3rem;
        border-left: 4px solid #2d7a4f; box-shadow: 0 2px 8px rgba(0,0,0,0.05); min-height: 160px;
    }
    .feature-card h4 { color: #1a472a; margin: 0 0 0.6rem 0; font-size: 1rem; }
    .feature-card p { color: #4a5568; margin: 0; font-size: 0.85rem; line-height: 1.5; }
    .step-card {
        background: #f0fff4; border-radius: 10px; padding: 1rem; text-align: center; border: 1px solid #c6f6d5;
    }
    .step-number {
        background: #2d7a4f; color: white; width: 32px; height: 32px; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1rem; margin-bottom: 0.4rem;
    }
    .step-text { color: #1a472a; font-size: 0.85rem; font-weight: 600; }
    .page-nav { text-align: center; color: #718096; font-size: 0.9rem; padding: 0.5rem 0; }
    .disclaimer-box {
        background: #fffbeb; border: 1px solid #f6e05e; border-radius: 10px;
        padding: 1rem 1.5rem; font-size: 0.82rem; color: #744210; margin-top: 2rem;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR (fully localized)
# =============================================================================

with st.sidebar:
    st.markdown("")
    st.markdown(f"### 🌾 {t('app_name')}")
    st.markdown(f"*{t('tagline')}*")
    st.markdown("---")

    lang = st.radio("🌐 Language / மொழி", ["English", "தமிழ் (Tamil)"], index=0)
    lang_code = "ta" if "தமிழ்" in lang else "en"
    st.session_state['lang'] = lang_code

    st.markdown("---")
    st.markdown(f"**v{APP_VERSION}**")
    st.markdown(t("sidebar_crops_markets", lang_code))
    st.markdown(t("sidebar_model", lang_code))
    st.markdown(t("sidebar_data", lang_code))

# Read lang_code from session
L = st.session_state.get('lang', 'en')

# =============================================================================
# HERO
# =============================================================================

st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">🌾 {t('app_name', L)}</div>
    <div class="hero-tagline">{t('tagline', L)}</div>
    <div class="hero-stat">{t('hero_stat', L)}</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# LOAD DATA
# =============================================================================

@st.cache_data(ttl=300)
def load_prices():
    fetcher = DataFetcher()
    cleaner = DataCleaner()
    df = fetcher.get_data()
    if df is not None:
        df = cleaner.clean(df)
        df['date'] = pd.to_datetime(df['date'])
    return df

df = load_prices()

# =============================================================================
# CROP CARDS WITH PAGINATION (fully localized)
# =============================================================================

if df is not None and not df.empty:
    latest_date = df['date'].max()
    prev_date = df[df['date'] < latest_date]['date'].max()

    st.markdown(f"### 📊 {t('todays_crop_prices', L)}")
    date_str = latest_date.strftime('%d %B %Y')
    unit_label = "Rs/Quintal" if L == "en" else "ரூ/குவிண்டால்"
    latest_lbl = "Latest" if L == "en" else "சமீபத்திய"
    st.caption(f"{latest_lbl}: {date_str} | {unit_label}")

    # Category filter (translated)
    cat_keys = list(CROP_CATEGORIES.keys())
    cat_options_display = [t("all_categories", L)] + [t_category(c, L) for c in cat_keys]
    col_filter, _ = st.columns([2, 3])
    with col_filter:
        selected_idx = st.selectbox(t("filter", L), range(len(cat_options_display)),
                                    format_func=lambda i: cat_options_display[i], index=0,
                                    label_visibility="collapsed")

    if selected_idx == 0:
        display_crops = CROPS
    else:
        display_crops = CROP_CATEGORIES.get(cat_keys[selected_idx - 1], CROPS)

    # Pagination
    total_crops = len(display_crops)
    total_pages = math.ceil(total_crops / CROPS_PER_PAGE)
    if 'home_page' not in st.session_state:
        st.session_state['home_page'] = 1
    if st.session_state['home_page'] > total_pages:
        st.session_state['home_page'] = total_pages
    if st.session_state['home_page'] < 1:
        st.session_state['home_page'] = 1

    current_page = st.session_state['home_page']
    start = (current_page - 1) * CROPS_PER_PAGE
    end = start + CROPS_PER_PAGE
    page_crops = display_crops[start:end]

    if total_pages > 1:
        p1, p2, p3 = st.columns([1, 3, 1])
        with p1:
            if st.button(t("prev", L), disabled=(current_page <= 1), key="prev_home"):
                st.session_state['home_page'] -= 1
                st.rerun()
        with p2:
            if L == "en":
                page_text = f"Page <b>{current_page}</b> of <b>{total_pages}</b> ({total_crops} crops)"
            else:
                page_text = f"<b>{total_pages}</b> பக்கங்களில் <b>{current_page}</b>வது பக்கம் ({total_crops} பயிர்கள்)"
            st.markdown(f'<div class="page-nav">{page_text}</div>', unsafe_allow_html=True)
        with p3:
            if st.button(t("next", L), disabled=(current_page >= total_pages), key="next_home"):
                st.session_state['home_page'] += 1
                st.rerun()

    # Render cards
    for row_start in range(0, len(page_crops), 4):
        row = page_crops[row_start:row_start + 4]
        cols = st.columns(4)
        for idx, crop in enumerate(row):
            with cols[idx]:
                info = CROP_DETAILS[crop]
                crop_latest = df[(df['crop'] == crop) & (df['date'] == latest_date)]
                crop_prev = df[(df['crop'] == crop) & (df['date'] == prev_date)]

                avg_price = crop_latest['modal_price'].mean() if not crop_latest.empty else 0
                prev_avg = crop_prev['modal_price'].mean() if not crop_prev.empty else avg_price
                change = avg_price - prev_avg
                change_pct = (change / prev_avg * 100) if prev_avg > 0 else 0

                chg_class = "crop-change-up" if change >= 0 else "crop-change-down"
                arrow = "▲" if change >= 0 else "▼"

                st.markdown(f"""
                <div class="crop-card">
                    <div class="crop-category">{t_category(info['category'], L)}</div>
                    <div class="crop-icon">{info['icon']}</div>
                    <div class="crop-name">{t_crop(crop, L)}</div>
                    <div class="crop-price">₹{avg_price:,.0f}</div>
                    <div class="{chg_class}">{arrow} {abs(change_pct):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")

# =============================================================================
# FEATURES (localized)
# =============================================================================

st.markdown(f"### 💡 {t('what_does_it_do', L)}")
st.markdown("")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="feature-card"><h4>{t('feat_forecast_title', L)}</h4>
    <p>{t('feat_forecast_desc', L)}</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="feature-card"><h4>{t('feat_compare_title', L)}</h4>
    <p>{t('feat_compare_desc', L)}</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="feature-card"><h4>{t('feat_advice_title', L)}</h4>
    <p>{t('feat_advice_desc', L)}</p></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="feature-card"><h4>{t('feat_risk_title', L)}</h4>
    <p>{t('feat_risk_desc', L)}</p></div>""", unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# HOW IT WORKS (localized)
# =============================================================================

st.markdown(f"### 🚀 {t('how_it_works', L)}")
cols = st.columns(4)
steps = [
    ("1", "step1_title", "step1_desc"),
    ("2", "step2_title", "step2_desc"),
    ("3", "step3_title", "step3_desc"),
    ("4", "step4_title", "step4_desc"),
]
for i, (num, title_key, desc_key) in enumerate(steps):
    with cols[i]:
        st.markdown(f"""<div class="step-card">
        <div class="step-number">{num}</div>
        <div class="step-text">{t(title_key, L)}</div>
        <p style="color:#4a5568; font-size:0.75rem; margin-top:0.2rem;">{t(desc_key, L)}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("")
st.info(t("start_prompt", L))

# Disclaimer
st.markdown(f"""<div class="disclaimer-box">⚠️ <strong>{'Disclaimer' if L=='en' else 'பொறுப்புத் துறப்பு'}:</strong> {t('disclaimer', L)}</div>""", unsafe_allow_html=True)
