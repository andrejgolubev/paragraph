import { useState, useEffect } from 'react';

export const useWindowSize = () => {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  })
  
  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return size
}


// 2й вариант, с дебаунсом (избыточный)

// import { useState, useEffect, useRef } from 'react';

// export const useWindowSize = () => {
//   const [size, setSize] = useState({
//     width: window.innerWidth,
//     height: window.innerHeight,
//   });

//   const timeoutRef = useRef(null);

//   useEffect(() => {
//     const handleResize = () => {
//       if (timeoutRef.current) {
//         clearTimeout(timeoutRef.current);
//       }
//       timeoutRef.current = setTimeout(() => {
//         setSize({
//           width: window.innerWidth,
//           height: window.innerHeight,
//         });
//       }, 50);
//     };

//     window.addEventListener('resize', handleResize);
//     return () => {
//       window.removeEventListener('resize', handleResize);
//       if (timeoutRef.current) {
//         clearTimeout(timeoutRef.current);
//       }
//     };
//   }, []);
  
//   return size;
// };