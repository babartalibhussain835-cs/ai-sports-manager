import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Elite Arena AI", page_icon="🏟️", layout="wide")

# --- ADVANCED UI/UX STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1504450758481-7338eba7524a?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        color: #ffffff;
    }
    
    /* Glassmorphism Effect */
    .stTextInput, .stSelectbox, .stNumberInput {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .plan-card {
        background: rgba(15, 23, 42, 0.9);
        border-left: 5px solid #00ff88;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1 {
        background: -webkit-linear-gradient(#00ff88, #00bdff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
    }

    /* Professional Glow Button */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00ff88, #00bdff) !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
        padding: 15px !important;
        border-radius: 50px !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
        transition: 0.3s ease;
    }

    div.stButton > button:first-child:hover {
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.7);
        transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIG (STABLE VERSION) ---
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- HEADER ---
st.write("<h1>ELITE ARENA AI</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; font-size: 1.2rem; color: #aaa;'>Powered by Gemini AI | Designed by Talib Hussain</p>", unsafe_allow_html=True)
st.write("---")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.markdown("### 🏆 Tournament Command Center")
    t_name = st.text_input("Tournament Name", "Iqra Champions League")
    
    c1, c2 = st.columns(2)
    with c1:
        sport = st.selectbox("Sport", ["Cricket", "Football", "Badminton", "Chess", "Basketball"])
    with c2:
        t_style = st.selectbox("Style", ["Knockout", "League (Round Robin)", "Group Stage + Finals"])
        
    teams = st.number_input("Total Teams", 2, 64, 8)
    
    st.markdown("#### 🏟️ Venue Details")
    venue = st.text_input("Ground/Court Location", "Main University Sports Complex")
    
    st.write("")
    generate_btn = st.button("GENERATE ELITE PLAN ⚡")

with col2:
    st.markdown("### 🏟️ Live Generated Arena Map")
    if generate_btn:
        with st.spinner("AI is analyzing teams and venue slots..."):
            try:
                prompt = f"""
                You are a world-class Sports Manager. 
                Create a professional {t_style} tournament plan for '{t_name}'.
                Sport: {sport}
                Teams: {teams}
                Location: {venue}
                
                Requirements:
                1. Match-by-match schedule with Time Slots.
                2. Specific Court/Ground assignments.
                3. A special section for 'Match Officials & Rules'.
                4. A weather-specific venue advisory for the players.
                Format everything with clean headings and bullet points.
                """
                response = model.generate_content(prompt)
                st.markdown(f'<div class="plan-card">{response.text}</div>', unsafe_allow_html=True)
                st.balloons() # Thora jashan bhi ho jaye!
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("👈 Enter tournament details on the left to activate AI Planner.")

st.write("---")
st.caption("Iqra University Project | © 2026 Talib Hussain")
