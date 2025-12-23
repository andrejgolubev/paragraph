const BASE_URL = 'http://127.0.0.1:8000'


const homeworkAPI = {
  saveHomework: (groupDataValue, dateDataValue, lessonIndex, homeworkText) => {
    return fetch(`${BASE_URL}/homework/save`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_data_value: groupDataValue,
        date_data_value: dateDataValue,
        lesson_index: lessonIndex,
        homework: homeworkText,
      }),
    })
  }
}