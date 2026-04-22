import { ElMessage } from 'element-plus'
import { computed, reactive, ref } from 'vue'

export const useRecordHistory = ({
  listFetcher,
  detailFetcher,
  initialFilters,
  requestMapper,
  listErrorMessage,
  detailErrorMessage,
}) => {
  const loading = ref(false)
  const detailLoading = ref(false)
  const drawerVisible = ref(false)
  const records = ref([])
  const detail = ref(null)
  const filters = reactive({ ...initialFilters })

  const payloadText = computed(() => JSON.stringify(detail.value?.payload || {}, null, 2))

  const fetchRecords = async () => {
    loading.value = true
    try {
      records.value = await listFetcher(requestMapper(filters))
    } catch (error) {
      ElMessage.error(error instanceof Error ? error.message : listErrorMessage)
    } finally {
      loading.value = false
    }
  }

  const openDetail = async (recordId) => {
    drawerVisible.value = true
    detailLoading.value = true
    detail.value = null

    try {
      detail.value = await detailFetcher(recordId)
    } catch (error) {
      ElMessage.error(error instanceof Error ? error.message : detailErrorMessage)
    } finally {
      detailLoading.value = false
    }
  }

  const resetFilters = async () => {
    Object.keys(initialFilters).forEach((key) => {
      filters[key] = initialFilters[key]
    })
    await fetchRecords()
  }

  return {
    loading,
    detailLoading,
    drawerVisible,
    records,
    detail,
    filters,
    payloadText,
    fetchRecords,
    openDetail,
    resetFilters,
  }
}
