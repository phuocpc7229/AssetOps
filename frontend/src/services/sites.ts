import { apiRequest } from './api'

export type Site = {
  id: number
  code: string
  name: string
  address: string
  notes: string
  is_deleted: boolean
  deleted_at: string | null
  created_at: string
  updated_at: string
}

export type SitePayload = {
  code?: string
  name: string
  address: string
  notes: string
}

export type SiteListParams = {
  search?: string
  ordering?: string
  page?: number
  page_size?: number
  include_deleted?: boolean
}

export type SiteListResponse = {
  count: number
  page: number
  page_size: number
  total_pages: number
  results: Site[]
}

const buildQueryString = (params: SiteListParams) => {
  const searchParams = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return
    }

    searchParams.set(key, String(value))
  })

  const queryString = searchParams.toString()
  return queryString ? `?${queryString}` : ''
}

export const fetchSites = (params: SiteListParams, token: string) =>
  apiRequest<SiteListResponse>(`/sites${buildQueryString(params)}`, { method: 'GET' }, { token })

export const createSite = (payload: SitePayload, token: string) =>
  apiRequest<Site>(
    '/sites',
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
    { token },
  )

export const updateSite = (siteId: number, payload: SitePayload, token: string) =>
  apiRequest<Site>(
    `/sites/${siteId}`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload),
    },
    { token },
  )

export const deleteSite = (siteId: number, token: string) =>
  apiRequest<void>(`/sites/${siteId}`, { method: 'DELETE' }, { token })
