import streamlit as st
from supabase import create_client

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .plant-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    .plant-title {
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ======================
# SUPABASE
# ======================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

data = supabase.table("plants").select("*").execute().data

# ======================
# HEADER
# ======================
st.title("🌿 Napta - نباتاتي الذكية")
st.caption("اكتشف النباتات، اعرف طريقة العناية، واحتفظ بالمفضلة ❤️")

# ======================
# SEARCH
# ======================
search = st.text_input("🔍 ابحث عن نبتة")

# ======================
# FILTER
# ======================
filter_type = st.selectbox("🌱 فلترة", ["الكل", "indoor", "desert"])

# ======================
# FILTER DATA
# ======================
plants = data

if search:
    plants = [p for p in plants if search in (p["name"] or "") or search in (p["name_ar"] or "")]

if filter_type != "الكل":
    plants = [p for p in plants if p["type"] == filter_type]

# ======================
# GRID DISPLAY
# ======================
cols = st.columns(3)

for i, plant in enumerate(plants):
    with cols[i % 3]:
        st.markdown("### 🌿 " + (plant["name_ar"] or plant["name"]))

        st.image(plant["image_url"], use_container_width=True)

        st.write("💧", plant["watering"])
        st.write("🌞", plant["sunlight"])

        if st.button("📖 التفاصيل", key=plant["id"]):
            st.session_state["selected"] = plant

        if st.button("❤️", key="fav_" + plant["id"]):
            st.toast("تمت الإضافة للمفضلة ❤️")
