import type { Response } from 'express'
import type { ApiResponse } from '../types/index.js'

export const ok = <T>(res: Response, data: T, message = 'success') => {
  const payload: ApiResponse<T> = { code: 0, message, data }
  return res.json(payload)
}

export const fail = (res: Response, code: number, message: string) => {
  return res.status(code).json({
    code,
    message,
    data: null,
  })
}

export const badRequest = (res: Response, message: string) => fail(res, 400, message)
export const notFound = (res: Response, message: string) => fail(res, 404, message)
