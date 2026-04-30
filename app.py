import streamlit as st
from supabase import create_client

# 📌 إعداد الصفحة
st.set_page_config(page_title="معرض نبتة", page_icon="🌿")

# 🌍 دعم اللغة العربية (RTL)
st.markdown("""
<style>
html, body, [class*="css"]  {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# 🏷️ العنوان
st.title("🌿 معرض النباتات الذكي")

# 🔍 Search + 🌿 Filter (واجهة فقط حالياً)
search = st.text_input("🔍 ابحث عن نبتة")

filter_type = st.selectbox(
    "🌱 نوع النبتة",
    ["الكل", "desert", "indoor"]
)

# 🔌 الاتصال بـ Supabase
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    response = supabase.table("plants").select("*").execute()
    data = response.data

    # 🌿 عرض البيانات (بدون فلترة بعد)
    if data:
        for plant in data:
            with st.container():
                st.markdown(f"### 🌱 {plant['name']}")
                st.image(plant['image_url'], use_container_width=True)
                st.write(plant['description'])
                st.divider()
    else:
        st.info("⚠️ لا توجد نباتات حالياً في قاعدة البيانات")

except Exception as e:
    st.error("❌ فشل الاتصال بقاعدة البيانات")
    st.warning(f"تفاصيل الخطأ: {e}")
