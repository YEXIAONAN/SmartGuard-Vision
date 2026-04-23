<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'
import PanelCard from '../../components/common/PanelCard.vue'
import { dashboardApi } from '../../services/api'

const loading = ref(false)
const rules = ref([])

const fetchRules = async () => {
  loading.value = true
  try {
    rules.value = await dashboardApi.getRules()
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '规则加载失败')
  } finally {
    loading.value = false
  }
}

const updateRule = async (row) => {
  try {
    await dashboardApi.updateRule(row.rule_key, {
      rule_value: row.rule_value,
      description: row.description,
    })
    ElMessage.success('规则更新成功')
    await fetchRules()
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '规则更新失败')
  }
}

onMounted(fetchRules)
</script>

<template>
  <div class="page-container">
    <PanelCard title="规则配置中心" extra="阈值与SLA可配置">
      <el-table v-loading="loading" :data="rules" border>
        <el-table-column prop="rule_key" label="规则键" min-width="180" />
        <el-table-column prop="description" label="说明" min-width="260" />
        <el-table-column label="规则值" min-width="180">
          <template #default="{ row }">
            <el-input v-model="row.rule_value" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="updateRule(row)">保存</el-button>
          </template>
        </el-table-column>
      </el-table>
    </PanelCard>
  </div>
</template>
