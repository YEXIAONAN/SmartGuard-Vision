import MainLayout from '../layouts/MainLayout.vue'

export const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('../views/dashboard/DashboardView.vue'),
        meta: {
          title: '首页总览',
        },
      },
      {
        path: 'vision-history',
        name: 'vision-history',
        component: () => import('../views/history/VisionHistoryView.vue'),
        meta: {
          title: '视觉历史',
        },
      },
      {
        path: 'sensor-history',
        name: 'sensor-history',
        component: () => import('../views/history/SensorHistoryView.vue'),
        meta: {
          title: '传感历史',
        },
      },
    ],
  },
]
