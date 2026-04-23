import type { NextFunction, Request, Response } from 'express'
import { fail } from '../utils/response.js'

export const notFoundHandler = (_req: Request, res: Response) => {
  fail(res, 404, '接口不存在')
}

export const errorHandler = (error: unknown, _req: Request, res: Response, _next: NextFunction) => {
  const message = error instanceof Error ? error.message : '服务器内部错误'
  fail(res, 500, message)
}
