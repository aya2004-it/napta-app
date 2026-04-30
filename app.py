import streamlit as st
from supabase import create_client

# 🔑 قراءة القيم من Secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

# 🧪 اختبار: هل القيم فعلاً مقروءة؟
st.write("URL:", url)
st.write("KEY start:", key[:10])  # يطبع أول 10 حروف فقط

# 🔌 إنشاء الاتصال
supabase = create_client(url, key)

# 🧪 جلب البيانات مع كشف الخطأ الحقيقي
try:
    response = supabase.table("plants").select("*").execute()
    data = response.data

    st.success("✅ Connected successfully!")
    st.write(data)

except Exception as e:
    st.error("🔥 ERROR DETAILS:")
    st.write(e)
