"""
Authentication module for Medical Diagnostics Application
Supports multiple authentication methods: Local, Firebase, and OAuth
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import requests

# Configuration
AUTH_CONFIG = {
    "session_timeout": 3600,  # 1 hour in seconds
    "max_login_attempts": 3,
    "lockout_duration": 300,  # 5 minutes in seconds
}

class AuthManager:
    def __init__(self, auth_type="local"):
        """
        Initialize authentication manager
        auth_type: "local", "firebase", or "oauth"
        """
        self.auth_type = auth_type
        self.users_file = "streamlit_ui/users.json"
        self.ensure_users_file()
    
    def ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password_hash": self.hash_password("admin123"),
                    "email": "admin@medicalai.com",
                    "role": "admin",
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "login_attempts": 0,
                    "locked_until": None
                },
                "doctor": {
                    "password_hash": self.hash_password("doctor123"),
                    "email": "doctor@medicalai.com", 
                    "role": "doctor",
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "login_attempts": 0,
                    "locked_until": None
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self) -> Dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users: Dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed attempts"""
        users = self.load_users()
        if username not in users:
            return False
        
        locked_until = users[username].get("locked_until")
        if locked_until:
            lock_time = datetime.fromisoformat(locked_until)
            if datetime.now() < lock_time:
                return True
            else:
                # Unlock account
                users[username]["locked_until"] = None
                users[username]["login_attempts"] = 0
                self.save_users(users)
        return False
    
    def authenticate_local(self, username: str, password: str) -> bool:
        """Authenticate user with local credentials"""
        if self.is_account_locked(username):
            st.error(f"Account locked. Try again later.")
            return False
        
        users = self.load_users()
        if username in users:
            stored_hash = users[username]["password_hash"]
            if self.hash_password(password) == stored_hash:
                # Reset login attempts on successful login
                users[username]["login_attempts"] = 0
                users[username]["last_login"] = datetime.now().isoformat()
                users[username]["locked_until"] = None
                self.save_users(users)
                return True
            else:
                # Increment failed attempts
                users[username]["login_attempts"] += 1
                if users[username]["login_attempts"] >= AUTH_CONFIG["max_login_attempts"]:
                    lock_time = datetime.now() + timedelta(seconds=AUTH_CONFIG["lockout_duration"])
                    users[username]["locked_until"] = lock_time.isoformat()
                    st.error(f"Too many failed attempts. Account locked for {AUTH_CONFIG['lockout_duration']//60} minutes.")
                else:
                    remaining = AUTH_CONFIG["max_login_attempts"] - users[username]["login_attempts"]
                    st.error(f"Invalid credentials. {remaining} attempts remaining.")
                self.save_users(users)
        return False
    
    def register_user(self, username: str, password: str, email: str, role: str = "user") -> bool:
        """Register new user"""
        users = self.load_users()
        if username in users:
            return False
        
        users[username] = {
            "password_hash": self.hash_password(password),
            "email": email,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "login_attempts": 0,
            "locked_until": None
        }
        self.save_users(users)
        return True
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        users = self.load_users()
        return users.get(username)

class FirebaseAuth:
    """Firebase Authentication integration"""
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize Firebase Auth
        config should contain: api_key, auth_domain, project_id
        """
        self.config = config
        self.auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts"
    
    def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        """Sign up new user with Firebase"""
        url = f"{self.auth_url}:signUp?key={self.config['api_key']}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        return response.json()
    
    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user with Firebase"""
        url = f"{self.auth_url}:signInWithPassword?key={self.config['api_key']}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        return response.json()

class OAuthProvider:
    """OAuth 2.0 Authentication provider"""
    
    def __init__(self, provider_config: Dict[str, str]):
        """
        Initialize OAuth provider
        provider_config should contain: client_id, client_secret, redirect_uri, auth_url, token_url
        """
        self.config = provider_config
    
    def get_auth_url(self) -> str:
        """Get OAuth authorization URL"""
        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": self.config["redirect_uri"],
            "response_type": "code",
            "scope": "openid email profile"
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.config['auth_url']}?{query_string}"
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.config["redirect_uri"]
        }
        response = requests.post(self.config["token_url"], data=data)
        return response.json()

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "login_time" not in st.session_state:
        st.session_state.login_time = None

def check_session_timeout():
    """Check if session has timed out"""
    if st.session_state.authenticated and st.session_state.login_time:
        login_time = datetime.fromisoformat(st.session_state.login_time)
        if datetime.now() - login_time > timedelta(seconds=AUTH_CONFIG["session_timeout"]):
            logout()
            st.warning("Session expired. Please log in again.")
            return True
    return False

def login(username: str, user_info: Dict):
    """Set user as logged in"""
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.user_info = user_info
    st.session_state.login_time = datetime.now().isoformat()

def logout():
    """Log out user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_info = None
    st.session_state.login_time = None

def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        init_session_state()
        if check_session_timeout():
            return
        
        if not st.session_state.authenticated:
            show_login_page()
            return
        
        return func(*args, **kwargs)
    return wrapper

def show_login_page():
    """Display login/register page"""
    st.title("🔐 Medical Diagnostics - Authentication")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "OAuth"])
    
    auth_manager = AuthManager()
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if auth_manager.authenticate_local(username, password):
                    user_info = auth_manager.get_user_info(username)
                    login(username, user_info)
                    st.success("Login successful!")
                    st.rerun()
    
    with tab2:
        st.subheader("Register")
        with st.form("register_form"):
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            role = st.selectbox("Role", ["user", "doctor", "admin"])
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif auth_manager.register_user(new_username, new_password, new_email, role):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")
    
    with tab3:
        st.subheader("OAuth Login")
        st.info("OAuth integration requires additional setup. Contact administrator.")
        
        # Example OAuth buttons (would need actual implementation)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔵 Google"):
                st.info("Google OAuth not configured")
        with col2:
            if st.button("📘 Facebook"):
                st.info("Facebook OAuth not configured")
        with col3:
            if st.button("🐙 GitHub"):
                st.info("GitHub OAuth not configured")
    
    # Default credentials info
    with st.expander("ℹ️ Default Credentials"):
        st.write("**Admin Account:**")
        st.code("Username: admin\nPassword: admin123")
        st.write("**Doctor Account:**")
        st.code("Username: doctor\nPassword: doctor123")
        st.warning("⚠️ Change default passwords in production!")
