import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. FAMPAY DESIGN ENGINE (ELITE DARK)
# ==========================================
st.set_page_config(page_title="Seed It Elite", page_icon="💳", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;900&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }

    /* FAMPAY CARD STYLE */
    .elite-card {
        background: #111111;
        border: 1px solid #1A1A1A;
        border-radius: 32px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }

    /* QUICK ACTIONS (STORY STYLE) */
    .story-container {
        display: flex; gap: 15px; overflow-x: auto; padding: 10px 0;
        scrollbar-width: none;
    }
    .story-circle {
        min-width: 65px; height: 65px; border-radius: 50%;
        border: 2px solid #DFFF00; display: flex; align-items: center;
        justify-content: center; font-weight: 800; font-size: 14px;
    }

    /* TYPOGRAPHY */
    .f-label { color: #666; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
    .f-value { font-size: 32px; font-weight: 900; color: #DFFF00; }
    
    /* PROGRESS BAR (THICK & NEON) */
    .stProgress > div > div > div > div { background-color: #DFFF00; height: 12px; border-radius: 10px; }

    /* BUTTONS */
    div.stButton > button {
        background: #DFFF00; color: black; border-radius: 24px;
        padding: 18px; font-weight: 900; border: none; width: 100%;
        font-size: 16px; margin-top: 10px;
    }
    
    /* SETTINGS LOGOUT BUTTON */
    .logout-btn button { background: #FF4B4B !important; color: white !important; }

    header, footer, .stDeployButton { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE DATA
# ==========================================
MY_VPA = "phathim630@oksbi" 
MY_NAME = "Hathim p"

if 'v' not in st.session_state: st.session_state.v = "AUTH"
if 'g' not in st.session_state: st.session_state.g = []

# ==========================================
# 3. SCREEN: LOGIN
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; font-weight:900; letter-spacing:-2px; font-size:50px;'>SEED<span style='color:#DFFF00;'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        st.markdown("<p class='f-label'>MOBILE NUMBER</p>", unsafe_allow_html=True)
        phone = st.text_input("Mobile", label_visibility="collapsed", placeholder="+91")
        st.markdown("<p class='f-label'>YOUR NAME</p>", unsafe_allow_html=True)
        name = st.text_input("Name", label_visibility="collapsed", placeholder="Full Name")
        if st.button("VERIFY ➝"):
            if name and phone:
                st.session_state.user = {"name": name, "phone": phone}
                st.session_state.v = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: DASHBOARD
# ==========================================
def show_home():
    st.markdown(f"### Hello, {st.session_state.user['name'].split()[0]}!")
    
    # TOTAL BALANCE CARD
    total = sum(item['b'] for item in st.session_state.g)
    st.markdown(f"""
        <div class='elite-card' style='background: #DFFF00; color: black;'>
            <p style='font-weight:700; font-size:12px; opacity:0.6;'>TOTAL ASSETS LOCKED</p>
            <h1 style='margin:0; font-weight:900;'>₹{total:,}</h1>
        </div>
    """, unsafe_allow_html=True)

    # SQUAD STORIES
    st.markdown("<p class='f-label'>YOUR SQUAD</p>", unsafe_allow_html=True)
    st.markdown("""
        <div class='story-container'>
            <div class='story-circle' style='background:#222; border-color:#DFFF00;'>YOU</div>
            <div class='story-circle'>F</div>
            <div class='story-circle'>H</div>
            <div class='story-circle'>R</div>
            <div class='story-circle' style='border-style:dashed; opacity:0.3;'>+</div>
        </div>
    """, unsafe_allow_html=True)

    # GOAL CARDS
    if not st.session_state.g:
        st.markdown("<div class='elite-card' style='text-align:center; opacity:0.5;'>No Active Goals</div>", unsafe_allow_html=True)
    else:
        for i, goal in enumerate(st.session_state.g):
            prog = (goal['b'] / goal['t'])
            st.markdown(f"<div class='elite-card'>", unsafe_allow_html=True)
            st.markdown(f"<b>{goal['n'].upper()}</b>", unsafe_allow_html=True)
            st.progress(prog)
            st.markdown(f"<div style='display:flex; justify-content:space-between;'><span class='f-label'>₹{goal['b']}</span><span class='f-label'>TARGET: ₹{goal['t']}</span></div>", unsafe_allow_html=True)
            
            with st.expander("TOP UP"):
                amt = st.number_input("Amount", min_value=1, key=f"a_{i}")
                url = f"upi://pay?pa={MY_VPA}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR"
                st.markdown(f"<a href='{url}' target='_self' style='text-decoration:none;'><div style='background:#DFFF00; color:black; padding:12px; border-radius:12px; text-align:center; font-weight:800;'>SEND TO LOCKER</div></a>", unsafe_allow_html=True)
                if st.button("I PAID", key=f"c_{i}"):
                    goal['b'] += amt
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: SET GOAL
# ==========================================
def show_create():
    st.markdown("### SET NEW GOAL")
    with st.container():
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        name = st.text_input("GOAL NAME", placeholder="e.g. Royal Enfield")
        target = st.number_input("TARGET AMOUNT (₹)", min_value=1)
        if st.button("ACTIVATE LOCKER"):
            if name and target > 0:
                st.session_state.g.append({"n": name, "t": target, "b": 0})
                st.session_state.v = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. SCREEN: SETTINGS (LOGOUT HERE)
# ==========================================
def show_settings():
    st.markdown("### SETTINGS")
    st.markdown(f"""
        <div class='elite-card'>
            <p class='f-label'>USER PROFILE</p>
            <b>{st.session_state.user['name']}</b><br>
            <span style='color:#666;'>{st.session_state.user['phone']}</span>
            <hr style='border-color:#222;'>
            <p class='f-label'>SETTLEMENT VPA</p>
            <b>{MY_VPA}</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("LOGOUT & WIPE DATA"):
        st.session_state.v = "AUTH"
        st.session_state.g = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# NAVIGATION
# ==========================================
if st.session_state.v != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("HOME"): st.session_state.v = "HOME"; st.rerun()
    with c2: 
        if st.button("PLUS"): st.session_state.view = "CREATE"; st.session_state.v = "CREATE"; st.rerun()
    with c3: 
        if st.button("GEAR"): st.session_state.v = "SETTINGS"; st.rerun()

if st.session_state.v == "AUTH": show_auth()
elif st.session_state.v == "HOME": show_home()
elif st.session_state.v == "CREATE": show_create()
elif st.session_state.v == "SETTINGS": show_settings()
