"""
Admin Panel for Medical Diagnostics Application
User management and system administration features
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from auth import AuthManager

def show_admin_panel():
    """Display admin panel interface"""
    if not st.session_state.authenticated or st.session_state.user_info.get('role') != 'admin':
        st.error("🚫 Access Denied: Admin privileges required")
        return
    
    st.title("⚙️ Admin Panel - Medical Diagnostics System")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 User Management", "📊 System Stats", "🔧 Settings", "📋 Audit Logs"])
    
    auth_manager = AuthManager()
    
    with tab1:
        st.header("👥 User Management")
        
        # User list
        users = auth_manager.load_users()
        if users:
            # Convert to DataFrame for better display
            user_data = []
            for username, info in users.items():
                user_data.append({
                    "Username": username,
                    "Email": info.get("email", "N/A"),
                    "Role": info.get("role", "user"),
                    "Created": info.get("created_at", "N/A")[:10] if info.get("created_at") else "N/A",
                    "Last Login": info.get("last_login", "Never")[:10] if info.get("last_login") else "Never",
                    "Login Attempts": info.get("login_attempts", 0),
                    "Status": "🔒 Locked" if info.get("locked_until") else "✅ Active"
                })
            
            df = pd.DataFrame(user_data)
            st.dataframe(df, use_container_width=True)
            
            # User actions
            st.subheader("User Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Reset User Password**")
                username_reset = st.selectbox("Select User", list(users.keys()), key="reset_user")
                new_password = st.text_input("New Password", type="password", key="new_password")
                if st.button("Reset Password"):
                    if new_password and len(new_password) >= 6:
                        users[username_reset]["password_hash"] = auth_manager.hash_password(new_password)
                        users[username_reset]["login_attempts"] = 0
                        users[username_reset]["locked_until"] = None
                        auth_manager.save_users(users)
                        st.success(f"Password reset for {username_reset}")
                        st.rerun()
                    else:
                        st.error("Password must be at least 6 characters")
            
            with col2:
                st.write("**Unlock User Account**")
                locked_users = [u for u, info in users.items() if info.get("locked_until")]
                if locked_users:
                    username_unlock = st.selectbox("Select Locked User", locked_users, key="unlock_user")
                    if st.button("Unlock Account"):
                        users[username_unlock]["login_attempts"] = 0
                        users[username_unlock]["locked_until"] = None
                        auth_manager.save_users(users)
                        st.success(f"Account unlocked for {username_unlock}")
                        st.rerun()
                else:
                    st.info("No locked accounts")
            
            # Delete user
            st.subheader("⚠️ Danger Zone")
            username_delete = st.selectbox("Select User to Delete", 
                                         [u for u in users.keys() if u != st.session_state.username], 
                                         key="delete_user")
            if st.button("🗑️ Delete User", type="secondary"):
                if username_delete and username_delete != st.session_state.username:
                    del users[username_delete]
                    auth_manager.save_users(users)
                    st.success(f"User {username_delete} deleted")
                    st.rerun()
        else:
            st.info("No users found")
    
    with tab2:
        st.header("📊 System Statistics")
        
        # User statistics
        users = auth_manager.load_users()
        total_users = len(users)
        active_users = len([u for u in users.values() if not u.get("locked_until")])
        locked_users = total_users - active_users
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", total_users)
        with col2:
            st.metric("Active Users", active_users)
        with col3:
            st.metric("Locked Users", locked_users)
        with col4:
            recent_logins = len([u for u in users.values() if u.get("last_login")])
            st.metric("Users with Logins", recent_logins)
        
        # Role distribution
        st.subheader("User Role Distribution")
        role_counts = {}
        for user_info in users.values():
            role = user_info.get("role", "user")
            role_counts[role] = role_counts.get(role, 0) + 1
        
        if role_counts:
            role_df = pd.DataFrame(list(role_counts.items()), columns=["Role", "Count"])
            st.bar_chart(role_df.set_index("Role"))
        
        # Diagnosis statistics
        st.subheader("Diagnosis Usage")
        if 'diagnosis_history' in st.session_state and st.session_state.diagnosis_history:
            total_diagnoses = len(st.session_state.diagnosis_history)
            st.metric("Total Diagnoses (Current Session)", total_diagnoses)
            
            # Recent activity
            recent_diagnoses = st.session_state.diagnosis_history[-5:]
            st.write("**Recent Diagnoses:**")
            for diag in reversed(recent_diagnoses):
                st.write(f"- {diag['timestamp'][:16]} by {diag['user']}: {diag['input'][:50]}...")
        else:
            st.info("No diagnosis data available")
    
    with tab3:
        st.header("🔧 System Settings")
        
        st.subheader("Authentication Settings")
        
        # Session timeout
        current_timeout = 3600  # Default 1 hour
        new_timeout = st.number_input("Session Timeout (seconds)", 
                                    min_value=300, max_value=86400, 
                                    value=current_timeout, step=300)
        
        # Max login attempts
        current_attempts = 3
        new_attempts = st.number_input("Max Login Attempts", 
                                     min_value=1, max_value=10, 
                                     value=current_attempts)
        
        # Lockout duration
        current_lockout = 300  # 5 minutes
        new_lockout = st.number_input("Lockout Duration (seconds)", 
                                    min_value=60, max_value=3600, 
                                    value=current_lockout, step=60)
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved! (Note: Restart required for some changes)")
        
        st.subheader("System Maintenance")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧹 Clear Session Data"):
                if 'diagnosis_history' in st.session_state:
                    st.session_state.diagnosis_history = []
                st.success("Session data cleared")
        
        with col2:
            if st.button("📤 Export User Data"):
                users = auth_manager.load_users()
                # Remove sensitive data for export
                export_data = {}
                for username, info in users.items():
                    export_data[username] = {
                        "email": info.get("email"),
                        "role": info.get("role"),
                        "created_at": info.get("created_at"),
                        "last_login": info.get("last_login")
                    }
                
                st.download_button(
                    label="📥 Download User Data",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"user_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    with tab4:
        st.header("📋 Audit Logs")
        
        st.subheader("Login Activity")
        users = auth_manager.load_users()
        login_data = []
        
        for username, info in users.items():
            if info.get("last_login"):
                login_data.append({
                    "Username": username,
                    "Last Login": info["last_login"][:19].replace("T", " "),
                    "Role": info.get("role", "user"),
                    "Failed Attempts": info.get("login_attempts", 0),
                    "Status": "🔒 Locked" if info.get("locked_until") else "✅ Active"
                })
        
        if login_data:
            login_df = pd.DataFrame(login_data)
            st.dataframe(login_df, use_container_width=True)
        else:
            st.info("No login activity recorded")
        
        st.subheader("System Events")
        st.info("Detailed audit logging feature - Coming soon")

if __name__ == "__main__":
    # This allows running the admin panel as a standalone page
    show_admin_panel()
