#!/bin/bash

# ============================================
# Testing Tools Portal 自动化部署脚本
# ============================================
set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
APP_NAME="Testing Tools Portal"
APP_PORT=8501
LOG_DIR="${PROJECT_DIR}/logs"
PID_FILE="${PROJECT_DIR}/portal.pid"
LOG_FILE="${LOG_DIR}/deploy.log"
HEALTH_CHECK_URL="http://localhost:${APP_PORT}"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${LOG_FILE}"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "${LOG_FILE}"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "${LOG_FILE}"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "${LOG_FILE}"
}

# 获取Git版本信息
get_git_version() {
    if [ -d "${PROJECT_DIR}/.git" ]; then
        git rev-parse --short HEAD 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# 检查Python环境
check_python() {
    log "检查Python环境..."
    if ! command -v python3 &> /dev/null; then
        log_error "未检测到Python3，请先安装Python3"
        exit 1
    fi
    PYTHON_VERSION=$(python3 --version)
    log_success "Python版本: ${PYTHON_VERSION}"
}

# 停止旧服务
stop_service() {
    log "停止旧服务..."
    
    if [ -f "${PID_FILE}" ]; then
        OLD_PID=$(cat "${PID_FILE}")
        if ps -p "${OLD_PID}" > /dev/null 2>&1; then
            log "找到运行中的进程 PID: ${OLD_PID}"
            kill "${OLD_PID}" || true
            sleep 2
            
            # 如果进程仍在运行，强制杀死
            if ps -p "${OLD_PID}" > /dev/null 2>&1; then
                log_warning "进程仍在运行，强制终止..."
                kill -9 "${OLD_PID}" || true
                sleep 1
            fi
        fi
        rm -f "${PID_FILE}"
    fi
    
    # 查找并停止所有streamlit进程（针对此项目）
    STREAMLIT_PIDS=$(ps aux | grep "[s]treamlit run Home.py" | awk '{print $2}' || true)
    if [ ! -z "${STREAMLIT_PIDS}" ]; then
        log "发现Streamlit进程，正在停止..."
        echo "${STREAMLIT_PIDS}" | xargs kill || true
        sleep 2
        echo "${STREAMLIT_PIDS}" | xargs kill -9 || true
    fi
    
    # 检查端口占用
    PORT_PID=$(lsof -ti:${APP_PORT} 2>/dev/null || true)
    if [ ! -z "${PORT_PID}" ]; then
        log "端口 ${APP_PORT} 被占用，正在释放..."
        kill "${PORT_PID}" || true
        sleep 1
    fi
    
    log_success "旧服务已停止"
}

# 创建/激活虚拟环境
setup_venv() {
    log "设置虚拟环境..."
    
    if [ ! -d "${PROJECT_DIR}/venv" ]; then
        log "创建虚拟环境..."
        python3 -m venv "${PROJECT_DIR}/venv"
        log_success "虚拟环境创建成功"
    fi
    
    # 激活虚拟环境
    source "${PROJECT_DIR}/venv/bin/activate"
    log_success "虚拟环境已激活"
    
    # 升级pip
    log "升级pip..."
    pip install --upgrade pip --quiet
    
    # 安装依赖
    log "安装依赖包..."
    pip install -r "${PROJECT_DIR}/requirements.txt" 
    log_success "依赖包安装完成"
}

# 启动服务
start_service() {
    log "启动服务..."
    
    # 确保虚拟环境已激活
    source "${PROJECT_DIR}/venv/bin/activate"
    
    # 创建日志文件
    APP_LOG="${LOG_DIR}/app_$(date '+%Y%m%d_%H%M%S').log"
    
    # 使用nohup启动服务，并确保在后台持续运行
    cd "${PROJECT_DIR}"
    
    # 设置环境变量，确保Streamlit在后台运行
    export STREAMLIT_SERVER_HEADLESS=true
    export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    export PYTHONUNBUFFERED=1
    
    # 使用nohup直接启动Streamlit，并重定向所有输出
    nohup streamlit run Home.py \
        --server.port=${APP_PORT} \
        --server.address=0.0.0.0 \
        --server.headless=true \
        --server.enableCORS=false \
        --server.enableXsrfProtection=false \
        > "${APP_LOG}" 2>&1 &
    
    APP_PID=$!
    echo "${APP_PID}" > "${PID_FILE}"
    
    log_success "服务已启动，PID: ${APP_PID}"
    log "日志文件: ${APP_LOG}"
    
    # 等待服务启动，并验证进程是否仍在运行
    sleep 5
    
    # 验证进程是否仍在运行
    if ! ps -p "${APP_PID}" > /dev/null 2>&1; then
        log_error "服务进程已退出，请检查日志: ${APP_LOG}"
        log "最近20行日志:"
        tail -20 "${APP_LOG}" || true
        return 1
    fi
    
    # 检查是否有streamlit子进程
    STREAMLIT_CHILD=$(pgrep -P "${APP_PID}" | head -1 || true)
    if [ ! -z "${STREAMLIT_CHILD}" ]; then
        log_success "Streamlit子进程运行正常 (PID: ${STREAMLIT_CHILD})"
    fi
    
    log_success "服务进程运行正常"
}

# 健康检查
health_check() {
    log "执行健康检查..."
    
    MAX_RETRIES=10
    RETRY_INTERVAL=3
    
    for i in $(seq 1 ${MAX_RETRIES}); do
        if curl -s -f "${HEALTH_CHECK_URL}" > /dev/null 2>&1; then
            log_success "健康检查通过！服务运行正常"
            return 0
        fi
        
        if [ ${i} -lt ${MAX_RETRIES} ]; then
            log "健康检查失败，${RETRY_INTERVAL}秒后重试 (${i}/${MAX_RETRIES})..."
            sleep ${RETRY_INTERVAL}
        fi
    done
    
    log_error "健康检查失败，服务可能未正常启动"
    return 1
}

# 主函数
main() {
    log "=========================================="
    log "开始部署 ${APP_NAME}"
    log "=========================================="
    log "项目目录: ${PROJECT_DIR}"
    log "Git版本: $(get_git_version)"
    log "=========================================="
    
    # 执行部署步骤
    check_python || exit 1
    stop_service || exit 1
    setup_venv || exit 1
    start_service || exit 1
    
    # 健康检查
    if health_check; then
        log_success "=========================================="
        log_success "部署成功！"
        log_success "服务地址: ${HEALTH_CHECK_URL}"
        log_success "=========================================="
        exit 0
    else
        log_error "健康检查失败，部署未成功"
        exit 1
    fi
}

# 执行主函数
main "$@"

