import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Sports Tournament Manager",
    page_icon="🏆",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-title {
        font-size: 50px;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    .stButton>button {
        background: linear-gradient(to right, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Tournament Settings")

sport = st.sidebar.selectbox(
    "Select Sport",
    ["Badminton", "Chess", "Throwball", "Cricket", "Futsal", "Table Tennis"]
)

participants = st.sidebar.number_input("Number of Participants/Teams", min_value=2, value=8)
resources = st.sidebar.number_input("Available Resources (Courts/Boards/Grounds)", min_value=1, value=2)
time_available = st.sidebar.number_input("Total Time Available (Hours)", min_value=0.5, value=4.0, step=0.5)

generate_btn = st.sidebar.button("👉 Generate Smart Tournament Plan", use_container_width=True)

# --- APP HEADER ---
st.markdown('<h1 class="main-title">AI Sports Tournament Manager</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligently generating tournament formats, optimized match schedules, and fair rules using AI.</p>', unsafe_allow_html=True)
st.divider()

# --- HELPER FUNCTIONS & LOGIC ---
def get_suggested_format(p_count):
    if p_count <= 8:
        return "Single Elimination Knockout"
    elif 9 <= p_count <= 20:
        return "Round Robin"
    else:
        return "Swiss System"

def call_gemini_ai(sport, participants, resources, time, suggested_format):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Missing Gemini API Key. Please set the GEMINI_API_KEY environment variable.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Act as a professional sports tournament director. 
    Create a tournament plan for a {sport} tournament.
    - Participants: {participants}
    - Resources: {resources} (e.g. courts/tables)
    - Time Limit: {time} hours
    - Suggested Primary Format: {suggested_format}

    Output the response in exactly these 3 sections without markdown code blocks:

    SECTION 1: Tournament Format Recommendation
    Explain why this format is optimal for {participants} participants and {resources} resources within {time} hours.

    SECTION 2: Optimized Match Schedule
    Provide a detailed table or list with time slots, resource allocation, and parallel match logic. Ensure maximum efficiency and minimum idle time.

    SECTION 3: Tournament Rules
    Provide 3 simple, clear, and fair rules for this tournament.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"AI Generation Error: {str(e)}")
        return None

# --- MAIN LOGIC ---
if generate_btn:
    # Validation
    if participants < 2 or resources < 1 or time_available <= 0:
        st.warning("Please provide valid tournament parameters in the sidebar.")
    else:
        suggested_fmt = get_suggested_format(participants)
        
        with st.spinner("AI is crafting the perfect tournament schedule... Please wait ⏳"):
            ai_output = call_gemini_ai(sport, participants, resources, time_available, suggested_fmt)
            
            if ai_output:
                st.session_state['result'] = ai_output
                st.session_state['inputs'] = {
                    "sport": sport,
                    "teams": participants,
                    "hours": time_available,
                    "resources": resources
                }
                st.success("Tournament Plan Generated Successfully! 🎉")

# --- DISPLAY RESULTS ---
if 'result' in st.session_state:
    res = st.session_state['inputs']
    
    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sport", res['sport'])
    col2.metric("Total Teams/Players", res['teams'])
    col3.metric("Time Limit", f"{res['hours']} hrs")
    col4.metric("Resources", res['resources'])
    
    st.divider()
    
    raw_text = st.session_state['result']
    sections = raw_text.split("SECTION")
    
    # Section 1: Format
    if len(sections) > 1:
        st.subheader("🏆 Tournament Format Recommendation")
        st.info(sections[1].replace("1:", "").strip())
        
    # Section 2: Schedule
    if len(sections) > 2:
        st.subheader("📅 Optimized Match Schedule")
        st.write(sections[2].replace("2:", "").strip())
        
    # Section 3: Rules
    if len(sections) > 3:
        with st.expander("📜 View Tournament Rules"):
            st.write(sections[3].replace("3:", "").strip())
else:
    st.info("Configure the tournament details in the sidebar and click 'Generate' to begin.")