import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { routes } from './routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  const requiresAuth = Boolean(to.meta?.requiresAuth)
  const guestOnly = Boolean(to.meta?.guestOnly)
  const allowedRoles = to.meta?.roles

  if (requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }

  if (requiresAuth && Array.isArray(allowedRoles) && allowedRoles.length > 0) {
    if (!allowedRoles.includes(authStore.role)) {
      return { name: 'dashboard' }
    }
  }

  return true
})

router.afterEach((to) => {
  const baseTitle = '智感护航'
  document.title = to.meta?.title ? `${to.meta.title} - ${baseTitle}` : baseTitle
})

export default router
