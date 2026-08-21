"""Page 2: Farmer Input — fully localized."""
import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import (APP_NAME, CROPS, MARKETS, CROP_DETAILS, MARKET_DETAILS,
    DEFAULT_STORAGE_COST_PER_DAY, DEFAULT_TRANSPORT_COST_PER_KM)
from utils.translations import t, t_crop, t_market

st.set_page_config(page_title=APP_NAME, page_icon="👨‍🌾", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&display=swap');
*{font-family:'Noto Sans Tamil','Latha',sans-serif;}
.block-container{padding-top:1.5rem;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a472a 0%,#2d5a3f 100%);}
[data-testid="stSidebar"] *{color:white !important;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>""", unsafe_allow_html=True)

L = st.session_state.get('lang', 'en')

st.markdown(f"## 👨‍🌾 {t('farmer_input_title', L)}")
st.markdown(t("farmer_input_subtitle", L))
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### 🌱 {t('crop_market_section', L)}")
    crop = st.selectbox(t('crop', L), CROPS,
        format_func=lambda x: f"{CROP_DETAILS[x]['icon']} {t_crop(x, L)} ({CROP_DETAILS[x]['category']})",
        index=CROPS.index("Tomato"))
    market = st.selectbox(t('market', L), MARKETS,
        format_func=lambda x: f"{t_market(x, L)} ({MARKET_DETAILS[x]['district']}, {MARKET_DETAILS[x]['state']})")
    quantity_kg = st.number_input(t('quantity_kg', L), min_value=10, max_value=100000, value=500, step=50,
        help=t('quantity_help', L))
    quantity_quintal = quantity_kg / 100
    quintal_word = t("quintal", L)
    kg_word = t("kg", L)
    st.info(f"📦 **{quantity_quintal:.1f} {quintal_word}** ({quantity_kg} {kg_word})")

with col2:
    st.markdown(f"#### 💰 {t('storage_transport_section', L)}")
    storage_available = st.radio(t('storage_available', L), [t('yes', L), t('no', L)], index=0, horizontal=True)
    storage_bool = storage_available == t('yes', L)
    if storage_bool:
        storage_cost = st.number_input(t('storage_cost', L), min_value=0.0, max_value=100.0,
            value=DEFAULT_STORAGE_COST_PER_DAY, step=0.5, help=t('storage_cost_help', L))
    else:
        storage_cost = 0.0
        st.caption(t("no_storage_note", L))
    transport_cost = st.number_input(t('transport_cost', L), min_value=0.0, max_value=50.0,
        value=DEFAULT_TRANSPORT_COST_PER_KM, step=0.5, help=t('transport_cost_help', L))
    max_distance = st.slider(t('max_distance', L), min_value=50, max_value=2500, value=700, step=50,
        help=t('max_distance_help', L))

st.markdown("---")
cl, cc, cr = st.columns([1, 2, 1])
with cc:
    submitted = st.button(t("analyze_button", L), use_container_width=True, type="primary")

if submitted:
    if quantity_kg <= 0:
        st.error(t("error_quantity", L))
    elif transport_cost < 0 or storage_cost < 0:
        st.error(t("error_cost_negative", L))
    else:
        st.session_state['farmer_input'] = {
            'crop': crop, 'market': market, 'quantity_kg': quantity_kg,
            'quantity_quintal': quantity_quintal, 'storage_available': storage_bool,
            'storage_cost': storage_cost, 'transport_cost': transport_cost, 'max_distance': max_distance
        }
        st.success(t("input_saved", L))
        st.markdown("")
        st.markdown(f"#### 📋 {t('input_summary', L)}")
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"- **{t('crop',L)}:** {CROP_DETAILS[crop]['icon']} {t_crop(crop,L)}")
            st.markdown(f"- **{t('market',L)}:** {t_market(market,L)} ({MARKET_DETAILS[market]['district']})")
            st.markdown(f"- **{t('quantity_kg',L)}:** {quantity_kg} {kg_word} ({quantity_quintal:.1f} {quintal_word})")
        with s2:
            st.markdown(f"- **{t('storage_available',L)}:** {t('storage_yes',L) if storage_bool else t('storage_no',L)}")
            st.markdown(f"- **{t('storage_cost',L)}:** ₹{storage_cost}")
            st.markdown(f"- **{t('transport_cost',L)}:** ₹{transport_cost}")
            st.markdown(f"- **{t('max_distance',L)}:** {max_distance} km")
        st.markdown("")
        st.info(t("navigate_prompt", L))

if 'farmer_input' in st.session_state and not submitted:
    inp = st.session_state['farmer_input']
    st.markdown("---")
    st.caption(f"✅ {t_crop(inp['crop'],L)} | {t_market(inp['market'],L)} | {inp['quantity_kg']} {kg_word}")
