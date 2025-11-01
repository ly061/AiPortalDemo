import streamlit as st
import sys
from pathlib import Path

# 添加当前目录到路径，确保可以导入components
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from components import (
    render_json_beautifier,
    render_json_diff,
    render_timestamp_converter,
    render_excel_tool,
    render_api_tester,
    render_tool_download
)

st.set_page_config(
    page_title="Practical Tools",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Practical Tools")
st.markdown("---")

st.markdown("""
### 🔧 Feature Introduction
Provides various practical development tools, including JSON processing, timestamp conversion, and more.
""")

# Sidebar tool selection (sub-menu effect)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Tool Selection")
tool_option = st.sidebar.radio(
    "Select Tool",
    ["📝 JSON Beautifier", "🔄 JSON Diff", "⏰ Timestamp Converter", "📊 Excel Tool", "🔌 API Tester", "🔗 Tool Download"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

st.markdown("---")

# ==================== Route to Components ====================
if tool_option == "📝 JSON Beautifier":
    render_json_beautifier()
elif tool_option == "🔄 JSON Diff":
    render_json_diff()
elif tool_option == "⏰ Timestamp Converter":
    render_timestamp_converter()
elif tool_option == "📊 Excel Tool":
    render_excel_tool()
elif tool_option == "🔌 API Tester":
    render_api_tester()
else:  # Tool Download
    render_tool_download()

# Footer tips
st.markdown("---")
st.info("""
💡 **Tips:** 
- These tools can significantly improve development and testing efficiency
- It is recommended to choose appropriate tools based on project requirements
- Update tools regularly to get the latest features and security fixes
""")
