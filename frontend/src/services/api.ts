const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

type RequestOptions = {
  token?: string | null
}

const getApiBaseUrl = () => {
  if (!apiBaseUrl) {
    throw new ApiError('Authentication service is not configured.', 0)
  }

  return apiBaseUrl.replace(/\/$/, '')
}

export const apiRequest = async <T>(
  path: string,
  init: RequestInit = {},
  options: RequestOptions = {},
): Promise<T> => {
  const headers = new Headers(init.headers)
  headers.set('Content-Type', 'application/json')

  if (options.token) {
    headers.set('Authorization', `Bearer ${options.token}`)
  }

  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    ...init,
    headers,
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message =
      data && typeof data.detail === 'string' ? data.detail : 'Request failed. Please try again.'
    throw new ApiError(message, response.status)
  }

  return data as T
}
