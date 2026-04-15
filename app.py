import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# SECTION 1 & 2: CONFIG & UI
st.set_page_config(page_title="AI Sports Tournament Manager", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(8,10,25,0.90), rgba(8,10,25,0.96)), 
                    url("https://images.unsplash.com/photo-1517649763962-0c623066013b");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    .glowing-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00ffcc, #00bfff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# SECTION 10: API INTEGRATION
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY Missing! Please set it in Cloud Run Environment Variables.")
    st.stop()

genai.configure(api_key=api_key)

# SECTION 5: SESSION STATE
if 'data' not in st.session_state:
    st.session_state.data = None

# SECTION 3: SIDEBAR
with st.sidebar:
    st.title("⚙️ Tournament Settings")
    sport = st.selectbox("Select Sport", ["Badminton", "Chess", "Throwball", "Cricket", "Futsal", "Table Tennis"])
    participants = st.number_input("Participants/Teams", min_value=2, value=8)
    resources = st.number_input("Resources (Courts/Boards)", min_value=1, value=2)
    time_avail = st.number_input("Available Time (Hours)", min_value=0.5, value=4.0)
    
    gen_btn = st.button("👉 Generate Smart Tournament Plan")
    if st.button("Reset Inputs"):
        st.session_state.data = None
        st.rerun()

# SECTION 4 & 6-9: SMART ENGINES
if gen_btn:
    with st.spinner("🚀 AI is crafting the perfect tournament schedule..."):
        # Format Engine
        if participants <= 8: fmt = "Knockout"
        elif participants <= 20: fmt = "Round Robin"
        else: fmt = "Swiss System"
        
        # Duration Engine
        dur_map = {"Badminton": 20, "Chess": 30, "Throwball": 25, "Cricket": 45, "Futsal": 40, "Table Tennis": 15}
        m_dur = dur_map.get(sport, 20)
        
        # Metrics Calculation
        est_matches = (participants - 1) if fmt == "Knockout" else (participants * (participants - 1) // 2)
        parallel = min(resources, participants // 2)
        efficiency = min(100, int(((est_matches * m_dur) / (time_avail * 60 * parallel)) * 100)) if parallel > 0 else 0
        
        prompt = f"""
        Role: Professional Sports Planner. Create a {fmt} {sport} tournament.
        Context: {participants} teams, {resources} resources, {time_avail} hours.
        Match duration: {m_dur} mins. 
        Requirements:
        1. Format Recommendation.
        2. Match Schedule (Times, Courts).
        3. Rules (Scoring, Tie-breaks, Fair-play, Eligibility).
        Return clean markdown.
        """
        
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            # Fixture Generator (Section 12)
            fixtures = [{"Match": f"Match {i+1}", "Teams": f"TBD vs TBD"} for i in range(min(est_matches, 10))]
            
            st.session_state.data = {
                "response": response.text,
                "metrics": {"teams": participants, "matches": est_matches, "parallel": parallel, "eff": efficiency},
                "fixtures": pd.DataFrame(fixtures),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("Tournament Plan Generated Successfully!")
        except Exception as e:
            st.error(f"AI Error: {str(e)}")

# UI DISPLAY
st.markdown('<div class="glowing-title">AI Sports Tournament Manager</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc; font-size:1.2rem;'>AI-powered tournament format selection and smart scheduling system</p>", unsafe_allow_html=True)

if st.session_state.data:
    d = st.session_state.data
    
    # SECTION 16: ANALYTICS
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Teams", d["metrics"]["teams"])
    col2.metric("Matches", d["metrics"]["matches"])
    col3.metric("Parallel Games", d["metrics"]["parallel"])
    col4.metric("Efficiency Score", f"{d['metrics']['eff']}%")
    
    st.progress(d["metrics"]["eff"] / 100)
    
    # SECTION 19: OUTPUT
    tab1, tab2, tab3 = st.tabs(["📋 Full Plan", "📅 Fixtures", "📊 Leaderboard"])
    
    with tab1:
        st.success(f"Plan Generated at: {d['timestamp']}")
        st.markdown(d["response"])
        
    with tab2:
        st.dataframe(d["fixtures"], use_container_width=True)
        
    with tab3:
        lb = pd.DataFrame({"Team": [f"Team {i+1}" for i in range(participants)], "P": [0]*participants, "W": [0]*participants, "Pts": [0]*participants})
        st.dataframe(lb, use_container_width=True)

    # SECTION 20: EXPORTS
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.download_button("📩 Download TXT", d["response"], "plan.txt")
    c2.download_button("📊 Download CSV", d["fixtures"].to_csv(), "schedule.csv")
    
    # Simple PDF
    pdf_buf = io.BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=letter)
    c.drawString(100, 750, f"AI Sports Plan - {sport}")
    c.drawString(100, 730, f"Generated at: {d['timestamp']}")
    c.save()
    c3.download_button("📄 Download PDF", pdf_buf.getvalue(), "plan.pdf")
