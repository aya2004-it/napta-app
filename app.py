import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

plants = supabase.table("plants").select("*").execute().data
favorites = supabase.table("favorites").select("*").execute().data

fav_ids = [f["plant_id"] for f in favorites]

# ======================
# TOGGLE FAVORITE
# ======================
def toggle_favorite(plant_id):
    if plant_id in fav_ids:
        supabase.table("favorites") \
            .delete() \
            .eq("plant_id", plant_id) \
            .execute()
        st.toast("💔 تم الحذف من المفضلة")
    else:
        supabase.table("favorites").insert({
            "plant_id": plant_id
        }).execute()
        st.toast("❤️ تمت الإضافة")

# ======================
# REFRESH FAVS
# ======================
def refresh_favs():
    global favorites, fav_ids
    favorites = supabase.table("favorites").select("*").execute().data
    fav_ids = [f["plant_id"] for f in favorites]


# ======================
# UI
# ======================
st.title("🌿 نبتاتي - النسخة الاحترافية")

cols = st.columns(3)

for i, plant in enumerate(plants):
    with cols[i % 3]:

        name = plant["name_ar"] or plant["name"]

        st.markdown(f"### 🌿 {name}")
        st.image(plant["image_url"], use_container_width=True)

        st.write("💧", plant["watering"])
        st.write("🌞", plant["sunlight"])

        heart = "❤️" if plant["id"] in fav_ids else "🤍"

        if st.button(f"{heart} مفضلة", key="fav_" + plant["id"]):
            toggle_favorite(plant["id"])
            refresh_favs()
            st.rerun()
