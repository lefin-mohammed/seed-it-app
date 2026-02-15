import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. PREMIUM NEUMORPHIC UI (LIGHT THEME)
# ==========================================
st.set_page_config(page_title="Seed It Infinity", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    /* MOBILE LIGHT THEME */
    .stApp { 
        background: #F0F4F3; 
        color: #1A1A1A; 
        font-family: 'Outfit', sans-serif;
    }

    /* NEUMORPHIC CARDS */
    .app-card {
        background: #F0F4F3;
        border-radius: 30px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 10px 10px 20px #D1D9D7, -10px -10px 20px #FFFFFF;
    }
    
    .accent-text { color: #00A67E; font-weight: 800; }
    .sub-text { color: #8E9A97; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }

    /* CIRCULAR PROGRESS RING SIMULATION */
    .progress-ring {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: conic-gradient(#00A67E var(--prog), #E0EAE8 0);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        box-shadow: inset 5px 5px 10px #D1D9D7, inset -5px -5px 10px #FFFFFF;
    }
    .progress-inner {
        width: 150px;
        height: 150px;
        background: #F0F4F3;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 5px 5px 10px #D1D9D7, -5px -5px 10px #FFFFFF;
    }

    /* TOP-UP & WITHDRAW BUTTONS */
    .action-btn {
        background: #F0F4F3;
        border: none;
        border-radius: 15px;
        padding: 12px 20px;
        box-shadow: 5px 5px 10px #D1D9D7, -5px -5px 10px #FFFFFF;
        font-weight: 700;
        color: #1A1A1A;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* BOTTOM NAV */
    .nav-item { text-align: center; font-size: 10px; font-weight: 700; color: #8E9A97; }
    .nav-active { color: #00A67E; }

    /* PRIVACY BLUR */
    .privacy-blur { filter: blur(8px); pointer-events: none; }

    /* HIDDEN ELEMENTS */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stButton > button {
        background: #00A67E; color: white; border-radius: 15px;
        padding: 15px; font-weight: 800; border: none; width: 100%;
        box-shadow: 5px 5px 15px rgba(0,166,126,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE CONFIG & SMART ICONS
# ==========================================
MY_UPI_ID = "phathim630@oksbi" 
MY_NAME = "Hathim p"

# Smart Category Logic
def get_goal_icon(name):
    name = name.lower()
    if any(x in name for x in ["car", "drive", "vehicle"]): return "🚗"
    if any(x in name for x in ["phone", "iphone", "mobile"]): return "📱"
    if any(x in name for x in ["home", "house", "rent"]): return "🏠"
    if any(x in name for x in ["travel", "trip", "flight", "goa"]): return "✈️"
    if any(x in name for x in ["bike", "cycle", "royal"]): return "🏍️"
    if any(x in name for x in ["food", "pizza", "party"]): return "🍕"
    return "🎯"

# Initialize Session
if 'view' not in st.session_state: st.session_state.view = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'privacy' not in st.session_state: st.session_state.privacy = False
if 'auto_save' not in st.session_state: st.session_state.auto_save = False

# ==========================================
# 3. APP SCREENS
# ==========================================

def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; color:#00A67E;'>🌱 Seed It</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("NAME", placeholder="Lefin Mohammed")
        age = st.text_input("AGE", placeholder="19")
        phone = st.text_input("MOBILE", placeholder="+91 XXXX")
        if st.button("AUTHENTICATE"):
            if name and age and phone:
                st.session_state.user = {"name": name, "age": age, "phone": phone}
                st.session_state.view = "DASHBOARD"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def show_dashboard():
    # Header with Privacy Toggle
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"**Hello, {st.session_state.user['name']}!**")
    with c2:
        if st.button("👁️" if not st.session_state.privacy else "🕶️"):
            st.session_state.privacy = not st.session_state.privacy
            st.rerun()

    if not st.session_state.goals:
        st.markdown("<div class='app-card' style='text-align:center; padding:50px;'><h3 style='color:#8E9A97;'>Your Garden is Empty</h3><p>Tap + to plant your first goal</p></div>", unsafe_allow_html=True)
    else:
        # TABS FOR GOALS
        goal_names = [g['name'] for g in st.session_state.goals]
        selected_goal_name = st.tabs(goal_names)
        
        for i, tab in enumerate(selected_goal_name):
            with tab:
                goal = st.session_state.goals[i]
                prog_pct = int((goal['balance'] / goal['target']) * 100) if goal['target'] > 0 else 0
                prog_clamped = min(max(prog_pct, 0), 100)
                
                # Dynamic Background Logic (Subtle Overlay)
                bg_opacity = prog_clamped / 200 # Max 0.5 opacity
                st.markdown(f"""
                    <div class='app-card' style='background: rgba(0, 166, 126, {bg_opacity});'>
                        <div class='progress-ring' style='--prog: {prog_clamped}%;'>
                            <div class='progress-inner'>
                                <div style='font-size:40px;'>{get_goal_icon(goal['name'])}</div>
                                <div class="{'privacy-blur' if st.session_state.privacy else ''}" style='font-size:20px; font-weight:900;'>₹{goal['balance']:,}</div>
                                <div class='sub-text'>of ₹{goal['target']:,}</div>
                            </div>
                        </div>
                """, unsafe_allow_html=True)

                # Action Buttons (Top Up / Withdraw)
                col_a, col_b = st.columns(2)
                with col_a:
                    with st.expander("➕ Top up"):
                        amt = st.number_input("Amount", min_value=1, key=f"amt_{i}")
                        upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR&mc=0000"
                        st.markdown(f"<a href='{upi_url}' target='_self'><div style='background:#00A67E; color:white; padding:10px; border-radius:10px; text-align:center;'>Open UPI App</div></a>", unsafe_allow_html=True)
                        if st.button("I have Paid ✅", key=f"pay_{i}"):
                            goal['balance'] += amt
                            st.toast("Contribution logged!")
                            time.sleep(0.5)
                            st.rerun()
                with col_b:
                    is_locked = goal['balance'] < goal['target']
                    if st.button("🔓 Withdraw", disabled=is_locked, key=f"wd_{i}"):
                        st.balloons()
                        st.session_state.goals.pop(i)
                        st.rerun()
                
                # SQUAD LEDGER
                if goal['type'] == "SQUAD":
                    st.markdown("<hr style='border: 0.5px solid #E0EAE8;'>", unsafe_allow_html=True)
                    st.markdown("**Squad Contributions**")
                    ledger_cols = st.columns(len(goal['ledger']))
                    for idx, (member, m_amt) in enumerate(goal['ledger'].items()):
                        with ledger_cols[idx]:
                            st.markdown(f"<div style='font-size:10px; color:#8E9A97;'>{member}</div><div style='font-weight:bold;'>₹{m_amt}</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

def show_plant():
    st.markdown("### 🌱 Plant Seed")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("Goal Name (e.g., iPhone 17)", key="g_name")
        target = st.number_input("Target Amount (₹)", min_value=1, key="g_target")
        is_squad = st.toggle("Squad Goal")
        if st.button("Plant Goal"):
            if name and target > 0:
                st.session_state.goals.append({
                    "name": name, "target": target, "balance": 0,
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 250, "RAHUL": 100} if is_squad else {"YOU": 0}
                })
                st.session_state.view = "DASHBOARD"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def show_settings():
    st.markdown("### Settings")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.session_state.auto_save = st.toggle("Daily Automatic Savings", value=st.session_state.auto_save)
        st.caption("When enabled, Seed It will round up your transactions and save the change.")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"**Linked Account:** {MY_UPI_ID}")
        if st.button("Log Out"):
            st.session_state.view = "AUTH"
            st.session_state.goals = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. NAVIGATION CONTROL
# ==========================================
if st.session_state.view != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    # Labeled Footer Nav
    n1, n2, n3 = st.columns(3)
    with n1:
        if st.button("Dashboard"): st.session_state.view = "DASHBOARD"; st.rerun()
    with n2:
        if st.button("Plant Seed"): st.session_state.view = "PLANT"; st.rerun()
    with n3:
        if st.button("Settings"): st.session_state.view = "SETTINGS"; st.rerun()

# Router
if st.session_state.view == "AUTH": show_auth()
elif st.session_state.view == "DASHBOARD": show_dashboard()
elif st.session_state.view == "PLANT": show_plant()
elif st.session_state.view == "SETTINGS": show_settings()
