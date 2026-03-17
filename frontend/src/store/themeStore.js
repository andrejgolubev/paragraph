import { create } from 'zustand' 

export const useThemeStore = create((set) => ({
  darkTheme: localStorage.getItem('darkTheme') === 'true',
  toggleTheme: () => set((state) => {
    const newState = !state.darkTheme
    localStorage.setItem('darkTheme', newState.toString())
    document.body.classList.toggle('dark', newState)
    return { darkTheme: newState }
  }),
  notesEnabled: localStorage.getItem('notesEnabled') === 'true',
  setNotesEnabled: () => set((state) => {
    const newState = !state.notesEnabled
    localStorage.setItem('notesEnabled', newState.toString())
    return { notesEnabled: newState }
  }),
}))

