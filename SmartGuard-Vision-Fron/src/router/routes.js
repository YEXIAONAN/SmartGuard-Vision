import MainLayout from '../layouts/MainLayout.vue'

export const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: {
      title: '登录',
      guestOnly: true,
    },
  },
  {
    path: '/',
    component: MainLayout,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('../views/dashboard/DashboardView.vue'),
        meta: {
          title: '首页总览',
          requiresAuth: true,
        },
      },
      {
        path: 'vision-history',
        name: 'vision-history',
        component: () => import('../views/history/VisionHistoryView.vue'),
        meta: {
          title: '视觉历史',
          requiresAuth: true,
        },
      },
      {
        path: 'sensor-history',
        name: 'sensor-history',
        component: () => import('../views/history/SensorHistoryView.vue'),
        meta: {
          title: '传感历史',
          requiresAuth: true,
        },
      },
    ],
  },
]
