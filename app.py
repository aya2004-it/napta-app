import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Napta 🌿", page_icon="🌿", layout="wide")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ======================
# AUTH
# ======================
if "user" not in st.session_state:
    st.session_state["user"] = None

st.sidebar.title("🔐 الدخول")

email = st.sidebar.text_input("Email")

if st.sidebar.button("تسجيل دخول"):
    res = supabase.auth.sign_in_with_password({
        "email": email,
        "password": "123456"  # للتجربة فقط
    })
    st.session_state["user"] = res.user
    st.sidebar.success("تم الدخول ✔")

if not st.session_state["user"]:
    st.warning("🔐 سجل دخول أولاً")
    st.stop()

user_id = st.session_state["user"].id


# ======================
# DATA
# ======================
plants = supabase.table("plants").select("*").execute().data

favorites = supabase.table("favorites") \
    .select("*") \
    .eq("user_id", user_id) \
    .execute().data

fav_ids = [f["plant_id"] for f in favorites]


# ======================
# FAVORITES TOGGLE
# ======================
def toggle_fav(pid):
    if pid in fav_ids:
        supabase.table("favorites") \
            .delete() \
            .eq("user_id", user_id) \
            .eq("plant_id", pid) \
            .execute()
        st.toast("💔 حذف من المفضلة")
    else:
        supabase.table("favorites").insert({
            "user_id": user_id,
            "plant_id": pid
        }).execute()
        st.toast("❤️ تمت الإضافة")


# ======================
# UI NAV
# ======================
page = st.sidebar.radio("القائمة", ["الرئيسية", "المفضلة"])


# ======================
# HOME
# ======================
if page == "الرئيسية":
    st.title("🌿 Napta - Plants")

    cols = st.columns(3)

    for i, plant in enumerate(plants):
        with cols[i % 3]:

            name = plant["name_ar"] or plant["name"]

            st.markdown(f"### 🌿 {name}")
            st.image(plant["image_url"], use_container_width=True)

            st.write("💧", plant["watering"])
            st.write("🌞", plant["sunlight"])

            heart = "❤️" if plant["id"] in fav_ids else "🤍"

            if st.button(f"{heart} مفضلة", key="f_" + plant["id"]):
                toggle_fav(plant["id"])
                st.rerun()


# ======================
# FAVORITES PAGE
# ======================
if page == "المفضلة":
    st.title("❤️ مفضلتي")

    fav_plants = supabase.table("plants") \
        .select("*") \
        .in_("id", fav_ids) \
        .execute().data

    if not fav_plants:
        st.info("لا توجد مفضلات")
    else:
        cols = st.columns(3)

        for i, plant in enumerate(fav_plants):
            with cols[i % 3]:

                st.markdown(f"### 🌿 {plant['name_ar']}")
                st.image(plant["image_url"], use_container_width=True)

                st.write("💧", plant["watering"])
                st.write("🌞", plant["sunlight"])
