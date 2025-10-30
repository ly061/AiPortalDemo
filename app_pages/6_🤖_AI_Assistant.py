import streamlit as st

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

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
    </style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-title">🤖 AI Assistant</div>', unsafe_allow_html=True)

# 初始化聊天历史
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 问题输入框（固定在顶部）
col1, col2 = st.columns([5, 1])
with col1:
    user_question = st.text_input("Ask a question...", key="question_input", label_visibility="collapsed", placeholder="Ask a question...")
with col2:
    send_button = st.button("📤 Send", type="primary", use_container_width=True)

st.markdown("---")

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入（只在点击发送按钮时）
if send_button and user_question:
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # 生成AI回复（这里是模拟回复，实际应该调用AI API）
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 模拟回复逻辑
            if "portal" in user_question.lower():
                response = """
**Testing Tools Portal** is a comprehensive platform designed to enhance team collaboration and automate workflows.

Key features include:
- 📋 **Test Case Generation**: Quickly generate test cases using AI
- 💬 **Guideline Chatbot**: Access team-specific guidelines
- ⚙️ **AI Automation**: Generate automation scripts
- 📊 **BA Toolkit**: Business analysis tools
- 🛠️ **Practical Tools**: JSON beautifier, diff tools, etc.

You can navigate to different modules from the sidebar!
                """
            elif "session state" in user_question.lower():
                response = """
**Session State** in Streamlit allows you to persist data across reruns.

Example usage:
```python
import streamlit as st

# Initialize session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Update session state
if st.button('Increment'):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")
```

Session state is perfect for:
- Storing user inputs
- Maintaining chat history
- Keeping track of application state
                """
            elif "interactive chart" in user_question.lower():
                response = """
**Creating Interactive Charts** in Streamlit is easy!

Using Plotly for interactivity:
```python
import streamlit as st
import plotly.express as px

# Sample data
df = px.data.iris()

# Create interactive chart
fig = px.scatter(df, x="sepal_width", y="sepal_length", 
                 color="species", size="petal_length")

st.plotly_chart(fig, use_container_width=True)
```

You can also use:
- `st.line_chart()` for simple line charts
- `st.bar_chart()` for bar charts
- Altair, Bokeh, or other charting libraries
                """
            elif "customize" in user_question.lower():
                response = """
**Customizing Your Streamlit App:**

1. **Theme Configuration** (.streamlit/config.toml):
```toml
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

2. **Custom CSS**:
```python
st.markdown('''
<style>
.custom-class {
    color: blue;
    font-size: 20px;
}
</style>
''', unsafe_allow_html=True)
```

3. **Page Configuration**:
```python
st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide"
)
```
                """
            elif "deploy" in user_question.lower():
                response = """
**Deploying Streamlit Apps:**

**Option 1: Streamlit Community Cloud (Free)**
1. Push your code to GitHub
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Deploy!

**Option 2: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "Home.py"]
```

**Option 3: Cloud Platforms**
- AWS EC2/ECS
- Google Cloud Run
- Azure App Service
- Heroku

Make sure to include a `requirements.txt` file!
                """
            elif "test case" in user_question.lower():
                response = """
**Writing Test Cases:**

Good test cases should include:
1. **Test Case ID**: Unique identifier
2. **Title**: Clear description
3. **Preconditions**: Setup requirements
4. **Test Steps**: Detailed steps to execute
5. **Expected Results**: What should happen
6. **Test Data**: Sample data to use

Example:
```
TC_001: User Login Test
Preconditions: User account exists
Steps:
1. Navigate to login page
2. Enter username and password
3. Click "Login" button
Expected: User is redirected to dashboard
```

You can use our **Generate Test Cases** module to automate this!
                """
            else:
                response = f"""
I understand you're asking about: "{user_question}"

This is a placeholder response. In a production environment, this would connect to an actual AI service like:
- OpenAI GPT API
- Anthropic Claude API
- Custom AI model

Feel free to ask more questions about Portal, Streamlit, testing, or development!
                """
            
            st.markdown(response)
            
            # 添加助手回复到历史
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 刷新页面以清空输入框
    st.rerun()

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9E9E9E; font-size: 0.85rem;">
    <p>⚖️ Legal Disclaimer: This AI assistant provides general guidance. Always verify information for production use.</p>

</div>
""", unsafe_allow_html=True)

# 清除对话按钮
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

