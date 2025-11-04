"""
API Tester Component - HTTP API testing tool similar to Postman
"""
import streamlit as st
import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

def render_api_tester():
    """Render API Tester tool interface"""
    st.markdown("## 🔌 API Tester")
    
    st.info("Test HTTP APIs with support for various methods, headers, query parameters (GET), and request bodies")
    
    # Initialize session state
    if 'request_history' not in st.session_state:
        st.session_state.request_history = []
    
    # Request Configuration Section
    st.markdown("### Request Configuration")
    
    # HTTP Method and URL in one row
    col_method, col_url = st.columns([1, 3])
    
    with col_method:
        # HTTP Method
        http_method = st.selectbox(
            "HTTP Method",
            ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            index=0
        )
    
    with col_url:
        # URL Input
        url = st.text_input(
            "Request URL",
            value="https://www.baidu.com",
            placeholder="https://www.baidu.com",
            help="Enter the full URL including protocol (http:// or https://)"
        )
    
    # Headers
    st.markdown("#### Headers")
    col_label, col_radio, col_num = st.columns([2, 2, 2])
    with col_label:
        st.markdown("**Headers Input Mode:**")
    with col_radio:
        headers_mode = st.radio(
            "Headers Input Mode",
            ["Simple", "JSON"],
            horizontal=True,
            help="Simple: Add headers one by one. JSON: Paste headers as JSON object.",
            label_visibility="hidden"
        )
    with col_num:
        num_headers = st.number_input(
            "Number of Headers",
            min_value=0,
            max_value=20,
            value=2,
            step=1
        )
    
    if headers_mode == "Simple":
        headers = {}
        for i in range(num_headers):
            col_key, col_val = st.columns(2)
            with col_key:
                key = st.text_input(
                    f"Header Key {i+1}",
                    value="Content-Type" if i == 0 else "",
                    key=f"header_key_{i}",
                    placeholder="Content-Type"
                )
            with col_val:
                val = st.text_input(
                    f"Header Value {i+1}",
                    value="application/json" if i == 0 else "",
                    key=f"header_val_{i}",
                    placeholder="application/json"
                )
            if key and val:
                headers[key] = val
    else:
        headers_json = st.text_area(
            "Headers (JSON)",
            value='{\n  "Content-Type": "application/json"\n}',
            height=150,
            help='Enter headers as JSON object, e.g., {"Content-Type": "application/json", "Authorization": "Bearer token"}'
        )
        headers = {}
        if headers_json:
            try:
                headers = json.loads(headers_json)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")
    
    # Query Parameters (for GET and other methods that use query string)
    query_params = {}
    if http_method in ["GET", "DELETE", "HEAD", "OPTIONS"]:
        st.markdown("#### Query Parameters")
        col_label, col_radio, col_num = st.columns([2, 2, 2])
        with col_label:
            st.markdown("**Query Parameters Mode:**")
        with col_radio:
            params_mode = st.radio(
                "Query Parameters Mode",
                ["Simple", "JSON"],
                horizontal=True,
                help="Simple: Add query parameters one by one. JSON: Paste parameters as JSON object.",
                label_visibility="hidden",
                key="params_mode"
            )
        with col_num:
            num_params = st.number_input(
                "Number of Parameters",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
                key="num_params"
            )
        
        if params_mode == "Simple":
            for i in range(num_params):
                col_key, col_val = st.columns(2)
                with col_key:
                    key = st.text_input(
                        f"Parameter Key {i+1}",
                        key=f"param_key_{i}",
                        placeholder="key"
                    )
                with col_val:
                    val = st.text_input(
                        f"Parameter Value {i+1}",
                        key=f"param_val_{i}",
                        placeholder="value"
                    )
                if key:
                    query_params[key] = val
        else:
            params_json = st.text_area(
                "Query Parameters (JSON)",
                value='{\n  "key": "value"\n}',
                height=150,
                help='Enter query parameters as JSON object, e.g., {"page": "1", "limit": "10"}',
                key="params_json"
            )
            if params_json:
                try:
                    query_params = json.loads(params_json)
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format: {e}")
    
    # Request Body (only for methods that support body)
    if http_method in ["POST", "PUT", "PATCH"]:
        st.markdown("#### Request Body")
        body_type = st.selectbox(
            "Body Type",
            ["None", "JSON", "Form Data", "x-www-form-urlencoded", "Raw Text"],
            help="Select the format of request body"
        )
        
        request_body = None
        request_data = None
        
        if body_type == "JSON":
            body_json = st.text_area(
                "JSON Body",
                value='{\n  "key": "value"\n}',
                height=200,
                help="Enter JSON data for request body"
            )
            if body_json:
                try:
                    request_body = json.loads(body_json)
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format: {e}")
        
        elif body_type == "Form Data":
            num_form_fields = st.number_input(
                "Number of Form Fields",
                min_value=0,
                max_value=20,
                value=1,
                step=1,
                key="form_data_count"
            )
            form_data = {}
            for i in range(num_form_fields):
                col_key, col_val = st.columns(2)
                with col_key:
                    key = st.text_input(
                        f"Field Key {i+1}",
                        key=f"form_key_{i}",
                        placeholder="key"
                    )
                with col_val:
                    val = st.text_input(
                        f"Field Value {i+1}",
                        key=f"form_val_{i}",
                        placeholder="value"
                    )
                if key:
                    form_data[key] = val
            request_data = form_data if form_data else None
        
        elif body_type == "x-www-form-urlencoded":
            num_url_fields = st.number_input(
                "Number of URL Encoded Fields",
                min_value=0,
                max_value=20,
                value=1,
                step=1,
                key="urlencoded_count"
            )
            urlencoded_data = {}
            for i in range(num_url_fields):
                col_key, col_val = st.columns(2)
                with col_key:
                    key = st.text_input(
                        f"Field Key {i+1}",
                        key=f"urlencoded_key_{i}",
                        placeholder="key"
                    )
                with col_val:
                    val = st.text_input(
                        f"Field Value {i+1}",
                        key=f"urlencoded_val_{i}",
                        placeholder="value"
                    )
                if key:
                    urlencoded_data[key] = val
            request_data = urlencoded_data if urlencoded_data else None
        
        elif body_type == "Raw Text":
            request_body = st.text_area(
                "Raw Text Body",
                height=200,
                help="Enter raw text data"
            )
    
    # Buttons
    send_button = st.button("🚀 Send Request", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    # Response Section (below request configuration)
    st.markdown("### Response")
    
    if send_button:
        if not url:
            st.error("❌ Please enter a URL")
        else:
            # Validate URL
            try:
                parsed_url = urlparse(url)
                if not parsed_url.scheme or not parsed_url.netloc:
                    st.error("❌ Invalid URL format. Please include protocol (http:// or https://)")
                else:
                    with st.spinner("Sending request..."):
                        try:
                            # Prepare request parameters
                            request_kwargs = {
                                'method': http_method,
                                'url': url,
                                'headers': headers,
                                'timeout': 30
                            }
                            
                            # Add query parameters for GET, DELETE, HEAD, OPTIONS
                            if http_method in ["GET", "DELETE", "HEAD", "OPTIONS"] and query_params:
                                request_kwargs['params'] = query_params
                            
                            # Add body/data based on body type
                            if http_method in ["POST", "PUT", "PATCH"]:
                                if body_type == "JSON" and request_body is not None:
                                    request_kwargs['json'] = request_body
                                elif body_type in ["Form Data", "x-www-form-urlencoded"] and request_data:
                                    request_kwargs['data'] = request_data
                                elif body_type == "Raw Text" and request_body:
                                    request_kwargs['data'] = request_body
                            
                            # Send request
                            start_time = time.time()
                            response = requests.request(**request_kwargs)
                            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                            
                            # Store in history
                            history_item = {
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'method': http_method,
                                'url': url,
                                'status_code': response.status_code,
                                'response_time': f"{response_time:.2f}ms"
                            }
                            st.session_state.request_history.insert(0, history_item)
                            
                            # Display response
                            st.markdown(f"#### Status: `{response.status_code} {response.reason}`")
                            st.markdown(f"**Response Time:** {response_time:.2f}ms")
                            
                            # Response Headers
                            with st.expander("📋 Response Headers", expanded=False):
                                response_headers_dict = dict(response.headers)
                                st.json(response_headers_dict)
                            
                            # Response Body
                            st.markdown("#### Response Body")
                            
                            # Try to parse as JSON
                            try:
                                response_json = response.json()
                                st.json(response_json)
                            except:
                                # If not JSON, display as text
                                response_text = response.text
                                
                                # Try to detect content type
                                content_type = response.headers.get('Content-Type', '')
                                if 'json' in content_type.lower():
                                    try:
                                        parsed_json = json.loads(response_text)
                                        st.json(parsed_json)
                                    except:
                                        st.code(response_text, language="text")
                                elif 'html' in content_type.lower():
                                    st.code(response_text, language="html")
                                elif 'xml' in content_type.lower():
                                    st.code(response_text, language="xml")
                                else:
                                    st.code(response_text, language="text")
                            
                            st.success("✅ Request sent successfully!")
                            
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timeout (30 seconds)")
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Connection error. Please check the URL and your network connection.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Request failed: {str(e)}")
                        except Exception as e:
                            st.error(f"❌ Unexpected error: {str(e)}")
                            st.code(str(e))
            except Exception as e:
                st.error(f"❌ URL validation error: {str(e)}")
    else:
        st.info("Click 'Send Request' to see the response here")
    
    st.markdown("---")
    
    # Request History
    st.markdown("### 📜 Request History")
    if st.session_state.request_history:
        # Show last 10 requests
        for idx, item in enumerate(st.session_state.request_history[:10]):
            status_color = "🟢" if 200 <= item['status_code'] < 300 else "🟡" if 300 <= item['status_code'] < 400 else "🔴"
            st.markdown(f"""
            **{status_color} {item['method']}** `{item['url']}`  
            Status: `{item['status_code']}` | Time: `{item['response_time']}` | {item['timestamp']}
            """)
        if len(st.session_state.request_history) > 10:
            st.info(f"... and {len(st.session_state.request_history) - 10} more requests")
        
        if st.button("🗑️ Clear History"):
            st.session_state.request_history = []
            st.rerun()
    else:
        st.info("No request history yet")
