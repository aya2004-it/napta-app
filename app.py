import streamlit as st
from supabase import create_client

st.set_page_config(page_title="معرض نبتة", page_icon="🌿")

# 🌍 RTL
st.markdown("""
<style>
html, body, [class*="css"]  {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 معرض النباتات الذكي")

# 🔍 Search + Filter
search = st.text_input("🔍 ابحث عن نبتة")

filter_type = st.selectbox(
    "🌱 نوع النبتة",
    ["الكل", "desert", "indoor"]
)

# 🔌 Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# =========================
# ❤️ جلب المفضلة
# =========================
fav_response = supabase.table("favorites").select("*").execute()
favorites = fav_response.data if fav_response.data else []

fav_ids = [f["plant_id"] for f in favorites]

# =========================
# زر إضافة / حذف المفضلة
# =========================
def toggle_fav(plant_id):
    if plant_id in fav_ids:
        supabase.table("favorites").delete().eq("plant_id", plant_id).execute()
    else:
        supabase.table("favorites").insert({"plant_id": plant_id}).execute()

    st.rerun()

# =========================
# جلب النباتات
# =========================
response = supabase.table("plants").select("*").execute()
data = response.data

# 🔍 فلترة البحث
if search:
    data = [p for p in data if search.lower() in p["name"].lower()]

# 🌿 فلترة النوع
if filter_type != "الكل":
    data = [p for p in data if p.get("type") == filter_type]

# =========================
# 📦 عرض النباتات
# =========================
if data:

    cols = st.columns(3)

    for i, plant in enumerate(data):
        with cols[i % 3]:

            st.markdown("----")

            st.image(plant["image_url"], use_container_width=True)

            st.markdown(f"### 🌱 {plant['name']}")

            st.write(plant["description"][:80] + "...")

            # ❤️ زر المفضلة
            is_fav = plant["id"] in fav_ids

            if st.button(
                "❤️ إزالة" if is_fav else "🤍 إضافة",
                key=f"fav_{plant['id']}"
            ):
                toggle_fav(plant["id"])

else:
    st.warning("لا توجد نتائج")
