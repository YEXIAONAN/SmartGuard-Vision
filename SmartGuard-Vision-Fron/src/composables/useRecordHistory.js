import { ElMessage } from 'element-plus'
import { computed, reactive, ref } from 'vue'

export const useRecordHistory = ({
  listFetcher,
  detailFetcher,
  optionsFetcher,
  initialFilters,
  requestMapper,
  optionsMapper,
  listErrorMessage,
  detailErrorMessage,
  optionsErrorMessage,
}) => {
  const loading = ref(false)
  const detailLoading = ref(false)
  const drawerVisible = ref(false)
  const records = ref([])
  const detail = ref(null)
  const filters = reactive({ ...initialFilters })
  const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0,
  })
  const filterOptions = reactive({
    first: [],
    risk: [],
  })

  let listRequestId = 0
  let optionsRequestId = 0
  let debounceTimer = null

  const payloadText = computed(() => JSON.stringify(detail.value?.payload || {}, null, 2))

  const fetchOptions = async () => {
    if (!optionsFetcher) return
    optionsRequestId += 1
    const currentId = optionsRequestId
    try {
      const options = await optionsFetcher(optionsMapper(filters))
      if (currentId !== optionsRequestId) return
      filterOptions.first = options.first || []
      filterOptions.risk = options.risk || []
    } catch (error) {
      ElMessage.error(error instanceof Error ? error.message : optionsErrorMessage)
    }
  }

  const fetchRecords = async () => {
    loading.value = true
    listRequestId += 1
    const currentId = listRequestId
    try {
      const pageData = await listFetcher(
        requestMapper(filters, {
          page: pagination.page,
          page_size: pagination.pageSize,
        }),
      )
      if (currentId !== listRequestId) return
      records.value = pageData.items || []
      pagination.total = pageData.total || 0
    } catch (error) {
      ElMessage.error(error instanceof Error ? error.message : listErrorMessage)
    } finally {
      if (currentId === listRequestId) loading.value = false
    }
  }

  const reload = async ({ syncOptions = false } = {}) => {
    if (syncOptions) await fetchOptions()
    await fetchRecords()
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
    pagination.page = 1
    await reload({ syncOptions: true })
  }

  const onFilterChanged = () => {
    pagination.page = 1
    if (debounceTimer) window.clearTimeout(debounceTimer)
    debounceTimer = window.setTimeout(() => {
      void reload({ syncOptions: true })
    }, 250)
  }

  const onPageChanged = async (nextPage) => {
    pagination.page = nextPage
    await fetchRecords()
  }

  const onPageSizeChanged = async (nextPageSize) => {
    pagination.pageSize = nextPageSize
    pagination.page = 1
    await fetchRecords()
  }

  return {
    loading,
    detailLoading,
    drawerVisible,
    records,
    detail,
    filters,
    filterOptions,
    pagination,
    payloadText,
    fetchRecords,
    fetchOptions,
    reload,
    openDetail,
    resetFilters,
    onFilterChanged,
    onPageChanged,
    onPageSizeChanged,
  }
}
