import streamlit as st

st.set_page_config(
    page_title="Guideline Chatbot",
    page_icon="💬",
    layout="wide"
)

st.title("💬 Guideline Chatbot")
st.markdown("---")

st.markdown("""
### 🤖 Feature Introduction
Get project guidelines, best practices, and technical support through dedicated Chatbots. 
Each team has a customized Chatbot providing targeted help and advice.
""")

st.markdown("---")

# Team Chatbot data
teams = [
    {
        "name": "PH",
        "icon": "👨‍💻",
        "color": "#1E88E5",
        "description": "Provides code standards, architecture design, best practices, and technical support",
        "url": "https://chatgpt.com/"
    },
    {
        "name": "HK",
        "icon": "🧪",
        "color": "#43A047",
        "description": "Provides guidance on testing strategies, testing tools, and defect management",
        "url": "https://chatgpt.com/"
    },
    {
        "name": "CN",
        "icon": "📊",
        "color": "#FB8C00",
        "description": "Provides support for requirements analysis, documentation, and process design",
        "url": "https://chatgpt.com/"
    },
    {
        "name": "BA",
        "icon": "⚙️",
        "color": "#8E24AA",
        "description": "Provides help with CI/CD processes, environment configuration, and deployment strategies",
        "url": "https://chatgpt.com/"
    },
    {
        "name": "AL",
        "icon": "🎯",
        "color": "#E53935",
        "description": "Provides guidance on product planning, user research, and feature prioritization",
        "url": "https://chatgpt.com/"
    },
    {
        "name": "Common",
        "icon": "🌐",
        "color": "#607D8B",
        "description": "Provides general guidelines, shared resources, and common best practices across all teams",
        "url": "https://chatgpt.com/"
    }
]

# Create 6 tabs
tab_labels = [f"{team['icon']} {team['name']}" for team in teams]
tabs = st.tabs(tab_labels)

# Display content for each tab
for idx, tab in enumerate(tabs):
    team = teams[idx]
    with tab:
        # Team header
        # st.markdown(f"""
        # <div style="background-color: {team['color']}15; padding: 1.5rem; border-radius: 10px; 
        #             border-left: 5px solid {team['color']}; margin-bottom: 1.5rem;">
        #     <h2 style="color: {team['color']}; margin-top: 0;">
        #         {team['icon']} {team['name']}
        #     </h2>
        #     <p style="font-size: 1.1rem; color: #666; margin-bottom: 0;">
        #         {team['description']}
        #     </p>
        # </div>
        # """, unsafe_allow_html=True)
        
        col1, = st.columns([2])
        
        with col1:
            st.markdown("### 🔗 Access Chatbot")
            
            # Use link_button to create clickable button
            st.link_button(
                f"{team['icon']} Access {team['name']} Chatbot",
                team['url'],
                use_container_width=True,
                type="primary"
            )
        st.markdown("---")
        st.markdown(f"{team['description']}")
            









