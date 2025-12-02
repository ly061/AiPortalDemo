import streamlit as st
import httpx
import json

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
API_KEY = "1LtJU5J8KxkjryJtuRfdf1BIriTDV2DE"
API_ENDPOINT = f"{API_BASE_URL}/api/v1/chat/completions"

# Custom CSS Styles
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #262730;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    /* Fix input box at bottom */
    form[data-testid="question_form"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background-color: white !important;
        padding: 1rem !important;
        z-index: 999 !important;
        border-top: 1px solid #e0e0e0 !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
        margin: 0 !important;
    }
    /* Add bottom padding to chat content to avoid being covered by fixed input box */
    .main .block-container {
        padding-bottom: 120px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<div class="main-title">🤖 AI Assistant</div>', unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize processing state
if 'processing' not in st.session_state:
    st.session_state.processing = False

def chat_completion(messages: list) -> str:
    """
    Non-streaming call to chat completions API
    """
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": messages,
        "stream": False
    }
    
    try:
        response = httpx.post(
            API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=600.0
        )
        
        # Check response status code
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_text = error_data.get("detail", response.text)
            except:
                error_text = response.text
            return f"❌ API Error (Status Code: {response.status_code}): {error_text}"
        
        # Parse response
        try:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                if content:
                    return content
                else:
                    return "❌ No content in API response"
            else:
                return "❌ No choices in API response"
        except json.JSONDecodeError as e:
            return f"❌ Unable to parse API response: {str(e)}"
            
    except httpx.TimeoutException:
        return "❌ Request timeout, please try again later"
    except httpx.ConnectError:
        return f"❌ Unable to connect to API server ({API_BASE_URL}), please ensure the service is running"
    except Exception as e:
        return f"❌ An error occurred: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# If processing, show thinking status
if st.session_state.processing:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare message list (convert to API format)
            api_messages = []
            for msg in st.session_state.messages:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            try:
                response = chat_completion(api_messages)
                st.markdown(response)
                
                # Add assistant reply to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.processing = False
            except Exception as e:
                error_msg = f"❌ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.session_state.processing = False
    
    # Refresh page to show new messages
    st.rerun()

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.processing = False
        st.rerun()

st.markdown("---")

# Question input box (fixed at bottom) - use form to auto-clear input box
with st.form("question_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_question = st.text_input("Ask a question...", key="question_input", label_visibility="collapsed", placeholder="Ask a question...")
    with col2:
        send_button = st.form_submit_button("📤 Send", type="primary", use_container_width=True)

# Process user input (only when send button is clicked)
if send_button and user_question:
    # Save user input
    question_text = user_question.strip()
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": question_text})
    
    # Set processing state
    st.session_state.processing = True
    
    # Refresh page to show user message and processing status
    st.rerun()

