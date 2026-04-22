# 智感护航（SmartGuard-Vision）

面向电动自行车停放与充电场景的多模态安全感知平台。  
项目由 `FastAPI` 后端和 `Vue 3` 前端组成，支持风险识别、告警联动和历史数据查询。

## 1. 项目结构

```text
SmartGuard-Vision/
├── app/                              # 后端主工程
│   ├── api/                          # 路由层
│   ├── core/                         # 配置与数据库初始化
│   ├── models/                       # SQLAlchemy 模型
│   ├── schemas/                      # Pydantic 模型
│   ├── services/                     # 业务逻辑层
│   └── main.py                       # FastAPI 入口
├── SmartGuard-Vision-Fron/           # 前端工程（Vue 3 + Vite）
├── docker/                           # Docker 构建文件
├── docker-compose.yml                # 一键容器编排
├── start-all.bat                     # Windows CMD 一键启动
├── start-all.ps1                     # Windows PowerShell 一键启动
├── start-all.sh                      # macOS / Linux 一键启动
├── pyproject.toml
├── uv.lock
└── smartguard_vision.db
```

## 2. 后端已实现功能

### 2.1 核心 API 能力

- 健康检查：`GET /health`
- 首页总览：`GET /api/dashboard/overview`
- 告警查询：`GET /api/alerts`
- 告警处置：`PATCH /api/alerts/{alert_id}/status`
- 设备查询：`GET /api/devices`
- 视觉数据上报：`POST /api/vision/report`
- 视觉历史列表/详情：`GET /api/vision`、`GET /api/vision/{id}`
- 传感数据上报：`POST /api/sensors/report`
- 传感历史列表/详情：`GET /api/sensors`、`GET /api/sensors/{id}`

### 2.2 业务逻辑能力

- 视觉与传感数据入库
- 风险事件自动触发告警（含高/中风险判定）
- 首页总览聚合（风险分布、趋势、区域排行、设备在线状态、监测快照）
- 联动处置字段支持：
- `handled_by`（处理人）
- `handling_note`（处理备注）
- `handled_at`（处置时间）
- 启动时自动建表 + 告警字段兼容补列（历史库可平滑升级）
- 启动时自动写入示例数据（空库）

## 3. 仍建议补充的功能

- 鉴权与权限控制（管理员、值班员、只读角色）
- 告警分页与高级筛选（时间范围、来源类型、区域）
- 审计日志（谁在何时做了什么处置）
- 异常检测规则配置化（阈值可后台动态调整）
- 数据导出（CSV/Excel）和报表生成
- 自动化测试（后端接口测试 + 前端组件/路由测试）
- CI/CD 流水线和代码质量门禁

## 4. 本地开发启动

### 4.1 依赖要求

- Python 3.11+
- `uv`
- Node.js 20+
- npm

### 4.2 手动启动

后端：

```bash
uv sync
uv run uvicorn app.main:app --reload
```

前端：

```bash
cd SmartGuard-Vision-Fron
npm install
npm run dev
```

默认地址：

- 后端 API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- 前端页面: `http://127.0.0.1:5173`

## 5. 一键启动脚本

根目录已提供：

- Windows CMD：`start-all.bat`
- Windows PowerShell：`start-all.ps1`
- macOS / Linux：`start-all.sh`

它们会自动拉起前后端开发服务。

## 6. Docker 启动

### 6.1 直接运行

```bash
docker compose up --build
```

容器地址：

- 前端：`http://127.0.0.1:5173`
- 后端：`http://127.0.0.1:8000`

### 6.2 停止

```bash
docker compose down
```

## 7. 许可证

未经允许，禁止将本项目用于竞赛或商业用途。
