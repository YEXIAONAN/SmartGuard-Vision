const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

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

const request = async (path, options = {}) => {
  const { params, headers, ...restOptions } = options
  const response = await fetch(buildUrl(path, params), {
    headers: {
      Accept: 'application/json',
      ...headers,
    },
    ...restOptions,
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  const payload = await response.json()
  if (payload.code !== 0) {
    throw new Error(payload.message || 'Request failed')
  }

  return payload.data
}

export const dashboardApi = {
  getHealth() {
    return request('/health')
  },
  getOverview() {
    return request('/api/dashboard/overview')
  },
  updateAlertStatus(alertId, payload) {
    return request(`/api/alerts/${alertId}/status`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
  },
  getAlertActions(alertId) {
    return request(`/api/alerts/${alertId}/actions`)
  },
  getVisionRecords(params = {}) {
    return request('/api/vision', { params })
  },
  getVisionFilterOptions(params = {}) {
    return request('/api/vision/filter-options', { params })
  },
  getVisionRecordDetail(recordId) {
    return request(`/api/vision/${recordId}`)
  },
  getSensorRecords(params = {}) {
    return request('/api/sensors', { params })
  },
  getSensorFilterOptions(params = {}) {
    return request('/api/sensors/filter-options', { params })
  },
  getSensorRecordDetail(recordId) {
    return request(`/api/sensors/${recordId}`)
  },
}
