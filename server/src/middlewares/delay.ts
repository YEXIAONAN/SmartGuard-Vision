import type { NextFunction, Request, Response } from 'express'

export const delayMiddleware = (_req: Request, _res: Response, next: NextFunction) => {
  const delay = 200 + Math.floor(Math.random() * 400)
  setTimeout(() => next(), delay)
}
