"""
JSON Beautifier Component - 格式化压缩的JSON数据
"""
import streamlit as st
import json

def render_json_beautifier():
    """渲染JSON Beautifier工具界面"""
    st.markdown("## 📝 JSON Beautifier")
    
    st.info("Format compressed JSON data into a readable format")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Input JSON")
        json_input = st.text_area(
            "Please enter JSON data",
            height=300,
            placeholder='{"name":"John","age":30,"city":"New York"}',
            key="json_beautify_input"
        )
        
        indent_size = st.slider("Indent Spaces", 2, 8, 4)
        sort_keys = st.checkbox("Sort Keys", value=False)
        
        beautify_button = st.button("🎨 Beautify JSON", type="primary")
    
    with col2:
        st.markdown("### Beautified Result")
        if beautify_button:
            if json_input:
                try:
                    parsed_json = json.loads(json_input)
                    beautified_json = json.dumps(parsed_json, indent=indent_size, sort_keys=sort_keys, ensure_ascii=False)
                    st.code(beautified_json, language="json")
                    st.success("✅ JSON beautified successfully!")
                except json.JSONDecodeError as e:
                    st.error(f"❌ JSON format error: {str(e)}")
            else:
                st.warning("⚠️ Please enter JSON data")
        else:
            st.info("Beautified JSON will be displayed here")

