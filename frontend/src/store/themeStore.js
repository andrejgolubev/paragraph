import { create } from 'zustand' 

export const useThemeStore = create((set) => ({
  darkTheme: localStorage.getItem('darkTheme') === 'true',
  toggleTheme: () => set((state) => {
    const newTheme = !state.darkTheme
    localStorage.setItem('darkTheme', newTheme.toString())
    document.body.classList.toggle('dark', newTheme)
    return { darkTheme: newTheme }
  }),
}))

