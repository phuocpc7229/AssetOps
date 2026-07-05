import { apiRequest } from './api'
import type { MasterDataRecord } from './masterData'

export type AssetStatus = 'active' | 'in_maintenance' | 'archived'
export type AssetCriticality = 'low' | 'medium' | 'high' | 'critical'

export type AssetIPAddress = {
  id?: number
  address: string
  is_primary: boolean
}

export type Asset = {
  id: number
  asset_tag: string
  name: string
  hostname: string
  asset_type: MasterDataRecord
  vendor: MasterDataRecord | null
  model: string
  serial_number: string
  ip_address: string | null
  ip_addresses: AssetIPAddress[]
  mac_address: string
  site: {
    id: number
    code: string
    name: string
  } | null
  location: MasterDataRecord | null
  status: AssetStatus
  criticality: AssetCriticality
  warranty_starts_on: string | null
  warranty_expires_on: string | null
  purchase_date: string | null
  notes: string
  created_at: string
  updated_at: string
  created_by: number | null
  updated_by: number | null
}

export type AssetPayload = {
  asset_tag: string
  name: string
  hostname: string
  asset_type_id: number | null
  vendor_id: number | null
  model: string
  serial_number: string
  ip_address: string | null
  ip_addresses: AssetIPAddress[]
  mac_address: string
  site_id: number | null
  location_id: number | null
  status: AssetStatus
  criticality: AssetCriticality
  warranty_starts_on: string | null
  warranty_expires_on: string | null
  purchase_date: string | null
  notes: string
}

export type AssetListParams = {
  search?: string
  status?: string
  criticality?: string
  asset_type?: string
  vendor?: string
  site?: string | number
  include_archived?: boolean
  ordering?: string
  page?: number
  page_size?: number
}

export type AssetListResponse = {
  count: number
  page: number
  page_size: number
  total_pages: number
  results: Asset[]
}

export type AssetPingResponse = {
  success: boolean
  ip_address: string
  latency_ms: number | null
  message: string
}

const buildQueryString = (params: AssetListParams) => {
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

export const fetchAssets = (params: AssetListParams, token: string) =>
  apiRequest<AssetListResponse>(`/assets${buildQueryString(params)}`, { method: 'GET' }, { token })

export const fetchAsset = (assetId: number, token: string) =>
  apiRequest<Asset>(`/assets/${assetId}`, { method: 'GET' }, { token })

export const createAsset = (payload: AssetPayload, token: string) =>
  apiRequest<Asset>(
    '/assets',
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
    { token },
  )

export const updateAsset = (assetId: number, payload: AssetPayload, token: string) =>
  apiRequest<Asset>(
    `/assets/${assetId}`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload),
    },
    { token },
  )

export const archiveAsset = (assetId: number, token: string) =>
  apiRequest<void>(`/assets/${assetId}`, { method: 'DELETE' }, { token })

export const pingAsset = (assetId: number, token: string, ipAddress?: string) =>
  apiRequest<AssetPingResponse>(
    `/assets/${assetId}/ping`,
    {
      method: 'POST',
      body: JSON.stringify(ipAddress ? { ip_address: ipAddress } : {}),
    },
    { token },
  )
