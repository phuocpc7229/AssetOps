import { apiRequest } from './api'

export type AuthUser = {
  id: number
  username: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

type LoginResponse = {
  access_token: string
  token_type: 'Bearer'
  user: AuthUser
}

type MeResponse = {
  user: AuthUser
}

export type ChangePasswordPayload = {
  current_password: string
  new_password: string
  confirm_password: string
}

type ChangePasswordResponse = {
  detail: string
}

export const login = (username: string, password: string) =>
  apiRequest<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })

export const fetchCurrentUser = (token: string) =>
  apiRequest<MeResponse>('/auth/me', { method: 'GET' }, { token })

export const changePassword = (payload: ChangePasswordPayload, token: string) =>
  apiRequest<ChangePasswordResponse>(
    '/auth/change-password',
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
    { token },
  )
