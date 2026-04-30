import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Napta 🌿", page_icon="🌱", layout="wide")

st.markdown("""
    <style>
    .plant-card {
        background: #0f172a;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .title {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Napta - معرض النباتات الذكي")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

response = supabase.table("plants").select("*").execute()
data = response.data

# حالة التنقل
if "page" not in st.session_state:
    st.session_state.page = "home"

# اختيار نبتة
if "selected" not in st.session_state:
    st.session_state.selected = None

# =========================
# 🏠 الصفحة الرئيسية
# =========================
if st.session_state.page == "home":

    for plant in data:

        with st.container():
            st.markdown(f"""
            <div class="plant-card">
                <div class="title">🌱 {plant['name']}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(plant['image_url'], use_container_width=True)

            with col2:
                st.write(plant['description'])

                if st.button(f"🌿 العناية بـ {plant['name']}", key=plant['id']):
                    st.session_state.selected = plant
                    st.session_state.page = "details"
                    st.rerun()

# =========================
# 🌿 صفحة التفاصيل
# =========================
elif st.session_state.page == "details":

    plant = st.session_state.selected

    st.button("⬅ الرجوع", on_click=lambda: st.session_state.update(page="home"))

    st.title(f"🌿 العناية بـ {plant['name']}")

    st.image(plant['image_url'], use_container_width=True)

    st.markdown("## 💧 الري")
    st.write(plant.get("care_water", "لا توجد معلومات"))

    st.markdown("## 🌞 الإضاءة")
    st.write(plant.get("care_light", "لا توجد معلومات"))

    st.markdown("## 🌱 التربة")
    st.write(plant.get("care_soil", "لا توجد معلومات"))

    st.markdown("## 🌡️ نصائح")
    st.write(plant.get("care_tips", "لا توجد نصائح"))
