<template>
  <div class="app-shell">
    <div class="app-backdrop"></div>
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
</style>
