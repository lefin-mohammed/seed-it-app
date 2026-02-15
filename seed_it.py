import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. ELITE OLED UI ENGINE (FAMPAY/CRED STYLE)
# ==========================================
st.set_page_config(page_title="Seed It Elite", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }

    /* SIGNATURE CARDS */
    .elite-card {
        background: #0D0D0D;
        border: 1px solid #1A1A1A;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .volt { color: #CCFF00; font-weight: 900; }
    .muted { color: #555555; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

    /* PROGRESS BAR (IMAGE 3 STYLE) */
    .stProgress > div > div > div > div { background-color: #CCFF00; height: 6px; border-radius: 10px; }

    /* CIRCULAR DETAIL RING */
    .detail-ring-container {
        position: relative; width: 100%; display: flex; justify-content: center; margin: 20px 0;
    }
    .svg-ring { transform: rotate(-90deg); }
    .ring-bg { fill: none; stroke: #1A1A1A; stroke-width: 8; }
    .ring-fill { fill: none; stroke: #CCFF00; stroke-width: 8; stroke-linecap: round; transition: 1s ease; }

    /* BOTTOM NAV BAR (IMAGE 2 ALIGNMENT) */
    .nav-bar {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(0,0,0,0.9); backdrop-filter: blur(20px);
        display: flex; justify-content: space-around; padding: 15px 0;
        border-top: 1px solid #111; z-index: 1000;
    }

    /* BUTTONS */
    div.stButton > button {
        background: #CCFF00; color: #000; border-radius: 100px;
        padding: 16px; font-weight: 900; border: none; width: 100%;
        font-size: 15px;
    }
    .secondary-btn button { background: #1A1A1A !important; color: white !important; }
    
    header, footer, .stDeployButton { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONFIG & LOGIC
# ==========================================
MY_VPA = "phathim630@oksbi" 
MY_NAME = "Hathim p"

if 'v' not in st.session_state: st.session_state.v = "AUTH"
if 'g' not in st.session_state: st.session_state.g = []
if 'p' not in st.session_state: st.session_state.p = False # Privacy
if 'sel' not in st.session_state: st.session_state.sel = None # Selected Goal

# ==========================================
# 3. SCREEN: LOGIN
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; font-weight:900; font-size:48px; letter-spacing:-2px;'>SEED<span class='volt'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        st.markdown("<span class='muted'>AUTHENTICATION</span>", unsafe_allow_html=True)
        name = st.text_input("Name", label_visibility="collapsed", placeholder="Full Name")
        age = st.text_input("Age", label_visibility="collapsed", placeholder="Age")
        phone = st.text_input("Mobile", label_visibility="collapsed", placeholder="+91")
        if st.button("LOGIN ➝"):
            if name and age and phone:
                st.session_state.u = {"n": name, "a": age, "p": phone}
                st.session_state.v = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: HOME (IMAGE 3 INSPIRED)
# ==========================================
def show_home():
    # Header
    c1, c2 = st.columns([5,1])
    with c1: st.markdown(f"**Hello, {st.session_state.u['n'].split()[0]}**<br><span class='muted'>Turn dreams into balance</span>", unsafe_allow_html=True)
    with c2: 
        if st.button("👁️"): 
            st.session_state.p = not st.session_state.p
            st.rerun()

    # Balance Card (Image 3 Top Widget)
    st.markdown(f"""
        <div class='elite-card'>
            <span class='muted'>Current Balance (USD)</span>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <h1 style='margin:0; font-weight:900;'>₹{"****" if st.session_state.p else f"{sum(item['b'] for item in st.session_state.g):,}"}</h1>
                <div style='background:#CCFF00; color:black; width:35px; height:35px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:900;'>+</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Goals List (Image 3 Alignment)
    st.markdown("<div style='display:flex; justify-content:space-between;'><b style='font-size:18px;'>My goals</b><span class='volt'>View All ></span></div>", unsafe_allow_html=True)
    
    if not st.session_state.g:
        st.markdown("<div class='elite-card' style='text-align:center; opacity:0.3;'>No goals active</div>", unsafe_allow_html=True)
    else:
        for i, goal in enumerate(st.session_state.g):
            prog = (goal['b'] / goal['t'])
            st.markdown(f"""
                <div class='elite-card'>
                    <div style='display:flex; gap:15px; align-items:center;'>
                        <div style='width:50px; height:50px; background:#1A1A1A; border-radius:15px; display:flex; align-items:center; justify-content:center; font-size:24px;'>🎯</div>
                        <div style='flex-grow:1;'>
                            <div style='display:flex; justify-content:space-between;'><b style='font-size:14px;'>{goal['n']}</b><span class='muted' style='font-size:14px;'>...</span></div>
                            <div class='muted' style='margin:2px 0;'>{int(prog*100)}%</div>
                            <div style='background:#1A1A1A; height:6px; border-radius:10px; width:100%; margin-top:5px;'>
                                <div style='background:#CCFF00; height:100%; border-radius:10px; width:{prog*100}%;'></div>
                            </div>
                            <div style='margin-top:5px;'><span style='font-weight:700;'>₹{goal['b']}</span> <span class='muted'>/ ₹{goal['t']}</span></div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("VIEW DETAIL", key=f"v_{i}"):
                st.session_state.sel = i
                st.session_state.v = "DETAIL"
                st.rerun()

# ==========================================
# 5. SCREEN: DETAIL (IMAGE 3 RIGHT PHONE)
# ==========================================
def show_detail():
    goal = st.session_state.g[st.session_state.sel]
    prog = (goal['b'] / goal['t'])
    offset = 565 - (prog * 565)

    # Back Arrow
    if st.button("←", key="back"): st.session_state.v = "HOME"; st.rerun()

    st.markdown(f"<div style='text-align:center;'><span class='muted'>GOAL</span><br><h3 style='margin:0;'>{goal['n']}</h3></div>", unsafe_allow_html=True)

    # Big Image/Icon + Progress
    st.markdown(f"""
        <div class='detail-ring-container'>
            <svg class='svg-ring' width='200' height='200'>
                <circle class='ring-bg' cx='100' cy='100' r='90'></circle>
                <circle class='ring-fill' cx='100' cy='100' r='90' style='stroke-dasharray: 565; stroke-dashoffset: {offset};'></circle>
            </svg>
            <div style='position:absolute; top:20px; width:120px; height:120px; background:#111; border-radius:20px; display:flex; align-items:center; justify-content:center; font-size:50px;'>🎯</div>
        </div>
        <div style='text-align:center;'>
            <h1 style='margin:0; font-weight:900; font-size:36px;'>₹{goal['b']} <span class='muted' style='font-size:18px;'>/ ₹{goal['t']}</span></h1>
            <div style='background:#CCFF00; color:black; display:inline-block; padding:2px 10px; border-radius:20px; font-weight:900; font-size:12px; margin-top:10px;'>{int(prog*100)}%</div>
        </div>
    """, unsafe_allow_html=True)

    # Transaction history (from Image 3)
    st.markdown("<br><div style='display:flex; justify-content:space-between;'><b class='muted'>TRANSACTION HISTORY</b><span class='volt'>View All ></span></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='display:flex; justify-content:space-between; margin:15px 0;'>
            <div><b style='font-size:14px;'>Top-up Contribution</b><br><span class='muted' style='font-size:10px;'>15 Feb 2026</span></div>
            <div class='volt'>+₹100.00</div>
        </div>
    """, unsafe_allow_html=True)

    # Bottom Fix Button (Image 3)
    amt = st.number_input("Enter Deposit", min_value=1, key="dep_amt")
    url = f"upi://pay?pa={MY_VPA}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR"
    st.markdown(f"<a href='{url}' target='_self' style='text-decoration:none;'><div style='background:#CCFF00; color:black; padding:18px; border-radius:100px; text-align:center; font-weight:900;'>Top up goal balance</div></a>", unsafe_allow_html=True)
    if st.button("CONFIRM PAYMENT ✅"):
        goal['b'] += amt
        st.rerun()

# ==========================================
# 6. SETTINGS (LOGOUT HERE)
# ==========================================
def show_settings():
    st.markdown("### Settings")
    st.markdown(f"<div class='elite-card'><b>{st.session_state.u['n']}</b><br><span class='muted'>{st.session_state.u['p']}</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
    if st.button("LOGOUT & ERASE DATA"):
        st.session_state.v = "AUTH"
        st.session_state.g = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# NAVIGATION BAR LOGIC
# ==========================================
if st.session_state.v != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🏠"): st.session_state.v = "HOME"; st.rerun()
    with c2: 
        if st.button("➕"): 
            st.session_state.v = "CREATE"
            st.rerun()
    with c3: 
        if st.button("⚙️"): st.session_state.v = "SETTINGS"; st.rerun()

# ROUTING
if st.session_state.v == "HOME": show_home()
elif st.session_state.v == "DETAIL": show_detail()
elif st.session_state.v == "SETTINGS": show_settings()
elif st.session_state.v == "CREATE":
    st.markdown("### Set New Goal")
    with st.container():
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        n = st.text_input("Goal Name")
        t = st.number_input("Target Amount", min_value=1)
        if st.button("ACTIVATE ➝"):
            if n and t > 0:
                st.session_state.g.append({"n": n, "t": t, "b": 0})
                st.session_state.v = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
