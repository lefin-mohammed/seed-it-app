import streamlit as st
from datetime import datetime, timedelta
import uuid
import urllib.parse

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Seed It - Digital Locker",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS STYLING ====================
def inject_custom_css():
    st.markdown("""
    <style>
    /* OLED Dark Theme */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Balance Card */
    .balance-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        border: 1px solid #333;
    }
    
    .balance-amount {
        font-size: 42px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 8px 0;
    }
    
    .balance-amount.blurred {
        filter: blur(12px);
        user-select: none;
    }
    
    /* Goal Cards */
    .goal-card {
        background: #1a1a1a;
        border-radius: 16px;
        padding: 18px;
        margin: 12px 0;
        border: 1px solid #2d2d2d;
        transition: all 0.2s;
    }
    
    .goal-card:hover {
        border-color: #C1FF72;
        transform: translateY(-4px);
    }
    
    /* Progress Bar */
    .progress-bar-container {
        width: 100%;
        height: 6px;
        background-color: #2d2d2d;
        border-radius: 10px;
        margin: 12px 0;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background-color: #C1FF72;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Onboarding */
    .onboarding-container {
        text-align: center;
        padding: 40px 20px;
    }
    
    .onboarding-illustration {
        font-size: 120px;
        margin: 40px 0;
    }
    
    .onboarding-title {
        font-size: 32px;
        font-weight: 700;
        margin: 20px 0;
        line-height: 1.2;
    }
    
    .onboarding-subtitle {
        font-size: 15px;
        color: #888;
        margin: 16px 0 40px 0;
        line-height: 1.6;
    }
    
    /* Input Fields */
    .stTextInput input {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        padding: 16px !important;
        font-size: 15px !important;
    }
    
    .stTextInput input:focus {
        border-color: #C1FF72 !important;
        box-shadow: 0 0 0 1px #C1FF72 !important;
    }
    
    .stNumberInput input {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
    }
    
    .stDateInput input {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
    }
    
    /* Transaction History */
    .transaction-item {
        display: flex;
        justify-content: space-between;
        padding: 14px 0;
        border-bottom: 1px solid #1a1a1a;
    }
    
    .transaction-date {
        color: #888;
        font-size: 13px;
    }
    
    .transaction-amount {
        font-size: 15px;
        font-weight: 600;
        color: #C1FF72;
    }
    
    /* Lock Status */
    .lock-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: #2d2d2d;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 8px;
    }
    
    .lock-status.locked {
        background: #3d2d2d;
        color: #ff6b6b;
    }
    
    .lock-status.unlocked {
        background: #2d3d2d;
        color: #C1FF72;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def get_emoji_for_goal(goal_name):
    """Smart categorization: Auto-assign emoji based on goal name"""
    name_lower = goal_name.lower()
    
    emoji_map = {
        'car': '🚗', 'bike': '🏍️', 'vehicle': '🚙',
        'phone': '📱', 'iphone': '📱', 'mobile': '📱',
        'laptop': '💻', 'computer': '🖥️', 'macbook': '💻',
        'watch': '⌚', 'airpods': '🎧', 'headphones': '🎧',
        'travel': '✈️', 'vacation': '🏖️', 'trip': '🗺️',
        'wedding': '💍', 'ring': '💎',
        'house': '🏠', 'home': '🏡', 'apartment': '🏢',
        'education': '📚', 'course': '🎓', 'college': '🎓',
        'camera': '📷', 'ps5': '🎮', 'gaming': '🎮',
        'sneakers': '👟', 'shoes': '👟',
        'gym': '💪', 'fitness': '🏋️',
        'tv': '📺', 'television': '📺',
        'furniture': '🛋️', 'sofa': '🛋️'
    }
    
    for keyword, emoji in emoji_map.items():
        if keyword in name_lower:
            return emoji
    
    return '🎯'

def generate_upi_link(amount, goal_name, vpa="phathim630@oksbi"):
    """Generate UPI payment deep link"""
    txn_id = f"SEED{uuid.uuid4().hex[:8].upper()}"
    
    upi_uri = f"upi://pay?pa={vpa}&pn=Seed It&am={amount:.2f}&cu=INR&tn={urllib.parse.quote(f'Adding to {goal_name}')}&tr={txn_id}&mode=02&mc=0000"
    
    return upi_uri, txn_id

def is_goal_unlocked(goal):
    """Check if goal is unlocked (can withdraw)"""
    balance_met = goal['current_balance'] >= goal['target_amount']
    
    if goal.get('maturity_date'):
        date_met = datetime.now() >= datetime.fromisoformat(goal['maturity_date'])
        return balance_met and date_met
    
    return balance_met

def calculate_progress_percentage(current, target):
    """Calculate progress percentage"""
    if target == 0:
        return 0
    return min(int((current / target) * 100), 100)

def create_circular_progress_svg(percentage, size=200):
    """Create SVG circular progress ring"""
    radius = (size / 2) - 10
    circumference = 2 * 3.14159 * radius
    offset = circumference - (percentage / 100) * circumference
    
    svg = f"""
    <svg width="{size}" height="{size}">
        <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#2d2d2d" stroke-width="12"/>
        <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#C1FF72" stroke-width="12"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                transform="rotate(-90 {size/2} {size/2})" stroke-linecap="round"/>
        <text x="50%" y="50%" text-anchor="middle" dy=".3em" font-size="48" font-weight="700" fill="#FFFFFF">{percentage}%</text>
    </svg>
    """
    return svg

# ==================== SESSION STATE ====================

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.view = 'ONBOARDING'
    st.session_state.user = None
    st.session_state.goals = []
    st.session_state.privacy_mode = False
    st.session_state.selected_goal_id = None

# ==================== VIEWS ====================

def render_onboarding():
    """Onboarding screen"""
    st.markdown("""
    <div class="onboarding-container">
        <div class="onboarding-illustration">🌱💰</div>
        <div class="onboarding-title">Set Your Goals.<br>Start Saving.</div>
        <div class="onboarding-subtitle">
            Create goals, track your progress, and watch<br>
            your savings grow — one step at a time.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        mobile = st.text_input("Mobile Number", placeholder="10-digit mobile number", max_chars=10)
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            if st.form_submit_button("Skip", use_container_width=True):
                st.session_state.user = {'name': 'Daisy', 'mobile': '9876543210', 'email': 'demo@seedit.app'}
                st.session_state.view = 'DASHBOARD'
                st.rerun()
        
        if submit:
            if name and mobile and email:
                if len(mobile) == 10 and mobile.isdigit():
                    st.session_state.user = {'name': name, 'mobile': mobile, 'email': email}
                    st.session_state.view = 'DASHBOARD'
                    st.rerun()
                else:
                    st.error("Please enter a valid 10-digit mobile number")
            else:
                st.error("Please fill all fields")

def render_dashboard():
    """Main dashboard"""
    user = st.session_state.user
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Hello, {user['name'].split()[0]}")
        st.caption("Turn dreams into balance")
    with col2:
        privacy_icon = "🙈" if st.session_state.privacy_mode else "👁️"
        if st.button(privacy_icon, key="privacy_toggle"):
            st.session_state.privacy_mode = not st.session_state.privacy_mode
            st.rerun()
    
    total_balance = sum(goal['current_balance'] for goal in st.session_state.goals)
    blur_class = "blurred" if st.session_state.privacy_mode else ""
    
    st.markdown(f"""
    <div class="balance-card">
        <div style="color: #888; font-size: 13px;">Current Balance</div>
        <div class="balance-amount {blur_class}">₹{total_balance:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### My goals")
    
    if st.session_state.goals:
        cols = st.columns(2)
        for idx, goal in enumerate(st.session_state.goals):
            with cols[idx % 2]:
                progress = calculate_progress_percentage(goal['current_balance'], goal['target_amount'])
                blur_class = "blurred" if st.session_state.privacy_mode else ""
                
                if st.button(f"{goal['emoji']} {goal['name']}", key=f"goal_{goal['id']}", use_container_width=True):
                    st.session_state.selected_goal_id = goal['id']
                    st.session_state.view = 'GOAL_DETAIL'
                    st.rerun()
                
                st.markdown(f"""
                <div class="goal-card">
                    <div style="font-size: 48px; margin-bottom: 12px;">{goal['emoji']}</div>
                    <div style="color: #888; font-size: 11px; text-transform: uppercase;">{goal.get('brand', 'Goal')}</div>
                    <div style="font-size: 18px; font-weight: 600; margin: 4px 0;">{goal['name']}</div>
                    <div style="font-size: 13px; color: #888; margin: 8px 0;">{progress}%</div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {progress}%"></div>
                    </div>
                    <div style="font-size: 20px; font-weight: 700;" class="{blur_class}">₹{goal['current_balance']:,.2f}</div>
                    <div style="font-size: 14px; color: #666;" class="{blur_class}">/ ₹{goal['target_amount']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No goals yet! Create your first goal below 👇")
    
    if st.button("➕ New goal", key="new_goal", use_container_width=True):
        st.session_state.view = 'CREATE_GOAL'
        st.rerun()

def render_create_goal():
    """Create new goal form"""
    st.markdown("### 🎯 Create New Goal")
    
    with st.form("create_goal_form"):
        goal_name = st.text_input("Goal Name", placeholder="e.g., iPhone 16 Pro")
        
        col1, col2 = st.columns(2)
        with col1:
            brand = st.text_input("Brand/Category", placeholder="e.g., Apple")
        with col2:
            target_amount = st.number_input("Target Amount (₹)", min_value=1, value=1000, step=100)
        
        maturity_date = st.date_input("Lock Until (Optional)", value=None, min_value=datetime.now().date())
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Create Goal", use_container_width=True):
                if goal_name and target_amount > 0:
                    new_goal = {
                        'id': str(uuid.uuid4()),
                        'name': goal_name,
                        'brand': brand or 'Goal',
                        'emoji': get_emoji_for_goal(goal_name),
                        'target_amount': float(target_amount),
                        'current_balance': 0.0,
                        'maturity_date': maturity_date.isoformat() if maturity_date else None,
                        'created_at': datetime.now().isoformat(),
                        'ledger': {},
                        'transactions': []
                    }
                    st.session_state.goals.append(new_goal)
                    st.success(f"✅ Goal '{goal_name}' created!")
                    st.session_state.view = 'DASHBOARD'
                    st.rerun()
        
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.view = 'DASHBOARD'
                st.rerun()

def render_goal_detail():
    """Goal detail view"""
    goal_id = st.session_state.selected_goal_id
    goal = next((g for g in st.session_state.goals if g['id'] == goal_id), None)
    
    if not goal:
        st.error("Goal not found")
        return
    
    if st.button("← Back", key="back"):
        st.session_state.view = 'DASHBOARD'
        st.rerun()
    
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <div style="font-size: 80px;">{goal['emoji']}</div>
        <div style="font-size: 12px; color: #888; text-transform: uppercase;">{goal['brand']}</div>
        <div style="font-size: 28px; font-weight: 700; margin: 8px 0;">{goal['name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    progress = calculate_progress_percentage(goal['current_balance'], goal['target_amount'])
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 32px; font-weight: 700;">₹{goal['current_balance']:,.2f}</div>
            <div style="font-size: 14px; color: #666;">/ ₹{goal['target_amount']:,.2f}</div>
            <div style="font-size: 16px; color: #888; margin-top: 8px;">{progress}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(create_circular_progress_svg(progress, 180), unsafe_allow_html=True)
    
    is_unlocked = is_goal_unlocked(goal)
    lock_emoji = "🔓" if is_unlocked else "🔒"
    lock_text = "Unlocked - Ready to Harvest!" if is_unlocked else "Locked - Keep Saving!"
    lock_class = "unlocked" if is_unlocked else "locked"
    
    st.markdown(f'<div style="text-align: center;"><span class="lock-status {lock_class}">{lock_emoji} {lock_text}</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💳 Top-up Goal")
    
    custom_amount = st.number_input("Amount (₹)", min_value=1, value=10, step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Generate UPI Link", use_container_width=True):
            upi_link, txn_id = generate_upi_link(custom_amount, goal['name'])
            st.code(upi_link, language=None)
            st.info(f"Transaction ID: {txn_id}")
    
    with col2:
        if st.button("✅ Confirm Payment", use_container_width=True):
            goal['current_balance'] += custom_amount
            goal['transactions'].append({
                'date': datetime.now().isoformat(),
                'amount': custom_amount,
                'status': 'pending',
                'type': 'deposit'
            })
            st.success(f"₹{custom_amount} added!")
            st.rerun()
    
    if is_unlocked:
        if st.button("🌾 Harvest (Withdraw)", use_container_width=True, type="primary"):
            st.success(f"🎉 Congratulations! You've unlocked ₹{goal['current_balance']:,.2f}!")
            st.balloons()
    else:
        st.button("🌾 Harvest (Locked)", use_container_width=True, disabled=True)
        remaining = goal['target_amount'] - goal['current_balance']
        st.caption(f"💡 Save ₹{remaining:,.2f} more to unlock!")
    
    st.markdown("---")
    st.markdown("### Transaction history")
    
    if goal['transactions']:
        for txn in sorted(goal['transactions'], key=lambda x: x['date'], reverse=True)[:5]:
            txn_date = datetime.fromisoformat(txn['date']).strftime("%d %B %Y")
            st.markdown(f"""
            <div class="transaction-item">
                <div class="transaction-date">{txn_date}</div>
                <div class="transaction-amount">+₹{txn['amount']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet")

def render_settings():
    """Settings page"""
    st.markdown("### ⚙️ Settings")
    
    user = st.session_state.user
    
    st.markdown(f"""
    <div style="background: #1a1a1a; padding: 20px; border-radius: 12px; margin: 20px 0;">
        <div style="font-size: 18px; font-weight: 600;">{user['name']}</div>
        <div style="color: #888; font-size: 14px;">📱 {user['mobile']}</div>
        <div style="color: #888; font-size: 14px;">📧 {user['email']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    privacy_state = "ON" if st.session_state.privacy_mode else "OFF"
    if st.button(f"🙈 Privacy Mode: {privacy_state}", use_container_width=True):
        st.session_state.privacy_mode = not st.session_state.privacy_mode
        st.rerun()
    
    st.markdown("---")
    
    total_goals = len(st.session_state.goals)
    total_saved = sum(g['current_balance'] for g in st.session_state.goals)
    total_target = sum(g['target_amount'] for g in st.session_state.goals)
    
    st.markdown(f"""
    <div style="background: #1a1a1a; padding: 20px; border-radius: 12px;">
        <div style="font-size: 14px; color: #888;">Your Progress</div>
        <div style="font-size: 24px; font-weight: 700; margin: 8px 0;">₹{total_saved:,.2f}</div>
        <div style="color: #666;">of ₹{total_target:,.2f} across {total_goals} goals</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

def render_bottom_nav():
    """Bottom navigation"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.view = 'DASHBOARD'
            st.rerun()
    with col2:
        if st.button("➕ Create", key="nav_create", use_container_width=True):
            st.session_state.view = 'CREATE_GOAL'
            st.rerun()
    with col3:
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.view = 'SETTINGS'
            st.rerun()

# ==================== MAIN ====================

def main():
    inject_custom_css()
    
    if st.session_state.view == 'ONBOARDING':
        render_onboarding()
    elif st.session_state.view == 'DASHBOARD':
        render_dashboard()
        render_bottom_nav()
    elif st.session_state.view == 'CREATE_GOAL':
        render_create_goal()
        render_bottom_nav()
    elif st.session_state.view == 'GOAL_DETAIL':
        render_goal_detail()
        render_bottom_nav()
    elif st.session_state.view == 'SETTINGS':
        render_settings()
        render_bottom_nav()

if __name__ == "__main__":
    main()
