import streamlit as st
from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

try:
    response = supabase.table("plants").select("*").execute()
    data = response.data
    st.write(data)

except Exception as e:
    st.error("🔥 ERROR DETAILS:")
    st.write(e)
