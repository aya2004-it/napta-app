import streamlit as st
from supabase import create_client

# 📌 إعداد الصفحة
st.set_page_config(page_title="معرض نبتة", page_icon="🌿")

# 🌍 RTL عربي
st.markdown("""
<style>
html, body, [class*="css"]  {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 معرض النباتات الذكي")

# 🔍 Search + 🌿 Filter (جاهز للخطوة القادمة)
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

    if data:

        # 📦 Grid layout (3 أعمدة)
        cols = st.columns(3)

        for i, plant in enumerate(data):
            with cols[i % 3]:

                st.markdown("----")

                # 🖼️ صورة صغيرة منظمة
                st.image(
                    plant["image_url"],
                    use_container_width=True
                )

                # 🌿 الاسم
                st.markdown(f"### 🌱 {plant['name']}")

                # 📄 وصف مختصر
                st.write(plant["description"][:80] + "...")

                # ❤️ زر مبدئي (جاهز لاحقاً للمفضلة)
                st.button("❤️ مفضلة", key=f"fav_{plant['id']}")

    else:
        st.info("⚠️ لا توجد نباتات")

except Exception as e:
    st.error("❌ خطأ في الاتصال")
    st.warning(e)
