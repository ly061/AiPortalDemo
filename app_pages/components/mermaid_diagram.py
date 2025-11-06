"""
Mermaid Diagram Generator Component - Generate flowcharts based on Mermaid code
"""
import streamlit as st

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

def get_mermaid_html(mermaid_code: str, theme: str = "default") -> str:
    """Generate HTML containing Mermaid diagram"""
    theme_config = {
        "default": "",
        "dark": 'theme: "dark",',
        "forest": 'theme: "forest",',
        "neutral": 'theme: "neutral",',
    }
    
    theme_js = theme_config.get(theme, "")
    
    html_template = f"""
    <div class="mermaid-container">
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                {theme_js}
                flowchart: {{
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: "basis"
                }},
                sequence: {{
                    diagramMarginX: 50,
                    diagramMarginY: 10,
                    actorMargin: 50
                }}
            }});
        </script>
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
    <style>
        .mermaid-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .mermaid {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
    </style>
    """
    return html_template

def render_mermaid_diagram():
    """Render Mermaid diagram generator tool interface"""
    
    # Use default theme
    theme = "default"
    
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
        
        # Get current code (prioritize text_area value)
        current_mermaid_code = st.session_state.get('mermaid_code_input', '')
        
        if current_mermaid_code and current_mermaid_code.strip():
            try:
                # Render Mermaid diagram
                html_content = get_mermaid_html(current_mermaid_code, theme)
                st.components.v1.html(html_content, height=450, scrolling=True)
                
                st.success("✅ Diagram rendered successfully!")
                
            except Exception as e:
                st.error(f"❌ Diagram rendering failed: {str(e)}")
                st.code(current_mermaid_code, language="mermaid")
        else:
            st.info("👈 Please enter Mermaid code on the left, diagram will be displayed here")
    
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
