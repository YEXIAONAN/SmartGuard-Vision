import { Router } from 'express'
import { body } from 'express-validator'
import { getAlertById, getAlerts, patchAlertStatus } from '../controllers/alertController.js'

const alertsRouter = Router()

alertsRouter.get('/', getAlerts)
alertsRouter.get('/:id', getAlertById)
alertsRouter.patch(
  '/:id/status',
  body('status')
    .isString()
    .isIn(['pending', 'processing', 'resolved'])
    .withMessage('status 必须是 pending/processing/resolved'),
  body('remark').optional().isString().withMessage('remark 必须是字符串'),
  patchAlertStatus,
)

export default alertsRouter
