import streamlit as st
import json
from datetime import datetime
import time
import html
import re

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
    ["📝 JSON Beautifier", "🔄 JSON Diff", "⏰ Timestamp Converter", "🔗 Tool Download"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

st.markdown("---")

# ==================== JSON Beautifier ====================
if tool_option == "📝 JSON Beautifier":
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

# ==================== JSON Diff ====================
elif tool_option == "🔄 JSON Diff":
    st.markdown("## 🔄 JSON Diff")
    
    st.info("Compare differences between two JSON data and highlight the differences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### JSON 1")
        json1 = st.text_area(
            "Please enter the first JSON",
            height=250,
            key="json1",
            placeholder='{"name":"John","age":30}'
        )
    
    with col2:
        st.markdown("### JSON 2")
        json2 = st.text_area(
            "Please enter the second JSON",
            height=250,
            key="json2",
            placeholder='{"name":"John","age":31,"city":"NYC"}'
        )
    
    compare_button = st.button("🔍 Compare Differences", type="primary")
    
    if compare_button and json1 and json2:
        try:
            parsed_json1 = json.loads(json1)
            parsed_json2 = json.loads(json2)
            
            # Format JSON
            formatted_json1 = json.dumps(parsed_json1, indent=2, ensure_ascii=False)
            formatted_json2 = json.dumps(parsed_json2, indent=2, ensure_ascii=False)
            
            lines1 = formatted_json1.split('\n')
            lines2 = formatted_json2.split('\n')
            
            # Find differing lines (using deep comparison)
            def find_diff_in_json(obj1, obj2, path=""):
                """Recursively find differences in JSON objects, return difference paths"""
                diffs = []
                
                if type(obj1) != type(obj2):
                    diffs.append(path)
                    return diffs
                
                if isinstance(obj1, dict) and isinstance(obj2, dict):
                    all_keys = set(obj1.keys()) | set(obj2.keys())
                    for key in all_keys:
                        current_path = f"{path}.{key}" if path else str(key)
                        if key not in obj1:
                            diffs.append(current_path + " [added]")
                        elif key not in obj2:
                            diffs.append(current_path + " [deleted]")
                        elif obj1[key] != obj2[key]:
                            diffs.extend(find_diff_in_json(obj1[key], obj2[key], current_path))
                elif isinstance(obj1, list) and isinstance(obj2, list):
                    for i in range(max(len(obj1), len(obj2))):
                        current_path = f"{path}[{i}]"
                        if i >= len(obj1):
                            diffs.append(current_path + " [added]")
                        elif i >= len(obj2):
                            diffs.append(current_path + " [deleted]")
                        elif obj1[i] != obj2[i]:
                            diffs.extend(find_diff_in_json(obj1[i], obj2[i], current_path))
                else:
                    if obj1 != obj2:
                        diffs.append(path)
                
                return diffs
            
            diff_paths = find_diff_in_json(parsed_json1, parsed_json2)
            
            # Categorize difference paths
            added_paths = [p for p in diff_paths if "[added]" in p]
            deleted_paths = [p for p in diff_paths if "[deleted]" in p]
            modified_paths = [p for p in diff_paths if "[added]" not in p and "[deleted]" not in p]
            
            # Find corresponding line numbers based on difference paths (more accurate matching)
            def find_lines_with_paths(lines, paths):
                """Find line numbers containing difference paths"""
                diff_lines = set()
                
                # Mark corresponding lines for each difference path
                for path in paths:
                    clean_path = path.replace(" [added]", "").replace(" [deleted]", "")
                    
                    # Extract all key names from path
                    keys = []
                    # Match all non-array index key names
                    matches = re.findall(r'\.?([^.\[\]]+)(?:\[(\d+)\])?', clean_path)
                    for match in matches:
                        if match[0]:
                            keys.append(match[0])
                    
                    # If there are key names, search in lines
                    if keys:
                        # Use the last key as the primary search target
                        last_key = keys[-1]
                        for i, line in enumerate(lines):
                            # Check if this line contains this key name (as a key, not a value)
                            if f'"{last_key}":' in line:
                                diff_lines.add(i)
                                break
                    else:
                        # If it's a pure array index case, use the parent key
                        parent_keys = re.findall(r'([^.\[\]]+)(?=\[)', clean_path)
                        if parent_keys:
                            parent_key = parent_keys[-1]
                            for i, line in enumerate(lines):
                                if f'"{parent_key}"' in line:
                                    # Find the line range where the parent key is located
                                    # Mark this line and its related sub-items
                                    diff_lines.add(i)
                
                return diff_lines
            
            # Find three types of difference lines separately
            deleted_lines1 = find_lines_with_paths(lines1, deleted_paths)  # Only in JSON1
            added_lines2 = find_lines_with_paths(lines2, added_paths)       # Only in JSON2
            modified_lines1 = find_lines_with_paths(lines1, modified_paths) # Modifications in both
            modified_lines2 = find_lines_with_paths(lines2, modified_paths)
            
            # Difference lines in JSON1: deleted + modified
            diff_lines1 = deleted_lines1 | modified_lines1
            # Difference lines in JSON2: added + modified
            diff_lines2 = added_lines2 | modified_lines2
            
            # Display comparison results
            st.markdown("---")
            st.markdown("### 📊 Side-by-Side Comparison")
            
            # Add color legend
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 0.5rem 1rem; border-radius: 5px; margin-bottom: 1rem;">
                <span style="background-color: #ffe5e5; padding: 0.2rem 0.5rem; margin-right: 1rem;">🔴 Deleted</span>
                <span style="background-color: #e5ffe5; padding: 0.2rem 0.5rem; margin-right: 1rem;">🟢 Added</span>
                <span style="background-color: #cce5ff; padding: 0.2rem 0.5rem;">🔵 Modified</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            # Generate highlighted HTML (distinguish between deleted/added/modified)
            def generate_highlighted_json(lines, modified_lines, deleted_or_added_lines, is_deleted=False):
                result_html = '<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; font-family: monospace; font-size: 0.9rem; line-height: 1.6; overflow-x: auto;">'
                for i, line in enumerate(lines):
                    line_num = i + 1
                    escaped_line = html.escape(line)
                    
                    if i in deleted_or_added_lines:
                        # Deleted or added lines (light red/light green background)
                        bg_color = "#ffe5e5" if is_deleted else "#e5ffe5"
                        result_html += f'<div style="background-color: {bg_color}; padding: 0.2rem 0.5rem; white-space: pre;">'
                        result_html += f'<span style="color: #999; margin-right: 1rem; user-select: none;">{line_num:3d}.</span>'
                        result_html += f'<span>{escaped_line}</span>'
                        result_html += '</div>'
                    elif i in modified_lines:
                        # Modified lines (light blue background)
                        result_html += f'<div style="background-color: #cce5ff; padding: 0.2rem 0.5rem; white-space: pre;">'
                        result_html += f'<span style="color: #999; margin-right: 1rem; user-select: none;">{line_num:3d}.</span>'
                        result_html += f'<span>{escaped_line}</span>'
                        result_html += '</div>'
                    else:
                        # Normal lines
                        result_html += f'<div style="padding: 0.2rem 0.5rem; white-space: pre;">'
                        result_html += f'<span style="color: #999; margin-right: 1rem; user-select: none;">{line_num:3d}.</span>'
                        result_html += f'<span>{escaped_line}</span>'
                        result_html += '</div>'
                result_html += '</div>'
                return result_html
            
            with col1:
                st.markdown("#### JSON 1")
                st.markdown(generate_highlighted_json(lines1, modified_lines1, deleted_lines1, is_deleted=True), unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### JSON 2")
                st.markdown(generate_highlighted_json(lines2, modified_lines2, added_lines2, is_deleted=False), unsafe_allow_html=True)
            
            # Difference details
            if diff_paths:
                st.markdown("---")
                st.markdown("### 📋 Difference Details")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if deleted_paths:
                        st.warning(f"**➖ Deleted Fields ({len(deleted_paths)})**")
                        st.caption("Does not exist in JSON 2")
                        for item in deleted_paths:
                            st.markdown(f"- `{item.replace(' [deleted]', '')}`")
                
                with col2:
                    if added_paths:
                        st.success(f"**➕ Added Fields ({len(added_paths)})**")
                        st.caption("Does not exist in JSON 1")
                        for item in added_paths:
                            st.markdown(f"- `{item.replace(' [added]', '')}`")
                
                with col3:
                    if modified_paths:
                        st.info(f"**✏️ Modified Fields ({len(modified_paths)})**")
                        st.caption("Both have but different values")
                        for item in modified_paths:
                            st.markdown(f"- `{item}`")
            
            # Statistics
            st.markdown("---")
            st.markdown("### 📈 Difference Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("JSON 1 Total Lines", len(lines1))
            
            with col2:
                st.metric("JSON 2 Total Lines", len(lines2))
            
            with col3:
                st.metric("Differing Fields", len(diff_paths))
            
            if len(diff_paths) == 0:
                st.success("✅ The two JSONs are identical!")
                    
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON format error: {str(e)}")
    elif compare_button:
        st.warning("⚠️ Please enter two JSON data")

# ==================== Timestamp Converter ====================
elif tool_option == "⏰ Timestamp Converter":
    st.markdown("## ⏰ Timestamp Converter")
    
    st.info("Convert between Unix timestamps and human-readable time")
    
    tab1, tab2 = st.tabs(["Timestamp → DateTime", "DateTime → Timestamp"])
    
    with tab1:
        st.markdown("### Convert Timestamp to DateTime")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            timestamp_input = st.number_input(
                "Enter timestamp (milliseconds)",
                value=int(time.time() * 1000),
                step=1
            )
        
        with col2:
            timestamp_unit = st.selectbox(
                "Unit",
                ["Seconds", "Milliseconds", "Microseconds"],
                index=1
            )
        
        if st.button("🔄 Convert", key="ts_to_dt"):
            try:
                if timestamp_unit == "Milliseconds":
                    timestamp = timestamp_input / 1000
                elif timestamp_unit == "Microseconds":
                    timestamp = timestamp_input / 1000000
                else:
                    timestamp = timestamp_input
                
                dt = datetime.fromtimestamp(timestamp)
                
                st.success("Conversion successful!")
                st.markdown(f"**DateTime:** {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**ISO Format:** {dt.isoformat()}")
                st.markdown(f"**UTC Time:** {datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')} UTC")
                
            except Exception as e:
                st.error(f"❌ Conversion error: {str(e)}")
    
    with tab2:
        st.markdown("### Convert DateTime to Timestamp")
        
        col1, col2 = st.columns(2)
        
        with col1:
            date_input = st.date_input("Select date", datetime.now())
        
        with col2:
            time_input = st.time_input("Select time", datetime.now().time())
        
        output_unit = st.selectbox(
            "Output unit",
            ["Seconds", "Milliseconds", "Microseconds"],
            index=1,
            key="output_unit"
        )
        
        if st.button("🔄 Convert", key="dt_to_ts"):
            dt = datetime.combine(date_input, time_input)
            timestamp = int(dt.timestamp())
            
            if output_unit == "Milliseconds":
                timestamp = timestamp * 1000
            elif output_unit == "Microseconds":
                timestamp = timestamp * 1000000
            
            st.success("Conversion successful!")
            st.markdown(f"**Timestamp:** {timestamp}")
            st.code(str(timestamp))

# ==================== Tool Download ====================
else:  # Tool Download
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

# Footer tips
st.markdown("---")
st.info("""
💡 **Tips:** 
- These tools can significantly improve development and testing efficiency
- It is recommended to choose appropriate tools based on project requirements
- Update tools regularly to get the latest features and security fixes
""")

