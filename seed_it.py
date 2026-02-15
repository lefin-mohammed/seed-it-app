import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. SIGNATURE UI ENGINE (OLED BLACK & LIME)
# ==========================================
st.set_page_config(page_title="Seed It Signature", page_icon="💳", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;900&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }

    /* ELITE CARD COMPONENT */
    .f-card {
        background: #0A0A0A;
        border: 1px solid #151515;
        border-radius: 28px;
        padding: 24px;
        margin-bottom: 16px;
        transition: 0.3s ease;
    }
    
    .accent { color: #CBFF00; font-weight: 900; }
    .muted { color: #444444; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; }

    /* SQUAD AVATARS */
    .squad-group { display: flex; align-items: center; margin-top: 10px; }
    .squad-user {
        width: 30px; height: 30px; border-radius: 50%; border: 2px solid #000;
        background: #1A1A1A; display: flex; align-items: center; justify-content: center;
        font-size: 9px; font-weight: 900; margin-right: -10px; color: #CBFF00;
    }

    /* NAVIGATION BAR */
    .nav-bar {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(0,0,0,0.8); backdrop-filter: blur(15px);
        display: flex; justify-content: space-around; padding: 20px 0;
        border-top: 1px solid #111; z-index: 999;
    }

    /* CUSTOM PROGRESS */
    .stProgress > div > div > div > div { background-color: #CBFF00; height: 8px; border-radius: 4px; }

    /* INPUTS & BUTTONS */
    div.stButton > button {
        background: #CBFF00; color: #000; border-radius: 16px;
        padding: 14px; font-weight: 900; border: none; width: 100%;
    }
    .logout-zone button { background: #FF3B30 !important; color: white !important; }

    header, footer, .stDeployButton { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE SYSTEM DATA
# ==========================================
MY_VPA = "phathim630@oksbi" 
MY_NAME = "Hathim p"

if 'v' not in st.session_state: st.session_state.v = "AUTH"
if 'g' not in st.session_state: st.session_state.g = []
if 'p' not in st.session_state: st.session_state.p = False # Privacy Mode

# ==========================================
# 3. SCREEN: LOGIN
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; font-weight:900; font-size:50px;'>SEED<span class='accent'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='f-card'>", unsafe_allow_html=True)
        name = st.text_input("NAME", placeholder="Full Name")
        age = st.text_input("AGE", placeholder="19")
        phone = st.text_input("MOBILE", placeholder="+91")
        if st.button("VERIFY IDENTITY ➝"):
            if name and age and phone:
                st.session_state.user = {"n": name, "a": age, "p": phone}
                st.session_state.v = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: DASHBOARD
# ==========================================
def show_home():
    # Header
    c1, c2 = st.columns([5,1])
    with c1: st.markdown(f"### Hello, {st.session_state.user['n'].split()[0]}")
    with c2: 
        if st.button("👁️"): 
            st.session_state.p = not st.session_state.p
            st.rerun()

    # Total Wealth Card
    total = sum(item['b'] for item in st.session_state.g)
    st.markdown(f"""
        <div class='f-card' style='background: #CBFF00; color: #000;'>
            <p class='muted' style='color:#000; opacity:0.6;'>NET ASSETS SECURED</p>
            <h1 style='margin:0; font-weight:900;'>₹{"****" if st.session_state.p else f"{total:,}"}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Goals Stack
    if not st.session_state.g:
        st.markdown("<div class='f-card' style='text-align:center; color:#333;'>VAULT EMPTY</div>", unsafe_allow_html=True)
    else:
        for i, goal in enumerate(st.session_state.g):
            prog = (goal['b'] / goal['t'])
            st.markdown(f"<div class='f-card'>", unsafe_allow_html=True)
            st.markdown(f"<p class='muted'>{goal['n']}</p>", unsafe_allow_html=True)
            st.progress(prog)
            st.markdown(f"<div style='display:flex; justify-content:space-between; margin-top:10px;'><span style='font-weight:900;'>₹{goal['b']}</span><span class='muted'>Target: ₹{goal['t']}</span></div>", unsafe_allow_html=True)
            
            # Squad UI
            if goal.get('squad'):
                st.markdown("<div class='squad-group'><div class='squad-user'>Y</div><div class='squad-user'>F</div><div class='squad-user'>H</div></div>", unsafe_allow_html=True)

            with st.expander("TOP UP"):
                amt = st.number_input("Amount", min_value=1, key=f"a_{i}")
                url = f"upi://pay?pa={MY_VPA}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR"
                st.markdown(f"<a href='{url}' target='_self' style='text-decoration:none;'><div style='background:#CBFF00; color:#000; padding:12px; border-radius:12px; text-align:center; font-weight:800;'>SEND TO UPI</div></a>", unsafe_allow_html=True)
                if st.button("I PAID ✅", key=f"c_{i}"):
                    goal['b'] += amt
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: SET GOAL
# ==========================================
def show_create():
    st.markdown("### Set New Goal")
    with st.container():
        st.markdown("<div class='f-card'>", unsafe_allow_html=True)
        name = st.text_input("Goal Name", placeholder="e.g. BMW M3")
        target = st.number_input("Target Amount (₹)", min_value=1)
        is_squad = st.toggle("Enable Squad Mode")
        if st.button("ACTIVATE ➝"):
            if name and target > 0:
                st.session_state.g.append({"n": name, "t": target, "b": 0, "squad": is_squad})
                st.session_state.v = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. SCREEN: SETTINGS (LOGOUT)
# ==========================================
def show_settings():
    st.markdown("### Settings")
    st.markdown(f"""
        <div class='f-card'>
            <p class='muted'>PROFILE</p>
            <b>{st.session_state.user['n']}</b><br>
            <span style='color:#555;'>{st.session_state.user['p']}</span>
            <hr style='border-color:#111;'>
            <p class='muted'>ESCROW ACCOUNT</p>
            <b>{MY_VPA}</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='logout-zone'>", unsafe_allow_html=True)
    if st.button("DISCONNECT & LOGOUT"):
        st.session_state.v = "AUTH"
        st.session_state.g = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
if st.session_state.v != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("HOME"): st.session_state.v = "HOME"; st.rerun()
    with c2: 
        if st.button("GOAL"): st.session_state.v = "CREATE"; st.rerun()
    with c3: 
        if st.button("GEAR"): st.session_state.v = "SETTINGS"; st.rerun()

if st.session_state.v == "AUTH": show_auth()
elif st.session_state.v == "HOME": show_home()
elif st.session_state.v == "CREATE": show_create()
elif st.session_state.v == "SETTINGS": show_settings()
