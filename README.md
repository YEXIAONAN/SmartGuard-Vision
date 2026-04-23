# 智感护航（SmartGuard-Vision）

智感护航是一个面向电动自行车停放与充电场景的多模态安全感知与联动处置系统，覆盖“风险发现、告警分级、处置流转、审计留痕、历史追溯”的完整闭环。  
项目由 **FastAPI 后端** 与 **Vue 3 前端** 两部分组成，适用于校园、社区、园区、地下车库、集中充电区等安全治理场景。

## 项目要解决的痛点

- 监测数据分散：视觉识别、传感器上报、设备状态分散在不同系统，无法统一查看。
- 告警处置断层：告警触发后缺少标准化处置流转，处理人、备注、时间不可追踪。
- 风险判断滞后：缺乏首页态势汇总与趋势分析，值班人员难以快速定位高风险事件。
- 追责依据不足：缺少审计日志与处置操作记录，无法形成可核查的过程证据。

## 核心能力

- 多角色登录认证（admin / operator / viewer）与会话管理（access/refresh token）
- 首页态势总览（在线设备、告警统计、高风险事件、SLA 超时、平均处置时长）
- 告警管理（列表筛选、状态流转、处置审计、CSV 导出）
- 视觉历史与传感历史（服务端分页 + 条件联动筛选 + 详情查看）
- 规则中心（SLA 与阈值可配置）
- 审计中心（关键操作留痕）
- 前端自动轮询刷新，风险详情与设备高亮联动

## 技术架构

- 后端：FastAPI、SQLAlchemy、Alembic、Passlib、JWT
- 前端：Vue 3、Vite、Pinia、Vue Router、Element Plus、ECharts、Axios、TypeScript
- 数据库：默认 SQLite（可扩展 MySQL）

## 项目结构

```text
SmartGuard-Vision/
├─ app/                          # FastAPI 后端
│  ├─ api/routes/                # auth/dashboard/alerts/devices/vision/sensors/rules/audit
│  ├─ core/                      # 配置、数据库、鉴权基础能力
│  ├─ models/                    # 数据模型
│  ├─ schemas/                   # Pydantic Schema
│  └─ services/                  # 业务服务层
├─ SmartGuard-Vision-Fron/       # Vue 前端
│  └─ src/
├─ alembic/                      # 数据库迁移
├─ tests/                        # 后端测试
├─ docker/                       # Dockerfile
├─ docker-compose.yml
├─ start-all.bat
├─ start-all.ps1
└─ start-all.sh
```

## 快速启动

### 1) 环境要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Node.js 20+
- npm 10+

### 2) 启动后端（根目录）

```bash
uv sync --group dev
uv run uvicorn app.main:app --reload
```

后端默认地址：

- API：`http://127.0.0.1:8000`
- 文档：`http://127.0.0.1:8000/docs`

### 3) 启动前端（新终端）

```bash
cd SmartGuard-Vision-Fron
npm install
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

> 前端开发代理默认转发到 `http://127.0.0.1:8000`。

## 一键启动脚本

- Windows CMD：`start-all.bat`
- Windows PowerShell：`start-all.ps1`
- macOS/Linux：`start-all.sh`

## Docker 启动

```bash
docker compose up --build
docker compose down
```

## 默认账号

- 管理员：`admin / admin123`
- 值班员：`operator / operator123`
- 只读用户：`viewer / viewer123`

## 常用后端接口

- `GET /health`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/dashboard/overview`
- `GET /api/devices`
- `GET /api/alerts`
- `PATCH /api/alerts/{alert_id}/status`
- `GET /api/vision`
- `GET /api/sensors`
- `GET /api/rules`
- `GET /api/audit`

## 测试与构建

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

## 使用限制（重要）

**本项目未经允许，禁止将其二次开发，用作展示项目，即使是非盈利活动展示也不允许。**

## 许可证

本项目采用仓库根目录下的 [`LICENSE`](./LICENSE)（`Proprietary / All Rights Reserved`）授权条款。
