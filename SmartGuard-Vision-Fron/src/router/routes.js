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
    ],
  },
]
