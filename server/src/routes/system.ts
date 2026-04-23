import { Router } from 'express'
import { getSystem } from '../controllers/dashboardController.js'

const systemRouter = Router()

systemRouter.get('/status', getSystem)

export default systemRouter
