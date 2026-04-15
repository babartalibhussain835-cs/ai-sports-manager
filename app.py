import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import io
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# SECTION 1: PAGE CONFIG
st.set_page_config(page_title="AI Sports Tournament Manager", page_icon="🏆", layout="wide")

# SECTION 2: CINEMATIC SPORTS STADIUM UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(8,10,25,0.90), rgba(8,10,25,0.96)), 
                    url("https://images.unsplash.com/photo-1517649763962-0c623066013b");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(15, 20, 35, 0.8);
        backdrop-filter: blur(10px);
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .glowing-title {
        font-size: 3.5rem; font-weight: 800;
        background: linear-gradient(to right, #00ffcc, #00bfff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# SECTION 10: API INTEGRATION
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY Missing! Please set it in Cloud Run Environment Variables.")
    st.stop()

# FIX: Configuration setup
genai.configure(api_key=api_key)

# SECTION 5: SESSION STATE MEMORY
if 'tournament_data' not in st.session_state:
    st.session_state.tournament_data = None

# SECTION 3: SIDEBAR INPUT PANEL
with st.sidebar:
    st.markdown("## ⚙️ Tournament Settings")
    sport = st.selectbox("Select Sport", ["Badminton", "Chess", "Throwball", "Cricket", "Futsal", "Table Tennis"])
    participants = st.number_input("Participants / Teams", min_value=2, value=8)
    resources = st.number_input("Resources (Courts/Boards/Grounds)", min_value=1, value=2)
    time_avail = st.number_input("Available Time (Hours)", min_value=0.5, value=4.0)
    
    col_a, col_b = st.columns(2)
    with col_a:
        generate_btn = st.button("Generate Plan")
    with col_b:
        if st.button("Reset Inputs"):
            st.session_state.tournament_data = None
            st.rerun()

# SECTION 4: INPUT VALIDATION
if generate_btn:
    if participants < 2 or resources < 1 or time_avail <= 0:
        st.warning("Please ensure participants ≥ 2, resources ≥ 1, and time > 0.")
        st.stop()

    with st.spinner("✨ AI is crafting the perfect tournament schedule..."):
        # SECTION 6: FORMAT ENGINE
        if participants <= 8: tournament_format = "Knockout"
        elif participants <= 20: tournament_format = "Round Robin"
        else: tournament_format = "Swiss System"

        # SECTION 7: DURATION ENGINE
        dur_map = {"Badminton": 20, "Chess": 30, "Throwball": 25, "Cricket": 45, "Futsal": 40, "Table Tennis": 15}
        match_dur = dur_map.get(sport, 20)

        # SECTION 14 & 15: ANALYTICS & FAIRNESS
        est_matches = (participants - 1) if tournament_format == "Knockout" else (participants * (participants - 1) // 2)
        parallel_matches = min(resources, participants // 2)
        efficiency = min(100, int(((est_matches * match_dur) / (time_avail * 60 * parallel_matches)) * 100)) if parallel_matches > 0 else 0
        fairness_score = 95 # Base score for AI distribution

        # SECTION 11: GEMINI CALL (FIXED MODEL NAME)
        try:
            # Model name fixed to avoid 404
            model = genai.GenerativeModel("gemini-1.5-flash") 
            
            prompt = f"""
            Act as a Senior Sports Planner. Create a {tournament_format} {sport} tournament for {participants} teams.
            Resources available: {resources} courts/grounds. Time limit: {time_avail} hours.
            Match Duration: {match_dur} minutes.
            
            Return:
            1. Format Recommendation & Why.
            2. Optimized Match Schedule with time slots and resource allocation.
            3. Professional Rulebook (Scoring, Tie-breaks, Fair-play, Eligibility).
            4. Resource optimization tips.
            """
            
            response = model.generate_content(prompt)
            
            # SECTION 12 & 13: FIXTURES & LEADERBOARD
            fixtures = pd.DataFrame([{"Round": "1", "Match": f"Match {i+1}", "Teams": "Team TBD vs Team TBD", "Resource": f"{sport} Area { (i % resources) + 1}"} for i in range(min(est_matches, 8))])
            leaderboard = pd.DataFrame({"Team": [f"Team {i+1}" for i in range(participants)], "Played": 0, "Wins": 0, "Losses": 0, "Points": 0, "Rank": "-"})
            
            st.session_state.tournament_data = {
                "ai_response": response.text,
                "fixtures": fixtures,
                "leaderboard": leaderboard,
                "metrics": {
                    "teams": participants, "matches": est_matches, "parallel": parallel_matches, 
                    "eff": efficiency, "time": time_avail, "fairness": fairness_score
                },
                "sport": sport,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("Tournament Plan Generated Successfully!")
        except Exception as e:
            st.error(f"AI Error: {str(e)}")

# SECTION 21: UI DISPLAY
st.markdown('<div class="glowing-title">AI Sports Tournament Manager</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc; font-size:1.2rem;'>AI-powered tournament format selection and smart scheduling system</p>", unsafe_allow_html=True)

if st.session_state.tournament_data:
    data = st.session_state.tournament_data
    
    # SECTION 16: ANALYTICS DASHBOARD
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Teams", data["metrics"]["teams"])
    col2.metric("Est. Matches", data["metrics"]["matches"])
    col3.metric("Parallel Games", data["metrics"]["parallel"])
    col4.metric("Efficiency", f"{data['metrics']['eff']}%")
    col5.metric("Fairness", f"{data['metrics']['fairness']}%")
    
    # SECTION 18: PROGRESS
    st.markdown("### 📈 Tournament Completion Tracker")
    st.progress(0) # Starts at 0%
    
    # SECTION 19: TABS FOR OUTPUT
    tab1, tab2, tab3, tab4 = st.tabs(["📋 AI Strategy & Rules", "📅 Smart Fixtures", "📊 Live Leaderboard", "💡 AI Suggestions"])
    
    with tab1:
        st.success(f"Strategy Generated at {data['timestamp']}")
        st.markdown(data["ai_response"])
        
    with tab2:
        st.dataframe(data["fixtures"], use_container_width=True)
        
    with tab3:
        st.table(data["leaderboard"])
        
    with tab4:
        st.info(f"AI Suggestion: Based on {data['metrics']['teams']} teams, {data['sport']} matches should be strictly timed to maintain the {data['metrics']['eff']}% efficiency.")

    # SECTION 20: EXPORT SYSTEM
    st.divider()
    ex1, ex2, ex3 = st.columns(3)
    ex1.download_button("Download TXT Plan", data["ai_response"], file_name="tournament_plan.txt")
    ex2.download_button("Download CSV Schedule", data["fixtures"].to_csv(index=False), file_name="schedule.csv")
    
    # PDF Generator
    pdf_buf = io.BytesIO()
    pdf = canvas.Canvas(pdf_buf, pagesize=letter)
    pdf.setTitle(f"{data['sport']} Tournament Plan")
    pdf.drawString(100, 750, f"Tournament: {data['sport']}")
    pdf.drawString(100, 730, f"Generated: {data['timestamp']}")
    pdf.save()
    ex3.download_button("Download PDF Report", pdf_buf.getvalue(), file_name="report.pdf")
