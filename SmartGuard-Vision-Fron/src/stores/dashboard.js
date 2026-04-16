import { defineStore } from 'pinia'
import { dashboardMock } from '../data/dashboard'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    ...dashboardMock,
  }),
  getters: {
    deviceStatusList: (state) =>
      state.devices.map((item) => ({
        ...item,
        rate: Math.round((item.online / item.total) * 100),
      })),
  },
})
