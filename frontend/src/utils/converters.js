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
    .split('')
    .map(char => latinToCyrillicMap[char] || char)
    .join('');
};

export const getDateValueFromDisplay = (dateDisplay, year) => {
  
  const months = {
    января: "01",
    февраля: "02",
    марта: "03",
    апреля: "04",
    мая: "05",
    июня: "06",
    июля: "07",
    августа: "08",
    сентября: "09",
    октября: "10",
    ноября: "11",
    декабря: "12",
  }

  const [day, month] = dateDisplay.split(" ")
  const monthNumber = months[month]
  
  
  return `${year}-${monthNumber}-${day.padStart(2, "0")}`
}


// Получение класса для типа занятия
export const getLessonTypeClass = (type) => {
  const typeMap = {
    "Лек.": "lecture",
    "Лаб.": "lab",
    "Упр.": "practice",
  }
  return typeMap[type] || "default"
}