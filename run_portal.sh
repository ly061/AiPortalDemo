#!/bin/bash

# Portal启动脚本
# 用于快速启动Testing Tools Portal

echo "=========================================="
echo "   Testing Tools Portal 启动脚本"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未检测到Python3"
    echo "请先安装Python3: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
    echo ""
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 检查Streamlit是否安装
if ! python -c "import streamlit" &> /dev/null; then
    echo "📥 安装依赖包..."
    pip install -r requirements.txt
    echo "✅ 依赖包安装完成"
    echo ""
fi

# 启动Streamlit应用
echo "🚀 启动Portal..."
echo ""
echo "=========================================="
echo "   Portal已启动"
echo "   访问地址: http://localhost:8501"
echo "   按 Ctrl+C 停止服务"
echo "=========================================="
echo ""

streamlit run Home.py

# 脚本结束
echo ""
echo "Portal已停止"

