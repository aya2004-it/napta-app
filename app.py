import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

data = supabase.table("plants").select("*").execute().data

st.title("🌿 نبتاتي - معرض النباتات الذكي")

# 🔥 صور حسب ID (أقوى حل)
fixed_images = {
    # حطينا أمثلة حسب الترتيب (تقدر تعدلهم)
    1: "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    2: "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc",
    3: "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07",
}

search = st.text_input("🔍 بحث")

filter_type = st.selectbox("🌱 فلترة", ["الكل", "indoor", "desert"])

plants = data

if search:
    plants = [p for p in plants if search in (p["name_ar"] or "")]

if filter_type != "الكل":
    plants = [p for p in plants if p["type"] == filter_type]

cols = st.columns(3)

for i, plant in enumerate(plants):
    with cols[i % 3]:

        st.markdown(f"### 🌿 {plant['name_ar']}")

        # 🔥 الحل الحقيقي
        image_url = fixed_images.get(i+1, plant["image_url"])

        st.image(image_url, use_container_width=True)

        st.write("💧", plant["watering"])
        st.write("🌞", plant["sunlight"])

        if st.button("📖 التفاصيل", key=plant["id"]):
            st.session_state["selected"] = plant

        if st.button("❤️ مفضلة", key="fav_" + plant["id"]):
            st.toast("تمت الإضافة ❤️")
