export const convertDate = (date) => {
  return date?.split("-").reverse().join(".");
}

export const latinToCyrillic = (str) => {
  if (!str || typeof str !== 'string') return str;
  
  const latinToCyrillicMap = {
    'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'K': 'К',
    'M': 'М', 'H': 'Н', 'O': 'О', 'P': 'Р', 'T': 'Т',
    'X': 'Х', 'Y': 'У'
  };
  
  return str
    .toUpperCase() // Приводим к верхнему регистру
    .split('')
    .map(char => latinToCyrillicMap[char] || char)
    .join('');
};