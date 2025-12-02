import streamlit as st
import httpx
import json

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# API配置
API_BASE_URL = "http://127.0.0.1:8000"
API_KEY = "1LtJU5J8KxkjryJtuRfdf1BIriTDV2DE"
API_ENDPOINT = f"{API_BASE_URL}/api/v1/chat/completions"

# 自定义CSS样式
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #262730;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    /* 固定输入框在底部 */
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
    /* 为聊天内容添加底部边距，避免被固定输入框遮挡 */
    .main .block-container {
        padding-bottom: 120px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-title">🤖 AI Assistant</div>', unsafe_allow_html=True)

# 初始化聊天历史
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 初始化处理状态
if 'processing' not in st.session_state:
    st.session_state.processing = False

def chat_completion(messages: list) -> str:
    """
    非流式调用chat completions API
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
        
        # 检查响应状态码
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_text = error_data.get("detail", response.text)
            except:
                error_text = response.text
            return f"❌ API错误 (状态码: {response.status_code}): {error_text}"
        
        # 解析响应
        try:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                if content:
                    return content
                else:
                    return "❌ API返回的响应中没有内容"
            else:
                return "❌ API返回的响应中没有choices"
        except json.JSONDecodeError as e:
            return f"❌ 无法解析API响应: {str(e)}"
            
    except httpx.TimeoutException:
        return "❌ 请求超时，请稍后重试"
    except httpx.ConnectError:
        return f"❌ 无法连接到API服务器 ({API_BASE_URL})，请确保服务正在运行"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 如果正在处理，显示思考状态
if st.session_state.processing:
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            # 准备消息列表（转换为API格式）
            api_messages = []
            for msg in st.session_state.messages:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            try:
                response = chat_completion(api_messages)
                st.markdown(response)
                
                # 添加助手回复到历史
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.processing = False
            except Exception as e:
                error_msg = f"❌ 发生错误: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.session_state.processing = False
    
    # 刷新页面以显示新消息
    st.rerun()

# 清除对话按钮
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.processing = False
        st.rerun()

st.markdown("---")

# 问题输入框（固定在底部）- 使用 form 来自动清空输入框
with st.form("question_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_question = st.text_input("Ask a question...", key="question_input", label_visibility="collapsed", placeholder="Ask a question...")
    with col2:
        send_button = st.form_submit_button("📤 Send", type="primary", use_container_width=True)

# 处理用户输入（只在点击发送按钮时）
if send_button and user_question:
    # 保存用户输入
    question_text = user_question.strip()
    
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": question_text})
    
    # 设置处理状态
    st.session_state.processing = True
    
    # 刷新页面以显示用户消息和处理状态
    st.rerun()

