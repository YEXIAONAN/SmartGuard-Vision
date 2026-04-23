<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppShell from '@/components/dashboard/AppShell.vue'
import AppCard from '@/components/common/AppCard.vue'
import { dashboardApi } from '@/services/api'

interface RuleItem {
  rule_key: string
  description: string
  rule_value: string | number
}

const loading = ref(false)
const rules = ref<RuleItem[]>([])

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

const updateRule = async (row: RuleItem) => {
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
  <AppShell @refresh="fetchRules">
    <AppCard title="规则中心" extra="阈值与 SLA 配置">
      <el-table v-loading="loading" :data="rules" border>
        <el-table-column prop="rule_key" label="规则键" min-width="220" />
        <el-table-column prop="description" label="说明" min-width="300" />
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
    </AppCard>
  </AppShell>
</template>
