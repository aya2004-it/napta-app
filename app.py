import streamlit as st
from supabase import create_client

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

# ======================
# SUPABASE
# ======================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

data = supabase.table("plants").select("*").execute().data

# ======================
# SESSION STATE
# ======================
if "selected" not in st.session_state:
    st.session_state["selected"] = None

# ======================
# PAGE: DETAILS
# ======================
def show_details(plant):
    st.markdown("## 🌿 تفاصيل النبتة")

    st.image(plant["image_url"], use_container_width=True)

    st.markdown(f"# {plant['name_ar'] or plant['name']}")

    st.markdown("### 📝 الوصف")
    st.write(plant["description"])

    st.markdown("### 💧 الري")
    st.write(plant["watering"])

    st.markdown("### 🌞 الضوء")
    st.write(plant["sunlight"])

    st.markdown("### 💡 النصائح")
    st.write(plant["tips"])

    st.markdown("### 🌍 البيئة")
    st.write(plant["location"])

    st.markdown("### 🌱 النوع")
    st.write(plant["type"])

    if st.button("⬅ الرجوع"):
        st.session_state["selected"] = None


# ======================
# DETAILS VIEW
# ======================
if st.session_state["selected"]:
    show_details(st.session_state["selected"])
    st.stop()

# ======================
# HEADER
# ======================
st.title("🌿 نبتاتي - معرض النباتات الذكي")
st.caption("اضغط على أي نبتة لمشاهدة التفاصيل")

# ======================
# SEARCH + FILTER
# ======================
search = st.text_input("🔍 بحث عن نبتة")

filter_type = st.selectbox("🌱 تصنيف", ["الكل", "indoor", "desert"])

plants = data

if search:
    plants = [p for p in plants if search in (p["name_ar"] or p["name"] or "")]

if filter_type != "الكل":
    plants = [p for p in plants if p["type"] == filter_type]

# ======================
# GRID UI CARDS (FINAL UI)
# ======================
cols = st.columns(3)

for i, plant in enumerate(plants):
    with cols[i % 3]:

        name = plant["name_ar"] or plant["name"]

        st.markdown(f"""
        <div style="
            background:white;
            padding:15px;
            border-radius:20px;
            box-shadow:0px 4px 15px rgba(0,0,0,0.1);
            margin-bottom:15px;
            text-align:center;
        ">
            <h3>🌿 {name}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.image(plant["image_url"], use_container_width=True)

        st.markdown(f"""
        <div style="margin-top:10px;">
            <b>💧 الري:</b> {plant['watering']}<br>
            <b>🌞 الضوء:</b> {plant['sunlight']}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📖 التفاصيل", key="details_" + plant["id"]):
                st.session_state["selected"] = plant

        with col2:
            if st.button("❤️ مفضلة", key="fav_" + plant["id"]):
                st.toast("تمت الإضافة ❤️")
