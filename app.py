import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Sports Manager", page_icon="🏟️", layout="wide")

# --- CUSTOM UI/UX ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(10, 15, 30, 0.85), rgba(10, 15, 30, 0.85)), 
                    url('https://images.unsplash.com/photo-1504450758481-7338eba7524a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        color: #ffffff;
    }
    
    /* Branding Header */
    .brand-header {
        text-align: center;
        padding: 20px;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 20px;
        border: 1px dashed #22c55e;
        margin-bottom: 30px;
    }

    .plan-card {
        background: rgba(15, 23, 42, 0.9);
        border-left: 5px solid #22c55e;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }

    h1 { color: #22c55e !important; font-size: 3rem !important; margin-bottom: 0px !important; }
    h3 { color: #38bdf8 !important; }
    
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #22c55e, #16a34a) !important;
        color: white !important;
        font-weight: 800 !important;
        height: 55px;
        width: 100%;
        border-radius: 50px !important;
        border: none !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AI CONFIG ---
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_ai_plan(t_name, sport, teams, venue):
    # Try multiple models to bypass the 404 issue
    for m_name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(m_name)
            prompt = f"""
            System: You are the 'AI SPORTS MANAGER'. 
            Task: Create a tournament plan for '{t_name}' at '{venue}'.
            Sport: {sport} | Teams: {teams}
            
            Format:
            1. ARENA ALLOCATION: Assign specific Court/Pitch numbers.
            2. TIME SLOTS: Provide exact match timings (e.g., 10:00 AM - 11:00 AM).
            3. FIXTURES: List the matches clearly.
            4. MANAGER'S NOTE: A professional tip for the event.
            """
            response = model.generate_content(prompt)
            return response.text
        except: continue
    return "Error: Connecting to AI Manager failed."

# --- MAIN APP INTERFACE ---
st.markdown("""
    <div class="brand-header">
        <h1>AI SPORTS MANAGER</h1>
        <p style='color: #38bdf8; font-weight: bold; font-size: 1.2rem;'>🏟️ ARENA COMMAND CENTER</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.markdown("### ⚙️ Setup Hub")
    t_name = st.text_input("Project / Tournament Name", "Iqra Champions League")
    venue = st.text_input("Venue / Ground Name", "Main University Sports Complex")
    sport = st.selectbox("Sport Category", ["Cricket", "Football", "Badminton", "Chess", "Tennis"])
    teams = st.number_input("Total Teams", 2, 64, 8)
    
    st.write("")
    generate_btn = st.button("Deploy AI Manager 🚀")

with col2:
    st.markdown("### 📊 Live Generated Arena Map")
    if generate_btn:
        with st.spinner("AI Manager is calculating arena slots..."):
            result = generate_ai_plan(t_name, sport, teams, venue)
            st.markdown(f'<div class="plan-card">{result}</div>', unsafe_allow_html=True)
    else:
        st.info("Fill the details and click 'Deploy' to see the AI Sports Manager in action.")

st.write("---")
st.markdown("<p style='text-align: center; opacity: 0.5;'>Talib Hussain | Computer Science Student | IU Project</p>", unsafe_allow_html=True)
