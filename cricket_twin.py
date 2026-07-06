import streamlit as st
import pandas as pd
import numpy as np
import cv2
import requests
import json
import matplotlib.pyplot as plt
import os

# Set configuration safely without broken rcParams attributes
st.set_page_config(page_title="⚔️ CHAMPIONSHIP COMMAND CORE", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 📡 DYNAMIC LOCAL AI ENGINE (OLLAMA ROUTER)
# ==========================================
def query_local_ollama(prompt, context_data=None):
    """
    Queries your local Ollama instance running llama3. 
    Constructs a highly descriptive engineering and strategic prompt using the live slider data.
    """
    url = "http://localhost:11434/api/generate"
    ctx = context_data or {}
    mode = ctx.get("type", "general")
    
    # 🎯 Tab 1 Context Builder
    if mode == "scout":
        system_role = "You are a world-class professional cricket head coach and elite technical analyst."
        engineered_prompt = f"""
        {system_role}
        Analyze the following live match matchup data and compile an aggressive, detailed tactical strategy:
        - Target Batsman: {ctx.get('batsman')}
        - Deployed Bowler: {ctx.get('bowler')}
        - Venue Context: {ctx.get('venue')}
        - Balls Faced in Lifecycle: {ctx.get('balls')}
        
        Provide:
        1. THE FIELD-SETTING TRAP (Explicit positions tailored to the player and venue boundaries)
        2. LINE AND LENGTH ASSIGNMENT (Target delivery coordinates in meters)
        3. PSYCHOLOGICAL VECTOR (How to exploit their current lifecycle progression)
        """
        
    # 📊 Tab 2 Context Builder
    elif mode == "simulator":
        system_role = "You are a real-time cricket data scientist and live tactical strategist."
        engineered_prompt = f"""
        {system_role}
        Analyze this live match state snapshot to optimize our field placements and bowler variations:
        - Live Score State: {ctx.get('score')}
        - Active Dot Ball Pressure String: {ctx.get('dots')} consecutive dots
        - Pitch Surface Condition: {ctx.get('pitch_type')}
        - Pitch Deterioration Index: {ctx.get('wear')}%
        - Deployed Bowler Type: {ctx.get('bowler')}
        
        Provide:
        1. DOT PRESSURE TRAP EXECUTOR (How to squeeze or adjust the infield based on the dot string)
        2. BALL VARIATION SELECTION (Specific tactical deliveries optimized for the pitch wear factor)
        """
        
    # 🎥 Tab 3 Context Builder
    elif mode == "biomechanics":
        system_role = "You are an elite sports science biomechanist specializing in professional cricket kinematics."
        engineered_prompt = f"""
        {system_role}
        Perform a comprehensive kinematic audit comparing historical base control vectors to active match state drift.
        Discipline Under Assessment: {ctx.get('discipline')}
        
        Provide:
        1. PAST PROFILE MECHANICS (Optimal form control baseline details)
        2. PRESENT PERFORMANCE DRIFT (Technical breakdown of the failure mode)
        3. PRESCRIPTIVE REPAIR DIRECTIVE (Specific biomechanical correction protocols and training drills)
        """
        
    # 🏥 Tab 4 Context Builder
    elif mode == "medical":
        system_role = "You are a chief high-performance athletic director and sports medical specialist."
        engineered_prompt = f"""
        {system_role}
        Calculate an elite physiological medical intervention using these active loading variables:
        - Athlete Name: {ctx.get('name')}
        - Acute-to-Chronic Workload Ratio (ACWR): {ctx.get('acwr')}
        - Pathological Medical History: {ctx.get('injuries')}
        - Polysomnographic Sleep Efficiency: {ctx.get('sleep')}%
        
        Provide:
        1. HIGH-PERFORMANCE WORKOUT RECONSTRUCTION (Specific loading or unloading protocols based on the ACWR)
        2. CLINICAL NUTRITION & BIO-INFUSION PLAN (Inflammatory macro-intake recommendation)
        3. MATCH AVAILABILITY CONCLUSION (Clear playing-11 re-entry clearance or shutdown directive)
        """
    else:
        engineered_prompt = prompt

    payload = {
        "model": "llama3",
        "prompt": engineered_prompt.strip(),
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"❌ Local Ollama Error: Server status code {response.status_code}"
    except Exception:
        return """
        ⚠️ **Ollama Connection Error!** Please ensure your local Ollama app is running in your terminal background via: `ollama run llama3`
        """

# ==========================================
# 🎨 BRAND SYSTEM UI DESIGN OVERLAYS
# ==========================================
st.markdown("""
    <style>
    #MainMenu, data-testid="stActionButtonIcon", .stDeployButton, footer, [data-testid="stManageAppButton"] {
        display: none !important;
    }
    header { visibility: hidden !important; }
    
    .reportview-container { background: #070d19; }
    .broadcast-header {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        padding: 25px; border-radius: 12px; border-bottom: 4px solid #3b82f6;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.5); text-align: left; margin-bottom: 25px;
    }
    .metric-box, .simulator-card {
        background: #1e293b; padding: 22px; border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.2); border-left: 5px solid #3b82f6;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.4); text-align: center; margin-bottom: 15px;
    }
    .label-title { color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }
    .value-display { color: #ffffff; font-size: 32px; font-weight: 800; margin-top: 4px; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="broadcast-header">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 800; letter-spacing: 1px;">⚔️ ELITE SQUAD PERFORMANCE ENGINE</h1>
        <p style="color: #3b82f6; margin: 6px 0 0 0; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 3px;">
            Tactical Trap Modeling, Dot-Ball Pressure Indices & Biomechanical Diagnostics
        </p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 TACTICAL DECK: Opponent Trap Modeler",
    "📊 LIVE SIMULATOR: Dot-Pressure Sandbox",
    "🎥 BIOMECHANICS: Structural Video Analyst",
    "🏥 ATHLETE BASE: Workload & Safety Core"
])

def process_vision_frame(uploaded_file, overlay_label):
    if uploaded_file is None: return None, None
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    cv2.line(img, (int(w*0.5), 0), (int(w*0.5), h), (59, 130, 246), 1)
    cv2.putText(img, f"PRO SCENE TARGET: {overlay_label}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (59, 130, 246), 2)
    rgb_view = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    _, buf = cv2.imencode(".jpg", img)
    return rgb_view, buf.tobytes()

# ==========================================
# MODULE 1: OPPOSITION TRAP MODELER
# ==========================================
with tab1:
    st.markdown("### 🔍 Strategic Opponent Weakness Dossier")
    st.write("---")
    col_scout_in, col_scout_out = st.columns([1, 1.3])

    with col_scout_in:
        st.subheader("📋 Targeted Setup")
        target_batsman = st.selectbox("Select Opposition Batsman Profile", ["Chris Gayle (LHB - Power Opening Anchor)", "Virat Kohli (RHB - Cover-Drive Dominant)", "Graeme Swann (SLA - Deflection Bias Athlete)"])
        bowler_type = st.selectbox("Our Tactical Attack Option", ["Express Right-Arm Fast-Bowler", "Left-Arm Quick Seam", "Mystery Wrist-Spinner"])
        match_venue = st.text_input("Match Location / Ground Analytics", "M. Chinnaswamy Stadium, Bengaluru (Small Boundaries / Flat Deck)")
        balls_faced_window = st.slider("Batsman Lifecycle Progression (Balls Faced)", 1, 60, 15)

        if "Chris Gayle" in target_batsman:
            leakage = "Covers & Square Leg Arc"
            vulnerability = "High vulnerability to incoming rapid full deliveries hitting the pads early on."
            strike_rate_phase = "SR 90 (First 25 Balls) -> SR 110 (Post 25)"
        else:
            leakage = "Off-Stump Corridor / Sweeper Coverage"
            vulnerability = "Prone to chasing away-swinging deliveries outside off stump early in the lifecycle."
            strike_rate_phase = "SR 75 (Initial Phase) -> SR 135 (Settled Phase)"

    with col_scout_out:
        st.subheader("📋 Pro Analyst Intelligence Streams")
        m_a, m_b = st.columns(2)
        m_a.markdown(f'<div class="metric-box" style="border-left-color: #3b82f6;"><div class="label-title">Core Leakage Sector Zone</div><div class="value-display" style="font-size:16px; margin-top:10px; color:#3b82f6;">{leakage}</div></div>', unsafe_allow_html=True)
        m_b.markdown(f'<div class="metric-box" style="border-left-color: #3b82f6;"><div class="label-title">Lifecycle Performance Curve</div><div class="value-display" style="font-size:14px; margin-top:12px;">{strike_rate_phase}</div></div>', unsafe_allow_html=True)

        st.write("---")
        st.markdown(f"**⚡ Current Technical Vulnerability Vector:** `{vulnerability}`")

        if st.button("🔥 Compile Head-Coach Pre-Match Kill-Plan"):
            with st.spinner("Compiling tactical dossier via local AI..."):
                scout_report = query_local_ollama("", context_data={
                    "type": "scout", "batsman": target_batsman, "bowler": bowler_type, "venue": match_venue, "balls": balls_faced_window
                })
                st.info(scout_report)

# ==========================================
# MODULE 2: LIVE SIMULATOR WITH DOT-BALL PRESSURE TRACER
# ==========================================
with tab2:
    st.markdown("### 🎯 Game State Simulation & Pressure Profiling Engine")
    st.write("---")

    if "balls_simulated" not in st.session_state:
        st.session_state.balls_simulated = 0
        st.session_state.current_score = 0
        st.session_state.current_wickets = 0
        st.session_state.history_log = []
        st.session_state.pressure_tracker = []
        st.session_state.batter_balls_faced = 0
        st.session_state.consecutive_dots = 0  

    col_ctrl, col_sim = st.columns([1, 1.4])

    with col_ctrl:
        st.subheader("⚙️ Match Boundary Parameters")
        target_score = st.number_input("Target Score to Chase", min_value=1, value=165)
        pitch_type = st.selectbox("Pitch Deck Surface Condition", ["Flat Highway Track", "Green Mamba (Heavy Seam)", "Dry Crumbling Square (Turn)"])
        pitch_wear = st.slider("Live Pitch Wear Level (Deterioration Factor)", 0, 100, 10) 
        bowler_profile = st.selectbox("Active Opponent Bowler Target Profile", ["Express Right-Arm Fast", "Left-Arm Quick Seam", "Mystery Wrist-Spinner", "Orthodox Finger-Spinner"])

        st.markdown("**🔬 Active Tracking Injected Vectors:**")
        batsman_temperament = st.checkbox("Track First-25-Balls Volatility Curve", value=True)
        leakage_sector = st.selectbox("Target Concession Zone", ["Covers & Square Leg (41% Leakage)", "Straight / Long-On", "Vulnerable Behind Square"])

        st.write("---")
        c_btn1, c_btn2 = st.columns(2)
        sim_ball = c_btn1.button("🏏 Simulate Next Ball")
        reset_sim = c_btn2.button("🔄 Reset Match Deck")

        if reset_sim:
            st.session_state.balls_simulated = 0
            st.session_state.current_score = 0
            st.session_state.current_wickets = 0
            st.session_state.history_log = []
            st.session_state.pressure_tracker = []
            st.session_state.batter_balls_faced = 0
            st.session_state.consecutive_dots = 0
            st.rerun()

    if sim_ball and st.session_state.current_wickets < 10 and st.session_state.balls_simulated < 120 and st.session_state.current_score < target_score:
        st.session_state.balls_simulated += 1
        st.session_state.batter_balls_faced += 1

        rand_val = np.random.rand()
        event = "0 runs"
        run_change, wicket_change = 0, 0

        wicket_chance = 0.05 + (pitch_wear * 0.001)
        boundaries = 0.14 - (pitch_wear * 0.0005)

        if st.session_state.consecutive_dots >= 3:
            wicket_chance += 0.08  
            boundaries += 0.06

        if batsman_temperament and st.session_state.batter_balls_faced <= 25:
            wicket_chance += 0.02
            boundaries += 0.04

        if rand_val < wicket_chance:
            event = "❌ OUT! Wicket Falls! Pressure Threshold Broken!"
            wicket_change = 1
            st.session_state.batter_balls_faced = 0 
            st.session_state.consecutive_dots = 0
        elif rand_val < (wicket_chance + boundaries):
            hit = np.random.choice([4, 6], p=[0.7, 0.3])
            event = f"💥 BOUNDARY! Cleared {leakage_sector.split(' ')[0]} for {hit}!"
            run_change = hit
            st.session_state.consecutive_dots = 0
        else:
            run_change = np.random.choice([0, 1, 2, 3], p=[0.5, 0.35, 0.12, 0.03])
            if run_change == 0:
                st.session_state.consecutive_dots += 1
                event = f"🎯 DOT BALL! Consecutive Dots: {st.session_state.consecutive_dots}"
            else:
                st.session_state.consecutive_dots = 0
                event = f"🏃 Rotation: {run_change} run(s) into space."

        st.session_state.current_score += run_change
        st.session_state.current_wickets += wicket_change

        over_num = (st.session_state.balls_simulated - 1) // 6
        ball_num = ((st.session_state.balls_simulated - 1) % 6) + 1
        st.session_state.history_log.insert(0, f"Over {over_num}.{ball_num} vs {bowler_profile}: {event}")

    balls_left = max(0, 120 - st.session_state.balls_simulated)
    runs_needed = max(0, target_score - st.session_state.current_score)
    overs_elapsed_str = f"{st.session_state.balls_simulated // 6}.{st.session_state.balls_simulated % 6}"

    current_crr = round((st.session_state.current_score / (st.session_state.balls_simulated / 6)), 2) if st.session_state.balls_simulated > 0 else 0.0
    current_rrr = round((runs_needed / (balls_left / 6)), 2) if balls_left > 0 else 0.0

    pressure_index = int(min(100, max(0, (current_rrr * 6) + (st.session_state.current_wickets * 8) + (st.session_state.consecutive_dots * 12))))
    if st.session_state.balls_simulated > 0 and (len(st.session_state.pressure_tracker) == 0 or st.session_state.balls_simulated == len(st.session_state.pressure_tracker) + 1):
        st.session_state.pressure_tracker.append(pressure_index)

    with col_sim:
        st.subheader("📊 Tactical Scoreboard Telemetry")
        m_s1, m_s2, m_s3 = st.columns(3)
        m_s1.markdown(f'<div class="simulator-card"><div class="label-title">Match Scorecard</div><div class="value-display">{st.session_state.current_score} / {st.session_state.current_wickets}</div><p style="margin:0; color:#8da2bb;">Overs completed: {overs_elapsed_str}</p></div>', unsafe_allow_html=True)
        m_s2.markdown(f'<div class="simulator-card"><div class="label-title">Active Dot String</div><div class="value-display" style="color: #ff4b4b;">{st.session_state.consecutive_dots} Dots</div><p style="margin:0; color:#8da2bb;">Batter Balls Faced: {st.session_state.batter_balls_faced}</p></div>', unsafe_allow_html=True)
        m_s3.markdown(f'<div class="simulator-card"><div class="label-title">Live Match Strain</div><div class="value-display">{pressure_index}%</div><p style="margin:0; color:#8da2bb;">Required Run Rate: {current_rrr}</p></div>', unsafe_allow_html=True)

        if len(st.session_state.pressure_tracker) > 0:
            fig, ax = plt.subplots(figsize=(7, 1.8), facecolor='#060b13')
            ax.set_facecolor('#0b131e')
            ax.plot(st.session_state.pressure_tracker, color='#3b82f6', linewidth=2)
            ax.tick_params(colors='white', labelsize=8)
            ax.set_ylim(0, 100)
            ax.grid(color='#ffffff', linestyle='--', linewidth=0.5, alpha=0.1)
            st.pyplot(fig)

    st.write("---")
    st.subheader("🧠 Live Tactical Engine Intelligence Output")
    if st.button("🤖 Run Strategic Recommendation Inference"):
        if st.session_state.balls_simulated == 0:
            st.warning("Initialize state variables by simulating at least one delivery stream.")
        else:
            with st.spinner("Processing local tactical parameters..."):
                analysis_result = query_local_ollama("", context_data={
                    "type": "simulator", "dots": st.session_state.consecutive_dots, "wear": pitch_wear, "score": f"{st.session_state.current_score}/{st.session_state.current_wickets}", "bowler": bowler_profile, "pitch_type": pitch_type
                })
                st.info(analysis_result)

# ==========================================
# MODULE 3: BIOMECHANICAL SUITE
# ==========================================
with tab3:
    st.markdown("### 🎥 Biomechanical Video Kinematic Vector Deck")
    st.write("---")

    col_v1, col_v2 = st.columns([1.2, 1])

    with col_v1:
        st.subheader("📤 Structural Target Analysis Configuration")
        discipline_type = st.radio("Select Performance Discipline", ["Batting Mechanics Analysis", "Bowling Release Mechanics"], horizontal=True)

        v_past = st.file_uploader("Upload PAST Baseline Video Frame (Optimal Form Baseline Anchor)", type=["png", "jpg", "jpeg"], key="vp")
        v_pres = st.file_uploader("Upload PRESENT Active Video Frame (Current Mechanics Decay Profile)", type=["png", "jpg", "jpeg"], key="vpr")

        rgb_p, bytes_p = process_vision_frame(v_past, "PAST_OPTIMAL")
        rgb_c, bytes_c = process_vision_frame(v_pres, "PRESENT_DRIFT")

        dv1, dv2 = st.columns(2)
        if rgb_p is not None: 
            dv1.image(rgb_p, caption="Historical Control Frame", use_container_width=True)
        if rgb_c is not None: 
            dv2.image(rgb_c, caption="Active Match State Frame", use_container_width=True)

    with col_v2:
        st.subheader("🔬 4-Quadrant Kinematic Audit Logs")
        if st.button("🔍 Execute Comparative Biomechanics Assessment"):
            if bytes_p is None or bytes_c is None:
                st.warning("Both baseline anchor and active drift frames must be uploaded to perform comparison loops.")
            else:
                with st.spinner("Processing alignment deviations via local AI..."):
                    bio_report = query_local_ollama("", context_data={
                        "type": "biomechanics", "discipline": discipline_type
                    })
                    st.markdown(bio_report)

# ==========================================
# MODULE 4: ATHLETE BASE & RECOVERY MATRIX
# ==========================================
with tab4:
    st.markdown("### 🏥 Acute-to-Chronic Clinical Fatigue & Prescription Suite")
    st.write("---")
    col_l1, col_l2 = st.columns([1, 1.2])

    with col_l1:
        st.subheader("📡 High-Performance Telemetry Inputs")
        p_name = st.text_input("Registered Athlete Profile", "Jasprit Bumrah (Fast Bowler)")
        acute = st.slider("7-Day Acute Fatigue Loading Index", 1.0, 15.0, 9.2, step=0.1)
        chronic = st.slider("28-Day Chronic Base Capacity Index", 1.0, 15.0, 5.8, step=0.1)
        injuries = st.multiselect("Pathological History Registry", ["Lumbar Spine Stress Fracture", "Patellar Tendonitis", "Grade 2 Hamstring Strain"], default=["Lumbar Spine Stress Fracture"])
        sleep_efficiency = st.slider("Polysomnographic Sleep Efficiency Level (%)", 30, 100, 74)

        calc_acwr = round(acute / max(0.1, chronic), 2)
        risk_pct = min(98, int((calc_acwr * 38) + (len(injuries) * 12) - (sleep_efficiency - 70) * 0.2))

    with col_l2:
        st.subheader("📊 Workload Matrix Outputs")
        cl1, cl2 = st.columns(2)
        cl1.markdown(f'<div class="metric-box"><div class="label-title">Calculated Workload Ratio (ACWR)</div><div class="value-display">{calc_acwr}</div></div>', unsafe_allow_html=True)
        cl2.markdown(f'<div class="metric-box"><div class="label-title">Tissue Breakdown Risk Probability</div><div class="value-display">{risk_pct}%</div></div>', unsafe_allow_html=True)

        st.write("---")
        if st.button("📋 Compile Clinical Recovery & Selection Manifesto"):
            with st.spinner("Compiling clinical metrics through local engine..."):
                load_res = query_local_ollama("", context_data={
                    "type": "medical", "name": p_name, "acwr": calc_acwr, "injuries": injuries, "sleep": sleep_efficiency
                })
                st.markdown(load_res)