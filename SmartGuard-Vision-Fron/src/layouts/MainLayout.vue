<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const navItems = [
  { path: '/', label: '首页总览' },
  { path: '/vision-history', label: '视觉历史' },
  { path: '/sensor-history', label: '传感历史' },
]

const activePath = computed(() => route.path)
</script>

<template>
  <div class="app-shell">
    <div class="app-backdrop"></div>
    <header class="top-nav">
      <div class="brand-block">
        <div class="brand-title">智感护航</div>
        <div class="brand-subtitle">停充场景多模态安全感知与联动处置平台</div>
      </div>
      <nav class="nav-links">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ 'nav-link-active': activePath === item.path }"
        >
          {{ item.label }}
        </router-link>
      </nav>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.top-nav {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 20px;
  background: rgba(245, 249, 254, 0.86);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(219, 229, 240, 0.9);
}

.brand-title {
  font-size: 22px;
  font-weight: 700;
  color: #1f3e68;
}

.brand-subtitle {
  margin-top: 4px;
  font-size: 13px;
  color: var(--sg-text-secondary);
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.nav-link {
  padding: 8px 14px;
  border: 1px solid var(--sg-border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  color: var(--sg-text-secondary);
  transition: all 0.2s ease;
}

.nav-link-active {
  border-color: rgba(47, 107, 255, 0.26);
  background: rgba(47, 107, 255, 0.12);
  color: #1d4fb4;
}

.app-backdrop {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top left, rgba(117, 164, 255, 0.14), transparent 28%),
    radial-gradient(circle at right 18%, rgba(112, 179, 255, 0.1), transparent 24%);
  pointer-events: none;
}

.app-main {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

@media (max-width: 960px) {
  .top-nav {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
