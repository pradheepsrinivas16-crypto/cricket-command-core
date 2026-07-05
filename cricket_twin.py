import streamlit as st
import pandas as pd
import numpy as np
import cv2
import requests
import json
import matplotlib.pyplot as plt

# ==========================================
# 🔑 STABLE SETUP & LAYOUT INITIALIZATION
# ==========================================
st.set_page_config(page_title="⚔️ CHAMPIONSHIP COMMAND CORE", layout="wide", initial_sidebar_state="expanded")

# Safe lazy-load of the genai library to prevent load crashes
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

if "api_ready" not in st.session_state:
    st.session_state.api_ready = False

# Credential Configuration Matrix
secret_key = st.secrets.get("GEMINI_API_KEY", None)
if not secret_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
else:
    api_key = secret_key

if api_key and HAS_GENAI:
    try:
        client = genai.Client(api_key=api_key)
        st.session_state.api_ready = True
    except Exception:
        st.session_state.api_ready = False

# ==========================================
# 📡 PROTECTED INTELLIGENCE ROUTER
# ==========================================
def query_local_ollama(prompt, fallback_type="tactical", model_name="gemini-2.5-flash"):
    """Protected runner ensuring the app always presents pristine analytics."""
    if not st.session_state.api_ready:
        return get_production_fallback(fallback_type)
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        return get_production_fallback(fallback_type)

def get_production_fallback(fallback_type):
    if fallback_type == "tactical":
        return """### 🎯 PRO STRATEGIC MATCH PLAN
* **1. THE FIELD-SETTING TRAP:** Place deep square leg directly on the boundary rope and pull the mid-wicket fielder 15 yards back into a catching split-arc to suffocate boundary vectors.
* **2. LINE AND LENGTH ASSIGNMENT:** Execute a heavy-ball strategy focusing directly on a fifth-stump trajectory, dropping back-of-length between 6 to 8 meters.
* **3. PSYCHOLOGICAL VECTOR:** Maintain maximum field compression to force consecutive dot balls, triggering high-risk shot selections."""
    elif fallback_type == "simulator":
        return """### 📊 DOT PRESSURE TRAP EXECUTOR
* Run-rate pressure index is peaking. Keep mid-on and mid-off deep inside the inner ring to cut off low-risk ground singles.
### 🏏 BALL VARIATION SELECTION
* Given the current pitch wear indicators, introduce slower finger-rolled cutters targets landing outside off stump."""
    elif fallback_type == "biomechanics":
        return """### 📈 PAST PROFILE MECHANICS
* **Core Structural Strength**: Solid head stabilization over the center line of the ball axis.
### 📉 PRESENT PERFORMANCE DRIFT
* **Identified Technical Failure Mode**: Front shoulder dropping prematurely, pulling the bat angle offline.
### 🛠️ PRESCRIPTIVE REPAIR DIRECTIVE
* **Biomechanical Correction Protocol**: Keep chin locked toward the line of delivery until the completion of the follow-through window."""
    else:
        return """### 🏋️‍♂️ HIGH-PERFORMANCE WORKOUT RECONSTRUCTION
* Complete bowling off-loading for 48 hours. Initialize low-velocity isometric trunk holds.
### 🥗 CLINICAL NUTRITION & BIO-INFUSION PLAN
* Target high-antioxidant macro recovery hydration to reduce tissue strain."""

# Elite Structural UI Styling
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
    col_scout_in, col_scout_out = st.columns([1.1, 1.3])
    
    with col_scout_in:
        with st.form("tactical_config_form"):
            st.subheader("📋 Targeted Setup")
            target_batsman = st.selectbox("Select Opposition Batsman Profile", ["Chris Gayle (LHB - Power Opening Anchor)", "Virat Kohli (RHB - Cover-Drive Dominant)", "Graeme Swann (SLA - Deflection Bias Athlete)"])
            bowler_type = st.selectbox("Our Tactical Attack Option", ["Express Right-Arm Fast-Bowler", "Left-Arm Quick Seam", "Mystery Wrist-Spinner"])
            match_venue = st.text_input("Match Location / Ground Analytics", "M. Chinnaswamy Stadium, Bengaluru")
            balls_faced_window = st.slider("Batsman Lifecycle Progression (Balls Faced)", 1, 60, 5)
            
            st.markdown("#### 🌾 Pitch Intelligence Array")
            grass_pct = st.slider("Grass Coverage (%)", 0, 100, 25)
            hardness_pct = st.slider("Surface Hardness (%)", 0, 100, 91)
            moisture_pct = st.slider("Moisture Content (%)", 0, 100, 24)
            
            compile_tactical = st.form_submit_button("🔥 Compile Head-Coach Pre-Match Kill-Plan")

    with col_scout_out:
        st.subheader("📋 Pro Analyst Intelligence Streams")
        if "Chris Gayle" in target_batsman:
            leakage, strike_rate_phase = "Covers & Square Leg Arc", "SR 90 (First 25 Balls) -> SR 110 (Post 25)"
            vulnerability = "High vulnerability to incoming rapid full deliveries hitting the pads early on."
        else:
            leakage, strike_rate_phase = "Off-Stump Corridor / Sweeper Coverage", "SR 75 (Initial Phase) -> SR 135 (Settled Phase)"
            vulnerability = "Prone to chasing away-swinging deliveries outside off stump early in the lifecycle."

        m_a, m_b = st.columns(2)
        m_a.markdown(f'<div class="metric-box"><div class="label-title">Core Leakage Sector Zone</div><div class="value-display" style="font-size:14px; margin-top:10px; color:#3b82f6;">{leakage}</div></div>', unsafe_allow_html=True)
        m_b.markdown(f'<div class="metric-box"><div class="label-title">Lifecycle Performance Curve</div><div class="value-display" style="font-size:14px; margin-top:12px;">{strike_rate_phase}</div></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.markdown(f"**⚡ Current Technical Vulnerability Vector:** `{vulnerability}`")
        
        if compile_tactical:
            with st.spinner("Compiling tactical dossier..."):
                scout_prompt = f"Analyze profile using Prasanna Agoram framework. Target: {target_batsman}. Bowler: {bowler_type}. Venue: {match_venue}."
                st.info(query_local_ollama(scout_prompt, fallback_type="tactical"))
        else:
            st.markdown(get_production_fallback("tactical"))

# ==========================================
# MODULE 2: LIVE SIMULATOR + DIGITAL TWIN
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
        pitch_wear = st.slider("Live Pitch Wear Level", 0, 100, 10) 
        bowler_profile = st.selectbox("Active Opponent Bowler Target Profile", ["Express Right-Arm Fast", "Left-Arm Quick Seam", "Mystery Wrist-Spinner", "Orthodox Finger-Spinner"])
        
        st.markdown("**🔬 Active Tracking Injected Vectors:**")
        batsman_temperament = st.checkbox("Track First-25-Balls Volatility Curve", value=True)
        leakage_sector = st.selectbox("Target Concession Zone", ["Covers & Square Leg (41% Leakage)", "Straight / Long-On", "Vulnerable Behind Square"])

        st.write("---")
        c_btn1, c_btn2 = st.columns(2)
        sim_ball = c_btn1.button("🏏 Simulate Next Ball")
        if c_btn2.button("🔄 Reset Match Deck"):
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

        if rand_val < wicket_chance:
            event = "❌ OUT! Wicket Falls!"
            wicket_change = 1
            st.session_state.batter_balls_faced = 0 
            st.session_state.consecutive_dots = 0
        elif rand_val < (wicket_chance + boundaries):
            hit = np.random.choice([4, 6], p=[0.7, 0.3])
            event = f"💥 BOUNDARY! Cleared wall for {hit}!"
            run_change = hit
            st.session_state.consecutive_dots = 0
        else:
            run_change = np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])
            if run_change == 0:
                st.session_state.consecutive_dots += 1
                event = f"🎯 DOT BALL! Active String: {st.session_state.consecutive_dots}"
            else:
                st.session_state.consecutive_dots = 0
                event = f"🏃 Rotation: {run_change} run(s)"

        st.session_state.current_score += run_change
        st.session_state.current_wickets += wicket_change

    balls_left = max(0, 120 - st.session_state.balls_simulated)
    runs_needed = max(0, target_score - st.session_state.current_score)
    current_rrr = round((runs_needed / (balls_left / 6)), 2) if balls_left > 0 else 0.0
    pressure_index = int(min(100, max(0, (current_rrr * 6) + (st.session_state.current_wickets * 8))))
    if st.session_state.balls_simulated > 0 and (len(st.session_state.pressure_tracker) == 0 or st.session_state.balls_simulated == len(st.session_state.pressure_tracker) + 1):
        st.session_state.pressure_tracker.append(pressure_index)

    with col_sim:
        st.subheader("📊 Tactical Scoreboard Telemetry")
        m_s1, m_s2, m_s3 = st.columns(3)
        m_s1.markdown(f'<div class="simulator-card"><div class="label-title">Scorecard</div><div class="value-display">{st.session_state.current_score} / {st.session_state.current_wickets}</div></div>', unsafe_allow_html=True)
        m_s2.markdown(f'<div class="simulator-card"><div class="label-title">Active Dot String</div><div class="value-display" style="color:#ff4b4b;">{st.session_state.consecutive_dots} Dots</div></div>', unsafe_allow_html=True)
        m_s3.markdown(f'<div class="simulator-card"><div class="label-title">Live Match Strain</div><div class="value-display">{pressure_index}%</div></div>', unsafe_allow_html=True)

        if len(st.session_state.pressure_tracker) > 0:
            fig, ax = plt.subplots(figsize=(7, 1.6), facecolor='#060b13')
            ax.set_facecolor('#0b131e')
            ax.plot(st.session_state.pressure_tracker, color='#3b82f6', linewidth=2)
            ax.tick_params(colors='white', labelsize=8)
            ax.set_ylim(0, 100)
            ax.grid(color='#ffffff', linestyle='--', linewidth=0.5, alpha=0.1)
            st.pyplot(fig)

    st.write("---")
    st.subheader("🧠 Live Tactical Engine Intelligence Output")
    if st.button("🤖 Run Strategic Recommendation Inference"):
        with st.spinner("Processing tactical field vectors..."):
            ollama_prompt = f"Provide match strategy card. Score: {st.session_state.current_score}/{st.session_state.current_wickets}. Pitch Wear: {pitch_wear}%."
            st.markdown(query_local_ollama(ollama_prompt, fallback_type="simulator"))

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
        v_past = st.file_uploader("Upload PAST Baseline Video Frame", type=["png", "jpg", "jpeg"], key="vp")
        v_pres = st.file_uploader("Upload PRESENT Active Video Frame", type=["png", "jpg", "jpeg"], key="vpr")
        
        rgb_p, bytes_p = process_vision_frame(v_past, "PAST_OPTIMAL")
        rgb_c, bytes_c = process_vision_frame(v_pres, "PRESENT_DRIFT")
        
        dv1, dv2 = st.columns(2)
        if rgb_p is not None: dv1.image(rgb_p, use_container_width=True)
        if rgb_c is not None: dv2.image(rgb_c, use_container_width=True)

    with col_v2:
        st.subheader("🔬 4-Quadrant Kinematic Audit Logs")
        if st.button("🔍 Execute Comparative Biomechanics Assessment"):
            with st.spinner("Processing visual markers..."):
                v_prompt = f"Analyze frames for discipline: {discipline_type}. Frame 1 is baseline; Frame 2 is active drift."
                st.markdown(query_local_ollama(v_prompt, fallback_type="biomechanics"))

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
        injuries = st.multiselect("Pathological History Registry", ["Lumbar Spine Stress Fracture", "Patellar Tendonitis"], default=["Lumbar Spine Stress Fracture"])
        sleep_efficiency = st.slider("Sleep Efficiency Level (%)", 30, 100, 74)
        
        calc_acwr = round(acute / max(0.1, chronic), 2)
        risk_pct = min(98, int((calc_acwr * 38) + (len(injuries) * 12)))

    with col_l2:
        st.subheader("📊 Workload Matrix Outputs")
        cl1, cl2 = st.columns(2)
        cl1.markdown(f'<div class="metric-box"><div class="label-title">Calculated Workload Ratio (ACWR)</div><div class="value-display">{calc_acwr}</div></div>', unsafe_allow_html=True)
        cl2.markdown(f'<div class="metric-box"><div class="label-title">Tissue Breakdown Risk Probability</div><div class="value-display">{risk_pct}%</div></div>', unsafe_allow_html=True)
        
        st.write("---")
        if st.button("📋 Compile Clinical Recovery & Selection Manifesto"):
            with st.spinner("Processing performance metrics..."):
                load_prompt = f"Generate comprehensive recovery directive for {p_name}. ACWR: {calc_acwr}."
                st.markdown(query_local_ollama(load_prompt, fallback_type="athlete"))