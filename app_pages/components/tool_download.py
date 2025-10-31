"""
Tool Download Component - 工具下载链接
"""
import streamlit as st

def render_tool_download():
    """渲染Tool Download工具界面"""
    st.markdown("## 🔗 Tool Download")
    
    st.info("Common development and testing tool download links")
    
    st.markdown("### Development Tools")
    
    tools = [
        {
            "name": "Visual Studio Code",
            "desc": "Lightweight code editor",
            "url": "https://code.visualstudio.com/",
            "icon": "💻"
        },
        {
            "name": "Postman",
            "desc": "API development and testing tool",
            "url": "https://www.postman.com/downloads/",
            "icon": "📮"
        },
        {
            "name": "Git",
            "desc": "Version control system",
            "url": "https://git-scm.com/downloads",
            "icon": "📦"
        },
        {
            "name": "Docker",
            "desc": "Containerization platform",
            "url": "https://www.docker.com/products/docker-desktop",
            "icon": "🐳"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, tool in enumerate(tools):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4>{tool['icon']} {tool['name']}</h4>
                <p style="color: #666;">{tool['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.link_button(
                f"Download {tool['name']}",
                tool['url'],
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown("### Testing Tools")
    
    test_tools = [
        {
            "name": "Selenium",
            "desc": "Web automation testing framework",
            "url": "https://www.selenium.dev/downloads/",
            "icon": "🌐"
        },
        {
            "name": "JMeter",
            "desc": "Performance testing tool",
            "url": "https://jmeter.apache.org/download_jmeter.cgi",
            "icon": "⚡"
        },
        {
            "name": "Playwright",
            "desc": "Modern web testing framework",
            "url": "https://playwright.dev/",
            "icon": "🎭"
        },
        {
            "name": "Cypress",
            "desc": "Front-end testing tool",
            "url": "https://www.cypress.io/",
            "icon": "🌲"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, tool in enumerate(test_tools):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4>{tool['icon']} {tool['name']}</h4>
                <p style="color: #666;">{tool['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.link_button(
                f"Visit {tool['name']}",
                tool['url'],
                use_container_width=True
            )

