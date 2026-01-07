import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
from pathlib import Path

st.set_page_config(
    page_title="图表展示",
    page_icon="📈",
    layout="wide"
)

# 添加右上角图表按钮（图表页面不需要显示）
# 已移除，因为用户已经在图表页面了

# 自定义样式
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .chart-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-title">📈 图表展示中心</div>', unsafe_allow_html=True)
st.markdown("---")

# 默认图表类型（不再显示在侧边栏）
chart_type = "📊 折线图"

# 数据上传区域
st.markdown("### 📁 数据上传")
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "上传CSV或Excel文件",
        type=['csv', 'xlsx', 'xls'],
        help="支持CSV和Excel格式文件"
    )

with col2:
    use_sample_data = st.checkbox("使用示例数据", value=True)

# 生成示例数据
@st.cache_data
def generate_sample_data():
    """生成示例数据"""
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    data = {
        '日期': dates,
        '销售额': np.random.randint(1000, 5000, 30) + np.random.randn(30) * 200,
        '访问量': np.random.randint(500, 2000, 30),
        '转化率': np.random.uniform(0.02, 0.15, 30),
        '类别': np.random.choice(['A', 'B', 'C'], 30),
        '地区': np.random.choice(['北京', '上海', '广州', '深圳'], 30)
    }
    return pd.DataFrame(data)

# 加载数据
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ 成功加载数据，共 {len(df)} 行，{len(df.columns)} 列")
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"❌ 数据加载失败: {str(e)}")
        df = None
elif use_sample_data:
    df = generate_sample_data()
    st.info("💡 当前使用示例数据")
    st.dataframe(df.head(10), use_container_width=True)
else:
    df = None
    st.warning("⚠️ 请上传数据文件或选择使用示例数据")

st.markdown("---")

# ==================== 折线图 ====================
if chart_type == "📊 折线图" and df is not None:
    st.markdown("## 📊 折线图")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_column = st.selectbox("X轴列", df.columns.tolist())
    
    with col2:
        y_columns = st.multiselect("Y轴列（可多选）", df.columns.tolist(), default=df.columns[1] if len(df.columns) > 1 else None)
    
    if y_columns:
        fig = go.Figure()
        
        for y_col in y_columns:
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[y_col],
                mode='lines+markers',
                name=y_col,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title=f"折线图: {', '.join(y_columns)} vs {x_column}",
            xaxis_title=x_column,
            yaxis_title="数值",
            hovermode='x unified',
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== 柱状图 ====================
elif chart_type == "📊 柱状图" and df is not None:
    st.markdown("## 📊 柱状图")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_column = st.selectbox("X轴列", df.columns.tolist())
    
    with col2:
        y_column = st.selectbox("Y轴列", df.columns.tolist())
    
    with col3:
        chart_orientation = st.selectbox("图表方向", ["垂直", "水平"])
    
    orientation = 'v' if chart_orientation == "垂直" else 'h'
    
    fig = px.bar(
        df,
        x=x_column if orientation == 'v' else y_column,
        y=y_column if orientation == 'v' else x_column,
        orientation=orientation,
        title=f"柱状图: {y_column} vs {x_column}",
        color=x_column if orientation == 'v' else y_column,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        height=500,
        template="plotly_white",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== 饼图 ====================
elif chart_type == "📊 饼图" and df is not None:
    st.markdown("## 📊 饼图")
    
    col1, col2 = st.columns(2)
    
    with col1:
        labels_column = st.selectbox("标签列", df.columns.tolist())
    
    with col2:
        values_column = st.selectbox("数值列", df.columns.tolist())
    
    # 聚合数据
    if df[values_column].dtype in ['int64', 'float64']:
        pie_data = df.groupby(labels_column)[values_column].sum().reset_index()
        
        fig = px.pie(
            pie_data,
            values=values_column,
            names=labels_column,
            title=f"饼图: {values_column} 分布",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>数值: %{value}<br>占比: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ 数值列必须是数字类型")

# ==================== 散点图 ====================
elif chart_type == "📊 散点图" and df is not None:
    st.markdown("## 📊 散点图")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_column = st.selectbox("X轴列", df.columns.tolist())
    
    with col2:
        y_column = st.selectbox("Y轴列", df.columns.tolist())
    
    with col3:
        color_column = st.selectbox("颜色分组列（可选）", [None] + df.columns.tolist())
    
    if color_column:
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=f"散点图: {y_column} vs {x_column}",
            size_max=10
        )
    else:
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"散点图: {y_column} vs {x_column}"
        )
    
    fig.update_layout(
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== 热力图 ====================
elif chart_type == "📊 热力图" and df is not None:
    st.markdown("## 📊 热力图")
    
    # 选择数值列
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_columns) > 0:
        selected_columns = st.multiselect(
            "选择数值列",
            numeric_columns,
            default=numeric_columns[:5] if len(numeric_columns) >= 5 else numeric_columns
        )
        
        if selected_columns:
            # 计算相关性矩阵
            corr_matrix = df[selected_columns].corr()
            
            fig = px.imshow(
                corr_matrix,
                labels=dict(x="变量", y="变量", color="相关系数"),
                x=selected_columns,
                y=selected_columns,
                color_continuous_scale="RdBu",
                title="相关性热力图",
                aspect="auto"
            )
            
            fig.update_layout(
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示相关性数据表
            st.markdown("### 相关性数据表")
            st.dataframe(corr_matrix, use_container_width=True)
    else:
        st.warning("⚠️ 数据中没有数值列，无法生成热力图")

# ==================== 组合图表 ====================
elif chart_type == "📊 组合图表" and df is not None:
    st.markdown("## 📊 组合图表")
    
    st.info("💡 组合图表可以在同一图表中展示多种类型的图表")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_column = st.selectbox("X轴列", df.columns.tolist())
        line_column = st.selectbox("折线图列", df.columns.tolist())
    
    with col2:
        bar_column = st.selectbox("柱状图列", df.columns.tolist())
    
    # 创建子图
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 添加柱状图
    fig.add_trace(
        go.Bar(x=df[x_column], y=df[bar_column], name=bar_column),
        secondary_y=False,
    )
    
    # 添加折线图
    fig.add_trace(
        go.Scatter(x=df[x_column], y=df[line_column], name=line_column, mode='lines+markers'),
        secondary_y=True,
    )
    
    # 设置标题和轴标签
    fig.update_xaxes(title_text=x_column)
    fig.update_yaxes(title_text=bar_column, secondary_y=False)
    fig.update_yaxes(title_text=line_column, secondary_y=True)
    
    fig.update_layout(
        title_text=f"组合图表: {bar_column} (柱状图) & {line_column} (折线图)",
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== 3D图表 ====================
elif chart_type == "📊 3D图表" and df is not None:
    st.markdown("## 📊 3D图表")
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_columns) >= 3:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_column = st.selectbox("X轴列", numeric_columns)
        
        with col2:
            y_column = st.selectbox("Y轴列", numeric_columns)
        
        with col3:
            z_column = st.selectbox("Z轴列", numeric_columns)
        
        color_column = st.selectbox("颜色列（可选）", [None] + df.columns.tolist())
        
        if color_column:
            fig = px.scatter_3d(
                df,
                x=x_column,
                y=y_column,
                z=z_column,
                color=color_column,
                title=f"3D散点图: {x_column}, {y_column}, {z_column}"
            )
        else:
            fig = px.scatter_3d(
                df,
                x=x_column,
                y=y_column,
                z=z_column,
                title=f"3D散点图: {x_column}, {y_column}, {z_column}"
            )
        
        fig.update_layout(
            height=600,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ 需要至少3个数值列才能生成3D图表")

# ==================== 示例数据说明 ====================
if chart_type == "📊 示例数据":
    st.markdown("## 📊 示例数据说明")
    
    st.markdown("""
    ### 📋 示例数据包含以下字段：
    - **日期**: 时间序列数据（30天）
    - **销售额**: 模拟的销售数据
    - **访问量**: 模拟的网站访问量
    - **转化率**: 模拟的转化率数据
    - **类别**: 分类数据（A, B, C）
    - **地区**: 地区分类（北京、上海、广州、深圳）
    
    ### 💡 使用建议：
    1. **上传自己的数据**: 点击"上传CSV或Excel文件"按钮上传您的数据
    2. **数据格式要求**: 
       - CSV文件：UTF-8编码，第一行为列名
       - Excel文件：支持.xlsx和.xls格式
    3. **图表类型选择**: 根据数据特点选择合适的图表类型
    4. **交互功能**: 所有图表都支持缩放、平移、悬停查看详情等交互功能
    """)
    
    if df is not None:
        st.markdown("### 📊 当前数据预览")
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 📈 数据统计信息")
        st.dataframe(df.describe(), use_container_width=True)

# 页脚提示
if df is not None:
    st.markdown("---")
    st.info("""
    💡 **提示：** 
    - 所有图表都支持交互操作：缩放、平移、悬停查看详情
    - 可以将鼠标悬停在图表上查看详细数据
    - 使用工具栏可以下载图表为PNG格式
    - 建议根据数据特点选择合适的图表类型
    """)

