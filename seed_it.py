import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. PREMIUM FINTECH DESIGN ENGINE
# ==========================================
st.set_page_config(page_title="Seed It Prime", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    .stApp { background: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }
    
    /* FAMPAY STYLE CARDS */
    .app-card {
        background: linear-gradient(145deg, #0A0A0A, #050505);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 22px;
        margin-bottom: 16px;
    }
    
    .mint { color: #00FF94; font-weight: 800; }
    .sub-text { color: #666; font-size: 12px; }
    
    /* SUCCESS TICK ANIMATION */
    .success-tick {
        text-align: center; color: #00FF94; font-size: 70px;
        animation: pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes pop { from { transform: scale(0); } to { transform: scale(1); } }
    
    /* SUBTLE SQUAD LEDGER */
    .ledger-pill {
        display: flex; align-items: center; gap: 6px;
        background: rgba(255,255,255,0.03); padding: 4px 10px;
        border-radius: 100px; border: 1px solid rgba(255,255,255,0.05);
    }

    div.stButton > button {
        background: #00FF94; color: black; border-radius: 18px;
        padding: 12px; font-weight: 800; border: none; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. YOUR REAL BANKING DATA
# ==========================================
MY_UPI_ID = "shiflinsakkir112-1@oksbi" # <--- YOUR ID
MY_NAME = "Shiflin Sakkkr" # <--- YOUR NAME

if 'screen' not in st.session_state: st.session_state.screen = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []

# ==========================================
# 3. SCREEN: AUTH
# ==========================================
def show_auth():
    st.markdown("<br><br><h1 style='text-align:center;'>SEED <span class='mint'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("FULL NAME", value="K M LEFIN MOHAMMED")
        bank = st.selectbox("SETTLEMENT BANK", ["HDFC", "SBI", "AXIS", "ICICI", "FEDERAL"])
        if st.button("GET STARTED ➝"):
            st.session_state.user = {"name": name, "bank": bank}
            st.session_state.screen = "HOME" if st.session_state.goals else "CREATE"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. SCREEN: HOME (GARDEN)
# ==========================================
def show_home():
    st.markdown(f"### Hey, {st.session_state.user['name'].split()[0]} 👋")
    total_val = sum(g['balance'] for g in st.session_state.goals)
    st.markdown(f"<div class='app-card' style='background:linear-gradient(135deg, #00FF94, #00804A); color:black;'><div style='font-size:11px; font-weight:bold; opacity:0.8;'>TOTAL ASSETS</div><div style='font-size:32px; font-weight:900;'>₹{total_val:,}</div></div>", unsafe_allow_html=True)

    for i, goal in enumerate(st.session_state.goals):
        prog = min(max(goal['balance'] / goal['target'], 0.0), 1.0) if goal['target'] > 0 else 0
        st.markdown(f"<div class='app-card'><b>{goal['name'].upper()}</b>", unsafe_allow_html=True)
        st.progress(prog)
        st.markdown(f"<div style='display:flex; justify-content:space-between;'><span class='sub-text'>₹{goal['balance']:,}</span><span class='sub-text'>Target: ₹{goal['target']:,}</span></div>", unsafe_allow_html=True)
        
        if goal['type'] == "SQUAD":
            cols = st.columns(len(goal['ledger']))
            for idx, (member, amt) in enumerate(goal['ledger'].items()):
                with cols[idx]:
                    st.markdown(f"<div class='ledger-pill'><div style='font-size:10px; color:#00FF94;'>{member[0]}</div><div style='font-size:10px; color:#CCC;'>₹{amt:,}</div></div>", unsafe_allow_html=True)

        with st.expander("DEPOSIT FUNDS"):
            amt = st.number_input("Amount (₹)", min_value=1, key=f"a_{i}")
            encoded_name = urllib.parse.quote(MY_NAME)
            note = urllib.parse.quote(f"SeedIt_{goal['name']}")
            # Added mc=0000 for Google Pay Account fix
            upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={encoded_name}&am={amt}&tn={note}&cu=INR&mc=0000"
            
            st.markdown(f"""
                <a href="{upi_url}">
                    <div style="background:#222; color:#00FF94; border:1px solid #00FF94; padding:15px; border-radius:15px; text-align:center; font-weight:bold;">
                        OPEN UPI APP 📱
                    </div>
                </a>
                <p style='text-align:center; font-size:10px; margin:10px;'>OR SCAN QR ON LAPTOP</p>
            """, unsafe_allow_html=True)
            
            qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(upi_url)}"
            st.image(qr_api, width=150)

            if st.button("CONFIRM PAYMENT ✅", key=f"c_{i}"):
                with st.empty():
                    st.markdown("<div class='success-tick'>✔</div>", unsafe_allow_html=True)
                    time.sleep(1)
                goal['balance'] += amt
                st.rerun()

        if goal['balance'] >= goal['target']:
            if st.button("🏆 HARVEST", key=f"h_{i}"):
                st.session_state.goals.pop(i); st.rerun()
        else:
            st.button("🔒 LOCKED", disabled=True, key=f"l_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: CREATE (PLANT)
# ==========================================
def show_create():
    st.markdown("### Plant a New Seed")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        name = st.text_input("GOAL NAME", placeholder="e.g. Startup Fund")
        target = st.number_input("TARGET AMOUNT (₹)", min_value=100)
        is_squad = st.toggle("SQUAD GOAL")
        if st.button("INITIALIZE ➝"):
            if name:
                st.session_state.goals.append({
                    "name": name, "target": target, "balance": 0, 
                    "type": "SQUAD" if is_squad else "SOLO",
                    "ledger": {"YOU": 0, "FEZIN": 500, "RAHUL": 800} if is_squad else {"YOU": 0}
                })
                st.session_state.screen = "HOME"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. ROUTING & NAVIGATION
# ==========================================
if st.session_state.screen != "AUTH":
    nav_col = st.columns(3)
    with nav_col[0]: 
        if st.button("🏠"): st.session_state.screen = "HOME"; st.rerun()
    with nav_col[1]: 
        if st.button("➕"): st.session_state.screen = "CREATE"; st.rerun()
    with nav_col[2]: 
        if st.button("⚙️"): st.session_state.screen = "SETTINGS"; st.rerun()

if st.session_state.screen == "HOME": show_home()
elif st.session_state.screen == "CREATE": show_create()
elif st.session_state.screen == "AUTH": show_auth()
elif st.session_state.screen == "SETTINGS": 
    st.markdown("### Settings")
    st.markdown(f"<div class='app-card'>User: {st.session_state.user['name']}<br>Bank: {st.session_state.user['bank']}</div>", unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.screen = "AUTH"; st.rerun()
