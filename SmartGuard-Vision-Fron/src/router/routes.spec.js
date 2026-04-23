import { describe, expect, it } from 'vitest'

import { routes } from './routes'

describe('router meta', () => {
  it('should contain login route marked as guest only', () => {
    const loginRoute = routes.find((route) => route.path === '/login')
    expect(loginRoute).toBeTruthy()
    expect(loginRoute.meta?.guestOnly).toBe(true)
  })

  it('should require auth for main pages', () => {
    const rootRoute = routes.find((route) => route.path === '/')
    expect(rootRoute).toBeTruthy()
    expect(rootRoute.meta?.requiresAuth).toBe(true)
    expect(rootRoute.children?.length).toBeGreaterThan(0)
    rootRoute.children.forEach((child) => {
      expect(child.meta?.requiresAuth).toBe(true)
    })
  })
})
