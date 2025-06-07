"""
Authentication Configuration for Medical Diagnostics Application
Configure different authentication providers here
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase Configuration
FIREBASE_CONFIG = {
    "api_key": os.getenv("FIREBASE_API_KEY", ""),
    "auth_domain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
    "project_id": os.getenv("FIREBASE_PROJECT_ID", ""),
    "storage_bucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
    "messaging_sender_id": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
    "app_id": os.getenv("FIREBASE_APP_ID", "")
}

# Google OAuth Configuration
GOOGLE_OAUTH_CONFIG = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
    "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501/auth/callback"),
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo"
}

# GitHub OAuth Configuration
GITHUB_OAUTH_CONFIG = {
    "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
    "client_secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
    "redirect_uri": os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8501/auth/callback"),
    "auth_url": "https://github.com/login/oauth/authorize",
    "token_url": "https://github.com/login/oauth/access_token",
    "userinfo_url": "https://api.github.com/user"
}

# Facebook OAuth Configuration
FACEBOOK_OAUTH_CONFIG = {
    "client_id": os.getenv("FACEBOOK_CLIENT_ID", ""),
    "client_secret": os.getenv("FACEBOOK_CLIENT_SECRET", ""),
    "redirect_uri": os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8501/auth/callback"),
    "auth_url": "https://www.facebook.com/v18.0/dialog/oauth",
    "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
    "userinfo_url": "https://graph.facebook.com/me"
}

# Application Settings
APP_CONFIG = {
    "session_timeout": int(os.getenv("SESSION_TIMEOUT", "3600")),  # 1 hour
    "max_login_attempts": int(os.getenv("MAX_LOGIN_ATTEMPTS", "3")),
    "lockout_duration": int(os.getenv("LOCKOUT_DURATION", "300")),  # 5 minutes
    "secret_key": os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    "enable_registration": os.getenv("ENABLE_REGISTRATION", "true").lower() == "true",
    "default_role": os.getenv("DEFAULT_ROLE", "user"),
    "require_email_verification": os.getenv("REQUIRE_EMAIL_VERIFICATION", "false").lower() == "true"
}

# Email Configuration (for verification emails)
EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "smtp_username": os.getenv("SMTP_USERNAME", ""),
    "smtp_password": os.getenv("SMTP_PASSWORD", ""),
    "from_email": os.getenv("FROM_EMAIL", "noreply@medicalai.com")
}

# Database Configuration (for production)
DATABASE_CONFIG = {
    "type": os.getenv("DB_TYPE", "json"),  # json, sqlite, postgresql, mysql
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "name": os.getenv("DB_NAME", "medical_diagnostics"),
    "username": os.getenv("DB_USERNAME", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "ssl_mode": os.getenv("DB_SSL_MODE", "prefer")
}

def get_auth_provider_config(provider: str):
    """Get configuration for specific auth provider"""
    configs = {
        "firebase": FIREBASE_CONFIG,
        "google": GOOGLE_OAUTH_CONFIG,
        "github": GITHUB_OAUTH_CONFIG,
        "facebook": FACEBOOK_OAUTH_CONFIG
    }
    return configs.get(provider, {})

def is_provider_configured(provider: str) -> bool:
    """Check if auth provider is properly configured"""
    config = get_auth_provider_config(provider)
    if provider == "firebase":
        return bool(config.get("api_key") and config.get("project_id"))
    else:  # OAuth providers
        return bool(config.get("client_id") and config.get("client_secret"))

def get_configured_providers():
    """Get list of configured authentication providers"""
    providers = []
    
    if is_provider_configured("firebase"):
        providers.append(("firebase", "🔥 Firebase"))
    if is_provider_configured("google"):
        providers.append(("google", "🔵 Google"))
    if is_provider_configured("github"):
        providers.append(("github", "🐙 GitHub"))
    if is_provider_configured("facebook"):
        providers.append(("facebook", "📘 Facebook"))
    
    return providers
