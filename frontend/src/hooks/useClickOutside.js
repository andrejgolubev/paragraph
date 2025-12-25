import { useEffect } from "react"

export const useClickOutside = (refs, handler) => {
  // универсальный хук для закрытия чего либо открытого 
  // при клике на элементы НЕ ПРИНАДЛЕЖАЩИЕ массиву refs
  useEffect(() => {
    const handleClickOutside = (event) => {

      // клик был снаружи, если НИ ОДИН ref не содержит target
      const clickOutside = refs.every(
        (ref) => !ref.current || !ref.current.contains(event.target)
      )

      if (clickOutside) {
        handler(event)
      }

    }

    document.addEventListener("mousedown", handleClickOutside)
    document.addEventListener("touchstart", handleClickOutside) // для мобильных

    //очистка
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
      document.removeEventListener("touchstart", handleClickOutside)
    }
  }, [refs, handler]) // Пересоздаем эффект при изменении refs или handler
}
