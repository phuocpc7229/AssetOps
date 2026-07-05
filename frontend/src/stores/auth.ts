import { defineStore } from 'pinia'

import { fetchCurrentUser, login, type AuthUser } from '@/services/auth'

const TOKEN_STORAGE_KEY = 'assetops.accessToken'

type AuthState = {
  accessToken: string | null
  user: AuthUser | null
  isLoading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: localStorage.getItem(TOKEN_STORAGE_KEY),
    user: null,
    isLoading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.accessToken),
  },
  actions: {
    async signIn(username: string, password: string) {
      if (this.isLoading) {
        return
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await login(username, password)
        this.accessToken = response.access_token
        this.user = response.user
        localStorage.setItem(TOKEN_STORAGE_KEY, response.access_token)
      } catch (error) {
        this.accessToken = null
        this.user = null
        localStorage.removeItem(TOKEN_STORAGE_KEY)
        this.error = error instanceof Error ? error.message : 'Sign in failed. Please try again.'
        throw error
      } finally {
        this.isLoading = false
      }
    },
    async loadCurrentUser() {
      if (!this.accessToken || this.user) {
        return
      }

      try {
        const response = await fetchCurrentUser(this.accessToken)
        this.user = response.user
      } catch {
        this.signOut()
      }
    },
    signOut() {
      this.accessToken = null
      this.user = null
      this.error = null
      localStorage.removeItem(TOKEN_STORAGE_KEY)
    },
  },
})
