import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import io

# SECTION 1: PAGE CONFIG
st.set_page_config(page_title="AI Sports Tournament Manager", page_icon="🏆", layout="wide")

# SECTION 2: UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(8,10,25,0.90), rgba(8,10,25,0.96)), 
                    url("https://images.unsplash.com/photo-1517649763962-0c623066013b");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .glowing-title {
        font-size: 3rem; font-weight: 800; color: #00ffcc; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# SECTION 10: API INTEGRATION
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API Key Missing!")
    st.stop()

genai.configure(api_key=api_key)

# SIDEBAR
with st.sidebar:
    st.header("Settings")
    sport = st.selectbox("Sport", ["Badminton", "Chess", "Throwball", "Cricket", "Futsal", "Table Tennis"])
    pts = st.number_input("Teams", min_value=2, value=8)
    res = st.number_input("Resources", min_value=1, value=2)
    tm = st.number_input("Hours", min_value=0.5, value=4.0)
    btn = st.button("Generate Plan")

if btn:
    try:
        # ISS MODEL NAME PAR HI 404 AATA HAI - YE FIXED HAI AB
        model = genai.GenerativeModel("models/gemini-1.5-flash") 
        response = model.generate_content(f"Plan a {sport} tournament for {pts} teams.")
        
        st.markdown('<div class="glowing-title">Tournament Plan</div>', unsafe_allow_html=True)
        st.write(response.text)
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
