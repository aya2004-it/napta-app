import streamlit as st
from supabase import create_client

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
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
st.title("🌿 نبتاتي - معرض النباتات الذكي")
st.caption("اكتشف النباتات وتعرف على العناية بها 🌱")

# ======================
# SEARCH + FILTER
# ======================
search = st.text_input("🔍 ابحث عن نبتة")

filter_type = st.selectbox("🌱 تصنيف النباتات", ["الكل", "indoor", "desert"])

# ======================
# 🔥 FIXED IMAGES MAP (الحل الحقيقي)
# ======================
fixed_images = {
    "ألوفيرا": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "الصبار": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "الخزامى": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "النعناع": "https://images.unsplash.com/photo-1464375117522-1311dd51bb81",
    "الورد": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "الريحان": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "الياسمين": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "السرخس": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "نبتة المال": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "لسان الثعبان": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "شجرة الزيتون": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "نخيل التمر": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
}

# ======================
# FILTER LOGIC
# ======================
plants = data

if search:
    plants = [p for p in plants if search in (p["name_ar"] or p["name"] or "")]

if filter_type != "الكل":
    plants = [p for p in plants if p["type"] == filter_type]

# ======================
# DISPLAY GRID
# ======================
cols = st.columns(3)

for i, plant in enumerate(plants):
    with cols[i % 3]:

        name = plant["name_ar"] or plant["name"]

        st.markdown(f"### 🌿 {name}")

        # 🔥 هنا التغيير الحقيقي
        image_url = fixed_images.get(name, plant["image_url"])

        st.image(image_url, use_container_width=True)

        st.write("💧 الري:", plant["watering"])
        st.write("🌞 الضوء:", plant["sunlight"])

        if st.button("📖 التفاصيل", key="details_" + plant["id"]):
            st.session_state["selected"] = plant

        if st.button("❤️ مفضلة", key="fav_" + plant["id"]):
            st.toast("تمت الإضافة للمفضلة ❤️")
