# 智感护航（SmartGuard-Vision）

面向电动自行车停放与充电场景的多模态安全感知与联动处置平台。  
技术栈：`FastAPI + SQLAlchemy + Vue 3 + Vite + Element Plus + ECharts`

## 1. 已完成的高价值优化

### 1.1 认证与权限（RBAC + 安全加固）

- 用户登录：`POST /api/auth/login`
- Token 刷新：`POST /api/auth/refresh`
- 退出登录：`POST /api/auth/logout`
- 当前用户：`GET /api/auth/me`
- 角色模型：`admin / operator / viewer`
- 安全机制：
  - bcrypt 密码哈希
  - JWT 访问令牌（含 jti）
  - 刷新令牌持久化与轮换
  - 访问令牌撤销表（logout 后失效）
  - 登录失败限流与短时锁定

### 1.2 数据与流程能力增强

- 历史页：服务端分页 + 条件联动筛选
- 告警处置：必填校验 + 审计时间线闭环
- SLA 能力：
  - 告警 `sla_due_at` 字段
  - 超时扫描与自动升级
  - 首页展示 `SLA超时数 / 平均响应时长 / 平均处置时长`
- 告警导出：`GET /api/alerts/export/csv`

### 1.3 规则配置中心

- 规则读取：`GET /api/rules`
- 规则更新：`PUT /api/rules/{rule_key}`
- 默认规则：
  - `alert_sla_minutes`
  - `sensor_temp_threshold`
  - `sensor_smoke_threshold`

### 1.4 审计中心

- 审计日志查询：`GET /api/audit`
- 目前覆盖：
  - 登录/退出
  - 告警状态更新
  - SLA 扫描
  - 规则更新
  - 数据导出

### 1.5 前端优化

- 乱码清理与 UTF-8 文案统一
- 登录态接入 refresh token 自动续签
- 路由守卫（未登录拦截 + 角色路由限制）
- 首页补“导出告警 CSV / SLA 扫描”操作
- 新增页面：
  - 规则中心 `/rules`
  - 审计中心 `/audit`
- 性能优化：
  - Vite `manualChunks` 拆分（vue / element-plus / echarts）
  - 历史页筛选请求防抖与并发覆盖保护

## 2. 默认账号

- 管理员：`admin / admin123`
- 值班员：`operator / operator123`
- 只读用户：`viewer / viewer123`

## 3. 项目结构

```text
SmartGuard-Vision/
├─ app/
│  ├─ api/routes/                # auth/alerts/dashboard/devices/vision/sensors/rules/audit
│  ├─ core/                      # config/database/security
│  ├─ models/                    # 业务模型 + auth token + audit + rule
│  ├─ schemas/                   # pydantic schema
│  └─ services/                  # 业务逻辑
├─ SmartGuard-Vision-Fron/
│  └─ src/
│     ├─ views/auth              # 登录页
│     ├─ views/dashboard         # 首页
│     ├─ views/history           # 视觉/传感历史
│     └─ views/system            # 规则中心/审计中心
├─ tests/                        # 后端测试
├─ .github/workflows/ci.yml      # CI
└─ alembic/                      # 迁移脚手架
```

## 4. 本地启动

### 4.1 环境要求

- Python 3.11+
- `uv`
- Node.js 20+

### 4.2 后端

```bash
uv sync --group dev
uv run uvicorn app.main:app --reload
```

### 4.3 前端

```bash
cd SmartGuard-Vision-Fron
npm install
npm run dev
```

默认访问：

- 前端：`http://127.0.0.1:5173`
- 后端：`http://127.0.0.1:8000`
- Swagger：`http://127.0.0.1:8000/docs`

## 5. 一键脚本与 Docker

- Windows CMD：`start-all.bat`
- Windows PowerShell：`start-all.ps1`
- macOS/Linux：`start-all.sh`

```bash
docker compose up --build
docker compose down
```

## 6. 测试与质量

### 后端测试

```bash
uv run pytest -q
```

### 前端测试与构建

```bash
cd SmartGuard-Vision-Fron
npm run test
npm run build
```

### CI

- GitHub Actions 自动执行：
  - 后端测试
  - 前端测试
  - 前端构建

## 7. 数据库迁移（Alembic）

首次可用命令：

```bash
uv run alembic upgrade head
```

新增迁移：

```bash
uv run alembic revision --autogenerate -m "your message"
uv run alembic upgrade head
```

## 8. 许可说明

未经授权，禁止将本项目用于竞赛提交或商业用途。
