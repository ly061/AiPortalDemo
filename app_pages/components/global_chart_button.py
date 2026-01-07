"""
全局图表按钮组件
在所有页面右上角显示图表入口按钮
"""
import streamlit as st

def render_global_chart_button():
    """在所有页面右上角渲染图表入口按钮"""
    if st.session_state.get('user_role'):
        st.markdown("""
        <style>
        .chart-menu-button-container {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 999999;
        }
        .chart-menu-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
        }
        .chart-menu-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            color: white !important;
        }
        </style>
        <div class="chart-menu-button-container">
            <button class="chart-menu-button" onclick="
                const sidebar = window.parent.document.querySelector('[data-testid=\"stSidebar\"]');
                const navItems = sidebar.querySelectorAll('[data-testid=\"stSidebarNav\"] a');
                navItems.forEach(item => {
                    if (item.textContent.includes('图表展示') || item.textContent.includes('📈')) {
                        item.click();
                    }
                });
            ">
                <span>📈</span>
                <span>图表展示</span>
            </button>
        </div>
        """, unsafe_allow_html=True)


