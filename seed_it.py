import streamlit as st
import time
import urllib.parse
from datetime import datetime, date
import uuid

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Seed It Elite",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS STYLING (IMAGE REPLICA) ====================
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Hide Streamlit UI Elements */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* Dashboard Header */
    .profile-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
    .profile-pic { width: 42px; height: 42px; border-radius: 50%; overflow: hidden; border: 1px solid #333; }
    
    /* Balance Card */
    .balance-card {
        background: #121212;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 30px;
        border: 1px solid #1A1A1A;
    }
    .balance-amount { font-size: 38px; font-weight: 800; color: #FFFFFF; margin: 5px 0; }
    .balance-controls { display: flex; gap: 10px; margin-top: 15px; }
    .icon-circle { 
        width: 36px; height: 36px; border-radius: 50%; background: #1A1A1A; 
        display: flex; align-items: center; justify-content: center; border: 1px solid #333;
    }
    .icon-volt { background: #CCFF00 !important; color: #000 !important; border: none !important; font-weight: 900; }

    /* Goal Card (Horizontal Bar Style) */
    .goal-card {
        background: #0A0A0A; border-radius: 20px; padding: 18px;
        margin-bottom: 15px; border: 1px solid #151515; display: flex; gap: 15px;
    }
    .goal-thumb { width: 65px; height: 65px; border-radius: 14px; background: #151515; display: flex; align-items: center; justify-content: center; font-size: 30px; }
    
    /* Detail View Progress Ring */
    .ring-container { position: relative; width: 220px; height: 220px; margin: 20px auto; display: flex; align-items: center; justify-content: center; }
    .svg-ring { transform: rotate(-90deg); }
    .ring-bg { fill: none; stroke: #1A1A1A; stroke-width: 10; }
    .ring-fill { fill: none; stroke: #CCFF00; stroke-width: 10; stroke-linecap: round; transition: 1s ease; }

    /* Action Buttons */
    div.stButton > button {
        background: #CCFF00 !important; color: #000 !important; border-radius: 100px !important;
        padding: 16px !important; font-weight: 800 !important; border: none !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA & PAYMENT LOGIC ====================
MY_VPA = "phathim630@oksbi" 
MY_NAME = "Hathim p"

def get_goal_meta(name):
    name = name.lower()
    if "car" in name: return "Vehicle", "🚗"
    if "phone" in name or "iphone" in name: return "Apple", "📱"
    if "labubu" in name: return "Pop Mart", "🧸"
    if "airpods" in name: return "Apple", "🎧"
    return "Personal", "🎯"

# ==================== SESSION STATE ====================
if 'view' not in st.session_state: st.session_state.view = 'SIGNUP'
if 'goals' not in st.session_state: st.session_state.goals = []
if 'history' not in st.session_state: st.session_state.history = []

# ==================== UI RENDERING ====================

def render_dashboard():
    u = st.session_state.user
    
    # Header
    st.markdown(f"""
    <div class="profile-header">
        <div style="display:flex; gap:12px; align-items:center;">
            <div class="profile-pic"><div style="background:#CCFF00; color:#000; width:100%; height:100%; display:flex; align-items:center; justify-content:center; font-weight:800;">{u['name'][0]}</div></div>
            <div><b style='font-size:14px;'>Hello, {u['name'].split()[0]}</b><br><span style='color:#555; font-size:11px;'>Turn dreams into balance</span></div>
        </div>
        <div class="icon-circle">🔔</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Balance Card
    total = sum(g['current'] for g in st.session_state.goals)
    st.markdown(f"""
    <div class="balance-card">
        <span style="color:#555; font-size:11px; font-weight:700;">CURRENT BALANCE (USD)</span>
        <div class="balance-amount">₹{total:,.2f}</div>
        <div class="balance-controls">
            <div class="icon-circle">🔄</div>
            <div class="icon-circle">📈</div>
            <div class="icon-circle icon-volt">+</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='display:flex; justify-content:space-between; margin-bottom:15px;'><b>My goals</b><span style='color:#CCFF00; font-size:12px;'>View All ></span></div>", unsafe_allow_html=True)
    
    # Goals List (Horizontal Bar Style)
    for i, goal in enumerate(st.session_state.goals):
        prog = min(int((goal['current'] / goal['target']) * 100), 100)
        st.markdown(f"""
        <div class="goal-card">
            <div class="goal-thumb">{goal['emoji']}</div>
            <div style="flex-grow:1;">
                <div style="display:flex; justify-content:space-between;"><span style='color:#555; font-size:10px; font-weight:700;'>{goal['category'].upper()}</span></div>
                <b style='font-size:15px;'>{goal['name']}</b>
                <div style="display:flex; justify-content:space-between; margin-top:5px;"><span style='color:#555; font-size:11px;'>{prog}%</span></div>
                <div style="background:#1A1A1A; height:6px; border-radius:10px; width:100%; margin-top:4px;">
                    <div style="background:#CCFF00; height:100%; width:{prog}%; border-radius:10px;"></div>
                </div>
                <div style="margin-top:8px;"><b style='font-size:16px;'>₹{goal['current']:,}</b> <span style='color:#444; font-size:12px;'>/ ₹{goal['target']:,}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("VIEW DETAILS", key=f"view_{i}"):
            st.session_state.selected_goal = i
            st.session_state.view = 'DETAIL'
            st.rerun()

    if st.button("+ New goal"): st.session_state.view = 'CREATE'; st.rerun()

def render_detail():
    goal = st.session_state.goals[st.session_state.selected_goal]
    prog = goal['current'] / goal['target']
    offset = 565 - (prog * 565)

    if st.button("← Back"): st.session_state.view = 'DASHBOARD'; st.rerun()

    # Circular Progress Detail
    st.markdown(f"""
    <div style='text-align:center;'><span style='color:#555; font-size:11px; font-weight:700;'>{goal['category'].upper()}</span><br><h3>{goal['name']}</h3></div>
    <div class="ring-container">
        <svg class="svg-ring" width="200" height="200">
            <circle class="ring-bg" cx="100" cy="100" r="90"></circle>
            <circle class="ring-fill" cx="100" cy="100" r="90" style="stroke-dasharray: 565; stroke-dashoffset: {offset};"></circle>
        </svg>
        <div style="position:absolute; width:120px; height:120px; background:#111; border-radius:24px; display:flex; align-items:center; justify-content:center; font-size:60px;">{goal['emoji']}</div>
    </div>
    <div style="text-align:center;">
        <h1 style='margin:0;'>₹{goal['current']:,} <span style='color:#555; font-size:18px;'>/ ₹{goal['target']:,}</span></h1>
        <div style='background:#CCFF00; color:black; padding:3px 12px; border-radius:20px; display:inline-block; font-weight:900; margin-top:10px;'>{int(prog*1
