import streamlit as st

st.set_page_config(
    page_title="BA工具集",
    page_icon="📊",
    layout="wide"
)

st.title("📊 BA（业务分析）工具集")
st.markdown("---")

st.markdown("""
### 💼 功能介绍
BA工具集为业务分析师提供全方位的文档生成和流程设计工具，
帮助您高效完成从需求分析到文档输出的全流程工作。
""")

# 侧边栏工具选择（子菜单效果）
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 工具选择")
tool_option = st.sidebar.radio(
    "选择BA工具",
    ["📄 BRD生成FSD", "🔄 BRD转流程图", "📝 Meeting Minutes"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

st.markdown("---")

# ==================== BRD生成FSD ====================
if tool_option == "📄 BRD生成FSD":
    st.markdown("## 📄 根据BRD生成FSD")
    
    st.info("""
    **功能说明：** 根据业务需求文档（BRD - Business Requirements Document）自动生成
    功能规格说明书（FSD - Functional Specification Document）
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 输入BRD内容")
        
        brd_input = st.text_area(
            "请输入或粘贴BRD内容",
            height=300,
            placeholder="""示例BRD内容：

项目名称：用户管理系统
业务背景：
随着公司业务发展，需要一个统一的用户管理系统来管理所有用户信息...

业务目标：
1. 提供用户注册和登录功能
2. 支持用户信息的增删改查
3. 实现用户权限管理
...
            """
        )
        
        # 高级选项
        with st.expander("⚙️ 高级选项"):
            include_api = st.checkbox("包含API设计", value=True)
            include_db = st.checkbox("包含数据库设计", value=True)
            include_ui = st.checkbox("包含UI设计说明", value=False)
            detail_level = st.select_slider(
                "详细程度",
                options=["简要", "标准", "详细"],
                value="标准"
            )
    
    with col2:
        st.markdown("### 📋 生成步骤")
        st.markdown("""
        1. **分析BRD** - 提取关键业务需求
        2. **识别功能点** - 拆分功能模块
        3. **定义接口** - 设计API和数据结构
        4. **生成文档** - 输出结构化FSD
        """)
        
        if st.button("🚀 生成FSD", type="primary", use_container_width=True):
            if brd_input:
                with st.spinner("正在生成FSD..."):
                    # 这里应该调用实际的生成逻辑
                    st.success("✅ FSD生成成功！")
            else:
                st.warning("⚠️ 请先输入BRD内容")
    
    # FSD模版示例
    st.markdown("---")
    st.markdown("### 📖 FSD模版示例")
    
    with st.expander("查看完整的FSD模版", expanded=False):
        st.code("""
功能规格说明书（FSD）
========================

1. 文档信息
-----------
项目名称：用户管理系统
文档版本：v1.0
创建日期：2025-10-28
创建人：BA Team

2. 功能概述
-----------
本系统提供完整的用户管理功能，包括用户注册、登录、信息管理和权限控制。

3. 功能详细说明
---------------

3.1 用户注册功能
描述：新用户通过填写注册表单创建账号
输入：
  - 用户名（必填，唯一）
  - 邮箱（必填，唯一）
  - 密码（必填，8-20位，包含字母和数字）
  - 手机号（选填）
  
处理逻辑：
  1. 验证输入格式
  2. 检查用户名和邮箱唯一性
  3. 密码加密存储
  4. 发送验证邮件
  5. 创建用户记录
  
输出：
  - 成功：返回用户ID和注册成功消息
  - 失败：返回错误代码和错误信息

3.2 用户登录功能
描述：已注册用户通过用户名/邮箱和密码登录系统
输入：
  - 用户名/邮箱
  - 密码
  
处理逻辑：
  1. 验证用户是否存在
  2. 验证密码是否正确
  3. 检查账户状态
  4. 生成JWT token
  5. 记录登录日志
  
输出：
  - 成功：返回JWT token和用户基本信息
  - 失败：返回错误信息

4. API接口设计
--------------

4.1 用户注册接口
POST /api/v1/users/register
Request Body:
{
  "username": "string",
  "email": "string",
  "password": "string",
  "phone": "string"
}

Response (200):
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "userId": "12345",
    "username": "testuser"
  }
}

5. 数据库设计
-------------

5.1 用户表 (users)
字段：
  - id: BIGINT, 主键, 自增
  - username: VARCHAR(50), 唯一, 非空
  - email: VARCHAR(100), 唯一, 非空
  - password_hash: VARCHAR(255), 非空
  - phone: VARCHAR(20), 可空
  - status: TINYINT, 默认1（1-正常，0-禁用）
  - created_at: TIMESTAMP, 默认当前时间
  - updated_at: TIMESTAMP, 自动更新

索引：
  - PRIMARY KEY (id)
  - UNIQUE INDEX idx_username (username)
  - UNIQUE INDEX idx_email (email)

6. 非功能性需求
---------------
- 性能：注册接口响应时间 < 1秒
- 安全：密码使用bcrypt加密，强度10
- 可用性：系统可用性 > 99.9%
- 扩展性：支持水平扩展

7. 验收标准
-----------
1. 用户可以成功注册账号
2. 注册信息验证符合规则
3. 密码安全加密存储
4. 邮箱验证流程正常
5. 所有API返回格式统一
        """, language="text")
    
    # 注意事项
    st.markdown("### ⚠️ 注意事项")
    st.warning("""
    1. **完整性**：确保BRD包含所有必要的业务信息
    2. **清晰性**：使用明确的业务术语，避免歧义
    3. **可追溯性**：每个功能点都应能追溯到BRD的业务需求
    4. **一致性**：保持术语和命名的一致性
    5. **Review**：生成后需要进行人工review和完善
    """)

# ==================== BRD转流程图 ====================
elif tool_option == "🔄 BRD转流程图":
    st.markdown("## 🔄 BRD转流程图")
    
    st.info("""
    **功能说明：** 根据BRD文档自动生成业务流程图，直观展示业务流程和决策逻辑
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 输入业务流程描述")
        
        process_input = st.text_area(
            "请描述业务流程",
            height=250,
            placeholder="""示例：
用户登录流程：
1. 用户打开登录页面
2. 输入用户名和密码
3. 系统验证用户名是否存在
4. 如果不存在，提示"用户不存在"
5. 如果存在，验证密码是否正确
6. 如果密码错误，提示"密码错误"
7. 如果密码正确，生成token并跳转到首页
            """
        )
        
        flowchart_type = st.selectbox(
            "流程图类型",
            ["标准流程图", "泳道图", "活动图", "数据流图"]
        )
        
        if st.button("🎨 生成流程图", type="primary"):
            if process_input:
                with st.spinner("正在生成流程图..."):
                    st.success("✅ 流程图生成成功！")
                    # 这里应该显示实际生成的流程图
                    st.info("💡 流程图将以Mermaid或PlantUML格式生成，可导出为图片")
            else:
                st.warning("⚠️ 请先输入业务流程描述")
    
    with col2:
        st.markdown("### 🎨 流程图元素")
        st.markdown("""
        **基本元素：**
        - 🟢 开始/结束
        - 📦 处理步骤
        - 💎 判断/分支
        - 📄 数据/文档
        - ➡️ 流程方向
        
        **高级元素：**
        - 🏊 泳道（表示不同角色）
        - 🔄 循环
        - ⏸️ 等待
        - 📡 外部系统交互
        """)
    
    # 流程图示例
    st.markdown("---")
    st.markdown("### 📊 流程图示例 (Mermaid)")
    
    tab1, tab2 = st.tabs(["登录流程", "订单处理流程"])
    
    with tab1:
        st.code("""
graph TD
    A[开始] --> B[打开登录页面]
    B --> C[输入用户名和密码]
    C --> D{用户是否存在?}
    D -->|否| E[提示:用户不存在]
    E --> C
    D -->|是| F{密码是否正确?}
    F -->|否| G[提示:密码错误]
    G --> C
    F -->|是| H[生成JWT Token]
    H --> I[跳转到首页]
    I --> J[结束]
        """, language="mermaid")
    
    with tab2:
        st.code("""
graph TD
    A[开始] --> B[用户提交订单]
    B --> C{库存是否充足?}
    C -->|否| D[提示库存不足]
    D --> Z[结束]
    C -->|是| E[锁定库存]
    E --> F[创建订单]
    F --> G[调用支付接口]
    G --> H{支付是否成功?}
    H -->|否| I[释放库存]
    I --> J[订单状态:已取消]
    J --> Z
    H -->|是| K[扣减库存]
    K --> L[订单状态:已支付]
    L --> M[发送通知]
    M --> Z
        """, language="mermaid")
    
    # 转换注意事项
    st.markdown("---")
    st.markdown("### 📌 转换过程注意事项")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ✅ 应该做的：
        - 清晰标识每个决策点
        - 标注所有可能的分支路径
        - 使用统一的命名规范
        - 标注异常处理流程
        - 区分正常流程和异常流程
        """)
    
    with col2:
        st.markdown("""
        #### ❌ 避免做的：
        - 流程图过于复杂，难以理解
        - 遗漏重要的决策节点
        - 循环引用导致死循环
        - 缺少开始和结束节点
        - 流程方向混乱
        """)

# ==================== Meeting Minutes ====================
else:  # Meeting Minutes
    st.markdown("## 📝 Meeting Minutes（会议纪要）")
    
    st.info("""
    **功能说明：** 使用标准化模版记录会议内容，确保会议记录的有效性和一致性
    """)
    
    # 会议基本信息
    st.markdown("### 📋 会议基本信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        meeting_title = st.text_input("会议主题", placeholder="例：用户管理系统需求评审会")
    
    with col2:
        meeting_date = st.date_input("会议日期")
    
    with col3:
        meeting_time = st.text_input("会议时间", placeholder="例：14:00-16:00")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meeting_location = st.text_input("会议地点", placeholder="例：会议室A / Zoom")
    
    with col2:
        meeting_host = st.text_input("会议主持人")
    
    # 参会人员
    st.markdown("### 👥 参会人员")
    
    col1, col2 = st.columns(2)
    
    with col1:
        attendees = st.text_area(
            "参会人员（每行一个）",
            height=100,
            placeholder="张三 - 产品经理\n李四 - 技术负责人\n王五 - BA"
        )
    
    with col2:
        absentees = st.text_area(
            "缺席人员（每行一个）",
            height=100,
            placeholder="赵六 - 测试负责人"
        )
    
    # 会议内容
    st.markdown("### 📝 会议内容")
    
    tab1, tab2, tab3, tab4 = st.tabs(["会议议程", "讨论内容", "决策事项", "行动计划"])
    
    with tab1:
        agenda = st.text_area(
            "会议议程",
            height=200,
            placeholder="""1. 需求介绍（10分钟）
2. 技术方案讨论（30分钟）
3. 风险评估（20分钟）
4. 时间安排确认（10分钟）
5. 其他事项（10分钟）"""
        )
    
    with tab2:
        discussion = st.text_area(
            "讨论内容",
            height=200,
            placeholder="""主题1：用户登录功能
- 讨论点1：是否支持第三方登录
- 讨论点2：密码强度要求
- 结论：先实现基础登录，第三方登录纳入二期

主题2：数据库设计
- 讨论点1：用户表结构设计
- 结论：采用MySQL，添加软删除字段"""
        )
    
    with tab3:
        decisions = st.text_area(
            "决策事项",
            height=200,
            placeholder="""1. 【已决策】采用JWT作为认证方式 - 决策人：技术负责人
2. 【已决策】密码使用bcrypt加密 - 决策人：安全团队
3. 【待决策】是否需要图形验证码 - 决策人：产品经理"""
        )
    
    with tab4:
        action_items = st.text_area(
            "行动计划",
            height=200,
            placeholder="""1. 完成详细设计文档 - 负责人：张三 - 截止日期：2025-11-05
2. 搭建开发环境 - 负责人：李四 - 截止日期：2025-11-03
3. 准备测试用例 - 负责人：王五 - 截止日期：2025-11-10"""
        )
    
    # 其他信息
    st.markdown("### 📌 其他信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risks = st.text_area(
            "风险与问题",
            height=100,
            placeholder="1. 第三方接口可能不稳定\n2. 开发时间较紧"
        )
    
    with col2:
        next_meeting = st.text_area(
            "下次会议安排",
            height=100,
            placeholder="时间：2025-11-05 14:00\n地点：会议室B\n议题：技术方案终审"
        )
    
    # 生成按钮
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📄 生成Word文档", use_container_width=True):
            st.success("✅ Word文档生成成功！")
    
    with col2:
        if st.button("📧 发送邮件", use_container_width=True):
            st.success("✅ 会议纪要已发送给所有参会人员！")
    
    with col3:
        if st.button("💾 保存草稿", use_container_width=True):
            st.info("💾 草稿已保存")
    
    # Meeting Minutes模版
    st.markdown("---")
    st.markdown("### 📖 会议纪要标准模版")
    
    with st.expander("查看完整模版"):
        st.code("""
会议纪要
========================================

一、会议基本信息
----------------------------------------
会议主题：用户管理系统需求评审会
会议日期：2025-10-28
会议时间：14:00-16:00
会议地点：会议室A
会议主持人：张三
记录人：李四

二、参会人员
----------------------------------------
参会人员：
- 张三 - 产品经理
- 李四 - 技术负责人
- 王五 - BA
- 赵六 - 前端工程师
- 孙七 - 后端工程师

缺席人员：
- 周八 - 测试负责人（请假）

三、会议议程
----------------------------------------
1. 需求介绍（10分钟）
2. 技术方案讨论（30分钟）
3. 风险评估（20分钟）
4. 时间安排确认（10分钟）
5. 其他事项（10分钟）

四、讨论内容
----------------------------------------

主题1：用户登录功能
讨论要点：
- 是否支持第三方登录（微信、支付宝）
- 密码强度要求的具体规则
- 验证码的必要性

结论：
- 一期只实现基础登录功能
- 密码要求：8-20位，必须包含字母和数字
- 暂不实现验证码，根据后期使用情况决定

主题2：数据库设计
讨论要点：
- 用户表的字段设计
- 是否需要单独的登录日志表

结论：
- 采用MySQL数据库
- 用户表包含：id, username, email, password, status等
- 新建login_log表记录登录历史

五、决策事项
----------------------------------------
[已决策] 采用JWT作为认证方式
- 决策人：李四（技术负责人）
- 理由：无状态，便于扩展

[已决策] 密码使用bcrypt加密
- 决策人：安全团队
- 理由：行业标准，安全性高

[待决策] 是否需要图形验证码
- 决策人：张三（产品经理）
- 预计决策时间：2025-11-01

六、行动计划
----------------------------------------
序号 | 任务内容 | 负责人 | 截止日期 | 状态
-----|----------|--------|----------|------
1 | 完成详细设计文档 | 王五 | 2025-11-05 | 进行中
2 | 搭建开发环境 | 李四 | 2025-11-03 | 未开始
3 | 完成数据库设计 | 孙七 | 2025-11-04 | 未开始
4 | 准备测试用例 | 周八 | 2025-11-10 | 未开始

七、风险与问题
----------------------------------------
1. 风险：第三方接口稳定性未知
   缓解措施：提前进行技术调研和压测

2. 问题：开发时间较紧，可能无法如期完成
   解决方案：适当调整需求优先级，增加资源投入

八、下次会议安排
----------------------------------------
时间：2025-11-05 14:00-15:00
地点：会议室B
议题：技术方案终审
参会人员：全体项目成员

九、附件
----------------------------------------
1. 需求文档 v1.0
2. 原型设计图
3. 技术方案PPT

========================================
记录人：李四
审核人：张三
分发：全体参会人员
日期：2025-10-28
        """, language="text")
    
    # Guideline说明
    st.markdown("---")
    st.markdown("### 📚 Meeting Minutes Guideline")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ✍️ 记录原则：
        1. **及时性**：会议当天或次日完成
        2. **准确性**：如实记录讨论内容和决策
        3. **完整性**：包含所有必要信息
        4. **客观性**：避免主观评价和猜测
        5. **可追溯**：明确任务和责任人
        """)
    
    with col2:
        st.markdown("""
        #### 📋 必须包含的内容：
        - 会议基本信息（时间、地点、人员）
        - 会议讨论的主要内容
        - 形成的决策事项
        - 明确的行动计划（人、事、时）
        - 下次会议安排（如有）
        """)

# 页脚提示
st.markdown("---")
st.info("""
💡 **提示：** 
- BA工具集旨在标准化业务分析工作流程，提高文档质量和团队协作效率
- 建议定期review和更新生成的文档，确保与实际情况保持一致
- 可以根据项目特点定制模版，建立适合团队的最佳实践
""")

