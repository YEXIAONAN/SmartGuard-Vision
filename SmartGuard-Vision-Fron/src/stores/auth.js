import { defineStore } from 'pinia'

const TOKEN_KEY = 'sg_access_token'
const REFRESH_TOKEN_KEY = 'sg_refresh_token'
const USER_KEY = 'sg_current_user'

const readJson = (value, fallback = null) => {
  if (!value) return fallback
  try {
    return JSON.parse(value)
  } catch {
    return fallback
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    refreshToken: localStorage.getItem(REFRESH_TOKEN_KEY) || '',
    user: readJson(localStorage.getItem(USER_KEY), null),
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token && state.refreshToken && state.user),
    role: (state) => state.user?.role || '',
    displayName: (state) => state.user?.display_name || state.user?.username || '',
    canHandleAlerts: (state) => ['admin', 'operator'].includes(state.user?.role || ''),
  },
  actions: {
    setSession({ token, refreshToken, user }) {
      this.token = token
      this.refreshToken = refreshToken
      this.user = user
      localStorage.setItem(TOKEN_KEY, token)
      localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    },
    clearSession() {
      this.token = ''
      this.refreshToken = ''
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(REFRESH_TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
    },
  },
})
