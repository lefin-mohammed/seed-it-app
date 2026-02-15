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

if name == "main":
    main()
