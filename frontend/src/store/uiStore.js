import { create } from 'zustand'  

export const useUiStore = create((set) => ({
  linksActive: false,
  setLinksActive: () => set((state) => {
    return { linksActive: !state.linksActive}
  }),
  notificationOuterMessage: '',
  setNotificationOuterMessage: (message) => set({ notificationOuterMessage: message }),
  notificationOuterType: 'success',
  setNotificationOuterType: (type) => set({ notificationOuterType: type }),
  notificationOuterActive: false,
  setNotificationOuterActive: (isActive) => set({ notificationOuterActive: isActive }),
  tipActive: false,
  setTipActive: (isActive) => set({ tipActive: isActive }),
}))
