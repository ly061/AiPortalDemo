import streamlit as st

st.set_page_config(
    page_title="AI Testing Case Generator",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Generate Test Cases")
st.markdown("---")

st.markdown("""
### ℹ️ Feature Introduction
This module helps you quickly generate high-quality test cases using agent or preset templates to ensure completeness and standardization.
""")

# Quick access links
st.markdown("### 🚀 Quick Access")
col1, col2 = st.columns(2)

with col1:
    st.info("#### 🤖 Test Case Generator Agent")
    st.markdown("""
    Click the button below to access the test case generation Agent:
    """)
    
    # Preset link
    test_case_url = "https://chatgpt.com/"
    
    # Use link_button to create clickable link button
    st.link_button(
        "🤖 Access Test Case Generator Agent", 
        test_case_url,
        use_container_width=True
    )
    
    # Also display as text link
    # st.markdown(f"Or visit directly: [{test_case_url}]({test_case_url})")

with col2:
    st.info("#### 💻 Microsoft Copilot")
    st.markdown("""
    Click the button below to access the Microsoft Copilot and generate test cases with preset templates:
    """)
    
    # Preset link
    template_url = "https://chatgpt.com/"
    
    # Use link_button to create clickable link button
    st.link_button(
        "💻 Access Microsoft Copilot", 
        template_url,
        use_container_width=True
    )
    
    # Also display as text link
    st.markdown(f"Or visit directly: [SEAP]({template_url})")


# Example section
st.markdown("---")
st.markdown("### 📄 Prompt Templates")

tab1, = st.tabs(["📝 Functional Test Case Prompt"])

with tab1:
    st.code("""
Test Case ID: TC_FUNC_001
Test Case Name: User Login Function Test
Test Type: Functional Test
Priority: High

Preconditions:
1. User has registered an account
2. System is running normally

Test Steps:
1. Open login page
2. Enter correct username and password
3. Click "Login" button

Expected Results:
1. Successfully redirected to homepage
2. Username is displayed
3. Login state persists

Test Data:
- Username: test_user
- Password: Test@123
    """, language="text")



