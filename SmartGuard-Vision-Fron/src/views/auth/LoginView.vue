<script setup>
import { ElMessage } from 'element-plus'
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authApi } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loading = ref(false)
const formRef = ref(null)
const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const roleTips = [
  '管理员：admin / admin123',
  '值班员：operator / operator123',
  '只读用户：viewer / viewer123',
]

const submit = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const data = await authApi.login(form)
    authStore.setSession({
      token: data.access_token,
      refreshToken: data.refresh_token,
      user: data.user,
    })
    ElMessage.success('登录成功')
    const redirectPath = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.replace(redirectPath)
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <section class="login-card">
      <header class="login-header">
        <h1>智感护航</h1>
        <p>停充场景多模态安全感知与联动处置平台</p>
      </header>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" @keyup.enter="submit" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
            @keyup.enter="submit"
          />
        </el-form-item>
        <el-button type="primary" class="submit-btn" :loading="loading" @click="submit">
          登录系统
        </el-button>
      </el-form>

      <div class="tips">
        <div class="tips-title">默认账号</div>
        <div v-for="tip in roleTips" :key="tip" class="tip-item">{{ tip }}</div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at 16% 20%, #dce6f2 0%, rgba(220, 230, 242, 0) 40%),
    radial-gradient(circle at 88% 10%, #e7edf5 0%, rgba(231, 237, 245, 0) 36%),
    #eef3f8;
  padding: 18px;
}

.login-card {
  width: min(420px, 100%);
  background: #ffffff;
  border: 1px solid var(--sg-border-light);
  border-radius: 12px;
  box-shadow: var(--sg-shadow-soft);
  padding: 24px;
}

.login-header h1 {
  margin: 0;
  font-size: 24px;
  color: #23384f;
}

.login-header p {
  margin: 8px 0 18px;
  font-size: 13px;
  color: var(--sg-text-secondary);
}

.submit-btn {
  width: 100%;
  margin-top: 4px;
}

.tips {
  margin-top: 18px;
  border-top: 1px dashed #dce4ef;
  padding-top: 12px;
}

.tips-title {
  font-size: 13px;
  color: #2b425c;
  font-weight: 600;
}

.tip-item {
  margin-top: 4px;
  font-size: 12px;
  color: var(--sg-text-secondary);
}
</style>
