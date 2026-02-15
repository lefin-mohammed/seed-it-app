import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. ARCHITECTURAL UI (THE "APPLE WALLET" STYLE)
# ==========================================
st.set_page_config(page_title="Seed It Pro", page_icon="🏦", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }

    /* UNIFIED CONTAINER ALIGNMENT */
    .main-container { max-width: 400px; margin: auto; padding: 10px; }

    /* NEON GLASS CARDS */
    .glass-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 28px; padding: 24px; margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    /* SQUAD AVATARS ALIGNMENT */
    .squad-strip {
        display: flex; align-items: center; gap: -10px; margin-top: 15px;
    }
    .avatar {
        width: 32px; height: 32px; border-radius: 50%; 
        border: 2px solid #000; background: #222;
        display: flex; align-items: center; justify-content: center;
        font-size: 10px; font-weight: 800; margin-left: -8px;
    }

    /* TYPOGRAPHY */
    .label { color: #555; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; }
    .value { font-size: 24px; font-weight: 800; color: #00FF94; }

    /* ALIVE PROGRESS RING */
    .ring-container {
        position: relative; width: 200px; height: 200px; margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
    }
    .svg-ring { transform: rotate(-90deg); }
    .ring-bg { fill: none; stroke: #111; stroke-width: 8; }
    .ring-fill { 
        fill: none; stroke: #00FF94; stroke-width: 8; 
        stroke-linecap: round; transition: stroke-dasharray 1s ease;
    }

    /* NAVIGATION */
    .nav-bar {
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        width: 90%; background: rgba(15,15,15,0.8); border: 1px solid #222;
        border-radius: 24px; display: flex; justify-content: space-around; padding: 10px;
        backdrop-filter: blur(20px); z-index: 1000;
    }

    /* BUTTON ALIGNMENT */
    div.stButton > button {
        background: #FFFFFF; color: black; border-radius: 18px;
        padding: 14px; font-weight: 800; border: none; width: 100%;
        transition: 0.2s;
    }
    div.stButton > button:hover { background: #00FF94; color: black; }
    
    header, footer, .stDeployButton { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC & DATA MAPPING
# ==========================================
MY_UPI_ID = "phathim630@oksbi" 
MY_NAME = "Hathim p"

def get_icon(name):
    name = name.lower()
    if "car" in name: return "🚗"
    if "phone" in name: return "📱"
    if "home" in name: return "🏠"
    if "travel" in name: return "✈️"
    if "bike" in name: return "🏍️"
    return "🎯"

if 'view' not in st.session_state: st.session_state.view = "LOGIN"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'privacy' not in st.session_state: st.session_state.privacy = False

# ==========================================
# 3. SCREEN: LOGIN (CLEAN ALIGNMENT)
# ==========================================
def show_login():
    st.markdown("<br><br><br><h1 style='text-align:center; font-weight:800;'>SEED IT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#444;'>Secure Asset Locker</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        name = st.text_input("Name")
        age = st.text_input("Age")
        phone = st.text_input("Mobile Number")
        if st.button("LOGIN ➝"):
            if name and age and phone:
                st.session_state.user = {"name": name, "age": age, "phone": phone}
                st.session_state.view = "DASHBOARD"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: DASHBOARD (SQUAD FOCUS)
# ==========================================
def show_dashboard():
    # Top Bar
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"<span class='label'>User Portfolio</span><br><h2 style='margin:0;'>{st.session_state.user['name']}</h2>", unsafe_allow_html=True)
    with c2:
        if st.button("👁️" if not st.session_state.privacy else "🕶️"):
            st.session_state.privacy = not st.session_state.privacy
            st.rerun()

    if not st.session_state.goals:
        st.markdown("<div class='glass-card' style='text-align:center; margin-top:40px;'>No Active Goals</div>", unsafe_allow_html=True)
    else:
        for i, goal in enumerate(st.session_state.goals):
            prog = (goal['balance'] / goal['target'])
            offset = 565 - (prog * 565) # Calculation for SVG Ring
            
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            
            # THE RING UI
            st.markdown(f"""
                <div class='ring-container'>
                    <svg class='svg-ring' width='200' height='200'>
                        <circle class='ring-bg' cx='100' cy='100' r='90'></circle>
                        <circle class='ring-fill' cx='100' cy='100' r='90' style='stroke-dasharray: 565; stroke-dashoffset: {offset};'></circle>
                    </svg>
                    <div style='position:absolute; text-align:center;'>
                        <div style='font-size:40px;'>{get_icon(goal['name'])}</div>
                        <div class="{'privacy-blur' if st.session_state.privacy else ''} value">₹{goal['balance']:,}</div>
                        <div class='label'>of ₹{goal['target']:,}</div>
                    </div>
                </div>
                <div style='text-align:center; font-weight:800; font-size:18px; margin-bottom:10px;'>{goal['name'].upper()}</div>
            """, unsafe_allow_html=True)

            # THE SQUAD (VISUAL PEOPLE)
            if goal['type'] == "SQUAD":
                st.markdown("<span class='label'>Squad Members</span>", unsafe_allow_html=True)
                st.markdown("<div class='squad-strip'>", unsafe_allow_html=True)
                # Visual avatars for the people
                for member in goal['ledger']:
                    color = "#00FF94" if member == "YOU" else "#444"
                    st.markdown(f"<div class='avatar' style='border-color:{color};'>{member[0]}</div>", unsafe_allow_html=True)
                st.markdown(f"<span style='margin-left:15px; font-size:10px; color:#666;'>+ {len(goal['ledger'])} active savers</span></div>", unsafe_allow_html=True)

            # DEPOSIT
            with st.expander("DEPOSIT"):
                amt = st.number_input("Amount", min_value=1, key=f"amt_{i}")
                url = f"upi://pay?pa={MY_UPI_ID}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR"
                st.markdown(f"<a href='{url}' target='_self' style='text-decoration:none;'><div style='background:#00FF94; color:black; padding:12px; border-radius:12px; text-align:center; font-weight:800;'>SEND TO VAULT</div></a>", unsafe_allow_html=True)
                if st.button("CONFIRM PAYMENT ✅", key=f"conf_{i}"):
                    goal['balance'] += amt
                    goal['ledger']['YOU'] += amt
                    st.rerun()

            # WITHDRAW
            is_ready = goal['balance'] >= goal['target']
            if st.button("WITHDRAW FUNDS", disabled=not is_ready, key=f"wd_{i}"):
                st.session_state.goals.pop(i)
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: SET GOAL (PRECISION INPUT)
# ==========================================
def show_create():
    st.markdown("### SET NEW GOAL")
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        g_name = st.text_input("Goal Name (e.g. Car)")
        g_target = st.number_input("Target Amount (₹)", min_value=1)
        is_squad = st.toggle("Squad Goal")
        if st.button("CREATE GOAL ➝"):
            if g_name and g_target > 0:
                st.session_state.goals.append({
                    "name": g_name, "target": g_target, "balance": 0,
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 500, "RAHUL": 200, "HATHIM": 100} if is_squad else {"YOU": 0}
                })
                st.session_state.view = "DASHBOARD"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. NAVIGATION BOILERPLATE
# ==========================================
if st.session_state.view != "LOGIN":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("HOME"): st.session_state.view = "DASHBOARD"; st.rerun()
    with c2: 
        if st.button("GOAL"): st.session_state.view = "CREATE"; st.rerun()
    with c3: 
        if st.button("LOGOUT"): st.session_state.view = "LOGIN"; st.session_state.goals = []; st.rerun()

if st.session_state.view == "LOGIN": show_login()
elif st.session_state.view == "DASHBOARD": show_dashboard()
elif st.session_state.view == "CREATE": show_create()
