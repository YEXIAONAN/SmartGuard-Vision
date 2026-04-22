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

  const payloadText = computed(() => JSON.stringify(detail.value?.payload || {}, null, 2))

  const fetchOptions = async () => {
    if (!optionsFetcher) return
    try {
      const options = await optionsFetcher(optionsMapper(filters))
      filterOptions.first = options.first
      filterOptions.risk = options.risk
    } catch (error) {
      ElMessage.error(error instanceof Error ? error.message : optionsErrorMessage)
    }
  }

  const fetchRecords = async () => {
    loading.value = true
    try {
      const pageData = await listFetcher(
        requestMapper(filters, {
          page: pagination.page,
          page_size: pagination.pageSize,
        }),
      )
      records.value = pageData.items
      pagination.total = pageData.total
    } catch (error) {
      ElMessage.error(error instanceof Error ? error.message : listErrorMessage)
    } finally {
      loading.value = false
    }
  }

  const reload = async ({ syncOptions = false } = {}) => {
    if (syncOptions) {
      await fetchOptions()
    }
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

  const onFilterChanged = async () => {
    pagination.page = 1
    await reload({ syncOptions: true })
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
