import { onBeforeUnmount, onMounted, ref } from 'vue'

const formatNow = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const date = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')

  return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`
}

export const useClock = () => {
  const currentTime = ref(formatNow())
  let timer = null

  const update = () => {
    currentTime.value = formatNow()
  }

  onMounted(() => {
    update()
    timer = window.setInterval(update, 1000)
  })

  onBeforeUnmount(() => {
    if (timer) {
      window.clearInterval(timer)
    }
  })

  return {
    currentTime,
  }
}
