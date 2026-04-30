import streamlit as st
from supabase import create_client

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

# ======================
# SUPABASE
# ======================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ======================
# LOAD DATA
# ======================
plants = supabase.table("plants").select("*").execute().data


# ======================
# FAVORITES FUNCTIONS
# ======================
def add_favorite(plant_id):
    # منع التكرار
    check = supabase.table("favorites") \
        .select("*") \
        .eq("plant_id", plant_id) \
        .execute()

    if check.data:
        st.toast("❤️ موجودة مسبقًا")
    else:
        supabase.table("favorites").insert({
            "plant_id": plant_id
        }).execute()
        st.toast("❤️ تمت الإضافة")


def get_favorites():
    favs = supabase.table("favorites").select("*").execute().data

    plant_ids = [f["plant_id"] for f in favs]

    if not plant_ids:
        return []

    return supabase.table("plants") \
        .select("*") \
        .in_("id", plant_ids) \
        .execute().data


# ======================
# SESSION STATE
# ======================
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "selected" not in st.session_state:
    st.session_state["selected"] = None


# ======================
# NAVIGATION
# ======================
st.sidebar.title("🌿 Napta")

if st.sidebar.button("🏠 الرئيسية"):
    st.session_state["page"] = "home"

if st.sidebar.button("❤️ المفضلة"):
    st.session_state["page"] = "favorites"


# ======================
# FAVORITES PAGE
# ======================
if st.session_state["page"] == "favorites":
    st.title("❤️ المفضلة")

    favs = get_favorites()

    if not favs:
        st.info("لا توجد مفضلات بعد 🌿")
    else:
        cols = st.columns(3)

        for i, plant in enumerate(favs):
            with cols[i % 3]:

                st.markdown(f"### 🌿 {plant['name_ar'] or plant['name']}")
                st.image(plant["image_url"], use_container_width=True)

                st.write("💧", plant["watering"])
                st.write("🌞", plant["sunlight"])

                if st.button("📖 التفاصيل", key="fav_" + plant["id"]):
                    st.session_state["selected"] = plant
                    st.session_state["page"] = "home"
                    st.rerun()

    st.stop()


# ======================
# HOME PAGE
# ======================
if st.session_state["page"] == "home":

    st.title("🌿 نبتاتي - معرض النباتات")

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


# ======================
# DETAILS PAGE
# ======================
if st.session_state["selected"]:
    plant = st.session_state["selected"]

    st.title(f"🌿 {plant['name_ar'] or plant['name']}")
    st.image(plant["image_url"], use_container_width=True)

    st.markdown("### 📝 الوصف")
    st.write(plant["description"])

    st.markdown("### 💧 الري")
    st.write(plant["watering"])

    st.markdown("### 🌞 الضوء")
    st.write(plant["sunlight"])

    st.markdown("### 💡 النصائح")
    st.write(plant["tips"])

    if st.button("⬅ رجوع"):
        st.session_state["selected"] = None
        st.rerun()
