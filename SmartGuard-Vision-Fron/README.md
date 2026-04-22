# SmartGuard-Vision-Fron

SmartGuard Vision 的前端监控大屏，基于 `Vue 3 + Vite + Pinia + Element Plus + ECharts` 构建。

## 开发环境

```bash
npm install
npm run dev
```

默认通过 Vite 代理将以下请求转发到后端 `http://127.0.0.1:8000`：

* `/health`
* `/api/dashboard/overview`
* `/api/alerts/:id/status`

## 生产构建

```bash
npm run build
```

## 当前能力

* 实时展示设备在线状态、风险等级分布、区域风险排序和近 7 天告警趋势
* 展示停放识别、充电状态、温升异常等监测信息
* 支持在大屏上直接完成告警状态流转
