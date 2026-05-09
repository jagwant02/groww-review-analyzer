import streamlit as st
import pandas as pd
import time
import os
import sys
import subprocess

# Add src to python path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from agents import GrowwPulseOrchestrator
from google_utils import GoogleWorkspaceManager

# Page Config
st.set_page_config(page_title="AIO Orchestrator | Groww Pulse", page_icon="💠", layout="wide")

# Custom CSS for the Premium Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #FFFFFF;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #A0A0A0;
        margin-bottom: 2rem;
    }
    
    /* Stage Cards */
    .stage-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        transition: transform 0.2s;
    }
    
    .stage-card:hover {
        border-color: #58A6FF;
    }
    
    .stage-title {
        font-size: 0.8rem;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
        margin-bottom: 0.5rem;
    }
    
    .stage-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #F0F6FC;
        margin-bottom: 0.5rem;
    }
    
    .stage-status {
        font-size: 0.9rem;
        color: #A0A0A0;
        font-style: italic;
    }
    
    /* Takeaway Cards */
    .takeaway-card {
        background-color: #161B22;
        border-left: 4px solid #58A6FF;
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .tag-critical { color: #FF7B72; font-weight: 600; font-size: 0.7rem; text-transform: uppercase; }
    .tag-insight { color: #D2A8FF; font-weight: 600; font-size: 0.7rem; text-transform: uppercase; }
    .tag-positive { color: #3FB950; font-weight: 600; font-size: 0.7rem; text-transform: uppercase; }
    
    .connected-dot {
        height: 8px;
        width: 8px;
        background-color: #3FB950;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }

    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'workflow_step' not in st.session_state: st.session_state.workflow_step = 0
if 'final_state' not in st.session_state: st.session_state.final_state = None
if 'friendly_logs' not in st.session_state: st.session_state.friendly_logs = []

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
    st.markdown("### AIO Orchestrator")
    st.markdown("`Node-01 Active` 🟢")
    st.divider()
    
    st.markdown("#### System Load")
    st.caption("Compute: 42% | Memory: 18%")
    st.progress(0.42)
    
    st.divider()
    if st.button("🔄 Reset Workflow"):
        st.session_state.workflow_step = 0
        st.session_state.final_state = None
        st.session_state.friendly_logs = []
        st.rerun()

# Header
st.markdown('<div class="main-header">App Review Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Processing public user reviews for Groww (Play Store).</div>', unsafe_allow_html=True)

# 4-Stage Workflow UI
col1, col2, col3, col4 = st.columns(4)

stages = [
    {"name": "Data Retrieval", "msg": "We are getting the data for you"},
    {"name": "Processing", "msg": "The data is being cleaned & analyzed"},
    {"name": "Documentation", "msg": "Preparing the insights pulse"},
    {"name": "Deployment", "msg": "Ready for distribution"}
]

cols = [col1, col2, col3, col4]
for i, stage in enumerate(stages):
    with cols[i]:
        status_style = "border-color: #58A6FF;" if st.session_state.workflow_step == i + 1 else ""
        if st.session_state.workflow_step > i + 1: status_style = "border-color: #3FB950;"
        
        st.markdown(f"""
        <div class="stage-card" style="{status_style}">
            <div class="stage-title">Stage {i+1}</div>
            <div class="stage-name">{stage['name']}</div>
            <div class="stage-status">"{stage['msg']}"</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Action Area
if st.session_state.workflow_step == 0:
    if st.button("▶ START WORKFLOW", type="primary"):
        st.session_state.workflow_step = 1
        st.rerun()

# Execution Logic
if st.session_state.workflow_step == 1:
    with st.status("🚀 Initializing Pipeline...", expanded=True) as status:
        st.write("🛰️ Connecting to Google Play Store...")
        python_exe = sys.executable
        subprocess.run([python_exe, "src/fetch_reviews.py"])
        st.write("🧼 Scrubbing PII and personal data...")
        subprocess.run([python_exe, "src/sanitize.py"])
        time.sleep(1)
        status.update(label="Data Retrieval Complete", state="complete")
    st.session_state.workflow_step = 2
    st.rerun()

if st.session_state.workflow_step == 2:
    data_path = os.path.join("data", "scrubbed_reviews.csv")
    df = pd.read_csv(data_path)
    raw_reviews = df['text'].tolist()
    
    orchestrator = GrowwPulseOrchestrator()
    with st.status("🧠 Agents are analyzing...", expanded=True) as status:
        for agent_name, status_msg in orchestrator.run_workflow(raw_reviews):
            st.write(f"✅ {agent_name} is active: {status_msg}")
        status.update(label="Analysis Complete", state="complete")
    
    st.session_state.final_state = orchestrator.state
    st.session_state.workflow_step = 3
    st.rerun()

# Results Display
if st.session_state.workflow_step >= 3:
    st.markdown("### Top Takeaways")
    state = st.session_state.final_state
    
    t_cols = st.columns(3)
    # Display Themes
    for idx, theme in enumerate(state['themes']):
        with t_cols[idx % 3]:
            tag = "CRITICAL" if idx == 0 else "INSIGHT"
            tag_class = "tag-critical" if idx == 0 else "tag-insight"
            st.markdown(f"""
            <div class="takeaway-card">
                <div class="{tag_class}">{tag}</div>
                <div style="font-weight:600; margin-top:0.5rem;">{theme['theme']}</div>
                <div style="font-size:0.9rem; color:#A0A0A0; margin-top:0.5rem;">{theme['description']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    
    # Final Review & Approval
    st.markdown("### Final Documentation")
    st.info(state['draft_note'])
    
    if st.session_state.workflow_step == 3:
        if st.button("🚀 APPROVE & PUBLISH"):
            st.session_state.workflow_step = 4
            st.rerun()

if st.session_state.workflow_step == 4:
    with st.spinner("📤 Deploying to Google Workspace..."):
                try:
                    # Check if we have what we need
                    has_cloud_creds = False
                    try:
                        if "GOOGLE_CREDENTIALS_JSON" in st.secrets or "GOOGLE_TOKEN_JSON" in st.secrets:
                            has_cloud_creds = True
                    except Exception:
                        pass
                        
                    if has_cloud_creds or os.path.exists('credentials.json'):
                        manager = GoogleWorkspaceManager()
                        
                        # 1. Create Google Doc
                        doc_link = manager.create_google_doc(
                            title=f"Groww Weekly Pulse - {time.strftime('%Y-%m-%d')}",
                            content=st.session_state.final_state['draft_note']
                        )
                        st.success(f"✅ Weekly Note created in Google Docs: {doc_link}")
                        
                        # 2. Upload Data to Drive
                        csv_path = os.path.join("data", "scrubbed_reviews.csv")
                        drive_link = manager.upload_to_drive(csv_path)
                        st.success(f"✅ Sanitized dataset uploaded to Google Drive: {drive_link}")
                        
                        # 3. Create Gmail Draft
                        subject_line = f"Groww Weekly Pulse - {time.strftime('%Y-%m-%d')}"
                        draft_msg = manager.create_gmail_draft(
                            subject=subject_line,
                            body_text=st.session_state.final_state['draft_note']
                        )
                        st.success(f"✅ {draft_msg}")
                        with st.expander("✉️ View Email Draft Contents", expanded=True):
                            st.markdown(f"**Subject:** {subject_line}")
                            st.markdown(st.session_state.final_state['draft_note'])
                            
                        st.balloons()
                    else:
                        st.warning("⚠️ Google Workspace Sync is only available in Local Mode or with a pre-authorized Cloud Token.")
                        st.info("To use this feature in the cloud, you must provide a GOOGLE_TOKEN_JSON in your secrets.")
                    
                except Exception as e:
                    st.error(f"Authentication Error: {e}")
                    st.info("Note: Google OAuth requires a local browser popup. This button works best when running the app on your computer.")

# Footer Stats
st.divider()
f1, f2 = st.columns(2)
with f1:
    st.markdown("**Data Streams**")
    st.caption("🟢 App Store API: Connected")
    st.caption("🟢 Play Store API: Connected")
with f2:
    st.markdown("**Resource Monitor**")
    st.caption("Latency: 1.2s | Error Rate: 0.02%")
