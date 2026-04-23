# 智感护航前端（SmartGuard-Vision-Fron）

本目录为智感护航系统前端工程，负责首页态势、设备网格、风险详情、告警列表、视觉历史、传感历史、规则中心、审计中心等页面展示与交互联动。

## 技术栈

- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- Element Plus
- ECharts
- Axios
- SCSS

## 前端能力概览

- Apple 风格玻璃态页面框架（统一头部、导航、卡片）
- 首页 Dashboard 实时态势与图表展示
- 告警列表与风险详情联动
- 设备网格高亮联动
- 历史页面服务端分页与多条件筛选
- 规则中心与审计中心
- 登录态管理与 401 自动跳转登录
- 顶部刷新与退出登录

## 目录结构

```text
SmartGuard-Vision-Fron/
├─ src/
│  ├─ api/                       # API 封装
│  ├─ components/
│  │  ├─ common/                 # 通用组件
│  │  └─ dashboard/              # 首页与壳层组件
│  ├─ constants/                 # 常量（导航等）
│  ├─ router/                    # 路由与守卫
│  ├─ stores/                    # Pinia 状态管理
│  ├─ styles/                    # 全局样式
│  ├─ types/                     # TS 类型定义
│  └─ views/                     # 页面视图
├─ vite.config.js
└─ package.json
```

## 运行方式

在 `SmartGuard-Vision-Fron` 目录下执行：

```bash
npm install
npm run dev
```

默认访问地址：`http://127.0.0.1:5173`

## 与后端联调要求

前端依赖根项目后端服务（默认 `http://127.0.0.1:8000`），请先启动后端再启动前端。  
当前 Vite 代理已配置：

- `/api` -> `http://127.0.0.1:8000`
- `/health` -> `http://127.0.0.1:8000`

如后端端口变化，请同步修改 `vite.config.js`。

## 常用脚本

```bash
npm run dev       # 本地开发
npm run build     # 生产构建
npm run preview   # 构建产物预览
npm run test      # 单元测试
```

## 登录与权限说明

- 登录成功后会写入本地 `sg_access_token / sg_refresh_token / sg_current_user`
- 路由守卫控制未登录访问
- 接口 `401` 会自动清理会话并跳转 `/login`

## 页面路由

- `/` 首页总览
- `/vision-history` 视频历史
- `/sensor-history` 传感历史
- `/rules` 规则中心
- `/audit` 审计中心
- `/login` 登录页

## 开发规范建议

- 所有接口请求统一走 `src/utils/request.ts`
- 页面统一放入 `AppShell`，保持头部和导航样式一致
- 新增页面时同步更新 `src/constants/navigation.ts`
- 保持 TS 类型与后端响应结构一致，避免隐式 any

## 许可与使用限制

前端代码遵循仓库根目录 LICENSE（Proprietary / All Rights Reserved），请勿在未授权情况下复制、分发或二次利用。
