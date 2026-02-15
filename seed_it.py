import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. PREMIUM APP UI (DARK NEON)
# ==========================================
st.set_page_config(page_title="Seed It Prime", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }
    
    .app-card {
        background: linear-gradient(145deg, #0F0F0F, #050505);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px; padding: 20px; margin-bottom: 15px;
    }
    
    .mint { color: #00FF94; font-weight: 800; }
    .sub-text { color: #555; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }

    .tx-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 0; border-bottom: 1px solid #111;
    }

    div.stButton > button {
        background: #00FF94; color: black; border-radius: 14px;
        padding: 14px; font-weight: 800; border: none; width: 100%;
    }
    
    .stProgress > div > div > div > div { background-color: #00FF94; }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE SYSTEM LOGIC & STATE
# ==========================================
MY_UPI_ID = "lefinmohammed@okhdfcbank" 
MY_NAME = "K M LEFIN MOHAMMED"

if 'view' not in st.session_state: st.session_state.view = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'history' not in st.session_state: st.session_state.history = []
if 'user' not in st.session_state: st.session_state.user = None

# ==========================================
# 3. SCREEN FUNCTIONS
# ==========================================

def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; font-size:50px;'>SEED <span class='mint'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("ENTER NAME", key="reg_name")
        age = st.text_input("ENTER AGE", key="reg_age")
        bank = st.selectbox("PRIMARY BANK", ["HDFC", "SBI", "AXIS", "ICICI", "FEDERAL"])
        if st.button("UNLOCK VAULT 🔓"):
            if name and age:
                st.session_state.user = {"name": name, "age": age, "bank": bank}
                st.session_state.view = "HOME"
                st.rerun()
            else:
                st.error("Please fill all details")
        st.markdown("</div>", unsafe_allow_html=True)

def show_home():
    st.markdown(f"### Hello, {st.session_state.user['name'].split()[0]} 👋")
    
    total_val = sum(g['balance'] for g in st.session_state.goals)
    st.markdown(f"""
        <div class='app-card' style='background: linear-gradient(135deg, #00FF94, #00804A); color:black;'>
            <div style='font-size:10px; font-weight:bold; opacity:0.8;'>TOTAL SEED VALUE</div>
            <div style='font-size:36px; font-weight:900;'>₹{total_val:,}</div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.goals:
        st.info("No active seeds. Tap + to plant one.")
    else:
        for i, goal in enumerate(st.session_state.goals):
            prog = min(max(goal['balance'] / goal['target'], 0.0), 1.0) if goal['target'] > 0 else 0
            
            st.markdown(f"<div class='app-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='display:flex; justify-content:space-between;'><b>{goal['name'].upper()}</b><span class='mint'>{int(prog*100)}%</span></div>", unsafe_allow_html=True)
            st.progress(prog)
            st.markdown(f"<div style='display:flex; justify-content:space-between; margin-top:5px;'><span style='font-size:14px; font-weight:bold;'>₹{goal['balance']:,}</span><span style='color:#555; font-size:12px;'>Goal: ₹{goal['target']:,}</span></div>", unsafe_allow_html=True)
            
            if goal['type'] == "SQUAD":
                st.markdown("<div style='display:flex; gap:8px; margin-top:10px;'>", unsafe_allow_html=True)
                for member, amt in goal['ledger'].items():
                    st.markdown(f"<div style='background:#111; padding:4px 10px; border-radius:10px; font-size:10px; border:1px solid #222;'>{member[0]}: ₹{amt}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("DEPOSIT FUNDS"):
                amt = st.number_input("Amount (₹)", min_value=1.0, key=f"amt_in_{i}")
                encoded_name = urllib.parse.quote(MY_NAME)
                upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={encoded_name}&am={amt}&cu=INR&mc=0000"
                
                st.markdown(f"""<a href="{upi_url}" target="_self" style="text-decoration:none;"><div style="background:#111; color:#00FF94; border:1px solid #00FF94; padding:12px; border-radius:12px; text-align:center; font-weight:bold; margin-bottom:10px;">OPEN UPI APP 📱</div></a>""", unsafe_allow_html=True)

                if st.button("I HAVE PAID ✅", key=f"confirm_pay_{i}"):
                    goal['balance'] += amt
                    goal['ledger']['YOU'] += amt
                    st.session_state.history.append({"msg": f"Deposited to {goal['name']}", "amt": f"+₹{amt}", "status": "CONFIRMED"})
                    st.toast("Payment Logged!")
                    time.sleep(0.5)
                    st.rerun()

            target_met = goal['balance'] >= goal['target']
            date_met = True if not goal['date'] else (date.today() >= goal['date'])
            
            if target_met and date_met:
                if st.button("🏆 HARVEST ASSET", key=f"harvest_{i}"):
                    st.balloons()
                    st.session_state.goals.pop(i)
                    st.rerun()
            else:
                reason = "Target Not Met" if not target_met else f"Locked until {goal['date']}"
                st.button(f"🔒 {reason.upper()}", disabled=True, key=f_locked_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

def show_create():
    st.markdown("### Plant a New Seed")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("WHAT ARE YOU SAVING FOR?", key="new_goal_name")
        target = st.number_input("TARGET AMOUNT (₹)", min_value=1.0, key="new_goal_target")
        
        col1, col2 = st.columns(2)
        with col1:
            use_date = st.checkbox("SET LOCK DATE", key="use_date")
        with col2:
            lock_date = st.date_input("MATURITY", key="lock_date") if use_date else None
            
        is_squad = st.toggle("SQUAD GOAL (POOL WITH FRIENDS)", key="is_squad")
        
        if st.button("INITIALIZE VAULT ➝"):
            if name and target >= 1.0: # FIXED: Added the colon here
                st.session_state.goals.append({
                    "name": name, "target": target, "balance": 0, "date": lock_date,
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 500, "RAHUL": 200} if is_squad else {"YOU": 0}
                })
                st.session_state.view = "HOME"
                st.rerun()
            else:
                st.error("Enter goal name and target")
        st.markdown("</div>", unsafe_allow_html=True)

def show_history():
    st.markdown("### Activity Feed")
    if not st.session_state.history:
        st.info("No recent activity.")
    else:
        for tx in reversed(st.session_state.history):
            st.markdown(f"""<div class='tx-row'><div><div style='font-size:14px;'>{tx['msg']}</div><div style='font-size:10px; color:#555;'>{tx['status']}</div></div><div class='mint'>{tx['amt']}</div></div>""", unsafe_allow_html=True)

def show_settings():
    st.markdown("### Account Settings")
    st.markdown(f"<div class='app-card'><b>{st.session_state.user['name']}</b><br>Age: {st.session_state.user['age']}<br><span class='sub-text'>{st.session_state.user['bank']} USER</span></div>", unsafe_allow_html=True)
    if st.button("LOGOUT"):
        st.session_state.view = "AUTH"
        st.session_state.goals = []
        st.session_state.user = None
        st.rerun()

# ==========================================
# 4. MAIN ROUTER & NAVIGATION
# ==========================================

if st.session_state.view == "AUTH":
    show_auth()
else:
    if st.session_state.view == "HOME": show_home()
    elif st.session_state.view == "CREATE": show_create()
    elif st.session_state.view == "HISTORY": show_history()
    elif st.session_state.view == "SETTINGS": show_settings()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🏠", key="nav_home"): st.session_state.view = "HOME"; st.rerun()
    with c2:
        if st.button("➕", key="nav_add"): st.session_state.view = "CREATE"; st.rerun()
    with c3:
        if st.button("📜", key="nav_hist"): st.session_state.view = "HISTORY"; st.rerun()
    with c4:
        if st.button("⚙️", key="nav_sett"): st.session_state.view = "SETTINGS"; st.rerun()
