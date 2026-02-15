import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. ELITE DARK MODE UI (PREMIUM FINTECH)
# ==========================================
st.set_page_config(page_title="Seed It Infinity", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    /* GLOBAL DARK THEME */
    .stApp { 
        background: #000000; 
        color: #FFFFFF; 
        font-family: 'Outfit', sans-serif;
    }

    /* GLASSMORPHISM CARDS */
    .app-card {
        background: linear-gradient(145deg, #0F0F0F, #050505);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    
    .mint { color: #00FF94; font-weight: 800; }
    .sub-text { color: #555555; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }

    /* CIRCULAR PROGRESS RING */
    .progress-ring {
        width: 200px; height: 200px;
        border-radius: 50%;
        background: conic-gradient(#00FF94 var(--prog), #111111 0);
        display: flex; align-items: center; justify-content: center;
        margin: 25px auto;
        box-shadow: 0 0 30px rgba(0, 255, 148, 0.1);
    }
    .progress-inner {
        width: 170px; height: 170px;
        background: #000000;
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }

    /* ACTION BUTTONS (NEUMORPHIC DARK) */
    .btn-container { display: flex; gap: 12px; margin-top: 20px; }
    
    /* PRIVACY BLUR */
    .privacy-blur { filter: blur(10px); transition: 0.3s; }

    /* HIDE STREAMLIT BARS */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; background-color: #0F0F0F; border-radius: 12px;
        padding: 0 20px; color: #555; border: 1px solid #222;
    }
    .stTabs [aria-selected="true"] { background-color: #00FF94 !important; color: black !important; }

    div.stButton > button {
        background: #00FF94; color: black; border-radius: 18px;
        padding: 16px; font-weight: 800; border: none; width: 100%;
        font-size: 16px; box-shadow: 0 10px 20px rgba(0, 255, 148, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONFIG & LOGIC
# ==========================================
MY_UPI_ID = "phathim630@oksbi" 
MY_NAME = "Hathim p"

def get_goal_icon(name):
    name = name.lower()
    if any(x in name for x in ["car", "drive"]): return "🚗"
    if any(x in name for x in ["phone", "iphone", "mobile"]): return "📱"
    if any(x in name for x in ["home", "house", "room"]): return "🏠"
    if any(x in name for x in ["travel", "trip", "goa", "flight"]): return "✈️"
    if any(x in name for x in ["bike", "cycle", "gt", "royal"]): return "🏍️"
    if any(x in name for x in ["pizza", "food", "party"]): return "🍕"
    if any(x in name for x in ["gym", "fit", "health"]): return "💪"
    return "🎯"

if 'view' not in st.session_state: st.session_state.view = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'privacy' not in st.session_state: st.session_state.privacy = False

# ==========================================
# 3. SCREEN: ONBOARDING
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center;'>SEED <span class='mint'>IT</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#444; font-size:12px;'>ELITE BEHAVIORAL ESCROW</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("FULL NAME", key="reg_name", placeholder="K M LEFIN MOHAMMED")
        age = st.text_input("AGE", key="reg_age", placeholder="19")
        phone = st.text_input("MOBILE NUMBER", key="reg_phone", placeholder="9876543210")
        
        if st.button("GET STARTED ➝"):
            if name and age and phone:
                st.session_state.user = {"name": name, "age": age, "phone": phone}
                st.session_state.view = "DASHBOARD"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: DASHBOARD (TABBED)
# ==========================================
def show_dashboard():
    # Header with Privacy Mode
    h1, h2 = st.columns([5, 1])
    with h1:
        st.markdown(f"<span class='sub-text'>WELCOME BACK</span><br><h2 style='margin:0;'>{st.session_state.user['name'].split()[0]}</h2>", unsafe_allow_html=True)
    with h2:
        if st.button("👁️" if not st.session_state.privacy else "🕶️"):
            st.session_state.privacy = not st.session_state.privacy
            st.rerun()

    if not st.session_state.goals:
        st.markdown("<br><div class='app-card' style='text-align:center;'><h4 style='color:#333;'>NO ACTIVE SEEDS</h4><p class='sub-text'>Your vault is empty.</p></div>", unsafe_allow_html=True)
    else:
        # GOAL TABS
        tab_titles = [g['name'].upper() for g in st.session_state.goals]
        tabs = st.tabs(tab_titles)

        for i, tab in enumerate(tabs):
            with tab:
                goal = st.session_state.goals[i]
                prog_pct = int((goal['balance'] / goal['target']) * 100) if goal['target'] > 0 else 0
                prog_clamped = min(prog_pct, 100)
                
                # Dynamic Background Logic
                bg_grad = f"rgba(0, 255, 148, {prog_clamped/400})"
                
                st.markdown(f"""
                    <div class='app-card' style='background: {bg_grad};'>
                        <div class='progress-ring' style='--prog: {prog_clamped}%;'>
                            <div class='progress-inner'>
                                <div style='font-size:45px;'>{get_goal_icon(goal['name'])}</div>
                                <div class="{'privacy-blur' if st.session_state.privacy else ''}" style='font-size:24px; font-weight:900;'>₹{goal['balance']:,}</div>
                                <div class='sub-text'>Target: ₹{goal['target']:,}</div>
                            </div>
                        </div>
                """, unsafe_allow_html=True)

                # TOP UP SECTION
                with st.expander("💸 ADD FUNDS"):
                    amt = st.number_input("Amount", min_value=1, key=f"amt_{i}")
                    encoded_name = urllib.parse.quote(MY_NAME)
                    upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={encoded_name}&am={amt}&cu=INR&mode=02&tr=SEED{int(time.time())}"
                    
                    st.markdown(f"""<a href="{upi_url}" target="_self" style="text-decoration:none;"><div style="background:#00FF94; color:black; padding:15px; border-radius:15px; text-align:center; font-weight:900; margin-bottom:10px;">OPEN UPI APP 📱</div></a>""", unsafe_allow_html=True)
                    
                    if st.button("I HAVE PAID ✅", key=f"conf_{i}"):
                        goal['balance'] += amt
                        st.toast("Contribution logged!")
                        time.sleep(0.5)
                        st.rerun()

                # WITHDRAWAL STATUS
                is_locked = goal['balance'] < goal['target']
                if st.button("🏆 HARVEST ASSET", disabled=is_locked, key=f"wd_{i}"):
                    st.balloons()
                    st.session_state.goals.pop(i)
                    st.rerun()
                
                if is_locked:
                    st.markdown("<p style='text-align:center; font-size:10px; color:#444; margin-top:10px;'>🔒 FUND IS CURRENTLY IN ESCROW</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: SET A NEW GOAL
# ==========================================
def show_plant():
    st.markdown("### 🌱 Plant New Seed")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("GOAL NAME", placeholder="e.g. Iphone 17 pro max")
        target = st.number_input("TARGET AMOUNT (₹)", min_value=1)
        is_squad = st.toggle("SQUAD GOAL (GROUP SAVING)")
        
        if st.button("INITIALIZE VAULT ➝"):
            if name and target >= 1:
                st.session_state.goals.append({
                    "name": name, "target": target, "balance": 0,
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 500} if is_squad else {"YOU": 0}
                })
                st.session_state.view = "DASHBOARD"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. ROUTING & NAVIGATION
# ==========================================
if st.session_state.view != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("Dashboard"): st.session_state.view = "DASHBOARD"; st.rerun()
    with c2: 
        if st.button("set a new goal"): st.session_state.view = "SET A NEW GOAL"; st.rerun()
    with c3: 
        if st.button("Settings"): st.session_state.view = "SETTINGS"; st.rerun()

if st.session_state.view == "AUTH": show_auth()
elif st.session_state.view == "DASHBOARD": show_dashboard()
elif st.session_state.view == "SET A NEW GOAL": show_set a new goal()
elif st.session_state.view == "SETTINGS":
    st.markdown("### Settings")
    st.markdown(f"<div class='app-card'><b>{st.session_state.user['name']}</b><br><span class='sub-text'>HATHIM'S SEED IT PROTOCOL</span></div>", unsafe_allow_html=True)
    if st.button("LOGOUT"):
        st.session_state.view = "AUTH"
        st.session_state.goals = []
        st.rerun()
