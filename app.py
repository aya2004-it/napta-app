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
# SESSION STATE (PAGE + SELECTED PLANT)
# ======================
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "selected_plant" not in st.session_state:
    st.session_state["selected_plant"] = None


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
# SIDEBAR
# ======================
st.sidebar.title("🌿 Napta")

page = st.sidebar.radio("القائمة", ["🏠 الرئيسية", "❤️ المفضلة"])

search = st.sidebar.text_input("🔍 ابحث عن نبتة")


# ======================
# FILTER
# ======================
filtered_plants = plants

if search:
    filtered_plants = [
        p for p in plants
        if search.lower() in (p["name_ar"] or p["name"]).lower()
    ]


# ======================
# DETAILS PAGE (NEW 🚀)
# ======================
if st.session_state["page"] == "details":

    plant = st.session_state["selected_plant"]

    st.title(f"🌿 {plant['name_ar'] or plant['name']}")

    st.image(plant["image_url"], use_container_width=True)

    st.markdown("## 📝 الوصف")
    st.write(plant["description"])

    st.markdown("## 💧 طريقة الري")
    st.write(plant["watering"])

    st.markdown("## 🌞 الإضاءة")
    st.write(plant["sunlight"])

    st.markdown("## 💡 نصائح العناية")
    st.write(plant["tips"])

    st.markdown("## 🌍 البيئة المناسبة")
    st.write(plant["location"])

    if st.button("⬅ رجوع"):
        st.session_state["page"] = "home"
        st.rerun()

    st.stop()


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

            # ❤️ favorite
            heart = "❤️" if plant["id"] in fav_ids else "🤍"

            if st.button(f"{heart} مفضلة", key="fav_" + plant["id"]):
                toggle_favorite(plant["id"])
                refresh()
                st.rerun()

            # 📖 details button
            if st.button("📖 تفاصيل العناية", key="det_" + plant["id"]):
                st.session_state["selected_plant"] = plant
                st.session_state["page"] = "details"
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
