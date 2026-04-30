import streamlit as st
from supabase import create_client

st.set_page_config(page_title="معرض نبتة", page_icon="🌿")
st.title("🌿 معرض النباتات الذكي")

# جلب البيانات من Secrets
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # محاولة جلب البيانات
    response = supabase.table("plants").select("*").execute()
    
    if response.data:
        for plant in response.data:
            with st.container():
                st.markdown(f"### {plant['name']}")
                st.image(plant['image_url'], width=300)
                st.write(plant['description'])
                st.divider()
    else:
        st.info("الجدول فارغ، أضيفي بعض النباتات في Supabase!")

except Exception as e:
    st.error("❌ فشل الاتصال بقاعدة البيانات")
    st.info("تأكدي من صحة الـ API Key والـ URL في إعدادات Secrets")
    st.warning(f"تفاصيل الخطأ التقني: {e}")
