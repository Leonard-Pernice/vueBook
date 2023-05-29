import { defineStore } from 'pinia'

export const useAccountStore = defineStore('account', {
  state: () => ({
    token: '',
    isAuthenticated: false,
    isLoading: false,
    loadedFile: {}
  }),
  actions: {
    checkToken () {
      if (localStorage.getItem('token')) {
        this.token = localStorage.getItem('token')
        this.isAuthenticated = true
      } else {
        this.token = ''
        this.isAuthenticated = false
      }
    },
    setToken (token) {
      this.token = token
      this.isAuthenticated = true
    },
    removeToken () {
      this.token = null
      this.isAuthenticated = false
    }
  },
  getters: {
  }
})
