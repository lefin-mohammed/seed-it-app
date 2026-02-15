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
    
    /* MOBILE NAVIGATION BAR */
    .nav-container {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(10, 10, 10, 0.9); backdrop-filter: blur(10px);
        display: flex; justify-content: space-around; padding: 15px 0;
        border-top: 1px solid #222; z-index: 1000;
    }

    /* PREMIUM APP CARDS */
    .app-card {
        background: linear-gradient(145deg, #0F0F0F, #050505);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px; padding: 20px; margin-bottom: 15px;
    }
    
    .mint { color: #00FF94; font-weight: 800; }
    .sub-text { color: #555; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }

    /* TRANSACTION LIST */
    .tx-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 0; border-bottom: 1px solid #111;
    }

    div.stButton > button {
        background: #00FF94; color: black; border-radius: 14px;
        padding: 14px; font-weight: 800; border: none; width: 100%;
    }
    
    /* PROGRESS BAR OVERRIDE */
    .stProgress > div > div > div > div { background-color: #00FF94; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE SYSTEM LOGIC
# ==========================================
MY_UPI_ID = "lefinmohammed@okhdfcbank" # Update to your ID
MY_NAME = "K M LEFIN MOHAMMED"

# Initialize Global App Data
if 'view' not in st.session_state: st.session_state.view = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'history' not in st.session_state: st.session_state.history = []

# ==========================================
# 3. SCREEN: LOGIN (AUTH)
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center; font-size:50px;'>SEED <span class='mint'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("ENTER NAME")
        age= st.text_input("ENTER AGE")
        bank = st.selectbox("PRIMARY BANK", ["HDFC", "SBI", "AXIS", "ICICI", "FEDERAL"])
        if st.button("UNLOCK VAULT 🔓"):
            st.session_state.user = {"name": name, "bank": bank}
            st.session_state.view = "HOME"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: HOME (GARDEN)
# ==========================================
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
            
            # SQUAD LEDGER
            if goal['type'] == "SQUAD":
                st.markdown("<div style='display:flex; gap:8px; margin-top:10px;'>", unsafe_allow_html=True)
                for member, amt in goal['ledger'].items():
                    st.markdown(f"<div style='background:#111; padding:4px 10px; border-radius:10px; font-size:10px; border:1px solid #222;'>{member[0]}: ₹{amt}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # DEPOSIT WITH VERIFICATION LOGIC
            with st.expander("DEPOSIT FUNDS"):
                amt = st.number_input("Amount (₹)", min_value=1.0, key=f"a_{i}")
                
                # UPI Intent
                encoded_name = urllib.parse.quote(MY_NAME)
                upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={encoded_name}&am={amt}&cu=INR&mc=0000"
                
                st.markdown(f"""
                    <a href="{upi_url}" target="_self" style="text-decoration:none;">
                        <div style="background:#111; color:#00FF94; border:1px solid #00FF94; padding:12px; border-radius:12px; text-align:center; font-weight:bold; margin-bottom:10px;">
                            OPEN UPI APP 📱
                        </div>
                    </a>
                """, unsafe_allow_html=True)

                if st.button("I HAVE PAID ✅", key=f"c_{i}"):
                    # In a real app, this would show "Pending Approval"
                    # For your demo, we add it but log it in history
                    goal['balance'] += amt
                    goal['ledger']['YOU'] += amt
                    st.session_state.history.append({"msg": f"Deposited to {goal['name']}", "amt": f"+₹{amt}", "status": "CONFIRMED"})
                    st.toast("Payment Logged!")
                    time.sleep(1)
                    st.rerun()

            # WITHDRAWAL (WITH MATURITY CHECK)
            target_met = goal['balance'] >= goal['target']
            date_met = True if not goal['date'] else (date.today() >= goal['date'])
            
            if target_met and date_met:
                if st.button("🏆 HARVEST ASSET", key=f"h_{i}"):
                    st.balloons()
                    st.session_state.goals.pop(i)
                    st.rerun()
            else:
                reason = "Target Not Met" if not target_met else f"Locked until {goal['date']}"
                st.button(f"🔒 {reason.upper()}", disabled=True, key=f"l_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: TRANSACTIONS (HISTORY)
# ==========================================
def show_history():
    st.markdown("### Activity Feed")
    if not st.session_state.history:
        st.info("No recent activity.")
    else:
        for tx in reversed(st.session_state.history):
            st.markdown(f"""
                <div class='tx-row'>
                    <div>
                        <div style='font-size:14px;'>{tx['msg']}</div>
                        <div style='font-size:10px; color:#555;'>{tx['status']}</div>
                    </div>
                    <div class='mint'>{tx['amt']}</div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 6. SCREEN: CREATE GOAL
# ==========================================
def show_create():
    st.markdown("### Plant a New Seed")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("WHAT ARE YOU SAVING FOR?")
        target = st.number_input("TARGET AMOUNT (₹)", min_value=1.0) # SET TO RS 1 MIN
        
        col1, col2 = st.columns(2)
        with col1:
            use_date = st.checkbox("SET LOCK DATE")
        with col2:
            lock_date = st.date_input("MATURITY") if use_date else None
            
        is_squad = st.toggle("SQUAD GOAL (POOL WITH FRIENDS)")
        
        if st.button("INITIALIZE VAULT ➝"):
            if name:
                st.session_state.goals.append({
                    "name": name, "target": target, "balance": 0, "date": lock_date,
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 500, "RAHUL": 200} if is_squad else {"YOU": 0}
                })
                st.session_state.view = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 7. NAVIGATION BAR LOGIC
# ==========================================
if st.session_state.view != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🏠"): st.session_state.view = "HOME"; st.rerun()
    with c2:
        if st.button("➕"): st.session_state.view = "CREATE"; st.rerun()
    with c3:
        if st.button("📜"): st.session_state.view = "HISTORY"; st.rerun()
    with c4:
        if st.button("⚙️"): st.session_state.view = "SETTINGS"; st.rerun()

# ROUTING
if st.session_state.view == "HOME": show_home()
elif st.session_state.view == "CREATE": show_create()
elif st.session_state.view == "HISTORY": show_history()
elif st.session_state.view == "SETTINGS": 
    st.markdown("### Account Settings")
    st.markdown(f"<div class='app-card'><b>{st.session_state.user['name']}</b><br><span class='sub-text'>{st.session_state.user['bank']} USER</span></div>", unsafe_allow_html=True)
    if st.button("LOGOUT"): st.session_state.view = "AUTH"; st.session_state.goals = []; st.rerun()
