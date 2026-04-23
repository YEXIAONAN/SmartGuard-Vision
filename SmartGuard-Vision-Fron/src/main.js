import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import { ElMessage } from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'
import './assets/styles/theme.css'
import './assets/styles/global.css'

const app = createApp(App)

app.config.errorHandler = (error, instance, info) => {
  console.error('Vue runtime error:', error, info, instance)
  ElMessage.error('页面渲染异常，请刷新后重试')
}

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason)
  ElMessage.error('请求处理异常，请稍后重试')
})

app.use(createPinia())
app.use(ElementPlus)
app.use(router)

app.mount('#app')
