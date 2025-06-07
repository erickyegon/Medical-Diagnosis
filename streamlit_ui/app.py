import streamlit as st
import requests
import os
from datetime import datetime
from auth import init_session_state, check_session_timeout, show_login_page, logout

# Health check endpoint for Render
if st.query_params.get("health") == "check":
    st.write("OK")
    st.stop()

# Page configuration with modern settings
st.set_page_config(
    page_title="AI Medical Diagnostics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/erickyegon/Medical-Diagnosis',
        'Report a bug': 'https://github.com/erickyegon/Medical-Diagnosis/issues',
        'About': """
        # AI Medical Diagnostics Support System

        An advanced AI-powered platform for symptom analysis and medical guidance.

        **Features:**
        - 🤖 AI-powered symptom analysis
        - 🔐 Secure authentication system
        - 👥 Role-based access control
        - 📊 Real-time health monitoring

        **Version:** 1.0.0
        **Author:** Erick Yegon
        """
    }
)

# Initialize authentication
init_session_state()

# Check for session timeout
if check_session_timeout():
    st.stop()

# Show login page if not authenticated
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# Custom CSS for modern, professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding and confusing elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stDecoration {visibility: hidden;}

    /* Hide any default labels or confusing text */
    .stTextArea > label {display: none !important;}
    .stTextInput > label {display: none !important;}

    /* Hide any potential confusing elements */
    .stAlert {margin-top: 0 !important;}
    .stMarkdown > div > p:empty {display: none !important;}

    /* Ensure clean spacing around main content */
    .main .block-container {
        padding-top: 1rem !important;
        max-width: 1200px !important;
    }

    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Header styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Card styles */
    .card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }

    /* Input section */
    .input-section {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 2px solid #e2e8f0;
    }

    /* Results section */
    .results-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-top: 2rem;
    }

    .symptom-card {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .diagnosis-card {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .warning-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.2);
    }

    /* Example buttons */
    .example-btn {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.875rem;
        color: #475569;
        transition: all 0.2s ease;
    }

    .example-btn:hover {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        transform: translateY(-1px);
    }

    /* Sidebar styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* Loading animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }

    .loading-spinner {
        border: 3px solid #f3f4f6;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .status-success {
        background-color: #dcfce7;
        color: #166534;
    }

    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
    }

    .status-error {
        background-color: #fee2e2;
        color: #991b1b;
    }

    /* Typography */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .result-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }

        .card {
            padding: 1.5rem;
        }

        .input-section {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main header with modern design
st.markdown("""
<div class="main-container">
    <h1 class="main-header">🩺 AI Medical Diagnostics Assistant</h1>
    <p class="subtitle">Advanced AI-powered symptom analysis and medical guidance</p>
</div>
""", unsafe_allow_html=True)

# Modern sidebar with compact design
with st.sidebar:
    # Get user info
    user_info = st.session_state.user_info

    # User profile card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;">
        <h3 style="margin: 0; color: white;">👤 Welcome</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            <strong>{}</strong><br>
            <small>{} • {}</small>
        </p>
    </div>
    """.format(
        st.session_state.username,
        user_info.get('role', 'user').title(),
        user_info.get('email', 'N/A')
    ), unsafe_allow_html=True)

    # Logout button
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        logout()
        st.rerun()

    # System status - compact
    st.markdown("### 🔧 System Status")
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")

    try:
        health_response = requests.get(f"{backend_url}/", timeout=3)
        if health_response.status_code == 200:
            st.markdown('<span class="status-indicator status-success">✅ System Online</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-error">❌ System Error</span>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<span class="status-indicator status-error">❌ System Offline</span>', unsafe_allow_html=True)

    # Quick stats
    if 'diagnosis_history' in st.session_state and st.session_state.diagnosis_history:
        total_diagnoses = len(st.session_state.diagnosis_history)
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; text-align: center;">
                <strong style="font-size: 1.5rem; color: #667eea;">{total_diagnoses}</strong><br>
                <small style="color: #64748b;">Diagnoses This Session</small>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Recent diagnoses - compact
    st.markdown("### 📋 Recent Activity")
    if 'diagnosis_history' in st.session_state and st.session_state.diagnosis_history:
        recent_diagnoses = st.session_state.diagnosis_history[-2:]  # Show last 2
        for record in reversed(recent_diagnoses):
            st.markdown(f"""
            <div style="background: white; padding: 0.75rem; border-radius: 8px;
                        margin-bottom: 0.5rem; border-left: 3px solid #667eea;">
                <p style="margin: 0; font-size: 0.875rem;">
                    <strong>{record['symptom_area']}</strong><br>
                    <small style="color: #64748b;">{record['timestamp'][:16]}</small>
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity")

    # Admin features - compact
    if user_info.get('role') == 'admin':
        st.markdown("### ⚙️ Admin")
        admin_col1, admin_col2 = st.columns(2)
        with admin_col1:
            if st.button("📊", help="System Logs"):
                st.info("Coming soon")
        with admin_col2:
            if st.button("👥", help="Manage Users"):
                st.info("Coming soon")

    # About section - collapsible
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        **AI Medical Diagnostics** uses advanced AI to:
        - 🎯 Categorize symptoms
        - 🩺 Suggest possible diagnoses
        - 💊 Recommend next steps
        - ⚠️ Provide safety guidance

        **Remember:** Always consult healthcare professionals for medical decisions.
        """)



# Clear separation and main content area
st.markdown('<br>', unsafe_allow_html=True)

# Main content area with modern layout
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# Symptom input section - clean and clear
st.markdown('<h2 class="section-title">📝 Describe Your Symptoms</h2>', unsafe_allow_html=True)

# Input area with better UX
symptom_input = st.text_area(
    "",
    placeholder="Example: I have a headache, fever, and feel nauseous. The headache started this morning and is getting worse...",
    height=120,
    help="💡 Be as specific as possible about your symptoms, when they started, their severity, and any other relevant details.",
    label_visibility="collapsed"
)

# Quick example buttons
st.markdown('<h3 class="result-title">💡 Quick Examples</h3>', unsafe_allow_html=True)
example_col1, example_col2, example_col3, example_col4 = st.columns(4)

with example_col1:
    if st.button("🤒 Fever & Headache", key="ex1", help="High fever with severe headache"):
        symptom_input = "I have a high fever of 102°F and severe headache that started this morning"
        st.rerun()

with example_col2:
    if st.button("😷 Respiratory Issues", key="ex2", help="Cough and breathing problems"):
        symptom_input = "I have a persistent dry cough and difficulty breathing for the past 3 days"
        st.rerun()

with example_col3:
    if st.button("🤢 Digestive Problems", key="ex3", help="Stomach pain and nausea"):
        symptom_input = "I have severe stomach pain, nausea, and have been vomiting since yesterday"
        st.rerun()

with example_col4:
    if st.button("🧠 Neurological", key="ex4", help="Headache and dizziness"):
        symptom_input = "I have a severe headache on the right side and feel dizzy when standing up"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Analysis button - prominent and centered
st.markdown('<br>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🔍 Analyze Symptoms with AI",
        type="primary",
        use_container_width=True,
        help="Get AI-powered analysis of your symptoms"
    )

# Results section
if analyze_button:
    if not symptom_input or symptom_input.strip() == "":
        st.markdown("""
        <div class="warning-card">
            <h3>⚠️ Input Required</h3>
            <p>Please describe your symptoms in the text area above before getting a diagnosis.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Loading state
        with st.container():
            st.markdown("""
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<h3 style="text-align: center; color: #667eea;">🤖 AI is analyzing your symptoms...</h3>', unsafe_allow_html=True)

            try:
                # API call
                backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
                response = requests.post(
                    f"{backend_url}/test",
                    headers={"Content-Type": "application/json"},
                    json={"input": symptom_input},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    # Clear loading state
                    st.empty()

                    # Results container
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)

                    # Success indicator
                    st.markdown("""
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <span class="status-indicator status-success">✅ Analysis Complete</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Results in two columns for better layout
                    result_col1, result_col2 = st.columns([1, 2])

                    with result_col1:
                        # Symptom Category
                        st.markdown(f"""
                        <div class="symptom-card">
                            <h3 class="result-title">🎯 Symptom Category</h3>
                            <h2 style="color: #3b82f6; margin: 0; font-size: 1.5rem;">{data.get("symptom_area", "Unknown")}</h2>
                        </div>
                        """, unsafe_allow_html=True)

                        # Analysis metadata
                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <p style="margin: 0; font-size: 0.875rem; color: #64748b;">
                                <strong>Analyzed:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                                <strong>By:</strong> {st.session_state.username} ({user_info.get('role', 'user')})<br>
                                <strong>Input Length:</strong> {len(symptom_input)} characters
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    with result_col2:
                        # Diagnosis and Recommendations
                        diagnosis_text = data.get("diagnosis", "No diagnosis available")
                        st.markdown(f"""
                        <div class="diagnosis-card">
                            <h3 class="result-title">🩺 AI Diagnosis & Recommendations</h3>
                            <div style="line-height: 1.6; color: #374151;">
                                {diagnosis_text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Medical disclaimer
                    st.markdown("""
                    <div class="warning-card">
                        <h4>⚠️ Important Medical Disclaimer</h4>
                        <p>This AI analysis is for informational purposes only and should not replace professional medical advice.
                        Always consult with qualified healthcare providers for proper diagnosis and treatment.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # Save to session history
                    if 'diagnosis_history' not in st.session_state:
                        st.session_state.diagnosis_history = []

                    diagnosis_record = {
                        "timestamp": datetime.now().isoformat(),
                        "user": st.session_state.username,
                        "input": symptom_input,
                        "symptom_area": data.get("symptom_area", ""),
                        "diagnosis": data.get("diagnosis", "")[:200] + "..." if len(data.get("diagnosis", "")) > 200 else data.get("diagnosis", "")
                    }
                    st.session_state.diagnosis_history.append(diagnosis_record)

                else:
                    st.markdown(f"""
                    <div class="warning-card">
                        <h3>❌ Server Error</h3>
                        <p>Error {response.status_code}: {response.text}</p>
                    </div>
                    """, unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.markdown("""
                <div class="warning-card">
                    <h3>⏱️ Request Timeout</h3>
                    <p>The request took too long to process. Please try again.</p>
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown("""
                <div class="warning-card">
                    <h3>🔌 Connection Error</h3>
                    <p>Cannot connect to the backend server. Please check if the service is running.</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="warning-card">
                    <h3>❌ Unexpected Error</h3>
                    <p>An error occurred: {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

# Modern footer
st.markdown('<br><br>', unsafe_allow_html=True)
st.markdown("""
<div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 2rem; border-radius: 16px; text-align: center;
            border: 1px solid #e2e8f0; margin-top: 3rem;">
    <h4 style="color: #1e293b; margin-bottom: 1rem;">🏥 AI Medical Diagnostics Assistant</h4>
    <p style="color: #64748b; margin-bottom: 1rem;">
        Powered by advanced AI technology including LangChain, FastAPI, and Streamlit
    </p>
    <div style="background: #fef3c7; padding: 1rem; border-radius: 8px;
                border-left: 4px solid #f59e0b; margin: 1rem 0;">
        <p style="margin: 0; color: #92400e; font-weight: 500;">
            ⚠️ <strong>Medical Disclaimer:</strong> This tool provides AI-generated suggestions for informational purposes only.
            Always consult qualified healthcare professionals for proper medical diagnosis and treatment.
        </p>
    </div>
    <p style="color: #94a3b8; font-size: 0.875rem; margin: 0;">
        Built with ❤️ for better healthcare accessibility | Version 1.0.0
    </p>
</div>
""", unsafe_allow_html=True)