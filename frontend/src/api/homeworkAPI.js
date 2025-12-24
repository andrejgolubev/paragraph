const BASE_URL = "http://127.0.0.1:8000"
const headers = {"Content-Type": "application/json"}


const homeworkAPI = {
  saveHomework: (groupDataValue, dateDataValue, lessonIndex, homeworkText) => {
    return fetch(`${BASE_URL}/homework/save`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        group_data_value: String(groupDataValue),
        date_data_value: dateDataValue,
        lesson_index: lessonIndex,
        homework: homeworkText,
      }),
    })
  },

  loadHomeworkData: async function loadHomeworkData(
    groupDataValue,
    dateDataValue,
    lessonIndex,
  ) {

    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue,
      lesson_index: lessonIndex,
    })

    // console.log('http://127.0.0.1:8000/homework/get?${params.toString() :>> ', `http://127.0.0.1:8000/homework/get?${params.toString()}`)
    return fetch(`http://127.0.0.1:8000/homework/get?${params.toString()}`, {
      method: "GET",
    })
      .then((resp) => resp.json())
      .catch((e) => console.error(e))
  },

  loadGroups: async function loadGroups() {
    return fetch("http://127.0.0.1:8000/schedule/get-all-groups")
      .then((response) => response.json())
      .catch((err) => {
        console.log("Error loading dates:", err)
        return []
      })
  },

  loadDates: async function loadDates() {
    return fetch("http://127.0.0.1:8000/schedule/get-all-dates")
      .then((response) => response.json())
      .catch((err) => {
        console.log("Error loading dates:", err)
        return []
      })
  },
}

export default homeworkAPI
