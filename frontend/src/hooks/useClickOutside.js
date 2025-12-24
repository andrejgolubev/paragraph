import { useEffect } from 'react'

export const useClickOutside = (ref, handler) => {
  useEffect(() => {
    const handleClickOutside = (event) => {
      // клик был внутри элемента - игнорируем
      if (!ref.current || ref.current.contains(event.target)) {
        return
      }
      //иначе вызываем функцию-обработчик
      handler(event)
    }

    document.addEventListener('mousedown', handleClickOutside)
    document.addEventListener('touchstart', handleClickOutside) // для мобильных

    //очистка 
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
      document.removeEventListener('touchstart', handleClickOutside)
    } 
  }, [ref, handler]) // Пересоздаем эффект при изменении ref или handler
}