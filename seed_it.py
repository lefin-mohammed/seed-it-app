import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. DESIGN SYSTEM (ELITE DARK GRID)
# ==========================================
st.set_page_config(page_title="Seed It Obsidian", page_icon="🔒", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Plus Jakarta Sans', sans-serif; }

    /* GRID LAYOUT (INSPIRED BY IMAGE 2) */
    .goal-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-top: 20px;
    }

    /* PREMIUM CARDS */
    .main-card {
        background: #0D1117;
        border: 1px solid #1A1C1E;
        border-radius: 28px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .goal-card {
        background: #0D1117;
        border-radius: 24px;
        padding: 20px;
        border: 1px solid #1A1C1E;
        text-align: left;
        transition: transform 0.2s ease;
    }
    
    .goal-card:active { transform: scale(0.96); }

    /* VOLT ACCENTS (INSPIRED BY IMAGE 3) */
    .volt { color: #DFFF00; font-weight: 800; }
    .label-muted { color: #8C9196; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; }

    /* TOP UP BUTTON (INSPIRED BY IMAGE 2) */
    .topup-btn-main {
        background: #DFFF00;
        color: #000000;
        padding: 12px 24px;
        border-radius: 100px;
        font-weight: 800;
        text-align: center;
        display: inline-block;
        margin-top: 15px;
        text-decoration: none;
    }

    /* CIRCULAR PROGRESS (DETAIL VIEW) */
    .ring-container {
        width: 220px; height: 220px; margin: 20px auto;
        position: relative; display: flex; align-items: center; justify-content: center;
    }
    .svg-ring { transform: rotate(-90deg); }
    .ring-bg { fill: none; stroke: #1A1C1E; stroke-width: 10; }
    .ring-fill { 
        fill: none; stroke: #DFFF00; stroke-width: 10; 
        stroke-linecap: round; transition: all 1s ease;
    }

    /* BOTTOM NAV */
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; border-top: 1px solid #1A1C1E; display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; }

    header, footer, .stDeployButton { visibility: hidden; }
    
    div.stButton > button {
        background: #DFFF00; color: #000; border-radius: 100px;
        padding: 14px; font-weight: 800; border: none; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC & DATA
# ==========================================
MY_UPI_ID = "phathim630@oksbi" 
MY_NAME = "Hathim p"

if 'view' not in st.session_state: st.session_state.view = "LOGIN"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'selected_goal' not in st.session_state: st.session_state.selected_goal = None

def get_goal_icon(name):
    name = name.lower()
    if "car" in name: return "🚗"
    if "phone" in name: return "📱"
    if "home" in name: return "🏠"
    if "tv" in name: return "📺"
    if "ring" in name: return "💍"
    return "🎯"

# ==========================================
# 3. SCREEN: LOGIN
# ==========================================
def show_login():
    st.markdown("<br><br><h1 style='text-align:center; font-weight:800; font-size:40px;'>Seed<span class='volt'>It</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="Lefin Mohammed")
        age = st.text_input("Age", placeholder="19")
        phone = st.text_input("Mobile Number", placeholder="+91")
        if st.button("Sign In"):
            if name and age and phone:
                st.session_state.user = {"name": name, "age": age, "phone": phone}
                st.session_state.view = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: HOME (GRID DASHBOARD)
# ==========================================
def show_home():
    # Welcome Header
    st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; padding: 20px 0;'>
            <div><span class='label-muted'>Welcome back,</span><br><b style='font-size:20px;'>{st.session_state.user['name']}</b></div>
            <div style='width:40px; height:40px; border-radius:50%; background:#1A1C1E; border:1px solid #DFFF00; display:flex; align-items:center; justify-content:center;'>👤</div>
        </div>
    """, unsafe_allow_html=True)

    # Main Balance Card (Inspired by Image 2 - Safely)
    total_bal = sum(g['balance'] for g in st.session_state.goals)
    st.markdown(f"""
        <div class='main-card' style='background: linear-gradient(135deg, #0D1117 0%, #000 100%); border-left: 4px solid #DFFF00;'>
            <span class='label-muted'>Current Balance</span>
            <div style='font-size:36px; font-weight:900;'>₹{total_bal:,.2f}</div>
            <a href='#' class='topup-btn-main'>+ Top up</a>
        </div>
    """, unsafe_allow_html=True)

    # Goal Grid (Inspired by Image 2)
    st.markdown("<b style='font-size:18px;'>My goals</b>", unsafe_allow_html=True)
    
    if not st.session_state.goals:
        st.markdown("<p class='label-muted'>No active goals.</p>", unsafe_allow_html=True)
    else:
        # Streamlit columns to mimic the 2-column grid
        col1, col2 = st.columns(2)
        for i, goal in enumerate(st.session_state.goals):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                    <div class='goal-card'>
                        <div style='font-size:24px; background:#1A1C1E; width:40px; height:40px; border-radius:12px; display:flex; align-items:center; justify-content:center;'>{get_goal_icon(goal['name'])}</div>
                        <div style='margin-top:15px; font-weight:700;'>{goal['name']}</div>
                        <div class='label-muted' style='font-size:10px;'>Target: ₹{goal['target']:,}</div>
                        <div style='background:#1A1C1E; height:4px; width:100%; border-radius:2px; margin-top:10px;'>
                            <div style='background:#DFFF00; height:100%; width:{min(100, (goal['balance']/goal['target'])*100)}%; border-radius:2px;'></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("View Detail", key=f"btn_{i}"):
                    st.session_state.selected_goal = i
                    st.session_state.view = "DETAIL"
                    st.rerun()

# ==========================================
# 5. SCREEN: GOAL DETAIL (IMAGE 1 REPLICA)
# ==========================================
def show_detail():
    goal = st.session_state.goals[st.session_state.selected_goal]
    prog = goal['balance'] / goal['target'] if goal['target'] > 0 else 0
    offset = 565 - (prog * 565)

    if st.button("← Back"):
        st.session_state.view = "HOME"
        st.rerun()

    st.markdown(f"<h3 style='text-align:center;'>{goal['name']}</h3>", unsafe_allow_html=True)

    # Circular Progress (Inspired by Image 1/3)
    st.markdown(f"""
        <div class='ring-container'>
            <svg class='svg-ring' width='220' height='220'>
                <circle class='ring-bg' cx='110' cy='110' r='90'></circle>
                <circle class='ring-fill' cx='110' cy='110' r='90' style='stroke-dasharray: 565; stroke-dashoffset: {offset};'></circle>
            </svg>
            <div style='position:absolute; text-align:center;'>
                <div style='font-size:50px;'>{get_goal_icon(goal['name'])}</div>
            </div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:32px; font-weight:800;'>₹{goal['balance']:,.2f}</div>
            <span class='label-muted'>of ₹{goal['target']:,.2f}</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interaction Row
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📥 Top Up"):
            st.session_state.show_topup = True
    with c2:
        st.button("📤 Withdraw", disabled=(goal['balance'] < goal['target']))

    if st.session_state.get('show_topup'):
        amt = st.number_input("Enter Amount", min_value=1)
        url = f"upi://pay?pa={MY_UPI_ID}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR&mc=0000"
        st.markdown(f"<a href='{url}' target='_self' style='text-decoration:none;'><div style='background:#DFFF00; color:#000; padding:15px; border-radius:100px; text-align:center; font-weight:800;'>Authorize via UPI</div></a>", unsafe_allow_html=True)
        if st.button("Confirm Deposit"):
            goal['balance'] += amt
            st.session_state.show_topup = False
            st.rerun()

# ==========================================
# 6. SCREEN: CREATE GOAL
# ==========================================
def show_create():
    st.markdown("### Set a New Goal")
    with st.container():
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        g_name = st.text_input("What are you saving for?")
        g_target = st.number_input("Target Amount (₹)", min_value=1)
        if st.button("Create Goal"):
            if g_name and g_target > 0:
                st.session_state.goals.append({"name": g_name, "target": g_target, "balance": 0})
                st.session_state.view = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ROUTER & NAVIGATION
# ==========================================
if st.session_state.view == "LOGIN":
    show_login()
else:
    if st.session_state.view == "HOME": show_home()
    elif st.session_state.view == "DETAIL": show_detail()
    elif st.session_state.view == "CREATE": show_create()
    elif st.session_state.view == "SETTINGS": 
        st.markdown("### Settings")
        if st.button("Log Out"):
            st.session_state.view = "LOGIN"
            st.rerun()

    # Bottom Sticky Nav
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1: 
        if st.button("🏠"): st.session_state.view = "HOME"; st.rerun()
    with n2: 
        if st.button("➕"): st.session_state.view = "CREATE"; st.rerun()
    with n3: 
        if st.button("⚙️"): st.session_state.view = "SETTINGS"; st.rerun()
