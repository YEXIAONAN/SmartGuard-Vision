# SmartGuard-Vision

智感护航 — 面向停充场景的多模态安全感知平台。

本项目聚焦电动自行车在**停放与充电场景**中的安全管理问题，结合**视觉识别、多模态感知、异常分析与风险预警**等技术，实现对车辆停放状态、充电状态以及温升异常的智能识别与联动预警。

---

## 项目结构

```text
SmartGuard-Vision/
├── app/                            # 后端源码
│   ├── main.py                     # FastAPI 入口
│   ├── api/                        # 路由层
│   ├── core/                       # 配置层
│   ├── models/                     # 数据模型
│   ├── schemas/                    # 请求/响应模型
│   ├── services/                   # 业务逻辑
│   └── utils/                      # 工具函数
├── SmartGuard-Vision-Fron/         # 前端项目（Vue 3）
├── pyproject.toml                  # Python 项目配置
├── uv.lock                         # uv 锁定文件
├── .gitignore
└── README.md
````

---

## 环境要求

### 后端

* Python 3.11
* uv

### 前端

* Node.js（建议使用 LTS 版本）
* npm

---

## 克隆项目

```bash
git clone <your-repo-url>
cd SmartGuard-Vision
```

---

## 后端启动方式

### 1. 安装 uv

请先在本机安装 `uv`。

### 2. 同步依赖并创建虚拟环境

在项目根目录执行：

```bash
uv sync
```

执行后，`uv` 会根据 `pyproject.toml` 和 `uv.lock` 自动创建本地 `.venv` 环境，并安装项目所需依赖。

### 3. 启动后端服务

```bash
uv run uvicorn app.main:app --reload
```

启动成功后，默认可访问：

* API 服务：[http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc 文档：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 前端启动方式

进入前端目录：

```bash
cd SmartGuard-Vision-Fron
```

安装依赖：

```bash
npm install
```

启动开发环境：

```bash
npm run dev
```

---

## 首次拉取后的完整启动流程

### 终端 1：启动后端

```bash
cd SmartGuard-Vision
uv sync
uv run uvicorn app.main:app --reload
```

### 终端 2：启动前端

```bash
cd SmartGuard-Vision/SmartGuard-Vision-Fron
npm install
npm run dev
```

---

## 创建虚拟环境

```bash
uv sync
```

就可以自动创建自己的虚拟环境并安装依赖。

---


## 常用命令

### 添加后端依赖

```bash
uv add fastapi uvicorn sqlalchemy pymysql
```

### 启动后端

```bash
uv run uvicorn app.main:app --reload
```

### 查看已安装依赖树

```bash
uv tree
```

### 启动前端

```bash
cd smartguard-vision-frontend
npm run dev
```

---

## 开发说明

本项目采用“后端主工程 + 前端子目录”结构：

* 根目录负责后端服务、模型推理、接口设计与数据存储
* `SmartGuard-Vision-Fron/` 负责前端页面、告警展示与可视化大屏

推荐开发顺序：

1. 先完成后端 API 与识别逻辑
2. 再接入前端展示页面
3. 最后联调告警、感知与可视化模块

---

## 后续计划

* 电动自行车停放规范识别
* 充电状态监测
* 温度异常感知
* 风险分级预警
* 平台联动处置
* 可视化监控大屏

目前已补齐：

* 大屏接入后端真实数据，不再依赖前端本地 mock
* 首页总览已聚合设备状态、风险分布、区域风险、停充监测和最近告警
* 告警支持基础处置流转：待处理、处理中、已处理

---

## License

未经允许，任何人禁止使用本项目作为竞赛，商业用途使用。

