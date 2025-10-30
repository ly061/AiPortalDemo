import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Testing Tools Portal",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# 定义角色权限映射
ROLE_PERMISSIONS = {
    "Manual Tester": [1, 2, 5, 6],
    "Automation Tester": [2, 3, 5, 6],
    "BA": [2, 4, 5, 6]
}

# 定义页面信息
PAGE_INFO = {
    1: {"icon": "🧪", "title": "Generate Test Cases", "file": "app_pages/1_🧪_Generate_Testcases.py"},
    2: {"icon": "💬", "title": "Guideline Chatbot", "file": "app_pages/2_💬_Guideline_Chatbot.py"},
    3: {"icon": "⚙️", "title": "AI Automation", "file": "app_pages/3_⚙️_AI_Automation.py"},
    4: {"icon": "📊", "title": "BA工具集", "file": "app_pages/4_📊_BA工具集.py"},
    5: {"icon": "🛠️", "title": "Tools", "file": "app_pages/5_🛠️_Tools.py"},
    6: {"icon": "🤖", "title": "AI Assistant", "file": "app_pages/6_🤖_AI_Assistant.py"}
}

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
    .role-card {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #1E88E5;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        cursor: pointer;
    }
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .role-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    .role-desc {
        color: #616161;
        font-size: 1rem;
        text-align: center;
    }
    .selected-role {
        background-color: #E3F2FD;
        border-color: #0D47A1;
    }
    </style>
""", unsafe_allow_html=True)

# 构建动态导航
def build_navigation():
    if st.session_state.user_role is None:
        # 没有选择角色，只显示Home页
        return None
    
    # 根据角色构建页面列表
    role = st.session_state.user_role
    allowed_pages = ROLE_PERMISSIONS.get(role, [])
    
    pages = []
    for page_num in sorted(allowed_pages):
        page_info = PAGE_INFO[page_num]
        pages.append(
            st.Page(
                page_info["file"],
                title=page_info["title"],
                icon=page_info["icon"]
            )
        )
    
    return pages

# 主页面内容
def show_home_page():
    # Page title
    st.markdown('<div class="main-header">🚀 Testing Tools Portal</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("---")
    st.markdown("### 👋 欢迎使用Testing Tools Portal")
    st.markdown("""
    Testing Tools Portal是一个综合性平台，集成了多种实用功能，
    旨在提升团队协作效率、自动化工作流程，并为业务分析提供强大工具。
    """)
    
    # 角色选择
    st.markdown("---")
    st.markdown("### 🎭 请选择您的角色")
    st.markdown("选择您的角色以访问相应的功能模块")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍💻 Manual Tester", use_container_width=True, type="primary" if st.session_state.user_role == "Manual Tester" else "secondary"):
            st.session_state.user_role = "Manual Tester"
            st.rerun()
        
        st.markdown("""
        <div class="role-card">
            <div class="role-title">👨‍💻 Manual Tester</div>
            <div class="role-desc">
                手动测试工程师<br><br>
                <b>可访问功能：</b><br>
                🧪 生成测试用例<br>
                💬 指南聊天机器人<br>
                🛠️ 实用工具<br>
                🤖 AI助手
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🤖 Automation Tester", use_container_width=True, type="primary" if st.session_state.user_role == "Automation Tester" else "secondary"):
            st.session_state.user_role = "Automation Tester"
            st.rerun()
        
        st.markdown("""
        <div class="role-card">
            <div class="role-title">🤖 Automation Tester</div>
            <div class="role-desc">
                自动化测试工程师<br><br>
                <b>可访问功能：</b><br>
                💬 指南聊天机器人<br>
                ⚙️ AI自动化<br>
                🛠️ 实用工具<br>
                🤖 AI助手
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("📊 BA", use_container_width=True, type="primary" if st.session_state.user_role == "BA" else "secondary"):
            st.session_state.user_role = "BA"
            st.rerun()
        
        st.markdown("""
        <div class="role-card">
            <div class="role-title">📊 BA</div>
            <div class="role-desc">
                业务分析师<br><br>
                <b>可访问功能：</b><br>
                💬 指南聊天机器人<br>
                📊 BA工具集<br>
                🛠️ 实用工具<br>
                🤖 AI助手
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 显示当前选择的角色
    if st.session_state.user_role:
        st.markdown("---")
        st.success(f"✅ 当前角色：**{st.session_state.user_role}**")
        st.info("👈 请从左侧菜单栏选择功能模块")
        
        # 添加切换角色按钮
        if st.button("🔄 切换角色", use_container_width=False):
            st.session_state.user_role = None
            st.rerun()
    else:
        st.markdown("---")
        st.warning("⚠️ 请先选择角色以访问功能模块")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #9E9E9E; font-size: 0.9rem;">
        <p>© 2025 Testing Tools Portal - 为团队协作和自动化而构建</p>
        <p>Version 2.0.0 | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# 主程序逻辑
home_page = st.Page(show_home_page, title="首页", icon="🏠", default=True)

pages = build_navigation()

if pages:
    # 有角色选择，显示完整导航
    pg = st.navigation([home_page] + pages)
else:
    # 没有角色选择，只显示Home页
    pg = st.navigation([home_page])

pg.run()

