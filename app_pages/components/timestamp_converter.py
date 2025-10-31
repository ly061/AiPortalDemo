"""
Timestamp Converter Component - 时间戳转换工具
"""
import streamlit as st
import time
from datetime import datetime

def render_timestamp_converter():
    """渲染Timestamp Converter工具界面"""
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

