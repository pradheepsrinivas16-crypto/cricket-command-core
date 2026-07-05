import streamlit as st
import pandas as pd
import numpy as np
import cv2
import requests
import json
import matplotlib.pyplot as plt
from google import genai

st.set_page_config(page_title="⚔️ CHAMPIONSHIP COMMAND CORE", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 🔑 CREDENTIAL CONFIGURATION (CLOUD SECURE)
# ==========================================
# Safely reads from secrets or sidebar fallback input without throwing KeyErrors!
secret_key = st.secrets.get("GEMINI_API_KEY", None)

if not secret_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
else:
    api_key = secret_key

client = None
api_ready = False
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        api_ready = True
    except Exception:
        pass

# ==========================================
# 📡 GLOBAL CLOUD INTELLIGENCE ROUTER
# ==========================================
def query_local_ollama(prompt, model_name="gemini-2.5-flash"):
    if not api_ready or not client:
        return "⚠️ Cloud GenAI node unconfigured. Please enter your Gemini API Key in the sidebar to activate the intelligence engine."
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Cloud Generation Fault: {str(e)}"

# Franchise Level Custom Theme
st.markdown("""
    <style>
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
    .status-alert { padding: 12px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 16px; margin: 15px 0; }
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
        balls_faced_window = st.slider("Batsman Lifecycle Progression (Balls Faced)", 1, 60, 5)
        
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
            with st.spinner("Compiling tactical dossier..."):
                scout_prompt = f"""
                You are a senior head performance director for a tier-1 international cricket squad.
                Analyze this profile using the Prasanna Agoram analytical framework.
                Target Batsman: {target_batsman}. Our Bowling Asset: {bowler_type}. Venue Profile: {match_venue}. Lifecycle Stage: {balls_faced_window} balls faced.
                Provide a professional pre-match scouting card for the team meeting. Format exactly with these headers:
                1. THE FIELD-SETTING TRAP: (Specify exactly where to place fielders to cut off their {leakage} metrics)
                2. LINE AND LENGTH ASSIGNMENT: (Exact tactical command for the bowler based on the {balls_faced_window} ball lifecycle stage)
                3. PSYCHOLOGICAL VECTOR: (How to exploit their phase-based strike rate change)
                """
                scout_report = query_local_ollama(scout_prompt)
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
            with st.spinner("Processing tactical field vectors via cloud engine..."):
                ollama_prompt = f"""
                You are an advanced digital twin system mimicking Pro Analyst Prasanna Agoram.
                Context: Score {st.session_state.current_score}/{st.session_state.current_wickets}. Active dot string: {st.session_state.consecutive_dots} consecutive dots. Pitch Wear: {pitch_wear}%.
                Surface Deck: {pitch_type}. Bowling: {bowler_profile}. Target Leakage: {leakage_sector}.
                Output a professional match strategy card under these two exact headers:
                1. DOT PRESSURE TRAP EXECUTOR: (How to structure the fielders right now to maintain the {st.session_state.consecutive_dots} dot pressure choke)
                2. BALL VARIATION SELECTION: (What variation should be delivered based on the current pitch wear layer of {pitch_wear}%)
                """
                analysis_result = query_local_ollama(ollama_prompt)
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
        if rgb_p is not None: dv1.image(rgb_p, caption="Historical Control Frame", use_container_width=True)
        if rgb_c is not None: dv2.image(rgb_c, caption="Active Match State Frame", use_container_width=True)

    with col_v2:
        st.subheader("🔬 4-Quadrant Kinematic Audit Logs")
        if st.button("🔍 Execute Comparative Biomechanics Assessment"):
            if not api_ready or not client:
                st.error("Provide functional Google API key to activate visual processing node.")
            elif bytes_p is None or bytes_c is None:
                st.warning("Both baseline anchor and active drift frames must be uploaded to perform comparison loops.")
            else:
                with st.spinner("Processing visual markers & joint alignment parameters..."):
                    try:
                        from google.genai import types
                        p_part = types.Part.from_bytes(data=bytes_p, mime_type='image/jpeg')
                        c_part = types.Part.from_bytes(data=bytes_c, mime_type='image/jpeg')
                        
                        vision_prompt = f"""
                        Act as an elite National Team Performance Director and Biomechanical Technical Coach.
                        Analyze these two frames for discipline: {discipline_type}. Image 1 is the PAST baseline anchor; Image 2 is the PRESENT active drift.
                        Decompile the visual changes and return a strict, professional analysis using these exact headers:
                        
                        ### 📈 PAST PROFILE MECHANICS
                        * **Core Structural Strength**: (Specify exactly what was stable, e.g., head position, foot stride, or shoulder loading alignment)
                        * **Controlled Vulnerability Boundary**: (What hidden trait was masked by high efficiency)
                        
                        ### 📉 PRESENT PERFORMANCE DRIFT
                        * **Identified Technical Failure Mode**: (Explicitly name the breakdown, e.g., dropped wrists, unbraced front leg, falling shoulder line)
                        * **Emergent Structural Weakness**: (How this geometric deviation prevents clean execution and triggers dismissal/leakage maps)
                        
                        ### 🛠️ PRESCRIPTIVE REPAIR DIRECTIVE
                        * **Biomechanical Correction Protocol**: (Step-by-step physical adjustment commands to eradicate the mistake immediately)
                        * **Drill Simulation Prescription**: (Specify 2 world-class professional practice cage drills to lock the correction down)
                        """
                        res = client.models.generate_content(model='gemini-2.5-flash', contents=[vision_prompt, p_part, c_part])
                        st.markdown(res.text)
                    except Exception as e:
                        st.error(f"Cloud Engine Fault: {e}")

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
            with st.spinner("Processing medical variables and loading scripts..."):
                load_prompt = f"""
                Act as the Chief Medical Officer and Elite Sports Scientist for a national cricket team.
                Analyze player: {p_name}. ACWR: {calc_acwr}. Pathological History: {injuries}. Sleep Efficiency: {sleep_efficiency}%.
                Generate a comprehensive, team-management ready recovery directive using these exact markdown headers:
                
                ### 🏋️‍♂️ HIGH-PERFORMANCE WORKOUT RECONSTRUCTION
                (Specify explicit physical protocols based on the workload state, e.g., complete off-loading, low-velocity isometric holds, or specific targeted kinetic chain activation work)
                
                ### 🥗 CLINICAL NUTRITION & BIO-INFUSION PLAN
                (Provide high-end, exact nutritional directives: macro target counts, specific anti-inflammatory additions, and recovery hydration targets to repair muscle tissues)
                
                ### ⏳ MATCH AVAILABILITY CONCLUSION
                * **Rested Rest Window Target**: (Provide an exact numerical conclusion on how many weeks and matches this player MUST sit out to safely normalize their ACWR balance)
                * **Playing-11 Re-entry Criteria**: (List 2 data markers required from fitness tests before clearing them to return to active competition)
                """
                load_res = query_local_ollama(load_prompt)
                st.markdown(load_res)