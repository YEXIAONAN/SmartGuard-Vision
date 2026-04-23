import cors from 'cors'
import express from 'express'
import morgan from 'morgan'
import dashboardRouter from './routes/dashboard.js'
import alertsRouter from './routes/alerts.js'
import systemRouter from './routes/system.js'
import { delayMiddleware } from './middlewares/delay.js'
import { errorHandler, notFoundHandler } from './middlewares/errorHandler.js'
import { ok } from './utils/response.js'

const app = express()

app.use(cors())
app.use(express.json())
app.use(morgan('dev'))
app.use(delayMiddleware)

app.get('/health', (_req, res) => {
  ok(res, { status: 'ok', timestamp: new Date().toISOString() })
})

app.use('/api/dashboard', dashboardRouter)
app.use('/api/alerts', alertsRouter)
app.use('/api/system', systemRouter)

app.use(notFoundHandler)
app.use(errorHandler)

export default app
