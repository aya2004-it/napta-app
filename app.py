import streamlit as st
from supabase import create_client

# 🔑 Supabase credentials
url = "https://dpttbbaepbgyaaedingk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFidmVleHFta3hvamJ3aHp5cXViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0MDE2ODksImV4cCI6MjA5Mjk3NzY4OX0.kq2RAY0Wt8Q5Mjn3lB42L5lZCz0wxKZNX0fZLUvEf74"

supabase = create_client(url, key)

# 📥 جلب البيانات
response = supabase.table("plants").select("*").execute()
data = response.data

st.title("🌱 Napta Plants")

# 🖼️ صور النباتات
images = {
    "Aloe vera": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
    "Monstera deliciosa": "https://images.unsplash.com/photo-1598887142487-47d2c7a3b1f4",
    "Ficus lyrata": "https://images.unsplash.com/photo-1593691509543-c55fb32e5d9b",
}

# 🧠 إزالة التكرار
unique_plants = {}

for plant in data:
    name = plant["Plant_ID"]
    if name not in unique_plants:
        unique_plants[name] = plant

# 🎨 عرض البيانات بشكل موقع
for plant in unique_plants.values():
    st.markdown("---")

    st.subheader("🌿 " + plant["Plant_ID"])

    st.image(
        images.get(plant["Plant_ID"], "https://via.placeholder.com/300"),
        use_container_width=True
    )

    st.write("💧 Water every:", plant["Watering_Frequency_days"], "days")
    st.write("🌞 Sunlight:", plant["Sunlight_Exposure"])
    st.write("🪴 Health Score:", plant["Health_Score"])
