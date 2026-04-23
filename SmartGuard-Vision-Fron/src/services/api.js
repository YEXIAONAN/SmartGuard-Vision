const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const TOKEN_KEY = 'sg_access_token'
const REFRESH_TOKEN_KEY = 'sg_refresh_token'
const USER_KEY = 'sg_current_user'

const buildUrl = (path, params) => {
  const url = new URL(`${API_BASE_URL}${path}`, window.location.origin)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, value)
      }
    })
  }
  if (!API_BASE_URL) {
    return `${url.pathname}${url.search}`
  }
  return url.toString()
}

const getAccessToken = () => localStorage.getItem(TOKEN_KEY) || ''
const getRefreshToken = () => localStorage.getItem(REFRESH_TOKEN_KEY) || ''

const saveSession = (data) => {
  if (!data?.access_token || !data?.refresh_token || !data?.user) return
  localStorage.setItem(TOKEN_KEY, data.access_token)
  localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh_token)
  localStorage.setItem(USER_KEY, JSON.stringify(data.user))
}

const clearSessionAndRedirect = () => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

let refreshingPromise = null
const refreshAccessToken = async () => {
  if (refreshingPromise) return refreshingPromise

  const refreshToken = getRefreshToken()
  if (!refreshToken) throw new Error('missing refresh token')

  refreshingPromise = fetch(buildUrl('/api/auth/refresh'), {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
    .then(async (response) => {
      if (!response.ok) throw new Error('refresh failed')
      const payload = await response.json()
      if (payload.code !== 0) throw new Error(payload.message || 'refresh failed')
      saveSession(payload.data)
      return payload.data.access_token
    })
    .finally(() => {
      refreshingPromise = null
    })

  return refreshingPromise
}

const request = async (path, options = {}, retry = true) => {
  const { params, headers, skipAuth, ...restOptions } = options
  const token = getAccessToken()
  const finalHeaders = {
    Accept: 'application/json',
    ...headers,
  }
  if (!skipAuth && token) {
    finalHeaders.Authorization = `Bearer ${token}`
  }

  const response = await fetch(buildUrl(path, params), {
    headers: finalHeaders,
    ...restOptions,
  })

  if (response.status === 401 && !skipAuth && retry) {
    try {
      await refreshAccessToken()
      return request(path, options, false)
    } catch {
      clearSessionAndRedirect()
      throw new Error('登录状态已失效，请重新登录')
    }
  }

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  const payload = await response.json()
  if (payload.code !== 0) {
    throw new Error(payload.message || 'Request failed')
  }
  return payload.data
}

const requestBlob = async (path, options = {}, retry = true) => {
  const { params, headers, skipAuth, ...restOptions } = options
  const token = getAccessToken()
  const finalHeaders = {
    ...headers,
  }
  if (!skipAuth && token) {
    finalHeaders.Authorization = `Bearer ${token}`
  }

  const response = await fetch(buildUrl(path, params), {
    headers: finalHeaders,
    ...restOptions,
  })

  if (response.status === 401 && !skipAuth && retry) {
    try {
      await refreshAccessToken()
      return requestBlob(path, options, false)
    } catch {
      clearSessionAndRedirect()
      throw new Error('登录状态已失效，请重新登录')
    }
  }

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return response.blob()
}

export const authApi = {
  login(payload) {
    return request('/api/auth/login', {
      method: 'POST',
      skipAuth: true,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  },
  refresh(refreshToken) {
    return request('/api/auth/refresh', {
      method: 'POST',
      skipAuth: true,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })
  },
  logout(payload) {
    return request('/api/auth/logout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  },
  getMe() {
    return request('/api/auth/me')
  },
}

export const dashboardApi = {
  getHealth() {
    return request('/health', { skipAuth: true })
  },
  getOverview() {
    return request('/api/dashboard/overview')
  },
  getAlerts(params = {}) {
    return request('/api/alerts', { params })
  },
  updateAlertStatus(alertId, payload) {
    return request(`/api/alerts/${alertId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  },
  getAlertActions(alertId) {
    return request(`/api/alerts/${alertId}/actions`)
  },
  scanAlertSla() {
    return request('/api/alerts/sla/scan', { method: 'POST' })
  },
  exportAlertsCsv(params = {}) {
    return requestBlob('/api/alerts/export/csv', { params })
  },
  getVisionRecords(params = {}) {
    return request('/api/vision', { params })
  },
  getVisionFilterOptions(params = {}) {
    return request('/api/vision/filter-options', { params }).then((data) => ({
      first: data.event_types || [],
      risk: data.risk_levels || [],
    }))
  },
  getVisionRecordDetail(recordId) {
    return request(`/api/vision/${recordId}`)
  },
  getSensorRecords(params = {}) {
    return request('/api/sensors', { params })
  },
  getSensorFilterOptions(params = {}) {
    return request('/api/sensors/filter-options', { params }).then((data) => ({
      first: data.sensor_types || [],
      risk: data.risk_levels || [],
    }))
  },
  getSensorRecordDetail(recordId) {
    return request(`/api/sensors/${recordId}`)
  },
  getRules() {
    return request('/api/rules')
  },
  updateRule(ruleKey, payload) {
    return request(`/api/rules/${ruleKey}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  },
}

export const auditApi = {
  getAuditLogs(params = {}) {
    return request('/api/audit', { params })
  },
}
