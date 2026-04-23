import axios, { AxiosError, type AxiosInstance, type AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types/dashboard'

const TOKEN_KEY = 'sg_access_token'
const REFRESH_TOKEN_KEY = 'sg_refresh_token'
const USER_KEY = 'sg_current_user'

const clearSessionAndRedirect = () => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
})

request.interceptors.request.use((config) => {
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  <T>(response: AxiosResponse<ApiResponse<T>>) => {
    const payload = response.data
    if (payload.code !== 0) {
      return Promise.reject(new Error(payload.message || '请求失败'))
    }
    return payload.data as T
  },
  (error: AxiosError<{ message?: string }>) => {
    if (error.response?.status === 401) {
      clearSessionAndRedirect()
      return Promise.reject(new Error('登录状态已失效，请重新登录'))
    }
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('请求超时，请稍后重试'))
    }
    if (error.response?.data?.message) {
      return Promise.reject(new Error(error.response.data.message))
    }
    if (error.response?.status) {
      return Promise.reject(new Error(`服务异常(${error.response.status})`))
    }
    return Promise.reject(new Error('网络异常，请检查连接'))
  },
)

export default request
