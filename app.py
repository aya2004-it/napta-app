import streamlit as st
from supabase import create_client

# 🔑 بيانات Supabase
url = "https://dpttbbaepbgyaaedingk.supabase.co"
key = "sb_publishable_E5rLG4YeNSbObg860425pQ_gUngCzVf"

supabase = create_client(url, key)

# 🌱 عنوان الموقع
st.title("🌱 Napta Plants")

# 📥 جلب البيانات
data = supabase.table("plants").select("*").execute().data

# 🔍 بحث
search = st.text_input("🔍 Search for plant")

# 🪴 عرض النباتات
for plant in data:
    if search.lower() in plant["Plant_ID"].lower():
        st.markdown(f"## 🌿 {plant['Plant_ID']}")
        st.write("💧 Water every:", plant["Watering_Frequency_days"], "days")
        st.write("🌞 Sun:", plant["Sunlight_Exposure"])
        st.write("🪴 Health Score:", plant["Health_Score"])
        st.write("---")
