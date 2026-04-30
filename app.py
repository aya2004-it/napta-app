import streamlit as st
from supabase import create_client

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Napta | دليل العناية بالنباتات",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================
# CUSTOM CSS FOR PROFESSIONAL LOOK
# ======================
st.markdown(
    """
    <style>
    /* Main background and text */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e3c2c 0%, #2a4a35 100%);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* Professional sidebar buttons */
    .stButton button {
        background: linear-gradient(95deg, #2e7d32 0%, #4caf50 100%);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
        transition: 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton button:hover {
        transform: scale(0.98);
        background: linear-gradient(95deg, #1b5e20 0%, #388e3c 100%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    /* Titles */
    h1, h2, h3 {
        font-family: 'Segoe UI', 'Tahoma', sans-serif;
        font-weight: 600;
    }
    h1 {
        background: linear-gradient(90deg, #1e3c2c, #4caf50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    /* Cards for plants */
    .plant-card {
        background: white;
        border-radius: 24px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .plant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 30px rgba(0,0,0,0.1);
    }
    /* Uniform image styling */
    .plant-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 18px;
        margin-bottom: 0.8rem;
    }
    /* Info badges */
    .info-badge {
        background-color: #eef2e6;
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 0.8rem;
        color: #2c5e2e;
        display: inline-block;
        margin: 2px 0;
    }
    /* Favorite heart button special */
    .fav-button button {
        background: #ff6b6b;
        background: linear-gradient(95deg, #ff6b6b, #ff8e8e);
    }
    .fav-button button:hover {
        background: #e04e4e;
    }
    /* Details page styling */
    .detail-section {
        background: white;
        border-radius: 28px;
        padding: 1.5rem;
        margin: 1.2rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .detail-icon {
        font-size: 1.8rem;
        margin-left: 10px;
        vertical-align: middle;
    }
    hr {
        margin: 1rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #c8e6c9, #4caf50, #c8e6c9);
    }
    /* Search bar styling */
    .search-container {
        margin-bottom: 2rem;
        padding: 0 0.5rem;
    }
    .search-container input {
        width: 100%;
        padding: 12px 20px;
        font-size: 1rem;
        border: 2px solid #e0e0e0;
        border-radius: 50px;
        transition: all 0.3s ease;
        background: white;
        text-align: right;
    }
    .search-container input:focus {
        outline: none;
        border-color: #4caf50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    /* Remove label from search input */
    .stTextInput label {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================
# SUPABASE CONNECTION
# ======================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ======================
# DATA LOADING
# ======================
@st.cache_data(ttl=60)
def load_plants():
    return supabase.table("plants").select("*").execute().data

@st.cache_data(ttl=30)
def load_favorites():
    return supabase.table("favorites").select("*").execute().data

plants = load_plants()
favorites = load_favorites()
fav_ids = [f["plant_id"] for f in favorites]

# ======================
# SESSION STATE
# ======================
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "selected_plant" not in st.session_state:
    st.session_state["selected_plant"] = None

# ======================
# HELPER FUNCTIONS
# ======================
def toggle_favorite(plant_id):
    if plant_id in fav_ids:
        supabase.table("favorites").delete().eq("plant_id", plant_id).execute()
        st.toast("💔 تم إزالتها من المفضلة", icon="🌿")
    else:
        supabase.table("favorites").insert({"plant_id": plant_id}).execute()
        st.toast("❤️ أُضيفت إلى المفضلة", icon="✨")
    st.cache_data.clear()
    st.rerun()

def refresh():
    global favorites, fav_ids
    favorites = load_favorites()
    fav_ids = [f["plant_id"] for f in favorites]

def display_plant_card(plant, is_fav_page=False):
    """Reusable card with consistent styling"""
    name = plant["name_ar"] or plant["name"]
    
    # HTML card structure
    card_html = f"""
    <div class="plant-card">
        <img src="{plant['image_url']}" class="plant-img" alt="{name}">
        <h3 style="margin: 0 0 5px 0;">🌿 {name}</h3>
        <div style="margin: 8px 0;">
            <span class="info-badge">💧 {plant['watering']}</span>
            <span class="info-badge">🌞 {plant['sunlight']}</span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Buttons row
    col1, col2 = st.columns(2)
    with col1:
        if is_fav_page:
            if st.button("💔 إزالة", key=f"del_{plant['id']}", use_container_width=True):
                toggle_favorite(plant["id"])
        else:
            heart = "❤️" if plant["id"] in fav_ids else "🤍"
            if st.button(f"{heart} مفضلة", key=f"fav_{plant['id']}", use_container_width=True):
                toggle_favorite(plant["id"])
    with col2:
        if st.button("📖 تفاصيل العناية", key=f"det_{plant['id']}", use_container_width=True):
            st.session_state["selected_plant"] = plant
            st.session_state["page"] = "details"
            st.rerun()

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/leaf.png", width=60)
    st.title("🌿 Napta")
    st.markdown("---")
    
    # Professional buttons in sidebar
    if st.button("🏠 الرئيسية", key="sidebar_home", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()
    
    if st.button("❤️ المفضلة", key="sidebar_fav", use_container_width=True):
        st.session_state["page"] = "favorites"
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2025 Napta")

# ======================
# DETAILS PAGE
# ======================
if st.session_state["page"] == "details":
    plant = st.session_state["selected_plant"]
    name = plant["name_ar"] or plant["name"]
    
    st.markdown(f"<h1 style='text-align: right;'>🌿 {name}</h1>", unsafe_allow_html=True)
    
    # Image with consistent height
    st.markdown(
        f'<img src="{plant["image_url"]}" style="width:100%; max-height:450px; object-fit:cover; border-radius:32px; margin-bottom:1rem;">',
        unsafe_allow_html=True
    )
    
    # Description
    with st.container():
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("## 📝 الوصف")
        st.write(plant["description"])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Care details in columns
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("## 💧 طريقة الري")
        st.write(plant["watering"])
        st.markdown("## 🌞 الإضاءة")
        st.write(plant["sunlight"])
        st.markdown("</div>", unsafe_allow_html=True)
    with col_info2:
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("## 🌿 نصائح العناية")
        st.write(plant["tips"])
        st.markdown("## 🌍 البيئة المناسبة")
        st.write(plant["location"])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Back button
    if st.button("⬅ العودة إلى الرئيسية", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()
    st.stop()

# ======================
# MAIN CONTENT
# ======================

# Show search bar only on home page (without label)
if st.session_state["page"] == "home":
    search = st.text_input("", placeholder="🔍 ابحث عن نبتة...", key="search_main")
else:
    search = ""

# ======================
# FILTER LOGIC
# ======================
filtered_plants = plants
if search:
    filtered_plants = [
        p for p in plants
        if search.lower() in (p.get("name_ar", "") or p.get("name", "")).lower()
    ]

# ======================
# HOME PAGE
# ======================
if st.session_state["page"] == "home":
    st.markdown("<h1 style='text-align: right;'>🌿 Napta</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not filtered_plants:
        st.warning("🚫 لا توجد نباتات مطابقة للبحث")
    else:
        # Display in responsive grid
        cols_per_row = 3
        for i in range(0, len(filtered_plants), cols_per_row):
            cols = st.columns(cols_per_row, gap="large")
            for j, plant in enumerate(filtered_plants[i:i+cols_per_row]):
                with cols[j]:
                    display_plant_card(plant, is_fav_page=False)

# ======================
# FAVORITES PAGE
# ======================
if st.session_state["page"] == "favorites":
    st.markdown("<h1 style='text-align: right;'>❤️ My Favorite Plants</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not fav_ids:
        st.info("✨ لا توجد مفضلات بعد... أضف نباتاتك المفضلة لرؤيتها هنا")
    else:
        fav_plants_data = supabase.table("plants").select("*").in_("id", fav_ids).execute().data
        if fav_plants_data:
            cols_per_row = 3
            for i in range(0, len(fav_plants_data), cols_per_row):
                cols = st.columns(cols_per_row, gap="large")
                for j, plant in enumerate(fav_plants_data[i:i+cols_per_row]):
                    with cols[j]:
                        display_plant_card(plant, is_fav_page=True)
        else:
            st.info("⚠️ لم نتمكن من تحميل النباتات المفضلة")
