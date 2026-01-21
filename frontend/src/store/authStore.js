import { create } from 'zustand'
import API from '../api/API'


export const useAuthStore = create((set) => ({
  user: null,
  loading: false,
  fetchUser: async () => {
    set({ loading: true })
    try {
      const resp = await API.getUserData()
      if (resp?.status === 'ok') {
        set({
          user: {
            username: resp.username,
            role: resp.role,
            email: resp.email,
            group: resp.group
          }
        })
      } else {
        set({ user: null })
      }
    } catch {
      set({ user: null })
    }
    set({ loading: false })
  },
  
  logout: async () => {
    await API.logout()
    set({ user: null })
  }
})) 