import streamlit as st
from supabase import create_client

# إعداد الصفحة
st.set_page_config(page_title="نبتة - Napta", page_icon="🌿")
st.title("🌿 معرض النباتات الذكي")

# الربط بقاعدة البيانات
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# جلب البيانات
try:
    response = supabase.table("plants").select("*").execute()
    data = response.data

    if data:
        for plant in data:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(plant['image_url'], use_container_width=True)
            with col2:
                st.subheader(plant['name'])
                st.write(plant['description'])
                st.info(f"📍 المكان: {plant.get('location', 'غير محدد')}")
    else:
        st.warning("لا توجد نباتات في الجدول حالياً.")

except Exception as e:
    st.error(f"حدث خطأ أثناء الاتصال: {e}")
