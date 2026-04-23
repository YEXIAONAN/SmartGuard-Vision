import type { Request, Response } from 'express'
import { validationResult } from 'express-validator'
import type { AlertLevel, AlertStatus } from '../types/index.js'
import { getAlertDetailById, listAlerts, updateAlertStatusById } from '../services/alertService.js'
import { badRequest, notFound, ok } from '../utils/response.js'

export const getAlerts = (req: Request, res: Response) => {
  const status = req.query.status as AlertStatus | undefined
  const level = req.query.level as AlertLevel | undefined
  const keyword = req.query.keyword as string | undefined
  ok(res, listAlerts({ status, level, keyword }))
}

export const getAlertById = (req: Request, res: Response) => {
  const data = getAlertDetailById(req.params.id)
  if (!data) return notFound(res, '告警不存在')
  ok(res, data)
}

export const patchAlertStatus = (req: Request, res: Response) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return badRequest(res, errors.array()[0]?.msg || '参数错误')
  }

  const status = req.body.status as AlertStatus
  const remark = (req.body.remark as string | undefined) || ''
  const data = updateAlertStatusById(req.params.id, status, remark, '系统管理员')
  if (!data) return notFound(res, '告警不存在')
  ok(res, data, '状态更新成功')
}
