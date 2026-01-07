"""
全局图表菜单按钮组件
在所有页面右上角显示图表入口按钮
"""
import streamlit as st

def render_chart_menu_button():
    """渲染右上角图表菜单按钮"""
    # 只在用户已选择角色时显示
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
            color: white;
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
        }
        </style>
        <div class="chart-menu-button-container">
            <a href="#" onclick="window.parent.postMessage({type: 'streamlit:setFrameHeight', height: 0}, '*'); return false;" 
               style="text-decoration: none;">
                <div class="chart-menu-button">
                    <span>📈</span>
                    <span>图表展示</span>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # 使用 Streamlit 的方式：添加一个隐藏的按钮，通过 JavaScript 触发导航
        # 由于 Streamlit 的限制，我们使用侧边栏的方式更可靠
        pass


