"""
Mermaid Diagram Generator Component - Generate flowcharts based on Mermaid code
"""
import streamlit as st
import streamlit_mermaid as st_mermaid

# Mermaid diagram type templates
MERMAID_TEMPLATES = {
    "Flowchart": {
        "code": """graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E""",
        "description": "Display processes and decision logic"
    },
    "Sequence Diagram": {
        "code": """sequenceDiagram
    participant A as User
    participant B as System
    participant C as Database
    
    A->>B: Send Request
    B->>C: Query Data
    C-->>B: Return Result
    B-->>A: Response""",
        "description": "Show interaction sequence between objects"
    },
    "Gantt Chart": {
        "code": """gantt
    title Project Development Plan
    dateFormat  YYYY-MM-DD
    section Requirements
    Research           :a1, 2024-01-01, 5d
    Documentation           :a2, after a1, 3d
    section Design
    System Design           :b1, after a2, 7d
    Database Design         :b2, after b1, 3d
    section Development
    Frontend           :c1, after b2, 10d
    Backend           :c2, after b2, 12d""",
        "description": "Display project timeline and work plan"
    },
    "Class Diagram": {
        "code": """classDiagram
    class Animal {
        +String name
        +int age
        +eat()
        +sleep()
    }
    class Dog {
        +String breed
        +bark()
    }
    class Cat {
        +String color
        +meow()
    }
    
    Animal <|-- Dog
    Animal <|-- Cat""",
        "description": "Show relationships and structure between classes"
    },
    "State Diagram": {
        "code": """stateDiagram-v2
    [*] --> Pending
    Pending --> Processing: Start
    Processing --> Completed: Success
    Processing --> Failed: Error
    Failed --> Pending: Retry
    Completed --> [*]""",
        "description": "Show state transitions of objects"
    },
    "ER Diagram": {
        "code": """erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER {
        string name
        string email
        int id
    }
    ORDER {
        int id
        date orderDate
    }
    LINE-ITEM {
        int quantity
        float price
    }""",
        "description": "Show database entity relationships"
    },
    "Pie Chart": {
        "code": """pie title Market Share
    "Product A" : 42.5
    "Product B" : 28.3
    "Product C" : 15.2
    "Others" : 14.0""",
        "description": "Display data proportions"
    },
    "User Journey": {
        "code": """journey
    title User Purchase Flow
    section Browse
      Visit Website: 5: User
      View Products: 4: User
    section Select
      Add to Cart: 5: User
      Choose Specs: 3: User
    section Purchase
      Fill Order: 4: User
      Payment: 5: User
      Confirm Order: 5: User, System""",
        "description": "Show user flow and experience"
    },
    "Git Graph": {
        "code": """gitGraph
    commit id: "Initial Commit"
    branch develop
    checkout develop
    commit id: "Create Develop Branch"
    commit id: "Feature Development"
    checkout main
    merge develop
    commit id: "Merge Develop Branch" """,
        "description": "Show Git branches and commit history"
    }
}

def apply_flowchart_colors(mermaid_code: str, color: str) -> str:
    """Apply colors to flowchart nodes"""
    import re
    
    if not color or color == "None":
        return mermaid_code
    
    # Extract color hex code
    if color.startswith('#'):
        color_hex = color
    else:
        # Color name to hex mapping
        color_map = {
            'red': '#ff6b6b',
            'blue': '#4dabf7',
            'green': '#51cf66',
            'yellow': '#ffd43b',
            'purple': '#9775fa',
            'orange': '#ff922b',
            'pink': '#f06595',
            'cyan': '#3bc9db',
            'gray': '#868e96',
        }
        color_hex = color_map.get(color.lower(), '#4dabf7')
    
    lines = mermaid_code.split('\n')
    result_lines = []
    node_ids = set()
    class_def_added = False
    
    # First pass: collect all node IDs
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('graph') or stripped.startswith('flowchart'):
            continue
        
        # Match node patterns: A[text], A(text), A{text}, A((text))
        node_pattern = r'\b([A-Za-z0-9_]+)(?:\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\}|\(\([^\)]+\)\))'
        matches = re.finditer(node_pattern, stripped)
        for match in matches:
            node_ids.add(match.group(1))
    
    if not node_ids:
        return mermaid_code
    
    # Second pass: build result with classDef and apply classes
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Add classDef after graph declaration
        if (stripped.startswith('graph') or stripped.startswith('flowchart')) and not class_def_added:
            result_lines.append(line)
            result_lines.append(f'    classDef nodeColor fill:{color_hex},stroke:#333,stroke-width:2px')
            class_def_added = True
            continue
        
        # Apply color class to nodes in this line
        if any(node_id in stripped for node_id in node_ids):
            # Replace node definitions to add class
            def add_class(match):
                node_id = match.group(1)
                node_content = match.group(2)
                # Check if class already applied
                if ':::' in line:
                    return match.group(0)
                return f'{node_id}{node_content}:::nodeColor'
            
            line = re.sub(r'\b([A-Za-z0-9_]+)(\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\}|\(\([^\)]+\)\))', add_class, line)
        
        result_lines.append(line)
    
    return '\n'.join(result_lines)


def render_mermaid_diagram():
    """Render Mermaid diagram generator tool interface"""
    
    # Main interface - Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Mermaid Code")
        
        # Initialize session_state
        if 'mermaid_code_input' not in st.session_state:
            st.session_state.mermaid_code_input = MERMAID_TEMPLATES["Flowchart"]["code"]
        
        # Handle code updates triggered from other areas
        if 'update_code' in st.session_state:
            st.session_state.mermaid_code_input = st.session_state.update_code
            del st.session_state.update_code
            st.rerun()
        
        # Code input area
        mermaid_code = st.text_area(
            "Enter Mermaid Code",
            height=400,
            key="mermaid_code_input",
            help="Enter Mermaid syntax code, supports multiple diagram types",
            placeholder="graph TD\n    A[Start] --> B[End]"
        )
        
        # Action buttons (below code input)
        st.markdown("#### ⚡ Actions")
        action_cols = st.columns(2)
        
        clear_code = False
        example_code_clicked = False
        
        with action_cols[0]:
            clear_code = st.button("🗑️ Clear", help="Clear code", use_container_width=True)
        
        with action_cols[1]:
            if st.button("💡 Example Code", use_container_width=True, help="Load example code"):
                example_code_clicked = True
        
        # Flowchart color selection (only show for flowcharts)
        # Check if current code is a flowchart (before widget creation)
        current_code_check = st.session_state.get('mermaid_code_input', '')
        is_flowchart = False
        if current_code_check:
            code_lower = current_code_check.lower().strip()
            is_flowchart = code_lower.startswith("graph") or code_lower.startswith("flowchart")
        
        # Initialize color if not set
        if 'flowchart_color' not in st.session_state:
            st.session_state.flowchart_color = "None"
        
        if is_flowchart:
            st.markdown("#### 🎨 Flowchart Color")
            
            color_options = {
                "None": "None",
                "Red": "#ff6b6b",
                "Blue": "#4dabf7",
                "Green": "#51cf66",
                "Yellow": "#ffd43b",
                "Purple": "#9775fa",
                "Orange": "#ff922b",
                "Pink": "#f06595",
                "Cyan": "#3bc9db",
                "Gray": "#868e96",
            }
            
            # Get current selected color index
            current_color_index = 0
            if st.session_state.flowchart_color:
                for idx, (name, value) in enumerate(color_options.items()):
                    if value == st.session_state.flowchart_color:
                        current_color_index = idx
                        break
            
            # Use key to track changes - Streamlit will automatically rerun on selectbox change
            # The key ensures the selectbox value is stored in session_state
            selected_color_name = st.selectbox(
                "Node Color",
                list(color_options.keys()),
                index=current_color_index,
                help="Select color for flowchart nodes",
                key="flowchart_color_selectbox"
            )
            
            # Update session state with selected color value immediately
            # Streamlit's selectbox automatically triggers rerun when value changes
            selected_color_value = color_options[selected_color_name]
            st.session_state.flowchart_color = selected_color_value
        
        # Handle action button clicks (Note: these occur after widget creation, so special handling needed)
        if clear_code:
            # Use update_code flag to update code
            st.session_state.update_code = ""
            st.rerun()
        
        if example_code_clicked:
            # Use update_code flag to update code
            st.session_state.update_code = MERMAID_TEMPLATES["Flowchart"]["code"]
            st.rerun()
    
    with col2:
        st.markdown("### 🎨 Diagram Preview")
        
        # Add CSS to move control buttons to the right, hide RESET button, and prevent overlap
        st.markdown("""
        <style>
        /* Style for mermaid diagram container */
        div[data-testid="stMermaid"],
        div[data-testid="stMermaid"] > div,
        iframe[title*="mermaid"],
        iframe[title*="streamlit-mermaid"] {
            position: relative !important;
            overflow: visible !important;
        }
        /* Target control buttons - move to right side */
        div[data-testid="stMermaid"] button,
        div[data-testid="stMermaid"] div[role="button"],
        div[data-testid="stMermaid"] > div:last-child {
            position: absolute !important;
            right: 10px !important;
            top: 10px !important;
            z-index: 1000 !important;
            background: white !important;
            padding: 5px 10px !important;
            border: 1px solid #ccc !important;
            border-radius: 4px !important;
        }
        /* Hide RESET button specifically */
        div[data-testid="stMermaid"] button:contains("RESET"),
        button[title*="Reset"],
        button[title*="RESET"],
        button:has-text("RESET") {
            display: none !important;
        }
        /* Hide RESET button using attribute selector */
        iframe[title*="mermaid"] {
            position: relative !important;
        }
        /* Ensure diagram has padding on right to avoid overlap */
        div[data-testid="stMermaid"] svg,
        div[data-testid="stMermaid"] > div:first-child {
            margin-right: 80px !important;
            padding-right: 80px !important;
        }
        </style>
        <script>
        // Hide RESET button using JavaScript
        function hideResetButton() {
            setTimeout(function() {
                // Try to find and hide RESET button in iframe
                var iframes = document.querySelectorAll('iframe[title*="mermaid"], iframe[title*="streamlit"]');
                iframes.forEach(function(iframe) {
                    try {
                        var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                        var buttons = iframeDoc.querySelectorAll('button, div[role="button"]');
                        buttons.forEach(function(btn) {
                            if (btn.textContent && btn.textContent.includes('RESET')) {
                                btn.style.display = 'none';
                            }
                        });
                    } catch(e) {
                        // Cross-origin restrictions
                    }
                });
                // Also try in main document
                var allButtons = document.querySelectorAll('button, div[role="button"]');
                allButtons.forEach(function(btn) {
                    if (btn.textContent && btn.textContent.includes('RESET')) {
                        btn.style.display = 'none';
                    }
                });
            }, 500);
        }
        window.addEventListener('load', hideResetButton);
        // Use MutationObserver to watch for new elements
        var observer = new MutationObserver(hideResetButton);
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
        """, unsafe_allow_html=True)
        
        # Get current code (use text_area value from session_state)
        # Note: In Streamlit, when selectbox changes, it triggers rerun automatically
        # So we need to get the latest value from session_state
        current_mermaid_code = st.session_state.get('mermaid_code_input', '')
        
        # Check if it's a flowchart and apply colors
        processed_code = current_mermaid_code
        if current_mermaid_code and current_mermaid_code.strip():
            code_lower = current_mermaid_code.lower().strip()
            is_flowchart = code_lower.startswith("graph") or code_lower.startswith("flowchart")
            
            # Apply colors if it's a flowchart and color is selected
            # Get the latest color value from session_state (updated by selectbox)
            flowchart_color = st.session_state.get('flowchart_color', "None")
            if is_flowchart and flowchart_color and flowchart_color != "None":
                processed_code = apply_flowchart_colors(current_mermaid_code, flowchart_color)
        
        # Create a container with relative positioning for the diagram
        st.markdown('<div style="position: relative; width: 100%;">', unsafe_allow_html=True)
        
        if processed_code and processed_code.strip():
            try:
                # Render Mermaid diagram using streamlit-mermaid library
                st_mermaid.st_mermaid(processed_code)
                
                st.success("✅ Diagram rendered successfully!")
                
            except Exception as e:
                st.error(f"❌ Diagram rendering failed: {str(e)}")
                st.code(processed_code, language="mermaid")
        else:
            st.info("👈 Please enter Mermaid code on the left, diagram will be displayed here")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Syntax help (displayed by default)
    # st.markdown("---")
    st.markdown("### 📖 Mermaid Syntax Help")
    
    help_tabs = st.tabs(["Flowchart", "Sequence Diagram", "Pie Chart", "Others"])
    
    with help_tabs[0]:
        if st.button("🚀 Quick Try", key="try_flowchart", use_container_width=True):
            flowchart_code = """graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E"""
            st.session_state.update_code = flowchart_code
            st.rerun()
        
        st.markdown("""
        #### Flowchart Syntax
        ```mermaid
        graph TD
            A[Start] --> B{Decision}
            B -->|Yes| C[Action 1]
            B -->|No| D[Action 2]
            C --> E[End]
            D --> E
        ```
        
        **Common Node Shapes:**
        - `A[text]` - Rectangle
        - `A(text)` - Rounded rectangle
        - `A{text}` - Diamond (decision)
        - `A((text))` - Circle
        - `A>text]` - Asymmetric shape
        
        **Directions:**
        - `TD` - Top to bottom
        - `LR` - Left to right
        - `BT` - Bottom to top
        - `RL` - Right to left
        """)
    
    with help_tabs[1]:
        if st.button("🚀 Quick Try", key="try_sequence", use_container_width=True):
            sequence_code = """sequenceDiagram
    participant A as User
    participant B as System
    participant C as Database
    
    A->>B: Send Request
    B->>C: Query Data
    C-->>B: Return Result
    B-->>A: Response"""
            st.session_state.update_code = sequence_code
            st.rerun()
        
        st.markdown("""
        #### Sequence Diagram Syntax
        ```mermaid
        sequenceDiagram
            participant A as User
            participant B as System
            A->>B: Request
            B-->>A: Response
        ```
        
        **Arrow Types:**
        - `->>` - Solid arrow
        - `-->>` - Dashed arrow
        - `->>` - Solid arrow with arrowhead
        - `-->>` - Dashed arrow with arrowhead
        """)
    
    with help_tabs[2]:
        if st.button("🚀 Quick Try", key="try_pie", use_container_width=True):
            pie_code = """pie title Market Share
    "Product A" : 42.5
    "Product B" : 28.3
    "Product C" : 15.2
    "Others" : 14.0"""
            st.session_state.update_code = pie_code
            st.rerun()
        
        st.markdown("""
        #### Pie Chart Syntax
        ```mermaid
        pie title Market Share
            "Product A" : 42.5
            "Product B" : 28.3
            "Product C" : 15.2
            "Others" : 14.0
        ```
        
        **Syntax:**
        - `pie title Title` - Define pie chart title
        - `"Label" : Value` - Define data item
        - Values can be percentages or any numbers
        """)
    
    with help_tabs[3]:
        st.markdown("""
        #### Other Diagram Types
        - **Gantt Chart**: `gantt`
        - **Class Diagram**: `classDiagram`
        - **State Diagram**: `stateDiagram-v2`
        - **ER Diagram**: `erDiagram`
        - **User Journey**: `journey`
        - **Git Graph**: `gitGraph`
        
        For more syntax, please refer to [Mermaid Official Documentation](https://mermaid.js.org/)
        """)
    
    # Bottom tips
    st.markdown("---")
    st.info("""
    💡 **Usage Tips:**
    - Diagrams will automatically update preview after code modification
    - Supports multiple diagram types
    - For more syntax, refer to: [Mermaid Official Documentation](https://mermaid.js.org/)
    """)
