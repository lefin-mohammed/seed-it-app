import streamlit as st
import time
import urllib.parse
from datetime import datetime, date
import uuid

# ==========================================
# 1. ELITE UI ENGINE (OLED DARK)
# ==========================================
st.set_page_config(page_title="Seed It Infinity", page_icon="🌱", layout="centered")

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
        
        .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }
        
        /* HIDE DEFAULT STREAMLIT INTERFACE */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
        
        /* DASHBOARD COMPONENTS */
        .profile-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        .avatar-box { width: 44px; height: 44px; border-radius: 50%; background: #CCFF00; color: #000; display: flex; align-items: center; justify-content: center; font-weight: 800; }
        
        .balance-box {
            background: #121212;
            border: 1px solid #1A1A1A; border-radius: 28px; padding: 25px; margin-bottom: 30px;
        }
        .balance-label { color: #555; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
        .balance-val { font-size: 42px; font-weight: 900; margin: 10px 0; }
        
        /* GOAL CARDS (IMAGE 3 REPLICA) */
        .goal-card-ui {
            background: #0D0D0D; border: 1px solid #151515; border-radius: 24px;
            padding: 20px; margin-bottom: 15px; display: flex; gap: 18px; align-items: center;
        }
        .goal-icon-box { width: 60px; height: 60px; border-radius: 18px; background: #1A1A1A; display: flex; align-items: center; justify-content: center; font-size: 32px; }
        .prog-bar-container { background: #1A1A1A; height: 6px; border-radius: 10px; width: 100%; margin: 8px 0; overflow: hidden; }
        .prog-bar-fill { background: #CCFF00; height: 100%; border-radius: 10px; }

        /* DETAIL VIEW RING (IMAGE 3 REPLICA) */
        .ring-container { position: relative; width: 220px; height: 220px; margin: 20px auto; display: flex; align-items: center; justify-content: center; }
        .svg-ring { transform: rotate(-90deg); }
        .ring-bg { fill: none; stroke: #1A1A1A; stroke-width: 10; }
        .ring-fill { fill: none; stroke: #CCFF00; stroke-width: 10; stroke-linecap: round; }
        .inner-asset-box { position: absolute; width: 120px; height: 120px; background: #111; border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 60px; }

        /* PRIVACY */
        .blur-mode { filter: blur(12px); }

        /* BUTTONS */
        div.stButton > button {
            background: #CCFF00 !important; color: #000 !important; border-radius: 100px !important;
            padding: 16px !important; font-weight: 800 !important; border: none !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CONFIG & LOGIC
# ==========================================
MY_VPA = "phathim630@oksbi" 
MY_NAME = "Hathim p"

def get_goal_meta(name):
    name = name.lower()
    if "car" in name: return "Vehicle", "🚗"
    if "phone" in name or "iphone" in name: return "Apple", "📱"
    if "labubu" in name: return "Pop Mart", "🧸"
    if "airpods" in name: return "Apple", "🎧"
    return "Personal", "🎯"

# Initialize State
if 'v' not in st.session_state: st.session_state.v = 'SIGNUP'
if 'g' not in st.session_state: st.session_state.g = []
if 'p' not in st.session_state: st.session_state.p = False

# ==========================================
# 3. VIEWS
# ==================== ======================

def show_signup():
    st.markdown("""<div style='text-align:center; padding-top:60px;'><div style='font-size:120px;'>🌱💰</div><h1 style='font-weight:900; font-size:38px;'>Set Your Goals.<br>Start Saving.</h1></div>""", unsafe_allow_html=True)
    with st.form("signup"):
        n = st.text_input("Name", placeholder="Lefin Mohammed")
        m = st.text_input("Mobile", max_chars=10)
        if st.form_submit_button("Create Account"):
            if n and m:
                st.session_state.u = {'n': n, 'm': m}
                st.session_state.v = 'DASH'; st.rerun()

def show_dash():
    u = st.session_state.u
    total = sum(item['b'] for item in st.session_state.g)
    
    st.markdown(f"""
    <div class="profile-header">
        <div style="display:flex; gap:12px; align-items:center;">
            <div class="avatar-box">{u['n'][0]}</div>
            <div><b style='font-size:14px;'>Hello, {u['n'].split()[0]}</b><br><span style='color:#555; font-size:11px;'>Turn dreams into balance</span></div>
        </div>
    </div>
    <div class="balance-card">
        <span class="balance-label">CURRENT BALANCE (USD)</span>
        <div class="balance-amount {'blur-mode' if st.session_state.p else ''}">₹{total:,.2f}</div>
        <div style="display:flex; gap:10px; margin-top:15px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#1A1A1A; display:flex; align-items:center; justify-content:center;">🔄</div>
            <div style="width:36px; height:36px; border-radius:50%; background:#CCFF00; color:#000; display:flex; align-items:center; justify-content:center; font-weight:900;">+</div>
        </div>
    </div>
    <div style='display:flex; justify-content:space-between; margin-bottom:15px;'><b>My goals</b><span style='color:#CCFF00; font-size:12px;'>View All ></span></div>
    """, unsafe_allow_html=True)

    for i, goal in enumerate(st.session_state.g):
        prog = min(int((goal['b'] / goal['t']) * 100), 100) if goal['t'] > 0 else 0
        st.markdown(f"""
        <div class="goal-card-ui">
            <div class="goal-icon-box">{goal['e']}</div>
            <div style="flex-grow:1;">
                <span style='color:#555; font-size:10px; font-weight:700;'>{goal['c'].upper()}</span><br>
                <b style='font-size:15px;'>{goal['n']}</b>
                <div style="display:flex; justify-content:space-between; margin-top:5px;"><span style='color:#555; font-size:11px;'>{prog}%</span></div>
                <div class="prog-bar-container"><div class="prog-bar-fill" style="width:{prog}%;"></div></div>
                <div><b style='font-size:16px;'>₹{goal['b']:,}</b> <span style='color:#444; font-size:12px;'>/ ₹{goal['t']:,}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("VIEW DETAILS", key=f"v_{i}"):
            st.session_state.sel = i; st.session_state.v = 'DETAIL'; st.rerun()

    if st.button("+ New goal"): st.session_state.v = 'CREATE'; st.rerun()

def show_detail():
    goal = st.session_state.g[st.session_state.sel]
    prog = goal['b'] / goal['target'] if goal['target'] > 0 else 0
    offset = 565 - (prog * 565)

    if st.button("← Back"): st.session_state.v = 'DASH'; st.rerun()

    st.markdown(f"""
    <div style='text-align:center;'><span style='color:#555; font-size:11px; font-weight:700;'>{goal['c'].upper()}</span><br><h3>{goal['n']}</h3></div>
    <div class="ring-container">
        <svg class="svg-ring" width="200" height="200">
            <circle class="ring-bg" cx="100" cy="100" r="90"></circle>
            <circle class="ring-fill" cx="100" cy="100" r="90" style="stroke-dasharray: 565; stroke-dashoffset: {offset};"></circle>
        </svg>
        <div class="inner-asset-box">{goal['e']}</div>
    </div>
    <div style="text-align:center;">
        <h1 style='margin:0;'>₹{goal['b']:,} <span style='color:#555; font-size:18px;'>/ ₹{goal['target']:,}</span></h1>
        <div style='background:#CCFF00; color:black; padding:3px 12px; border-radius:20px; display:inline-block; font-weight:900; margin-top:10px;'>{int(prog*100)}%</div>
    </div>
    """, unsafe_allow_html=True)

    amt = st.number_input("Amount to Seed", min_value=1)
    upi_url = f"upi://pay?pa={MY_VPA}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR&mode=02&tr=SEED{int(time.time())}"
    
    st.markdown(f"""<a href="{upi_url}" target="_self" style="text-decoration:none;"><div style="background:#CCFF00; color:black; padding:18px; border-radius:100px; text-align:center; font-weight:900;">Top up goal balance</div></a>""", unsafe_allow_html=True)
    if st.button("I HAVE PAID ✅"):
        goal['b'] += amt; st.rerun()

def main():
    inject_custom_css()
    if st.session_state.v == 'SIGNUP': show_signup()
    elif st.session_state.v == 'DASH': show_dash()
    elif st.session_state.v == 'DETAIL': show_detail()
    elif st.session_state.v == 'CREATE':
        st.markdown("### 🎯 New Goal")
        n = st.text_input("Goal Name")
        t = st.number_input("Target", min_value=1)
        if st.button("Initialize"):
            if n and t > 0:
                cat, emo = get_goal_meta(n)
                st.session_state.g.append({'n': n, 'target': float(t), 'b': 0.0, 'c': cat, 'e': emo})
                st.session_state.v = 'DASH'; st.rerun()

if __name__ == "__main__":
    main()
