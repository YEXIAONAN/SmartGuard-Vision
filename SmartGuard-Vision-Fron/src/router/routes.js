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
      {
        path: 'rules',
        name: 'rules',
        component: () => import('../views/system/RuleCenterView.vue'),
        meta: {
          title: '规则中心',
          requiresAuth: true,
          roles: ['admin', 'operator'],
        },
      },
      {
        path: 'audit',
        name: 'audit',
        component: () => import('../views/system/AuditCenterView.vue'),
        meta: {
          title: '审计中心',
          requiresAuth: true,
          roles: ['admin'],
        },
      },
    ],
  },
]
