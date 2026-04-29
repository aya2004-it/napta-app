import streamlit as st

data = supabase.table("plants").select("*").execute().data

st.title("🌱 Napta Plants")

images = {
    "Aloe vera": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
}

unique_plants = {}

for plant in data:
    name = plant["Plant_ID"]
    if name not in unique_plants:
        unique_plants[name] = plant

for plant in unique_plants.values():
    st.subheader("🌿 " + plant["Plant_ID"])
    
    st.image(images.get(plant["Plant_ID"], "https://via.placeholder.com/200"))
    
    st.write("💧 Water every:", plant["Watering_Frequency_days"], "days")
    st.write("🌞 Sun:", plant["Sunlight_Exposure"])
    st.write("🪴 Health Score:", plant["Health_Score"])
    
    st.write("---")
