import streamlit as st
import time
import urllib.parse
from datetime import datetime, date
import uuid

# ==========================================
# 1. THE ULTIMATE DESIGN SYSTEM (OLED DARK)
# ==========================================
st.set_page_config(page_title="Seed It Infinity", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Outfit', sans-serif; }
    
    /* HIDE DEFAULT STREAMLIT INTERFACE */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .main-container { max-width: 400px; margin: 0 auto; padding-bottom: 100px; }

    /* --- DASHBOARD COMPONENTS --- */
    .profile-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .avatar-box { width: 44px; height: 44px; border-radius: 50%; background: #CCFF00; color: #000; display: flex; align-items: center; justify-content: center; font-weight: 800; }
    
    .balance-box {
        background: linear-gradient(135deg, #121212 0%, #050505 100%);
        border: 1px solid #1A1A1A; border-radius: 28px; padding: 25px; margin-bottom: 35px;
    }
    .balance-label { color: #555; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
    .balance-val { font-size: 42px; font-weight: 900; margin: 10px 0; }
    
    /* GOAL CARDS (HORIZONTAL ALIGNMENT - IMAGE 3) */
    .goal-card-ui {
        background: #0D0D0D; border: 1px solid #151515; border-radius: 24px;
        padding: 20px; margin-bottom: 15px; display: flex; gap: 18px; align-items: center;
    }
    .goal-icon-box { width: 60px; height: 60px; border-radius: 18px; background: #1A1A1A; display: flex; align-items: center; justify-content: center; font-size: 32px; }
    .prog-bar-container { background: #1A1A1A; height: 6px; border-radius: 10px; width: 100%; margin: 8px 0; overflow: hidden; }
    .prog-bar-fill { background: #CCFF00; height: 100%; border-radius: 10px; transition: width 1s ease; }

    /* --- DETAIL VIEW (CIRCULAR - IMAGE 3) --- */
    .detail-ring-wrapper { position: relative; width: 240px; height: 240px; margin: 30px auto; display: flex; align-items: center; justify-content: center; }
    .ring-svg { transform: rotate(-90deg); }
    .ring-bg-svg { fill: none; stroke: #151515; stroke-width: 12; }
    .ring-fill-svg { fill: none; stroke: #CCFF00; stroke-width: 12; stroke-linecap: round; transition: stroke-dashoffset 1s ease; }
    .inner-asset-box { position: absolute; width: 130px; height: 130px; background: #0D0D0D; border-radius: 28px; border: 1px solid #1A1A1A; display: flex; align-items: center; justify-content: center; font-size: 65px; }

    /* --- BUTTONS & NAV --- */
    .footer-action-btn {
        background: #CCFF00; color: #000; border: none; border-radius: 100px;
        padding: 18px; font-weight: 900; font-size: 16px; width: 100%; text-align: center;
        display: block; text-decoration: none; box-shadow: 0 10px 30px rgba(204, 255, 0, 0.2);
    }
    .sticky-nav {
        position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(0,0,0,0.95);
        border-top: 1px solid #111; display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000;
    }

    .blur-mode { filter: blur(10px); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIC & UPI PROTOCOL
# ==========================================
MY_VPA = "phathim630@oksbi" 
MY_NAME = "Hathim p"

def get_goal_style(name):
    name = name.lower()
    if "car" in name: return "VEHICLE", "🚗"
    if "phone" in name or "iphone" in name: return "APPLE", "📱"
    if "labubu" in name: return "POP MART", "🧸"
    if "airpods" in name: return "APPLE", "🎧"
    return "PERSONAL", "🎯"

if 'v' not in st.session_state: st.session_state.v = 'SIGNUP'
if 'g' not in st.session_state: st.session_state.g = []
if 'p' not in st.session_state: st.session_state.p = False

# ==========================================
# 3. SCREEN: SIGNUP (IMAGE 3 - CENTER)
# ==========================================
def show_signup():
    st.markdown("""<div class='main-container' style='text-align:center; padding-top:60px;'><div style='font-size:120px;'>🌱💰</div><h1 style='font-weight:900; font-size:38px; line-height:1.1;'>Set Your Goals.<br>Start Saving.</h1><p style='color:#555; margin-top:20px;'>Create goals, track your progress, and watch<br>your savings grow — one step at a time.</p></div>""", unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("NAME", placeholder="Full Name")
        m = st.text_input("MOBILE", placeholder="10-digit number")
        if st.form_submit_button("CONTINUE ➝"):
            if n and m:
                st.session_state.u = {'n': n, 'm': m}
                st.session_state.v = 'DASH'
                st.rerun()

# ==========================================
# 4. SCREEN: DASHBOARD (IMAGE 3 - LEFT)
# ==========================================
def show_dash():
    u = st.session_state.u
    total = sum(item['b'] for item in st.session_state.g)
    
    st.markdown(f"""
    <div class='main-container'>
        <div class='profile-row'>
            <div style='display:flex; gap:12px; align-items:center;'>
                <div class='avatar-box'>{u['n'][0]}</div>
                <div><b style='font-size:15px;'>Hello, {u['n'].split()[0]}</b><br><span style='color:#555; font-size:11px;'>Turn dreams into balance</span></div>
            </div>
            <div style='font-size:20px;'>🔔</div>
        </div>
        
        <div class='balance-box'>
            <span class='balance-label'>CURRENT BALANCE (USD)</span>
            <div class='balance-val {"blur-mode" if st.session_state.p else ""}'>₹{total:,.2f}</div>
            <div style='display:flex; gap:12px; margin-top:15px;'>
                <div class='avatar-box' style='background:#1A1A1A; color:#FFF; width:36px; height:36px;'>🔄</div>
                <div class='avatar-box' style='background:#1A1A1A; color:#FFF; width:36px; height:36px;'>📈</div>
                <div class='avatar-box' style='background:#CCFF00; color:#000; width:36px; height:36px;'>+</div>
            </div>
        </div>
        
        <div style='display:flex; justify-content:space-between; margin-bottom:20px;'><b style='font-size:18px;'>My goals</b><span style='color:#CCFF00; font-size:12px;'>View All ></span></div>
    """, unsafe_allow_html=True)

    for i, goal in enumerate(st.session_state.g):
        prog = min(int((goal['b'] / goal['t']) * 100), 100) if goal['t'] > 0 else 0
        st.markdown(f"""
        <div class='goal-card-ui'>
            <div class='goal-icon-box'>{goal['e']}</div>
            <div style='flex-grow:1;'>
                <div style='display:flex; justify-content:space-between;'><span class='balance-label'>{goal['c']}</span></div>
                <b style='font-size:16px;'>{goal['n']}</b>
                <div style='display:flex; justify-content:space-between; margin-top:5px;'><span style='color:#555; font-size:12px;'>{prog}%</span></div>
                <div class='prog-bar-container'><div class='prog-bar-fill' style='width:{prog}%;'></div></div>
                <div style='margin-top:5px;'><b style='font-size:17px;'>₹{goal['b']:,}</b> <span style='color:#444; font-size:13px;'>/ ₹{goal['t']:,}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("MANAGE ASSET", key=f"v_{i}"):
            st.session_state.sel = i
            st.session_state.v = 'DETAIL'
            st.rerun()

    if st.button("+ New goal"): st.session_state.v = 'CREATE'; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: DETAIL (IMAGE 3 - RIGHT)
# ==========================================
def show_detail():
    goal = st.session_state.g[st.session_state.sel]
    prog = goal['b'] / goal['t'] if goal['t'] > 0 else 0
    offset = 565 - (prog * 565)

    if st.button("← Back"): st.session_state.v = 'DASH'; st.rerun()

    st.markdown(f"""
    <div class='main-container' style='text-align:center;'>
        <span class='balance-label'>{goal['c']}</span><br><h3 style='margin:0;'>{goal['n']}</h3>
        
        <div class='detail-ring-wrapper'>
            <svg class="ring-svg" width="200" height="200">
                <circle class="ring-bg-svg" cx="100" cy="100" r="90"></circle>
                <circle class="ring-fill-svg" cx="100" cy="100" r="90" style="stroke-dasharray: 565; stroke-dashoffset: {offset};"></circle>
            </svg>
            <div class='inner-asset-box'>{goal['e']}</div>
        </div>
        
        <h1 style='margin:0; font-weight:900; font-size:36px;'>₹{goal['b']:,} <span style='color:#555; font-size:18px;'>/ ₹{goal['t']:,}</span></h1>
        <div style='background:#CCFF00; color:black; padding:4px 14px; border-radius:20px; display:inline-block; font-weight:900; margin-top:10px;'>{int(prog*100)}%</div>
    """, unsafe_allow_html=True)

    st.markdown("<br><div style='text-align:left;'><b class='balance-label'>TRANSACTION HISTORY</b></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='display:flex; justify-content:space-between; margin:15px 0;'>
            <div><b style='font-size:14px;'>Vault Contribution</b><br><span style='color:#555; font-size:10px;'>{date.today().strftime('%d %b %Y')}</span></div>
            <div style='color:#CCFF00; font-weight:800;'>+₹0.00</div>
        </div>
    """, unsafe_allow_html=True)

    amt = st.number_input("DEPOSIT AMOUNT (₹)", min_value=1, key="da")
    
    # UPI PROTOCOL Hand-off
    vpa_url = f"upi://pay?pa={MY_VPA}&pn={urllib.parse.quote(MY_NAME)}&am={amt}&cu=INR&mode=02&tr=SEED{int(time.time())}"
    
    st.markdown(f"<a href='{vpa_url}' target='_self' class='footer-action-btn'>Top up goal balance</a>", unsafe_allow_html=True)
    
    if st.button("CONFIRM DEPOSIT ✅"):
        goal['b'] += amt
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. ROUTER & SETTINGS (LOGOUT)
# ==========================================
def show_settings():
    st.markdown(f"### Settings<br><div class='balance-box'><b>{st.session_state.u['n']}</b><br>{st.session_state.u['m']}</div>", unsafe_allow_html=True)
    if st.button("LOGOUT & WIPE"):
        st.session_state.v = 'SIGNUP'
        st.session_state.g = []
        st.rerun()

def main():
    inject_custom_css()
    if st.session_state.v == 'SIGNUP': show_signup()
    elif st.session_state.v == 'DASH': show_dash()
    elif st.session_state.v == 'DETAIL': show_detail()
    elif st.session_state.v == 'SETTINGS': show_settings()
    elif st.session_state.v == 'CREATE':
        st.markdown("### Set New Goal")
        n = st.text_input("Goal Name")
        t = st.number_input("Target Amount", min_value=1)
        if st.button("ACTIVATE VAULT ➝"):
            if n and t > 0:
                cat, emo = get_goal_style(n)
                st.session_state.g.append({'n': n, 't': float(t), 'b': 0.0, 'c': cat, 'e': emo})
                st.session_state.v = 'DASH'; st.rerun()

    if st.session_state.v != 'SIGNUP':
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        with n1: 
            if st.button("🏠"): st.session_state.v = 'DASH'; st.rerun()
        with n2: 
            if st.button("➕"): st.session_state.view = 'CREATE'; st.session_state.v = 'CREATE'; st.rerun()
        with n3: 
            if st.button("⚙️"): st.session_state.v = 'SETTINGS'; st.rerun()

if __name__ == "__main__":
    main()
