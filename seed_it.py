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
    
    /* Balance Card with Icons */
    .balance-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 20px;
        padding: 20px 24px;
        margin: 20px 0;
        border: 1px solid #333;
    }
    
    .balance-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .balance-info {
        flex: 1;
    }
    
    .balance-label {
        color: #888;
        font-size: 13px;
        margin-bottom: 4px;
    }
    
    .balance-amount {
        font-size: 38px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 4px 0;
    }
    
    .balance-amount.blurred {
        filter: blur(12px);
        user-select: none;
    }
    
    .balance-actions {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    
    .action-icon {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.2s;
    }
    
    .action-icon:hover {
        background: #3d3d3d;
        border-color: #C1FF72;
    }
    
    .action-icon.primary {
        background: #C1FF72;
        color: #000000;
        font-size: 20px;
        font-weight: 700;
    }
    
    .action-icon.primary:hover {
        background: #D4FF8F;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 28px 0 16px 0;
    }
    
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .view-all-link {
        color: #C1FF72;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none;
    }
    
    /* Goal Cards - Horizontal Layout */
    .goal-card {
        background: #1a1a1a;
        border-radius: 20px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid #2d2d2d;
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .goal-card:hover {
        border-color: #C1FF72;
        transform: translateY(-2px);
    }
    
    .goal-card-content {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .goal-image {
        width: 70px;
        height: 70px;
        border-radius: 12px;
        background: #2d2d2d;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        flex-shrink: 0;
    }
    
    .goal-details {
        flex: 1;
        min-width: 0;
    }
    
    .goal-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 6px;
    }
    
    .goal-brand {
        color: #888;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }
    
    .goal-name {
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .goal-progress-text {
        font-size: 12px;
        color: #888;
        margin-bottom: 6px;
    }
    
    .goal-menu {
        color: #666;
        font-size: 18px;
        cursor: pointer;
        padding: 0 4px;
    }
    
    .goal-menu:hover {
        color: #C1FF72;
    }
    
    /* Progress Bar */
    .progress-bar-container {
        width: 100%;
        height: 4px;
        background-color: #2d2d2d;
        border-radius: 10px;
        margin: 6px 0;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background-color: #C1FF72;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .goal-amounts {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-top: 6px;
    }
    
    .goal-current {
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .goal-target {
        font-size: 13px;
        color: #666;
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
    
    /* Buttons */
    .stButton > button {
        background-color: #C1FF72 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        padding: 14px 24px !important;
        transition: all 0.2s !important;
        font-size: 15px !important;
    }
    
    .stButton > button:hover {
        background-color: #D4FF8F !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(193, 255, 114, 0.3) !important;
    }
    
    .stButton > button:disabled {
        background-color: #3a3a3a !important;
        color: #666 !important;
        cursor: not-allowed !important;
    }
    
    /* Amount Pills */
    .amount-pills {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .amount-pill {
        background: #2d2d2d;
        border: 2px solid #3d3d3d;
        border-radius: 24px;
        padding: 12px 20px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        color: #FFFFFF;
    }
    
    .amount-pill:hover {
        background: #C1FF72;
        color: #000000;
        border-color: #C1FF72;
    }
    
    .amount-pill.selected {
        background: #C1FF72;
        color: #000000;
        border-color: #C1FF72;
    }
    
    /* Goal Detail Card */
    .goal-detail-card {
        background: linear-gradient(135deg, #1a1a2d 0%, #2d2d3d 100%);
        border-radius: 24px;
        padding: 32px;
        text-align: center;
        margin: 20px 0;
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
        padding: 8px 16px;
        background: #2d2d2d;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 12px;
    }
    
    .lock-status.locked {
        background: #3d2d2d;
        color: #ff6b6b;
    }
    
    .lock-status.unlocked {
        background: #2d3d2d;
        color: #C1FF72;
    }
    
    /* UPI Payment Link */
    .upi-payment-link {
        display: inline-block;
        background-color: #C1FF72;
        color: #000000;
        border: none;
        border-radius: 16px;
        font-weight: 600;
        padding: 16px 32px;
        font-size: 16px;
        text-decoration: none;
        transition: all 0.2s;
        width: 100%;
        text-align: center;
        margin: 10px 0;
    }
    
    .upi-payment-link:hover {
        background-color: #D4FF8F;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(193, 255, 114, 0.3);
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
        'furniture': '🛋️', 'sofa': '🛋️',
        'labubu': '🧸', 'toy': '🧸'
    }
    
    for keyword, emoji in emoji_map.items():
        if keyword in name_lower:
            return emoji
    
    return '🎯'

def generate_upi_payment_link(amount, goal_name, vpa="phathim630@oksbi", payee_name="Seed It"):
    """
    Generate UPI deep link that opens Google Pay/PhonePe/Paytm directly
    
    Technical Implementation:
    - Uses upi://pay protocol for mobile deep-linking
    - mode=02: P2P (Person-to-Person) mode for compatibility
    - mc=0000: Generic merchant code to avoid "unverified merchant" warnings
    - URL encoding for special characters (spaces, etc.)
    """
    txn_id = f"SEED{uuid.uuid4().hex[:8].upper()}"
    
    # URL encode the payee name and transaction note
    encoded_payee_name = urllib.parse.quote(payee_name)
    encoded_transaction_note = urllib.parse.quote(f"Adding to {goal_name}")
    
    # Construct the UPI URI
    upi_uri = (
        f"upi://pay?"
        f"pa={vpa}&"
        f"pn={encoded_payee_name}&"
        f"am={amount:.2f}&"
        f"cu=INR&"
        f"tn={encoded_transaction_note}&"
        f"tr={txn_id}&"
        f"mode=02&"
        f"mc=0000"
    )
    
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

# ==================== SESSION STATE ====================

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.view = 'ONBOARDING'
    st.session_state.user = None
    st.session_state.goals = []
    st.session_state.privacy_mode = False
    st.session_state.selected_goal_id = None
    st.session_state.quick_amount = 10

# ==================== VIEWS ====================

def render_onboarding():
    """Onboarding screen - KEPT AS ORIGINAL (you said it was perfect!)"""
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
                st.session_state.user = {
                    'name': 'Daisy',
                    'mobile': '9876543210',
                    'email': 'demo@seedit.app'
                }
                # Add demo goals
                st.session_state.goals = [
                    {
                        'id': str(uuid.uuid4()),
                        'name': 'Labubu',
                        'brand': 'Pop Mart',
                        'emoji': '🧸',
                        'target_amount': 116.00,
                        'current_balance': 104.00,
                        'maturity_date': None,
                        'created_at': datetime.now().isoformat(),
                        'ledger': {},
                        'transactions': [
                            {'date': '2025-07-10T10:00:00', 'amount': 5.00, 'status': 'confirmed', 'type': 'deposit'},
                            {'date': '2025-07-08T14:30:00', 'amount': 10.00, 'status': 'confirmed', 'type': 'deposit'},
                            {'date': '2025-07-02T09:15:00', 'amount': 20.00, 'status': 'confirmed', 'type': 'deposit'},
                        ]
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'name': 'AirPods Max',
                        'brand': 'Apple',
                        'emoji': '🎧',
                        'target_amount': 549.00,
                        'current_balance': 280.00,
                        'maturity_date': None,
                        'created_at': datetime.now().isoformat(),
                        'ledger': {},
                        'transactions': []
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'name': 'Sneakers',
                        'brand': 'FitVille',
                        'emoji': '👟',
                        'target_amount': 245.00,
                        'current_balance': 55.00,
                        'maturity_date': None,
                        'created_at': datetime.now().isoformat(),
                        'ledger': {},
                        'transactions': []
                    }
                ]
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
    """Main dashboard - Matches reference image exactly"""
    user = st.session_state.user
    
    # Header with profile avatar
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin: 20px 0;">
            <div style="width: 44px; height: 44px; border-radius: 50%; background: #C1FF72; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; color: #000;">
                {user['name'][0].upper()}
            </div>
            <div>
                <div style="font-size: 15px; font-weight: 600;">Hello, {user['name'].split()[0]}</div>
                <div style="font-size: 12px; color: #888;">Turn dreams into balance</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔔", key="notifications", help="Notifications"):
            pass
    
    # Balance Card with Action Icons
    total_balance = sum(goal['current_balance'] for goal in st.session_state.goals)
    blur_class = "blurred" if st.session_state.privacy_mode else ""
    
    st.markdown(f"""
    <div class="balance-card">
        <div class="balance-header">
            <div class="balance-info">
                <div class="balance-label">Current Balance (USD)</div>
                <div class="balance-amount {blur_class}">${total_balance:,.2f}</div>
            </div>
            <div class="balance-actions">
                <div class="action-icon" title="Refresh">🔄</div>
                <div class="action-icon" title="History">🕐</div>
                <div class="action-icon primary" title="Add Money">+</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # My Goals Section Header
    st.markdown("""
    <div class="section-header">
        <div class="section-title">My goals</div>
        <div class="view-all-link">View All ›</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Goals List (Horizontal Layout)
    if st.session_state.goals:
        for goal in st.session_state.goals:
            progress = calculate_progress_percentage(goal['current_balance'], goal['target_amount'])
            blur_class = "blurred" if st.session_state.privacy_mode else ""
            
            # Clickable goal card
            if st.button(f"view_{goal['id']}", key=f"goal_btn_{goal['id']}", label_visibility="collapsed", use_container_width=True):
                st.session_state.selected_goal_id = goal['id']
                st.session_state.view = 'GOAL_DETAIL'
                st.rerun()
            
            st.markdown(f"""
            <div class="goal-card">
                <div class="goal-card-content">
                    <div class="goal-image">{goal['emoji']}</div>
                    <div class="goal-details">
                        <div class="goal-header">
                            <div>
                                <div class="goal-brand">{goal.get('brand', 'Goal')}</div>
                                <div class="goal-name">{goal['name']}</div>
                                <div class="goal-progress-text">{progress}%</div>
                            </div>
                            <div class="goal-menu">⋮</div>
                        </div>
                        <div class="progress-bar-container">
                            <div class="progress-bar-fill" style="width: {progress}%"></div>
                        </div>
                        <div class="goal-amounts">
                            <div class="goal-current {blur_class}">${goal['current_balance']:,.2f}</div>
                            <div class="goal-target {blur_class}">/${goal['target_amount']:,.2f}</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No goals yet! Create your first goal below 👇")
    
    # New Goal Button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("+ New goal", key="new_goal", use_container_width=True):
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
            target_amount = st.number_input("Target Amount ($)", min_value=1, value=100, step=10)
        
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
    """Goal detail view - Matches reference with direct UPI app opening"""
    goal_id = st.session_state.selected_goal_id
    goal = next((g for g in st.session_state.goals if g['id'] == goal_id), None)
    
    if not goal:
        st.error("Goal not found")
        return
    
    # Header with back button and menu
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("←", key="back"):
            st.session_state.view = 'DASHBOARD'
            st.rerun()
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.5px;">{goal['brand']}</div>
            <div style="font-size: 20px; font-weight: 700; margin-top: 2px;">{goal['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("⋮", key="menu"):
            pass
    
    # Quick Amount Pills
    st.markdown('<div class="amount-pills">', unsafe_allow_html=True)
    cols = st.columns(5)
    quick_amounts = [5, 10, 50, 100, 116]
    for idx, amount in enumerate(quick_amounts):
        with cols[idx]:
            pill_class = "selected" if st.session_state.quick_amount == amount else ""
            if st.button(f"${amount}", key=f"quick_{amount}", use_container_width=True):
                st.session_state.quick_amount = amount
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Large Goal Display Card
    progress = calculate_progress_percentage(goal['current_balance'], goal['target_amount'])
    
    st.markdown(f"""
    <div class="goal-detail-card">
        <div style="font-size: 100px; margin: 20px 0;">{goal['emoji']}</div>
        <div style="font-size: 18px; font-weight: 600; margin: 12px 0;">{goal['name']}</div>
        <div style="font-size: 36px; font-weight: 700; margin: 8px 0;">${goal['current_balance']:,.2f}</div>
        <div style="font-size: 14px; color: #888;">/${goal['target_amount']:,.2f}</div>
        <div style="font-size: 18px; font-weight: 600; color: #C1FF72; margin-top: 12px;">{progress}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Lock Status
    is_unlocked = is_goal_unlocked(goal)
    lock_emoji = "🔓" if is_unlocked else "🔒"
    lock_text = "Unlocked - Ready to Harvest!" if is_unlocked else "Locked - Keep Saving!"
    lock_class = "unlocked" if is_unlocked else "locked"
    
    st.markdown(f'<div style="text-align: center; margin: 16px 0;"><span class="lock-status {lock_class}">{lock_emoji} {lock_text}</span></div>', unsafe_allow_html=True)
    
    # Transaction History Section
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 32px 0 16px 0;">
        <div style="font-size: 20px; font-weight: 700;">Transaction history</div>
        <div style="color: #C1FF72; font-size: 14px; cursor: pointer;">View All ›</div>
    </div>
    """, unsafe_allow_html=True)
    
    if goal['transactions']:
        for txn in sorted(goal['transactions'], key=lambda x: x['date'], reverse=True)[:3]:
            txn_date = datetime.fromisoformat(txn['date']).strftime("%d %B %Y")
            st.markdown(f"""
            <div class="transaction-item">
                <div class="transaction-date">{txn_date}</div>
                <div class="transaction-amount">+${txn['amount']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; color: #666; padding: 20px;">No transactions yet</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # UPI Payment - Opens Google Pay/PhonePe/Paytm directly
    amount_to_add = st.session_state.quick_amount
    upi_link, txn_id = generate_upi_payment_link(amount_to_add, goal['name'])
    
    # Direct link that opens payment app
    st.markdown(f"""
    <a href="{upi_link}" target="_self" class="upi-payment-link">
        💳 Top up goal balance (${amount_to_add})
    </a>
    """, unsafe_allow_html=True)
    
    st.caption(f"💡 Clicking above will open your payment app (Google Pay, PhonePe, Paytm, etc.)")
    
    # Manual confirmation for demo purposes
    if st.button("✅ I've completed the payment", key="confirm_payment", use_container_width=True):
        goal['current_balance'] += amount_to_add
        goal['transactions'].append({
            'date': datetime.now().isoformat(),
            'amount': amount_to_add,
            'status': 'confirmed',
            'type': 'deposit'
        })
        st.success(f"✅ ${amount_to_add} added to {goal['name']}!")
        st.balloons()
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Withdraw/Harvest Button
    if is_unlocked:
        if st.button("🌾 Harvest (Withdraw)", use_container_width=True, type="primary"):
            st.success(f"🎉 Congratulations! You've unlocked ${goal['current_balance']:,.2f}!")
            st.balloons()
    else:
        st.button("🌾 Harvest (Locked)", use_container_width=True, disabled=True)
        remaining = goal['target_amount'] - goal['current_balance']
        st.caption(f"💡 Save ${remaining:,.2f} more to unlock!")

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
        <div style="font-size: 24px; font-weight: 700; margin: 8px 0;">${total_saved:,.2f}</div>
        <div style="color: #666;">of ${total_target:,.2f} across {total_goals} goals</div>
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
