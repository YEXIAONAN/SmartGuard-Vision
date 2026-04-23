import { Router } from 'express'
import { getCharts, getDevices, getOverview } from '../controllers/dashboardController.js'

const dashboardRouter = Router()

dashboardRouter.get('/overview', getOverview)
dashboardRouter.get('/charts', getCharts)
dashboardRouter.get('/devices', getDevices)

export default dashboardRouter
