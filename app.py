import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Pro Sports Planner", page_icon="🏟️", layout="wide")

# --- PRO SPORTS UI/UX ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.9)), 
                    url('https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        color: #f8fafc;
    }
    
    /* Result Glass Card */
    .plan-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56, 189, 248, 0.5);
        padding: 30px;
        border-radius: 20px;
        color: #f1f5f9;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Neon Accents */
    h1 {
        color: #22c55e !important; /* Sports Green */
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
    }

    /* Action Button */
    div.stButton > button:first-child {
        background: #22c55e !important;
        color: #000 !important;
        border: none !important;
        font-weight: 900 !important;
        height: 60px;
        border-radius: 10px !important;
        transition: 0.4s ease;
    }
    
    div.stButton > button:first-child:hover {
        background: #4ade80 !important;
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(34, 197, 94, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIG ---
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- APP ---
st.write("<h1 style='text-align: center;'>🏟️ ARENA MASTER AI</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown("### 🏟️ Tournament Hub")
    t_name = st.text_input("Tournament Name", "Iqra Premier League")
    sport = st.selectbox("Sport Type", ["Cricket", "Football", "Badminton", "Chess", "Table Tennis"])
    teams = st.number_input("Total Teams", 2, 32, 8)
    
    st.info("💡 AI will auto-assign Courts and Timings.")
    btn = st.button("READY TO PLAY? 🚀")

with col2:
    st.markdown("### 📅 Match Schedule & Ground Info")
    if btn:
        with st.spinner("Assigning Courts and Timings..."):
            try:
                # Optimized prompt for Timings and Courts
                prompt = f"""
                Create a professional {sport} tournament plan for '{t_name}' with {teams} teams.
                IMPORTANT: 
                - Assign specific Court Numbers or Ground Sections for each match.
                - Provide exact Start and End Timings for each slot.
                - Format as a clean schedule list.
                - End with a 'Referee Guidelines' section.
                """
                response = model.generate_content(prompt)
                st.markdown(f'<div class="plan-card">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.write("---")
        st.caption("Enter details and generate to see the Arena Map.")

st.write("---")
st.markdown("<p style='text-align: center; opacity: 0.6;'>Developer: Talib Hussain | IU Sports Tech</p>", unsafe_allow_html=True)
