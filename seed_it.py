import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. ELITE DARK MODE UI (PREMIUM FINTECH)
# ==========================================
st.set_page_config(page_title="Seed It Infinity", page_icon="📈", layout="centered")

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
        background: linear-gradient(145deg, #121212, #080808);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 32px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.8);
        transition: transform 0.3s ease;
    }
    
    .mint { color: #00FF94; font-weight: 800; }
    .sub-text { color: #555555; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }

    /* CIRCULAR PROGRESS RING (ALIVE) */
    .progress-ring {
        width: 220px; height: 220px;
        border-radius: 50%;
        background: conic-gradient(#00FF94 var(--prog), #1A1A1A 0);
        display: flex; align-items: center; justify-content: center;
        margin: 25px auto;
        box-shadow: 0 0 40px rgba(0, 255, 148, 0.05);
        animation: pulse 3s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(0, 255, 148, 0.05); }
        50% { box-shadow: 0 0 50px rgba(0, 255, 148, 0.15); }
        100% { box-shadow: 0 0 20px rgba(0, 255, 148, 0.05); }
    }
    
    .progress-inner {
        width: 190px; height: 190px;
        background: #000000;
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        border: 1px solid rgba(255,255,255,0.03);
    }

    /* DASHBOARD WIDGETS */
    .widget-container {
        display: flex; justify-content: space-around;
        padding: 15px; background: #0A0A0A; border-radius: 20px;
        margin-bottom: 20px; border: 1px solid #111;
    }

    /* PRIVACY BLUR */
    .privacy-blur { filter: blur(12px); transition: 0.3s ease; }

    /* HIDE STREAMLIT BRANDING */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #0F0F0F; border-radius: 14px;
        padding: 0 24px; color: #666; border: 1px solid #222; font-weight: 700;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #00FF94 !important; color: black !important; 
        box-shadow: 0 5px 15px rgba(0, 255, 148, 0.2);
    }

    /* BUTTONS */
    div.stButton > button {
        background: #00FF94; color: black; border-radius: 20px;
        padding: 18px; font-weight: 900; border: none; width: 100%;
        font-size: 16px; transition: 0.2s;
    }
    div.stButton > button:active { transform: scale(0.96); opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONFIG & SMART LOGIC
# ==========================================
MY_UPI_ID = "phathim630@oksbi" 
MY_NAME = "Hathim p"

def get_goal_icon(name):
    name = name.lower()
    if any(x in name for x in ["car", "drive", "bmw", "audi"]): return "🚗"
    if any(x in name for x in ["phone", "iphone", "mobile"]): return "📱"
    if any(x in name for x in ["home", "house", "room"]): return "🏠"
    if any(x in name for x in ["travel", "trip", "goa", "flight"]): return "✈️"
    if any(x in name for x in ["bike", "cycle", "gt", "royal"]): return "🏍️"
    if any(x in name for x in ["pizza", "food", "party"]): return "🍕"
    if any(x in name for x in ["gym", "fit", "health"]): return "💪"
    if any(x in name for x in ["watch", "apple", "role-x"]): return "⌚"
    return "🎯"

if 'view' not in st.session_state: st.session_state.view = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'privacy' not in st.session_state: st.session_state.privacy = False
if 'history' not in st.session_state: st.session_state.history = []

# ==========================================
# 3. SCREEN: PREMIUM ONBOARDING
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; font-size:52px; letter-spacing:-2px;'>SEED <span class='mint'>IT</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#555; font-size:12px; font-weight:700;'>SECURE BEHAVIORAL ESCROW</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("FULL NAME", key="reg_name", placeholder="e.g. K M LEFIN MOHAMMED")
        age = st.text_input("AGE", key="reg_age", placeholder="19")
        phone = st.text_input("MOBILE NUMBER", key="reg_phone", placeholder="+91 XXXX XXX XXX")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INITIALIZE BIOMETRICS ➝"):
            if name and age and phone:
                st.session_state.user = {"name": name, "age": age, "phone": phone}
                st.session_state.view = "DASHBOARD"
                st.rerun()
            else:
                st.error("Authentication data required.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: DASHBOARD (ALIVE UI)
# ==========================================
def show_dashboard():
    # Dynamic Header
    h1, h2 = st.columns([5, 1])
    with h1:
        st.markdown(f"<span class='sub-text'>ACTIVE PORTFOLIO</span><br><h2 style='margin:0;'>{st.session_state.user['name'].split()[0]}</h2>", unsafe_allow_html=True)
    with h2:
        if st.button("👁️" if not st.session_state.privacy else "🕶️"):
            st.session_state.privacy = not st.session_state.privacy
            st.rerun()

    # Asset Overview Widget
    total_val = sum(g['balance'] for g in st.session_state.goals)
    st.markdown(f"""
        <div class='widget-container'>
            <div style='text-align:center;'><span class='sub-text'>TOTAL LOCKED</span><br><b class="{'privacy-blur' if st.session_state.privacy else ''}" style='font-size:18px;'>₹{total_val:,}</b></div>
            <div style='text-align:center;'><span class='sub-text'>ACTIVE GOALS</span><br><b style='font-size:18px;'>{len(st.session_state.goals)}</b></div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.goals:
        st.markdown("<br><div class='app-card' style='text-align:center;'><h4 style='color:#333;'>YOUR VAULT IS EMPTY</h4><p class='sub-text'>Tap + to set a new goal.</p></div>", unsafe_allow_html=True)
    else:
        # GOAL TABS (UX IMPROVEMENT)
        tab_titles = [g['name'].upper() for g in st.session_state.goals]
        tabs = st.tabs(tab_titles)

        for i, tab in enumerate(tabs):
            with tab:
                goal = st.session_state.goals[i]
                prog_pct = int((goal['balance'] / goal['target']) * 100) if goal['target'] > 0 else 0
                prog_clamped = min(prog_pct, 100)
                
                # Dynamic Breathing Background based on progress
                glow_opacity = prog_clamped / 400
                st.markdown(f"""
                    <div class='app-card' style='background: radial-gradient(circle at top right, rgba(0, 255, 148, {glow_opacity}), transparent);'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span class='sub-text'>GOAL PROGRESS</span>
                            <span class='mint'>{prog_clamped}%</span>
                        </div>
                        <div class='progress-ring' style='--prog: {prog_clamped}%;'>
                            <div class='progress-inner'>
                                <div style='font-size:55px; margin-bottom:5px;'>{get_goal_icon(goal['name'])}</div>
                                <div class="{'privacy-blur' if st.session_state.privacy else ''}" style='font-size:28px; font-weight:900;'>₹{goal['balance']:,}</div>
                                <div class='sub-text'>TARGET: ₹{goal['target']:,}</div>
                            </div>
                        </div>
                """, unsafe_allow_html=True)

                # TRANSACTION TOOLS
                col_top, col_wd = st.columns(2)
                with col_top:
                    with st.expander("💸 TOP UP"):
                        amt = st.number_input("Amount (₹)", min_value=1, key=f"amt_{i}")
                        encoded_name = urllib.parse.quote(MY_NAME)
                        upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={encoded_name}&am={amt}&cu=INR&mode=02&tr=SEED{int(time.time())}"
                        
                        st.markdown(f"""<a href="{upi_url}" target="_self" style="text-decoration:none;"><div style="background:#00FF94; color:black; padding:15px; border-radius:16px; text-align:center; font-weight:900; margin-bottom:10px;">OPEN UPI APP ➝</div></a>""", unsafe_allow_html=True)
                        
                        if st.button("CONFIRM PAYMENT ✅", key=f"conf_{i}"):
                            goal['balance'] += amt
                            st.session_state.history.append({"msg": f"Top-up: {goal['name']}", "amt": f"+₹{amt}", "time": datetime.now().strftime("%H:%M")})
                            st.toast("Vault Updated!")
                            time.sleep(0.5)
                            st.rerun()

                with col_wd:
                    is_locked = goal['balance'] < goal['target']
                    if st.button("🔓 WITHDRAW", disabled=is_locked, key=f"wd_{i}"):
                        st.balloons()
                        st.session_state.history.append({"msg": f"Harvested: {goal['name']}", "amt": f"-₹{goal['balance']}", "time": datetime.now().strftime("%H:%M")})
                        st.session_state.goals.pop(i)
                        st.rerun()
                
                if is_locked:
                    st.markdown("<p style='text-align:center; font-size:10px; color:#444; margin-top:10px; font-weight:bold;'>ESCROW LOCK ACTIVE 🛡️</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    # Activity Feed (Mimicking your Image)
    if st.session_state.history:
        st.markdown("<span class='sub-text'>RECENT ACTIVITY</span>", unsafe_allow_html=True)
        for log in reversed(st.session_state.history[-3:]):
            st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:15px; background:#0A0A0A; border-radius:15px; margin-bottom:10px; border-left:4px solid #00FF94;'>
                    <div><div style='font-size:13px; font-weight:bold;'>{log['msg']}</div><div style='font-size:10px; color:#444;'>{log['time']} Today</div></div>
                    <div class='mint' style='font-weight:900;'>{log['amt']}</div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: SET A NEW GOAL
# ==========================================
def show_create():
    st.markdown("### Set a New Goal")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("WHAT ARE WE SAVING FOR?", placeholder="e.g. BMW M3")
        target = st.number_input("TARGET AMOUNT (₹)", min_value=1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        is_squad = st.toggle("SQUAD MODE (POOL WITH FRIENDS)")
        
        if st.button("INITIALIZE GOAL ➝"):
            if name and target >= 1:
                st.session_state.goals.append({
                    "name": name, "target": target, "balance": 0,
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 500, "RAHUL": 120} if is_squad else {"YOU": 0}
                })
                st.session_state.view = "DASHBOARD"
                st.rerun()
            else:
                st.error("Goal name and target amount required.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. ROUTING & STICKY NAVIGATION
# ==========================================
if st.session_state.view != "AUTH":
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    nav_col = st.columns(3)
    with nav_col[0]: 
        if st.button("🏠 Dashboard"): st.session_state.view = "DASHBOARD"; st.rerun()
    with nav_col[1]: 
        if st.button("➕ Set Goal"): st.session_state.view = "CREATE"; st.rerun()
    with nav_col[2]: 
        if st.button("⚙️ Settings"): st.session_state.view = "SETTINGS"; st.rerun()

if st.session_state.view == "AUTH": show_auth()
elif st.session_state.view == "DASHBOARD": show_dashboard()
elif st.session_state.view == "CREATE": show_create()
elif st.session_state.view == "SETTINGS":
    st.markdown("### Account Settings")
    st.markdown(f"<div class='app-card'><span class='sub-text'>USER PROFILE</span><br><b>{st.session_state.user['name']}</b><br>Age: {st.session_state.user['age']}<br><br><span class='sub-text'>UPI LINK</span><br><b>{MY_UPI_ID}</b></div>", unsafe_allow_html=True)
    if st.button("WIPE DATA & LOGOUT"):
        st.session_state.view = "AUTH"
        st.session_state.goals = []
        st.session_state.history = []
        st.rerun()
