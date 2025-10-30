import streamlit as st

st.set_page_config(
    page_title="AI Automation Script Generator",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ AI Automation ")
st.markdown("---")

st.markdown("""
### 🤖 功能介绍
Generate automation script with github copilot and Playwright MCP。
""")

st.markdown("---")

# Quick access
st.markdown("### 🚀 快速访问")

col2, = st.columns(1)



with col2:
    st.info("#### Guideline 文档")
    st.markdown("""
    查看自动化脚本最佳实践指南：
    """)
    
    guideline_url = "https://chatgpt.com/"
    
    st.link_button(
        "📚 查看 Guideline",
        guideline_url,
        use_container_width=True
    )






# # Footer
# st.markdown("---")
# st.info("""
# 💡 **提示：** 
# - 遵循自动化测试最佳实践指南
# - 定期review和重构测试代码
# - 确保脚本的可维护性和可扩展性
# """)

