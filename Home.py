import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Testing Tools Portal",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styles
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .feature-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #616161;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown('<div class="main-header">🚀 Testing Tools Portal</div>', unsafe_allow_html=True)

# Welcome message
st.markdown("---")
st.markdown("### 👋 Welcome to Testing Tools Portal")
st.markdown("""
Testing Tools Portal is a comprehensive platform that integrates multiple practical features, 
designed to enhance team collaboration efficiency, automate workflows, and provide powerful 
tools for business analysis.
""")

# Main feature modules overview
st.markdown("---")
st.markdown("### 📋 Main Feature Modules")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📋 Generate Test Cases</div>
        <div class="feature-desc">
            Quickly generate high-quality test cases using preset templates to improve testing efficiency
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">💬 Guideline Chatbot</div>
        <div class="feature-desc">
            Access dedicated Chatbots for multiple teams to get project guidelines and best practices
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">⚙️ Generate Automation Scripts</div>
        <div class="feature-desc">
            Automatically generate efficient automation scripts following best practice guidelines
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📊 BA Toolkit</div>
        <div class="feature-desc">
            Business analysis tools including BRD to FSD conversion, flowchart generation, and meeting minutes
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🛠️ Practical Tools</div>
        <div class="feature-desc">
            Development tools including JSON beautifier, JSON diff, timestamp converter, and more
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🤖 AI Assistant</div>
        <div class="feature-desc">
            Interactive AI assistant to answer questions about Portal, Streamlit, testing, and more
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick start guide
st.markdown("---")
st.markdown("### 🚀 Quick Start Guide")

with st.expander("📖 How to Get Started with Portal?", expanded=True):
    st.markdown("""
    1. **Select a Feature Module**: Choose the feature module you need from the left sidebar
    2. **Read the Instructions**: Each page has detailed usage instructions and examples
    3. **Start Using**: Complete your tasks following the page prompts
    4. **Get Help**: If you have questions, check the FAQ or contact the support team
    """)



# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9E9E9E; font-size: 0.9rem;">
    <p>© 2025 Testing Tools Portal - Built for Team Collaboration and Automation</p>
    <p>Version 1.3.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

