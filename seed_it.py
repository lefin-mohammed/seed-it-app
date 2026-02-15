import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. DESIGN SYSTEM (LIGHT & CLEAN)
# ==========================================
st.set_page_config(page_title="Seed It Pro", page_icon="🏦", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* GLOBAL RESET */
    .stApp { background: #F8F9F8; color: #1A1C1E; font-family: 'Inter', sans-serif; }
    
    /* HEADER STYLING */
    .header-box { display: flex; align-items: center; justify-content: space-between; padding: 20px 0; }
    .avatar-circle { width: 45px; height: 45px; border-radius: 50%; background: #E2E8F0; display: flex; align-items: center; justify-content: center; font-size: 20px; }

    /* CARD SYSTEM */
    .white-card {
        background: #FFFFFF;
        border-radius: 28px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(0, 0, 0, 0.02);
    }

    /* THE PROGRESS RING (REPLICATING IMAGE 2) */
    .ring-container {
        width: 200px; height: 200px; margin: 20px auto;
        position: relative; display: flex; align-items: center; justify-content: center;
    }
    .svg-ring { transform: rotate(-90deg); }
    .ring-bg { fill: none; stroke: #F0F2F0; stroke-width: 10; }
    .ring-fill { 
        fill: none; stroke: #189F8D; stroke-width: 10; 
        stroke-linecap: round; transition: all 1s ease-in-out;
    }

    /* TRANSACTION LIST */
    .tx-item {
        display: flex; align-items: center; justify-content: space-between;
        padding: 16px 0; border-bottom: 1px solid #F1F3F4;
    }
    .tx-icon { width: 40px; height: 40px; border-radius: 12px; background: #F1F8F7; display: flex; align-items: center; justify-content: center; margin-right: 15px; }

    /* TYPOGRAPHY */
    .title-large { font-size: 32px; font-weight: 800; color: #1A1C1E; margin: 5px 0; }
    .label-muted { color: #8C9196; font-size: 13px; font-weight: 500; }
    .mint-text { color: #189F8D; font-weight: 700; }

    /* BUTTONS (TOP UP / WITHDRAW) */
    .btn-row { display: flex; gap: 15px; margin-top: 15px; }
    .btn-main {
        flex: 1; padding: 14px; border-radius: 16px; border: none;
        font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
        transition: transform 0.1s;
    }
    .btn-topup { background: #E8F5F3; color: #189F8D; }
    .btn-withdraw { background: #F8F9F8; color: #5F6368; border: 1px solid #E2E8F0; }

    /* NAVIGATION */
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #FFFFFF; border-top: 1px solid #F1F3F4; display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; }
    
    header, footer, .stDeployButton { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC & STATE
# ==========================================
MY_UPI_ID = "phathim630@oksbi" 
MY_NAME = "Hathim p"

if 'view' not in st.session_state: st.session_state.view = "LOGIN"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'selected_goal' not in st.session_state: st.session_state.selected_goal = None

def get_icon(name):
    name = name.lower()
    if "car" in name: return "🚗"
    if "phone" in name: return "📱"
    if "home" in name: return "🏠"
    return "🎯"

# ==========================================
# 3. SCREEN: LOGIN
# ==========================================
def show_login():
    st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#189F8D; font-weight:800;'>Seed It</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="Robert Fox")
        phone = st.text_input("Mobile Number", placeholder="+91")
        if st.button("Get Started", use_container_width=True):
            if name and phone:
                st.session_state.user = {"name": name, "phone": phone}
                st.session_state.view = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: HOME (DASHBOARD)
# ==========================================
def show_home():
    # Top Header
    st.markdown(f"""
        <div class='header-box'>
            <div><span class='label-muted'>Hello,</span><br><b>{st.session_state.user['name']}!</b></div>
            <div class='avatar-circle'>👤</div>
        </div>
    """, unsafe_allow_html=True)

    # Balance Card (Replicating Image 1)
    total_bal = sum(g['balance'] for g in st.session_state.goals)
    st.markdown(f"""
        <div class='white-card'>
            <span class='label-muted'>Total Balance</span>
            <div class='title-large'>₹{total_bal:,.2f}</div>
            <div style='display:flex; gap:10px; margin-top:15px;'>
                <div style='height:30px; width:4px; background:#189F8D; border-radius:2px;'></div>
                <div style='height:20px; width:4px; background:#E2E8F0; border-radius:2px; margin-top:10px;'></div>
                <div style='height:40px; width:4px; background:#189F8D; border-radius:2px; margin-top:-10px;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Savings Goal Horizontal List
    st.markdown("<div style='display:flex; justify-content:space-between;'><b>Savings</b> <span class='mint-text'>See all</span></div>", unsafe_allow_html=True)
    
    if not st.session_state.goals:
        st.markdown("<p class='label-muted'>No goals yet. Tap + to start.</p>", unsafe_allow_html=True)
    else:
        # Create small cards for each goal
        cols = st.columns(4)
        for i, goal in enumerate(st.session_state.goals[:4]):
            with cols[i]:
                if st.button(get_icon(goal['name']), key=f"icon_{i}"):
                    st.session_state.selected_goal = i
                    st.session_state.view = "DETAIL"
                    st.rerun()

    # Transaction History
    st.markdown("<br><b>Today</b>", unsafe_allow_html=True)
    st.markdown("""
        <div class='tx-item'>
            <div style='display:flex; align-items:center;'>
                <div class='tx-icon'>🍏</div>
                <div><b>Food Store</b><br><span class='label-muted'>Groceries</span></div>
            </div>
            <div style='text-align:right;'><b>-₹1,450.00</b><br><span class='label-muted'>12:45 PM</span></div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: GOAL DETAIL (IMAGE 2 REPLICA)
# ==========================================
def show_detail():
    goal = st.session_state.goals[st.session_state.selected_goal]
    prog = goal['balance'] / goal['target']
    offset = 565 - (prog * 565)

    # Back Button
    if st.button("← Back"):
        st.session_state.view = "HOME"
        st.rerun()

    st.markdown(f"<h3 style='text-align:center;'>{goal['name']}</h3>", unsafe_allow_html=True)

    # Circular Progress
    st.markdown(f"""
        <div class='ring-container'>
            <svg class='svg-ring' width='200' height='200'>
                <circle class='ring-bg' cx='100' cy='100' r='90'></circle>
                <circle class='ring-fill' cx='100' cy='100' r='90' style='stroke-dasharray: 565; stroke-dashoffset: {offset};'></circle>
            </svg>
            <div style='position:absolute; text-align:center;'>
                <div style='font-size:45px;'>{get_icon(goal['name'])}</div>
            </div>
        </div>
        <div style='text-align:center;'>
            <div class='title-large'>₹{goal['balance']:,.2f}</div>
            <span class='label-muted'>of ₹{goal['target']:,.2f}</span>
        </div>
    """, unsafe_allow_html=True)

    # Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📥 Top up", use_container_width=True):
            st.session_state.show_topup = True
    with c2:
        st.button("📤 Withdraw", disabled=(goal['balance'] < goal['target']), use_container_width=True)

    if st.session_state.get('show_topup'):
        amt = st.number_input("Enter Amount", min_value=1)
        url = f"upi://pay?pa={MY_UPI_ID}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR"
        st.markdown(f"<a href='{url}' target='_self' style='text-decoration:none;'><div class='btn-main btn-topup'>Proceed to UPI</div></a>", unsafe_allow_html=True)
        if st.button("Confirm Transfer"):
            goal['balance'] += amt
            st.session_state.show_topup = False
            st.rerun()

# ==========================================
# 6. SCREEN: CREATE GOAL
# ==========================================
def show_create():
    st.markdown("### Set New Goal")
    with st.container():
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        g_name = st.text_input("Goal Name (e.g. Car)")
        g_target = st.number_input("Target Amount (₹)", min_value=1)
        if st.button("Create", use_container_width=True):
            if g_name and g_target > 0:
                st.session_state.goals.append({"name": g_name, "target": g_target, "balance": 0})
                st.session_state.view = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MAIN ROUTER
# ==========================================
if st.session_state.view == "LOGIN":
    show_login()
else:
    if st.session_state.view == "HOME": show_home()
    elif st.session_state.view == "DETAIL": show_detail()
    elif st.session_state.view == "CREATE": show_create()

    # Fixed Bottom Nav
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🏠"): st.session_state.view = "HOME"; st.rerun()
    with c2: 
        if st.button("➕"): st.session_state.view = "CREATE"; st.rerun()
    with c3: 
        if st.button("👤"): st.session_state.view = "LOGIN"; st.rerun()
