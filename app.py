import streamlit as st
from supabase import create_client

# 🔐 Supabase credentials
url = "https://dpttbbaepbgyaaedingk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFidmVleHFta3hvamJ3aHp5cXViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0MDE2ODksImV4cCI6MjA5Mjk3NzY4OX0.kq2RAY0Wt8Q5Mjn3lB42L5lZCz0wxKZNX0fZLUvEf74"

supabase = create_client(url, key)

st.title("🌱 Napta Plants Dashboard")

try:
    response = supabase.table("plants").select("*").execute()
    data = response.data

    if not data:
        st.warning("No plants found 😢")
    else:
        for plant in data:
            st.subheader(f"🌿 {plant.get('Plant_ID', 'Unknown')}")

            st.write("💧 Water:", plant.get("Watering_Frequency_days"), "days")
            st.write("🌞 Sun:", plant.get("Sunlight_Exposure"))
            st.write("🪴 Health Score:", plant.get("Health_Score"))

            st.write("---")

except Exception as e:
    st.error("🔥 Error happened:")
    st.write(e)
