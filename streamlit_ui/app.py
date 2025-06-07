import streamlit as st
import requests
from datetime import datetime
from auth import init_session_state, check_session_timeout, show_login_page, logout, require_auth

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnostics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .symptom-area {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .diagnosis-area {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🩺 AI Medical Diagnostics Assistant</h1>', unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    # User information and logout
    st.header("👤 User Information")
    user_info = st.session_state.user_info
    st.write(f"**Welcome:** {st.session_state.username}")
    st.write(f"**Role:** {user_info.get('role', 'user').title()}")
    st.write(f"**Email:** {user_info.get('email', 'N/A')}")

    if st.button("🚪 Logout", type="secondary"):
        logout()
        st.rerun()

    st.divider()

    st.header("ℹ️ About")
    st.write("""
    This AI-powered medical diagnostics tool helps analyze symptoms and provides:
    - Symptom categorization
    - Possible diagnoses
    - Recommended next steps
    - Treatment suggestions
    """)

    st.header("⚠️ Important Disclaimer")
    st.warning("""
    This tool is for informational purposes only and should not replace professional medical advice.
    Always consult with a healthcare provider for proper diagnosis and treatment.
    """)

    st.header("🔧 System Status")
    # Check backend status
    try:
        health_response = requests.get("http://localhost:8000/", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ Backend Connected")
            # Test the diagnosis endpoint
            test_response = requests.post(
                "http://localhost:8000/test",
                headers={"Content-Type": "application/json"},
                json={"input": "test"},
                timeout=5
            )
            if test_response.status_code == 200:
                st.success("✅ Diagnosis API Working")
            else:
                st.warning("⚠️ Diagnosis API Issues")
        else:
            st.error("❌ Backend Error")
    except Exception:
        st.error("❌ Backend Offline")

    # Diagnosis History
    st.divider()
    st.header("📋 Recent Diagnoses")
    if 'diagnosis_history' in st.session_state and st.session_state.diagnosis_history:
        recent_diagnoses = st.session_state.diagnosis_history[-3:]  # Show last 3
        for i, record in enumerate(reversed(recent_diagnoses)):
            with st.expander(f"🕐 {record['timestamp'][:16]}"):
                st.write(f"**Input:** {record['input'][:50]}...")
                st.write(f"**Category:** {record['symptom_area']}")
                st.write(f"**Summary:** {record['diagnosis'][:100]}...")
    else:
        st.info("No diagnosis history yet")

    # Admin features
    if user_info.get('role') == 'admin':
        st.divider()
        st.header("⚙️ Admin Panel")
        if st.button("📊 View System Logs"):
            st.info("System logs feature - Coming soon")
        if st.button("👥 Manage Users"):
            st.info("User management feature - Coming soon")
        if st.button("🔧 System Settings"):
            st.info("System settings feature - Coming soon")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Describe Your Symptoms")

    # Input area with better UX
    symptom_input = st.text_area(
        "Please describe your symptoms in detail:",
        placeholder="Example: I have a headache, fever, and feel nauseous...",
        height=150,
        help="Be as specific as possible about your symptoms, when they started, and their severity."
    )

    # Example symptoms for quick testing
    st.subheader("💡 Quick Examples")
    example_col1, example_col2, example_col3 = st.columns(3)

    with example_col1:
        if st.button("🤒 Fever & Headache"):
            symptom_input = "I have a high fever and severe headache"
            st.rerun()

    with example_col2:
        if st.button("😷 Cough & Sore Throat"):
            symptom_input = "I have a persistent cough and sore throat"
            st.rerun()

    with example_col3:
        if st.button("🤢 Stomach Pain"):
            symptom_input = "I have stomach pain and nausea"
            st.rerun()

with col2:
    st.header("🎯 Analysis")

    # Diagnosis button
    if st.button("🔍 Get AI Diagnosis", type="primary", use_container_width=True):
        if not symptom_input or symptom_input.strip() == "":
            st.error("⚠️ Please describe your symptoms before getting a diagnosis.")
        else:
            # Show loading spinner
            with st.spinner("🤖 AI is analyzing your symptoms..."):
                try:
                    # Use the test endpoint which has simpler validation
                    response = requests.post(
                        "http://localhost:8000/test",
                        headers={"Content-Type": "application/json"},
                        json={"input": symptom_input},
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Display results
                        st.success("✅ Analysis Complete!")

                        # Symptom Area
                        st.markdown("### 🎯 Symptom Category")
                        st.markdown(f'<div class="symptom-area"><strong>{data.get("symptom_area", "Unknown")}</strong></div>',
                                  unsafe_allow_html=True)

                        # Diagnosis
                        st.markdown("### 🩺 AI Diagnosis & Recommendations")
                        diagnosis_text = data.get("diagnosis", "No diagnosis available")
                        st.markdown(f'<div class="diagnosis-area">{diagnosis_text}</div>',
                                  unsafe_allow_html=True)

                        # Timestamp and user info
                        st.caption(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        st.caption(f"Analyzed by: {st.session_state.username} ({user_info.get('role', 'user')})")

                        # Save to session history (if implemented)
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
                        st.error(f"❌ Server Error: {response.status_code}")
                        st.write("Response:", response.text)

                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to the backend server. Please ensure it's running on http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏥 AI Medical Diagnostics Assistant | Powered by LangServe & Streamlit</p>
    <p><small>Remember: This tool provides suggestions only. Always consult healthcare professionals for medical decisions.</small></p>
</div>
""", unsafe_allow_html=True)