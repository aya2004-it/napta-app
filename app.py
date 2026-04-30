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

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    response = supabase.table("plants").select("*").execute()
    data = response.data

    # =========================
    # 🧠 فلترة حقيقية هنا
    # =========================

    if search:
        data = [p for p in data if search.lower() in p["name"].lower()]

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

                st.image(
                    plant["image_url"],
                    use_container_width=True
                )

                st.markdown(f"### 🌱 {plant['name']}")

                st.write(plant["description"][:80] + "...")

                st.button("❤️ مفضلة", key=f"fav_{plant['id']}")

    else:
        st.warning("لا توجد نتائج تطابق البحث")

except Exception as e:
    st.error("❌ خطأ في الاتصال")
    st.warning(e)
