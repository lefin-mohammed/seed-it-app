import streamlit as st
from datetime import datetime
import uuid
import urllib.parse

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Seed It",
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
    
    /* Hide Streamlit UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Container */
    .main-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Profile Header */
    .profile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .profile-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .profile-pic {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        overflow: hidden;
    }
    
    .profile-pic img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .profile-info h2 {
        font-size: 16px;
        font-weight: 600;
        margin: 0;
        color: #FFFFFF;
    }
    
    .profile-info p {
        font-size: 12px;
        color: #888;
        margin: 2px 0 0 0;
    }
    
    .notification-btn {
        width: 36px;
        height: 36px;
        background: transparent;
        border: 1px solid #333;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 18px;
    }
    
    /* Balance Card */
    .balance-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 24px;
    }
    
    .balance-label {
        font-size: 12px;
        color: #888;
        margin-bottom: 8px;
    }
    
    .balance-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .balance-amount {
        font-size: 36px;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .balance-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .balance-icon {
        width: 36px;
        height: 36px;
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.2s;
    }
    
    .balance-icon:hover {
        border-color: #C1FF72;
    }
    
    .balance-icon.add {
        background: #C1FF72;
        color: #000;
        font-size: 20px;
        font-weight: 700;
        border: none;
    }
    
    .overall-progress {
        width: 100px;
        height: 6px;
        background: #2d2d2d;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .overall-progress-fill {
        height: 100%;
        background: #C1FF72;
        border-radius: 10px;
    }
    
    /* Section Header */
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .view-all {
        font-size: 14px;
        color: #C1FF72;
        cursor: pointer;
    }
    
    /* Goal Card */
    .goal-card {
        background: #1a1a1a;
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        gap: 16px;
        align-items: center;
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .goal-card:hover {
        transform: translateY(-2px);
    }
    
    .goal-image {
        width: 80px;
        height: 80px;
        border-radius: 12px;
        background: #2d2d2d;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        overflow: hidden;
    }
    
    .goal-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .goal-image-emoji {
        font-size: 40px;
    }
    
    .goal-details {
        flex: 1;
        min-width: 0;
    }
    
    .goal-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 6px;
    }
    
    .goal-info {
        flex: 1;
    }
    
    .goal-category {
        font-size: 10px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }
    
    .goal-name {
        font-size: 17px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    
    .goal-progress-text {
        font-size: 12px;
        color: #888;
        margin-bottom: 6px;
    }
    
    .goal-progress-bar {
        width: 100%;
        height: 4px;
        background: #2d2d2d;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    
    .goal-progress-fill {
        height: 100%;
        background: #C1FF72;
        border-radius: 10px;
        transition: width 0.3s;
    }
    
    .goal-amounts {
        display: flex;
        align-items: baseline;
        gap: 6px;
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
    
    .goal-add-btn {
        width: 32px;
        height: 32px;
        background: #C1FF72;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 18px;
        font-weight: 700;
        color: #000;
        border: none;
        flex-shrink: 0;
        transition: all 0.2s;
    }
    
    .goal-add-btn:hover {
        background: #D4FF8F;
        transform: scale(1.1);
    }
    
    /* New Goal Button */
    .new-goal-btn {
        background: #C1FF72;
        color: #000;
        border: none;
        border-radius: 16px;
        padding: 16px;
        width: 100%;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        margin-top: 20px;
    }
    
    .new-goal-btn:hover {
        background: #D4FF8F;
        transform: translateY(-2px);
    }
    
    /* Buttons */
    .stButton > button {
        background: #C1FF72 !important;
        color: #000 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #D4FF8F !important;
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stTextInput input {
        background: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 16px !important;
    }
    
    .stNumberInput input {
        background: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
        color: #fff !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
    }
    
    /* Onboarding */
    .onboarding {
        text-align: center;
        padding: 60px 20px;
    }
    
    .onboarding-illustration {
        font-size: 120px;
        margin: 40px 0;
    }
    
    .onboarding-title {
        font-size: 32px;
        font-weight: 700;
        line-height: 1.3;
        margin: 20px 0;
    }
    
    .onboarding-subtitle {
        font-size: 15px;
        color: #888;
        line-height: 1.6;
        margin: 20px 0 40px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def get_category_and_emoji(goal_name):
    """Auto-categorize and assign emoji"""
    name = goal_name.lower()
    
    if any(x in name for x in ['phone', 'iphone', 'laptop', 'airpods', 'watch']):
        return 'Tech', '📱' if 'phone' in name or 'iphone' in name else '🎧' if 'airpods' in name else '💻'
    elif any(x in name for x in ['travel', 'vacation', 'trip']):
        return 'Travel', '✈️'
    elif any(x in name for x in ['shoes', 'sneakers']):
        return 'Fashion', '👟'
    elif any(x in name for x in ['car', 'bike']):
        return 'Vehicle', '🚗'
    elif any(x in name for x in ['labubu', 'toy']):
        return 'Entertainment', '🧸'
    else:
        return 'Other', '🎯'

def calculate_progress(current, target):
    if target == 0:
        return 0
    return min(int((current / target) * 100), 100)

def calculate_overall_progress(goals):
    """Calculate overall progress across all goals"""
    if not goals:
        return 0
    total_current = sum(g['current'] for g in goals)
    total_target = sum(g['target'] for g in goals)
    if total_target == 0:
        return 0
    return min(int((total_current / total_target) * 100), 100)

# ==================== SESSION STATE ====================

if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.view = 'SIGNUP'
    st.session_state.user = None
    st.session_state.goals = []

# ==================== VIEWS ====================

def render_signup():
    """Sign up page"""
    st.markdown("""
    <div class="onboarding">
        <div class="onboarding-illustration">🌱💰</div>
        <div class="onboarding-title">Set Your Goals.<br>Start Saving.</div>
        <div class="onboarding-subtitle">
            Create goals, track your progress, and watch<br>
            your savings grow — one step at a time.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        mobile = st.text_input("Mobile Number", placeholder="10-digit number", max_chars=10)
        email = st.text_input("Email", placeholder="your.email@example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            skip = st.form_submit_button("Skip", use_container_width=True)
        
        if submit:
            if name and mobile and email and len(mobile) == 10:
                st.session_state.user = {'name': name, 'mobile': mobile, 'email': email}
                st.session_state.view = 'DASHBOARD'
                st.rerun()
            else:
                st.error("Please fill all fields correctly")
        
        if skip:
            # Demo user with demo goals
            st.session_state.user = {'name': 'Daisy', 'mobile': '9876543210', 'email': 'demo@seedit.app'}
            st.session_state.goals = [
                {
                    'id': '1',
                    'name': 'Labubu',
                    'category': 'Pop Mart',
                    'emoji': '🧸',
                    'target': 116.00,
                    'current': 104.00,
                },
                {
                    'id': '2',
                    'name': 'AirPods Max',
                    'category': 'Apple',
                    'emoji': '🎧',
                    'target': 549.00,
                    'current': 280.00,
                },
                {
                    'id': '3',
                    'name': 'Sneakers',
                    'category': 'FitVille',
                    'emoji': '👟',
                    'target': 245.00,
                    'current': 55.00,
                }
            ]
            st.session_state.view = 'DASHBOARD'
            st.rerun()

def render_dashboard():
    """Dashboard - EXACT REPLICA"""
    user = st.session_state.user
    
    # Profile Header
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-left">
            <div class="profile-pic">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #C1FF72; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 700; color: #000;">
                    {user['name'][0]}
                </div>
            </div>
            <div class="profile-info">
                <h2>Hello, {user['name'].split()[0]}</h2>
                <p>Turn dreams into balance</p>
            </div>
        </div>
        <div class="notification-btn">🔔</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Balance Card
    total = sum(g['current'] for g in st.session_state.goals)
    overall_progress = calculate_overall_progress(st.session_state.goals)
    
    st.markdown(f"""
    <div class="balance-card">
        <div class="balance-label">Current Balance (USD)</div>
        <div class="balance-row">
            <div class="balance-amount">${total:,.2f}</div>
            <div class="balance-right">
                <div class="balance-icon">🔄</div>
                <div class="balance-icon">🕐</div>
                <div class="balance-icon add">+</div>
                <div class="overall-progress">
                    <div class="overall-progress-fill" style="width: {overall_progress}%"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # My Goals Section
    st.markdown("""
    <div class="section-header">
        <div class="section-title">My goals</div>
        <div class="view-all">View All ›</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Goals List
    for goal in st.session_state.goals:
        progress = calculate_progress(goal['current'], goal['target'])
        
        # Create container for goal card
        col1, col2 = st.columns([20, 1])
        
        with col1:
            # Goal card content (clickable to view details)
            if st.button(f"view_{goal['id']}", key=f"view_{goal['id']}", label_visibility="collapsed", use_container_width=True):
                st.session_state.selected_goal = goal['id']
                st.session_state.view = 'DETAIL'
                st.rerun()
        
        # Render the goal card with + button
        st.markdown(f"""
        <div class="goal-card">
            <div class="goal-image">
                <div class="goal-image-emoji">{goal['emoji']}</div>
            </div>
            <div class="goal-details">
                <div class="goal-header">
                    <div class="goal-info">
                        <div class="goal-category">{goal['category']}</div>
                        <div class="goal-name">{goal['name']}</div>
                        <div class="goal-progress-text">{progress}%</div>
                    </div>
                </div>
                <div class="goal-progress-bar">
                    <div class="goal-progress-fill" style="width: {progress}%"></div>
                </div>
                <div class="goal-amounts">
                    <span class="goal-current">${goal['current']:,.2f}</span>
                    <span class="goal-target">/${goal['target']:,.2f}</span>
                </div>
            </div>
            <button class="goal-add-btn" onclick="alert('Add money to {goal['name']}')">+</button>
        </div>
        """, unsafe_allow_html=True)
    
    # New Goal Button
    if st.button("+ New goal", key="new_goal"):
        st.session_state.view = 'CREATE'
        st.rerun()

def render_create():
    """Create Goal"""
    st.markdown("### 🎯 Create New Goal")
    
    with st.form("create_goal"):
        name = st.text_input("Goal Name", placeholder="e.g., iPhone 16 Pro")
        target = st.number_input("Target Amount ($)", min_value=1, value=100, step=10)
        category = st.text_input("Category", placeholder="e.g., Tech, Travel, Fashion")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Create", use_container_width=True):
                if name and target > 0:
                    cat, emoji = get_category_and_emoji(name)
                    if category:
                        cat = category
                    
                    new_goal = {
                        'id': str(uuid.uuid4()),
                        'name': name,
                        'category': cat,
                        'emoji': emoji,
                        'target': float(target),
                        'current': 0.0,
                    }
                    st.session_state.goals.append(new_goal)
                    st.success(f"Goal '{name}' created!")
                    st.session_state.view = 'DASHBOARD'
                    st.rerun()
        
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.view = 'DASHBOARD'
                st.rerun()

# ==================== MAIN ====================

def main():
    inject_custom_css()
    
    if st.session_state.view == 'SIGNUP':
        render_signup()
    elif st.session_state.view == 'DASHBOARD':
        render_dashboard()
    elif st.session_state.view == 'CREATE':
        render_create()

if __name__ == "__main__":
    main()
