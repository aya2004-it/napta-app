import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ======================
# AUTH (بسيط)
# ======================
if "user" not in st.session_state:
    st.session_state["user"] = None

st.sidebar.title("🔐 الدخول")

email = st.sidebar.text_input("Email")

if st.sidebar.button("تسجيل دخول"):
    st.session_state["user"] = email
    st.sidebar.success("تم الدخول ✔")

if not st.session_state["user"]:
    st.warning("يجب تسجيل الدخول أولاً")
    st.stop()

user_id = st.session_state["user"]

# ======================
# FUNCTIONS
# ======================
def add_favorite(plant_id):
    check = supabase.table("favorites") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("plant_id", plant_id) \
        .execute()

    if check.data:
        st.toast("موجودة مسبقًا ❤️")
    else:
        supabase.table("favorites").insert({
            "user_id": user_id,
            "plant_id": plant_id
        }).execute()
        st.toast("تمت الإضافة ❤️")


def get_favorites():
    favs = supabase.table("favorites") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute().data

    plant_ids = [f["plant_id"] for f in favs]

    if not plant_ids:
        return []

    return supabase.table("plants") \
        .select("*") \
        .in_("id", plant_ids) \
        .execute().data


# ======================
# NAV
# ======================
page = st.sidebar.radio("القائمة", ["الرئيسية", "المفضلة"])

# ======================
# HOME
# ======================
if page == "الرئيسية":
    st.title("🌿 نبتاتي")

    data = supabase.table("plants").select("*").execute().data

    cols = st.columns(3)

    for i, plant in enumerate(data):
        with cols[i % 3]:

            st.markdown(f"### 🌿 {plant['name_ar']}")
            st.image(plant["image_url"], use_container_width=True)

            st.write("💧", plant["watering"])
            st.write("🌞", plant["sunlight"])

            if st.button("❤️ مفضلة", key="f_" + plant["id"]):
                add_favorite(plant["id"])

# ======================
# FAVORITES PAGE
# ======================
if page == "المفضلة":
    st.title("❤️ مفضلتي")

    favs = get_favorites()

    if not favs:
        st.info("لا توجد مفضلات بعد 🌿")
    else:
        cols = st.columns(3)

        for i, plant in enumerate(favs):
            with cols[i % 3]:

                st.markdown(f"### 🌿 {plant['name_ar']}")
                st.image(plant["image_url"], use_container_width=True)

                st.write("💧", plant["watering"])
                st.write("🌞", plant["sunlight"])
