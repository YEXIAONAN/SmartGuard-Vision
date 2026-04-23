import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import LoginView from '@/views/auth/LoginView.vue'
import VisionHistoryView from '@/views/history/VisionHistoryView.vue'
import SensorHistoryView from '@/views/history/SensorHistoryView.vue'
import RuleCenterView from '@/views/system/RuleCenterView.vue'
import AuditCenterView from '@/views/system/AuditCenterView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { public: true },
    },
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
    },
    {
      path: '/vision-history',
      name: 'vision-history',
      component: VisionHistoryView,
    },
    {
      path: '/sensor-history',
      name: 'sensor-history',
      component: SensorHistoryView,
    },
    {
      path: '/rules',
      name: 'rules',
      component: RuleCenterView,
    },
    {
      path: '/audit',
      name: 'audit',
      component: AuditCenterView,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  const isPublic = Boolean(to.meta.public)

  if (!isPublic && !authStore.isAuthenticated) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    return { path: '/' }
  }

  return true
})

export default router
