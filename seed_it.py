import streamlit as st
import time
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. PREMIUM MOBILE UI
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
    div.stButton > button {
        background: #00FF94; color: black; border-radius: 14px;
        padding: 14px; font-weight: 800; border: none; width: 100%;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONFIG (LEFIN'S DATA)
# ==========================================
MY_UPI_ID = "shiflinsakkir112-1@oksbi" 
MY_NAME = "Shiflin Sakkkr"

if 'view' not in st.session_state: st.session_state.view = "AUTH"
if 'goals' not in st.session_state: st.session_state.goals = []
if 'history' not in st.session_state: st.session_state.history = []

# ==========================================
# 3. ROUTING LOGIC
# ==========================================

if st.session_state.view == "AUTH":
    st.markdown("<br><br><h1 style='text-align:center;'>SEED <span class='mint'>IT</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        u_name = st.text_input("FULL NAME", key="u_name")
        u_age = st.text_input("AGE", key="u_age")
        if st.button("UNLOCK VAULT 🔓"):
            if u_name and u_age:
                st.session_state.user = {"name": u_name, "age": u_age}
                st.session_state.view = "HOME"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.view == "HOME":
    st.markdown(f"### Hello, {st.session_state.user['name'].split()[0]} 👋")
    total_val = sum(g['balance'] for g in st.session_state.goals)
    st.markdown(f"<div class='app-card' style='background:linear-gradient(135deg, #00FF94, #00804A); color:black;'><div style='font-size:10px; font-weight:bold; opacity:0.8;'>TOTAL VALUE</div><div style='font-size:36px; font-weight:900;'>₹{total_val:,}</div></div>", unsafe_allow_html=True)

    for i, goal in enumerate(st.session_state.goals):
        prog = min(max(goal['balance'] / goal['target'], 0.0), 1.0) if goal['target'] > 0 else 0
        st.markdown(f"<div class='app-card'><b>{goal['name'].upper()}</b>", unsafe_allow_html=True)
        st.progress(prog)
        
        with st.expander("💸 DEPOSIT FUNDS"):
            amt = st.number_input("Amount (₹)", min_value=1.0, key=f"amt_{i}")
            
            # --- IMPROVED UPI INTENT ---
            encoded_name = urllib.parse.quote(MY_NAME)
            # tr = Transaction Reference (Helps GPay identify the request)
            # mode = 02 (P2P transaction mode)
            upi_url = f"upi://pay?pa={MY_UPI_ID}&pn={encoded_name}&am={amt}&cu=INR&mode=02&tr=SEED{int(time.time())}"
            
            # 1. THE BUTTON
            st.markdown(f"""<a href="{upi_url}" target="_self" style="text-decoration:none;"><div style="background:#111; color:#00FF94; border:1px solid #00FF94; padding:15px; border-radius:12px; text-align:center; font-weight:800; margin-bottom:10px;">OPEN UPI APP 📱</div></a>""", unsafe_allow_html=True)
            
            # 2. THE FALLBACK (COPY ID)
            st.code(MY_UPI_ID, language="text")
            st.caption("If button fails: Copy ID & pay manually in GPay")

            # 3. THE QR CODE
            qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(upi_url)}"
            st.image(qr_api, width=150, caption="Scan to Pay")

            if st.button("CONFIRM PAYMENT ✅", key=f"c_{i}"):
                goal['balance'] += amt
                st.session_state.history.append({"msg": f"Seeded {goal['name']}", "amt": f"+₹{amt}"})
                st.rerun()

        # WITHDRAWAL (MATURITY CHECK)
        can_withdraw = goal['balance'] >= goal['target']
        if goal['date'] and date.today() < goal['date']: can_withdraw = False

        if can_withdraw:
            if st.button("🏆 HARVEST", key=f"h_{i}"):
                st.session_state.goals.pop(i); st.rerun()
        else:
            st.button("🔒 LOCKED", disabled=True, key=f"l_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

# NAVIGATION BAR
if st.session_state.view != "AUTH":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🏠"): st.session_state.view = "HOME"; st.rerun()
    with c2: 
        if st.button("➕"): 
            st.session_state.view = "CREATE"
            st.rerun()
    with c3: 
        if st.button("⚙️"): st.session_state.view = "SETTINGS"; st.rerun()

# OTHER SCREENS
if st.session_state.view == "CREATE":
    st.markdown("### Plant a Seed")
    with st.container():
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        g_name = st.text_input("GOAL NAME")
        g_target = st.number_input("TARGET (₹)", min_value=1.0)
        g_date = st.date_input("LOCK UNTIL")
        if st.button("PLANT 🌱"):
            st.session_state.goals.append({"name": g_name, "target": g_target, "balance": 0, "date": g_date})
            st.session_state.view = "HOME"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
