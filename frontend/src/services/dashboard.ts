import { apiRequest } from './api'
import type { AssetCriticality, AssetStatus } from './assets'

export type DashboardKpiKey =
  | 'total_assets'
  | 'active_assets'
  | 'maintenance_assets'
  | 'expiring_warranty'
  | 'online_assets'

export type DashboardTone = 'blue' | 'green' | 'orange' | 'red' | 'muted'

export type DashboardTrendPoint = {
  date: string
  value: number
}

export type DashboardKpi = {
  key: DashboardKpiKey
  label: string
  value: number
  helper: string
  percent: number | null
  tone: DashboardTone
  trend: DashboardTrendPoint[]
}

export type DashboardChartSegment = {
  key: string
  label: string
  value: number
  percent: number
  color: string
}

export type DashboardDonutChart = {
  total: number
  segments: DashboardChartSegment[]
}

export type DashboardMetrics = {
  generated_at: string
  kpis: DashboardKpi[]
  charts: {
    assets_by_type: DashboardDonutChart
    warranty_status: DashboardDonutChart
  }
  quick_action_badges: {
    maintenance_assets: number
    archived_assets: number
    expiring_warranty: number
  }
}

export type DashboardAsset = {
  id: number
  asset_tag: string
  name: string
  primary_ip: string | null
  ip_count: number
  asset_type: {
    id: number
    code: string
    name: string
  }
  vendor: {
    id: number
    code: string
    name: string
  } | null
  site: {
    id: number
    code: string
    name: string
  } | null
  status: AssetStatus
  criticality: AssetCriticality
  warranty_expires_on: string | null
  warranty_state: 'valid' | 'expiring' | 'expired' | 'unknown'
  updated_at: string
}

export type DashboardActivity = {
  id: string
  occurred_at: string
  entity_type: 'asset' | 'site' | 'master_data'
  action: 'created' | 'updated' | 'archived'
  title: string
  metadata: string
  severity: 'info' | 'success' | 'warning' | 'danger'
  route: string
}

export type DashboardRecentAssetsResponse = {
  results: DashboardAsset[]
}

export type DashboardRecentActivityResponse = {
  source: 'temporary_inferred'
  note: string
  results: DashboardActivity[]
}

export const fetchDashboardMetrics = (token: string) =>
  apiRequest<DashboardMetrics>('/dashboard/metrics', { method: 'GET' }, { token })

export const fetchDashboardRecentAssets = (token: string, limit = 8) =>
  apiRequest<DashboardRecentAssetsResponse>(
    `/dashboard/recent-assets?limit=${limit}`,
    { method: 'GET' },
    { token },
  )

export const fetchDashboardRecentActivity = (token: string, limit = 8) =>
  apiRequest<DashboardRecentActivityResponse>(
    `/dashboard/recent-activity?limit=${limit}`,
    { method: 'GET' },
    { token },
  )
