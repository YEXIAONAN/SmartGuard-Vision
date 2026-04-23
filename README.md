# 智感护航（SmartGuard-Vision）

面向电动自行车停放与充电场景的多模态安全感知与联动处置平台。  
项目由 `FastAPI` 后端与 `Vue 3 + Vite + Element Plus + ECharts` 前端组成，支持风险识别、实时告警、联动处置、历史查询与统计分析。

## 1. 项目结构

```text
SmartGuard-Vision/
├─ app/                              # 后端工程
│  ├─ api/                           # 路由层
│  ├─ core/                          # 配置与数据库初始化
│  ├─ models/                        # SQLAlchemy 模型
│  ├─ schemas/                       # Pydantic 模型
│  ├─ services/                      # 业务逻辑
│  └─ main.py                        # FastAPI 入口
├─ SmartGuard-Vision-Fron/           # 前端工程（Vue 3 + Vite）
├─ docker/                           # Docker 构建文件
├─ docker-compose.yml                # 容器编排
├─ start-all.bat                     # Windows CMD 一键启动
├─ start-all.ps1                     # Windows PowerShell 一键启动
├─ start-all.sh                      # macOS / Linux 一键启动
├─ pyproject.toml
├─ uv.lock
└─ smartguard_vision.db
```

## 2. 当前已实现功能

### 2.1 后端 API

- 健康检查：`GET /health`
- 首页总览：`GET /api/dashboard/overview`
- 告警列表：`GET /api/alerts`
- 告警状态更新：`PATCH /api/alerts/{alert_id}/status`
- 告警处置审计记录：`GET /api/alerts/{alert_id}/actions`
- 视觉上报：`POST /api/vision/report`
- 视觉历史分页与详情：`GET /api/vision`、`GET /api/vision/{id}`
- 视觉筛选联动选项：`GET /api/vision/filter-options`
- 传感上报：`POST /api/sensors/report`
- 传感历史分页与详情：`GET /api/sensors`、`GET /api/sensors/{id}`
- 传感筛选联动选项：`GET /api/sensors/filter-options`

### 2.2 业务能力

- 视觉与传感数据入库
- 风险事件自动触发告警（低/中/高风险）
- 首页态势聚合（风险分布、趋势、区域排行、设备在线状态、实时监测快照）
- 联动处置字段完整化：
  - `handled_by`（处理人）
  - `handling_note`（处理备注）
  - `handled_at`（处置时间）
- 处置闭环：
  - 前端处置弹窗必填校验
  - 审计日志时间线展示
- 历史记录能力：
  - 服务端分页
  - 条件联动筛选（点位/状态/时间等）

### 2.3 前端能力

- 控制台式顶部导航与系统状态区
- 首页三层布局（态势概览 / 实时风险中心 / 趋势统计）
- 统一状态标签规范（风险等级、处理状态、设备状态）
- 告警列表联动处置（转处理中 / 标记已处理）
- 视觉历史、传感历史的独立列表与详情页

## 3. 建议优先完善功能（新增）

以下是按价值与实施成本排序后的推荐清单。

### P0（优先立即做）

1. 鉴权与权限模型（RBAC）
- 目标：支持管理员、值班员、只读用户
- 最低实现：登录、JWT、接口权限拦截、按钮级权限
- 验收：不同角色看到的菜单与可执行操作不同

2. 告警升级与超时催办
- 目标：告警长时间未处理时自动升级
- 最低实现：增加告警 SLA 字段、定时任务扫描、升级状态流转
- 验收：超时告警自动进入升级状态并记录审计

3. 全量审计中心
- 目标：不仅记录告警处置，还记录关键配置与登录行为
- 最低实现：新增审计表 + 查询接口 + 前端审计页面
- 验收：可按用户、时间、操作类型查询

### P1（高价值增强）

1. 规则配置中心（阈值可配置）
- 目标：支持在后台动态调整温升、烟雾、违规停放等阈值
- 最低实现：规则表 + 配置 API + 缓存刷新机制
- 验收：修改阈值后新事件按新规则触发

2. 消息通知通道
- 目标：支持短信/企业微信/钉钉推送
- 最低实现：通知模板 + 通知策略 + 通道适配器
- 验收：高风险告警可自动触达指定人员

3. 数据导出与值班报表
- 目标：支持按时间段导出 CSV/Excel，生成日报周报
- 最低实现：导出接口 + 异步任务 + 下载记录
- 验收：可导出分页筛选后的数据结果

### P2（可持续建设）

1. 地图态势页（园区/楼栋/点位）
- 目标：直观看到空间分布与风险热力
- 最低实现：点位管理 + 地图组件 + 告警定位
- 验收：点击地图点位可联动打开历史与告警

2. 设备运维模块
- 目标：设备生命周期管理、离线诊断、固件版本追踪
- 最低实现：设备详情、心跳异常告警、维护记录
- 验收：可追溯设备健康状态与维护过程

3. 自动化测试与 CI/CD
- 目标：保证交付质量与迭代速度
- 最低实现：后端接口测试、前端关键页面测试、基础流水线
- 验收：PR 合并前自动通过质量门禁

## 4. 本地开发与启动

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

- 后端 API：`http://127.0.0.1:8000`
- Swagger：`http://127.0.0.1:8000/docs`
- 前端页面：`http://127.0.0.1:5173`

### 4.3 一键启动脚本

- Windows CMD：`start-all.bat`
- Windows PowerShell：`start-all.ps1`
- macOS / Linux：`start-all.sh`

## 5. Docker 启动

启动：

```bash
docker compose up --build
```

访问：

- 前端：`http://127.0.0.1:5173`
- 后端：`http://127.0.0.1:8000`

停止：

```bash
docker compose down
```

## 6. 后续里程碑建议

- 里程碑 A（1~2 周）：RBAC + 告警升级 + 审计中心
- 里程碑 B（2~4 周）：规则配置中心 + 通知通道 + 报表导出
- 里程碑 C（持续）：地图态势 + 运维模块 + 自动化测试体系

## 7. 许可说明

未经授权，禁止将本项目用于竞赛提交或商业用途。
