import streamlit as st
import google.generativeai as genai
import os

# Page Settings
st.set_page_config(page_title="AI Arena Manager", page_icon="🏆", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .header-style {
        text-align: center;
        padding: 30px;
        background-color: #1a1c24;
        border-radius: 15px;
        border: 2px solid #22c55e;
        margin-bottom: 25px;
    }
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        background-color: #262730 !important;
        color: #22c55e !important;
        border: 1px solid #444 !important;
    }
    label p { color: #22c55e !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .result-card {
        background-color: #1a1c24;
        border-left: 10px solid #22c55e;
        padding: 25px;
        border-radius: 10px;
    }
    div.stButton > button:first-child {
        background-color: #22c55e !important;
        color: black !important;
        font-weight: 900 !important;
        height: 55px;
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# AI Setup
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_response(prompt):
    # Multiple model fallback for 100% success
    for m in ["gemini-1.5-flash", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(m)
            return model.generate_content(prompt).text
        except: continue
    return "Error: AI not responding. Check API key."

# Header
st.markdown("<div class='header-style'><h1>🏆 AI SPORTS ARENA MANAGER</h1><p>The Ultimate Tournament Command Center</p></div>", unsafe_allow_html=True)

left, right = st.columns([1, 1.5], gap="large")

with left:
    st.subheader("📋 SETTINGS")
    t_name = st.text_input("TOURNAMENT NAME", "Iqra Champions Cup")
    venue = st.text_input("VENUE / GROUND NAME", "Main Sports Complex")
    sport = st.selectbox("SPORT CATEGORY", ["Cricket", "Football", "Badminton", "Tennis", "Chess"])
    teams = st.number_input("TOTAL TEAMS", 2, 64, 8)
    
    st.write("---")
    if st.button("GENERATE ARENA PLAN ✨"):
        prompt = f"Create a tournament schedule for {t_name} at {venue}. Sport: {sport}, Teams: {teams}. Assign Court/Ground numbers and exact time slots."
        st.session_state.arena_plan = get_response(prompt)

with right:
    st.subheader("🏟️ GENERATED ARENA MAP")
    if 'arena_plan' in st.session_state:
        st.markdown(f"<div class='result-card'>{st.session_state.arena_plan}</div>", unsafe_allow_html=True)
    else:
        st.info("Fill the details and generate your professional plan.")

st.write("---")
st.markdown("<p style='text-align: center; opacity: 0.5;'>Talib Hussain | CS Student | Iqra University Project</p>", unsafe_allow_html=True)
