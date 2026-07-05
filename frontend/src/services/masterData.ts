import { apiRequest } from './api'

export type MasterDataKind = 'asset-types' | 'vendors' | 'device-types' | 'locations'

export type MasterDataRecord = {
  id: number
  code: string
  name: string
  description: string
  is_deleted: boolean
  deleted_at: string | null
  created_at: string
  updated_at: string
}

export type MasterDataPayload = {
  code?: string
  name: string
  description: string
}

export type MasterDataListParams = {
  search?: string
  ordering?: string
  page?: number
  page_size?: number
  include_deleted?: boolean
}

export type MasterDataListResponse = {
  count: number
  page: number
  page_size: number
  total_pages: number
  results: MasterDataRecord[]
}

const buildQueryString = (params: MasterDataListParams) => {
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

export const fetchMasterData = (kind: MasterDataKind, params: MasterDataListParams, token: string) =>
  apiRequest<MasterDataListResponse>(`/${kind}${buildQueryString(params)}`, { method: 'GET' }, { token })

export const createMasterData = (kind: MasterDataKind, payload: MasterDataPayload, token: string) =>
  apiRequest<MasterDataRecord>(
    `/${kind}`,
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
    { token },
  )

export const updateMasterData = (
  kind: MasterDataKind,
  itemId: number,
  payload: MasterDataPayload,
  token: string,
) =>
  apiRequest<MasterDataRecord>(
    `/${kind}/${itemId}`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload),
    },
    { token },
  )

export const deleteMasterData = (kind: MasterDataKind, itemId: number, token: string) =>
  apiRequest<void>(`/${kind}/${itemId}`, { method: 'DELETE' }, { token })
