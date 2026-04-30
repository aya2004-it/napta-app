import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

data = supabase.table("plants").select("*").execute().data

# ======================
# FAVORITE FUNCTION
# ======================
def add_favorite(plant_id):
    supabase.table("favorites").insert({
        "plant_id": plant_id
    }).execute()
    st.toast("❤️ تمت الإضافة للمفضلة")

# ======================
# SESSION STATE
# ======================
if "selected" not in st.session_state:
    st.session_state["selected"] = None

# ======================
# DETAILS PAGE
# ======================
def show_details(plant):
    st.image(plant["image_url"], use_container_width=True)

    st.markdown(f"# {plant['name_ar'] or plant['name']}")

    st.write("📝", plant["description"])
    st.write("💧", plant["watering"])
    st.write("🌞", plant["sunlight"])
    st.write("💡", plant["tips"])

    if st.button("❤️ إضافة للمفضلة"):
        add_favorite(plant["id"])

    if st.button("⬅ رجوع"):
        st.session_state["selected"] = None


# ======================
# NAVIGATION
# ======================
if st.session_state["selected"]:
    show_details(st.session_state["selected"])
    st.stop()

# ======================
# HOME
# ======================
st.title("🌿 نبتاتي")

plants = data

cols = st.columns(3)

for i, plant in enumerate(plants):
    with cols[i % 3]:

        st.markdown(f"### 🌿 {plant['name_ar'] or plant['name']}")
        st.image(plant["image_url"], use_container_width=True)

        st.write("💧", plant["watering"])
        st.write("🌞", plant["sunlight"])

        if st.button("📖 التفاصيل", key="d_" + plant["id"]):
            st.session_state["selected"] = plant

        if st.button("❤️ مفضلة", key="f_" + plant["id"]):
            add_favorite(plant["id"])
