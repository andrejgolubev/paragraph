import { create } from 'zustand'  
import Cookies from 'js-cookie'

const COOKIE_EXPIRES = 30 // 30 дней


export const useDropdownStore = create((set) => ({
  groupDataValue: Cookies.get('groupDataValue') || '',
  setGroupDataValue: (groupDataValue) => {
    Cookies.set('groupDataValue', groupDataValue, {
      expires: COOKIE_EXPIRES,
      path: '/',
      secure: true,
      samesite: 'none',
    })
    set({ groupDataValue: groupDataValue })
  },
  dateDataValue: Cookies.get('dateDataValue') || '',
  setDateDataValue: (dateDataValue) => {
    Cookies.set('dateDataValue', dateDataValue, {
      expires: COOKIE_EXPIRES,
      path: '/',
      secure: true,
      samesite: 'none',
    })
    set({ dateDataValue: dateDataValue })
  },
  clearCookies: () => {
    Cookies.remove('groupDataValue', { path: '/' })
    Cookies.remove('dateDataValue', { path: '/' })
    set({ groupDataValue: null, dateDataValue: null })
  },
  syncFromCookies: () => {
    set({
      groupDataValue: Cookies.get('groupDataValue') || null,
      dateDataValue: Cookies.get('dateDataValue') || null
    })
  }
}))