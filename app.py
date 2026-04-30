import streamlit as st
from supabase import create_client

# 🔑 من secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

response = supabase.table("plants").select("*").execute()
data = response.data

st.title("🌱 Napta Plants")

for plant in data:
    st.subheader("🌿 " + plant["name"])
    st.image(plant["image_url"])
    st.write(plant["description"])
