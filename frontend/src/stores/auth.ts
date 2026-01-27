import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.is_admin || false,
    userAvatar: (state) => state.user?.avatar_url || `https://ui-avatars.com/api/?name=${state.user?.username || 'User'}`
  },
  actions: {
    async login(credentials: any) {
      const response = await axios.post('/api/users/login/', credentials)
      this.token = response.data.token
      this.user = {
        id: response.data.user_id,
        username: response.data.username,
        is_admin: response.data.is_admin,
        balance: response.data.balance,
        avatar_url: response.data.avatar_url
      }
      localStorage.setItem('token', this.token as string)
      localStorage.setItem('user', JSON.stringify(this.user))
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
    },
    async register(credentials: any) {
      await axios.post('/api/users/register/', credentials)
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },
    async fetchProfile() {
      if (!this.token) return
      try {
        axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
        const response = await axios.get('/api/users/profile/')
        // Ensure we keep the token and just update user details
        this.user = {
            ...this.user,
            ...response.data
        }
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (e) {
        this.logout()
        throw e // Re-throw to handle in component
      }
    }
  }
})
