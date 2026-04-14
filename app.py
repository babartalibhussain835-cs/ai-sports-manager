import streamlit as st
import google.generativeai as genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="AI Sports Manager Pro", page_icon="🏆", layout="wide")

# --- 2. ELITE DASHBOARD UI ---
st.markdown("""
    <style>
    /* Dark Theme with Contrast */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Input Field Styling - For readability */
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        background-color: #161b22 !important;
        color: #22c55e !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-weight: bold;
    }

    /* Green Labels */
    label p {
        color: #22c55e !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        letter-spacing: 1px;
    }

    /* Header Branding */
    .header-container {
        text-align: center;
        padding: 40px;
        background: linear-gradient(90deg, #0f172a, #1e293b);
        border-radius: 20px;
        border: 2px solid #22c55e;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.2);
    }

    .header-container h1 {
        color: #22c55e !important;
        font-size: 3.5rem !important;
        margin-bottom: 5px !important;
    }

    /* Result Arena Box */
    .arena-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #22c55e;
        padding: 30px;
        border-radius: 15px;
        color: #e6edf3;
        font-family: 'Courier New', monospace;
    }

    /* Pro Button */
    div.stButton > button:first-child {
        background: #22c55e !important;
        color: #000 !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        height: 60px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(34, 197, 94, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ARENA LOGIC ---
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_arena_map(t_name, venue, sport, teams):
    # Stabilized model calling
    model_list = ["gemini-1.5-flash", "gemini-pro"]
    for m_name in model_list:
        try:
            model = genai.GenerativeModel(m_name)
            prompt = f"""
            As an AI Sports Manager, generate a professional Arena Plan.
            Tournament: {t_name}
            Venue: {venue}
            Sport: {sport} | Teams: {teams}
            
            Structure:
            1. ARENA ALLOCATION (Court/Ground Nos)
            2. MASTER SCHEDULE (Exact Time Slots)
            3. MANAGER'S RULES (Fair Play & Venue Conduct)
            
            Be precise with timings and ground assignments.
            """
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "Error: AI System currently unavailable. Please check API settings."

# --- 4. INTERFACE ---
st.markdown("""
    <div class="header-container">
        <h1>AI SPORTS MANAGER</h1>
        <p style='color: #38bdf8; font-weight: bold;'>ARENA COMMAND & CONTROL CENTER</p>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([1, 1.6], gap="large")

with left:
    st.markdown("### ⚙️ SETUP HUB")
    project_name = st.text_input("PROJECT / TOURNAMENT NAME", value="Iqra Champions Cup")
    ground_name = st.text_input("VENUE NAME", value="Main University Complex")
    sport_type = st.selectbox("SPORT CATEGORY", ["Cricket", "Football", "Badminton", "Tennis", "Chess"])
    team_count = st.number_input("TOTAL TEAMS", 2, 64, 8)
    
    st.write("---")
    if st.button("GENERATE TOURNAMENT ARENA ✨"):
        with st.spinner("AI is calculating arena slots..."):
            st.session_state.plan = generate_arena_map(project_name, ground_name, sport_type, team_count)
    
with right:
    st.markdown("### 📋 GENERATED ARENA MAP")
    if 'plan' in st.session_state:
        st.markdown(f'<div class="arena-box">{st.session_state.plan}</div>', unsafe_allow_html=True)
    else:
        st.info("Input settings and click Generate to see the Arena Command Map.")

st.write("---")
st.markdown("<p style='text-align: center; opacity: 0.5;'>Talib Hussain | Computer Science Student | IU FINAL PROJECT</p>", unsafe_allow_html=True)
