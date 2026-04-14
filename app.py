import streamlit as st
import google.generativeai as genai
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(
    page_title="AI Sports Tournament Manager",
    page_icon="🏆",
    layout="wide"
)

# --- 2. PREMIUM CSS (ULTRA MODERN LOOK) ---
st.markdown("""
    <style>
    /* Main Background with Dark Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 2px solid #38bdf8;
    }

    /* Professional Glassmorphism Cards */
    .stAlert, .stMarkdown div[data-testid="stMarkdownContainer"] p {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
    }

    /* Titles */
    h1 {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
    }

    /* Animated Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0ea5e9 0%, #6366f1 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 20px;
        width: 100%;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    div.stButton > button:first-child:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
        border: none;
    }

    /* Styling Inputs */
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
        background-color: #1e293b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI CONFIGURATION (FIXED MODEL) ---
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Using the most stable model name for Cloud Run
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 4. APP LAYOUT ---
st.write("<h1>🏆 AI SPORTS TOURNAMENT MASTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Intelligently generating tournament formats, schedules, and rules.</p>", unsafe_allow_html=True)
st.write("---")

# Main Columns
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### ⚙️ Settings")
    t_name = st.text_input("Tournament Name", value="Champions Cup 2026")
    sport = st.selectbox("Sport Category", ["Cricket", "Football", "Badminton", "Chess", "Basketball", "Esports"])
    teams = st.number_input("Total Teams", min_value=2, max_value=64, value=8)
    
    generate_btn = st.button("Generate Plan ✨")

with col2:
    st.markdown("### 📋 AI Generated Plan")
    if generate_btn:
        if not api_key:
            st.error("Error: API Key is missing. Add it to Cloud Run Environment Variables.")
        else:
            with st.spinner("AI is crafting your tournament strategy..."):
                try:
                    prompt = f"""
                    As an expert Sports Manager, create a detailed tournament plan for '{t_name}'.
                    Sport: {sport}
                    Teams: {teams}
                    Include:
                    1. Tournament Format (Knockout/Round Robin)
                    2. Match Schedule (Day by Day)
                    3. Basic Rules & Fair Play Guidelines
                    4. A short motivational quote for the athletes.
                    Format the output nicely using bullet points.
                    """
                    response = model.generate_content(prompt)
                    st.success("Your plan is ready!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    else:
        st.info("Fill in the details on the left and hit the magic button!")

# --- FOOTER ---
st.write("---")
st.markdown(f"<p style='text-align: center; color: #64748b;'>Built with ❤️ by <b>Talib Hussain</b> | IU Student Project</p>", unsafe_allow_html=True)
