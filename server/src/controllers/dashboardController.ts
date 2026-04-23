import type { Request, Response } from 'express'
import { getChartData, getDeviceList, getOverviewStats, getSystemStatus } from '../services/dashboardService.js'
import { ok } from '../utils/response.js'

export const getOverview = (_req: Request, res: Response) => {
  ok(res, getOverviewStats())
}

export const getCharts = (_req: Request, res: Response) => {
  ok(res, getChartData())
}

export const getDevices = (_req: Request, res: Response) => {
  ok(res, getDeviceList())
}

export const getSystem = (_req: Request, res: Response) => {
  ok(res, getSystemStatus())
}
