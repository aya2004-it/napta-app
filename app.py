import streamlit as st
from supabase import create_client

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ======================
# DATA
# ======================
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
# REFRESH
# ======================
def refresh():
    global favorites, fav_ids
    favorites = supabase.table("favorites").select("*").execute().data
    fav_ids = [f["plant_id"] for f in favorites]


# ======================
# SIDEBAR NAVIGATION
# ======================
st.sidebar.title("🌿 Napta")

page = st.sidebar.radio("القائمة", ["🏠 الرئيسية", "❤️ المفضلة"])

# ======================
# SEARCH
# ======================
search = st.sidebar.text_input("🔍 ابحث عن نبتة")


# ======================
# FILTER PLANTS (SEARCH)
# ======================
filtered_plants = plants

if search:
    filtered_plants = [
        p for p in plants
        if search.lower() in (p["name_ar"] or p["name"]).lower()
    ]


# ======================
# HOME PAGE
# ======================
if page == "🏠 الرئيسية":

    st.title("🌿 نبتاتي")

    cols = st.columns(3)

    for i, plant in enumerate(filtered_plants):
        with cols[i % 3]:

            name = plant["name_ar"] or plant["name"]

            st.markdown(f"### 🌿 {name}")
            st.image(plant["image_url"], use_container_width=True)

            st.write("💧", plant["watering"])
            st.write("🌞", plant["sunlight"])

            heart = "❤️" if plant["id"] in fav_ids else "🤍"

            if st.button(f"{heart} مفضلة", key="fav_" + plant["id"]):
                toggle_favorite(plant["id"])
                refresh()
                st.rerun()


# ======================
# FAVORITES PAGE
# ======================
if page == "❤️ المفضلة":

    st.title("❤️ المفضلة")

    fav_plants = supabase.table("plants") \
        .select("*") \
        .in_("id", fav_ids) \
        .execute().data

    if not fav_plants:
        st.info("لا توجد مفضلات بعد 🌿")
    else:
        cols = st.columns(3)

        for i, plant in enumerate(fav_plants):
            with cols[i % 3]:

                name = plant["name_ar"] or plant["name"]

                st.markdown(f"### 🌿 {name}")
                st.image(plant["image_url"], use_container_width=True)

                st.write("💧", plant["watering"])
                st.write("🌞", plant["sunlight"])

                if st.button("💔 حذف", key="del_" + plant["id"]):
                    toggle_favorite(plant["id"])
                    refresh()
                    st.rerun()
